import json
import os
import subprocess
from collections import Counter
from math import log2, pow

import librosa
import pandas as pd
from main_app.models import Song
from main_app.models import Video
from sketch_web.celery import app
from sketch_web.settings import STATIC_DIR, AUDIO_DIR, VIDEO_DIR

# Pitch Formula


A4 = 440
C0 = A4 * pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def pitch(freq):
    h = round(12 * log2(freq / C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)


@app.task
def encode_video(original_name):
    video_input = VIDEO_DIR
    audio_input = AUDIO_DIR

    # video paths
    originals_path = os.path.join(video_input, "")
    originals_final_path = os.path.join(video_input, "Originals", "")
    encoded_path = os.path.join(video_input, "Encoded", "")
    final_destination = os.path.join(STATIC_DIR, 'videos', '')

    # audio paths
    audio_path = os.path.join(audio_input, "")
    csv_path = os.path.join(audio_input, "")
    csv_final_path = os.path.join(audio_input, "Originals", "")

    file_name = original_name.split('.')[0]

    # .webm to .mp4 + audio fades
    subprocess.call(
        f"ffmpeg -i {originals_path}{original_name} -filter_complex 'afade=d=2, areverse, afade=d=4, areverse' {encoded_path}{original_name}_fades.mp4",
        shell=True)

    # move original file
    os.rename(f"{originals_path}{original_name}", f"{originals_final_path}{original_name}")

    # audio filtering 200hz - 6000hz
    subprocess.call(
        f"ffmpeg -i {encoded_path}{original_name}_fades.mp4 -af 'highpass=f=200, lowpass=f=6000' {encoded_path}{original_name}_filtered.mp4",
        shell=True)

    # deleting intermediary file
    os.remove(f"{encoded_path}{original_name}_fades.mp4")

    encoded_file_name = file_name + '_final.mp4'

    # audio normalizing
    subprocess.call(
        f"ffmpeg-normalize {encoded_path}{original_name}_filtered.mp4 -o {encoded_path}{encoded_file_name} -c:a aac -b:a 192k",
        shell=True)

    # deleting intermediary file
    os.remove(f"{encoded_path}{original_name}_filtered.mp4")

    wav_file_name = file_name + '.wav'

    # REGISTER FILE NAMES
    Video.objects.get_or_create(name=encoded_file_name)

    # WAW Extraction
    subprocess.call(
        f"ffmpeg -i {encoded_path}{encoded_file_name} -acodec pcm_s16le -ar 128k -vn {audio_path}{wav_file_name}",
        shell=True)

    # Moving encoded videos to final destination (app folder)
    os.rename(f"{encoded_path}{encoded_file_name}", f"{final_destination}{encoded_file_name}")

    # WAW to CSV
    subprocess.call(f"crepe {audio_path}{wav_file_name}", shell=True)
    os.remove(f"{audio_path}{wav_file_name}")

    csv_file_name = file_name + '.f0.csv'

    # Read CSV
    df = pd.read_csv(f"{csv_path}{csv_file_name}")

    # dropping the 0 values
    df = df[(df[['frequency']] != 0).all(axis=1)]

    # mapping the notes
    df['note'] = df['frequency'].apply(pitch)

    # Store to DB
    notes_series = df.note.value_counts(normalize=True).head(5)
    notes_dict = notes_series.to_dict()

    Video.objects.filter(name=encoded_file_name).update(notes=json.dumps(notes_dict))

    # moving csvs to final destination
    os.rename(f"{csv_path}{csv_file_name}", f"{csv_final_path}{csv_file_name}")


@app.task
def scan(f):
    sounds_path = os.path.join(STATIC_DIR, "sounds", "")
    originals_path = os.path.join(STATIC_DIR, "sounds", "originals", "")

    def remove_num(my_string):
        for char in my_string:
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                new_str = my_string.replace(char, "")
                return new_str

    def percentages(value):
        return value / len(all_the_notes) * 100

    y, sr = librosa.load(f"{sounds_path + f}")

    # Tempo tracking
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

    # Fundamental Frequency Estimation
    fundamentals = librosa.yin(y=y, fmin=60, fmax=20000)
    fundamental_notes = []

    for freq in fundamentals:
        fundamental_notes.append(librosa.hz_to_note(freq))

    all_the_notes = list(map(remove_num, fundamental_notes))
    notes_dict = Counter(all_the_notes)

    # Calculating Percentages and Sorting
    rounded_notes = dict((k, round(percentages(v), 2)) for k, v in notes_dict.items())
    sorted_notes = sorted(rounded_notes.items(), key=lambda x: x[1], reverse=True)

    # Removing musical sharp sign to avoid DB storing problems
    notes_list = []
    for (a, b) in sorted_notes:
        notes_list.append((a.replace("♯", "#"), b))

    # Registering the final data
    Song.objects.get_or_create(filename=f, duration=round(librosa.get_duration(y)),
                               tempo=round(tempo, 2), notes=json.dumps(notes_list[:3]))

    # Moving songs to 'originals' folder
    os.rename(f"{sounds_path}{f}", f"{originals_path}{f}")
