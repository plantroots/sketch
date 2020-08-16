import json
import os
import subprocess
from math import log2, pow
from pathlib import Path

import pandas as pd
from main_app.models import Video
from sketch_web.celery import app

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
    home = str(Path.home())
    originals_path = os.path.join(home, "Videos", "Webcam", "")
    originals_final_path = os.path.join(home, "Videos", "Webcam", "Originals", "")
    encoded_path = os.path.join(home, "Videos", "Webcam", "Encoded", "")
    audio_path = os.path.join(home, "PycharmProjects", "Sketch", "sketch_web", "data", "csvs", "")
    csv_path = os.path.join(home, "PycharmProjects", "Sketch", "sketch_web", "data", "csvs", "")
    csv_final_path = os.path.join(home, "PycharmProjects", "Sketch", "sketch_web", "data", "csvs", "Originals", "")
    final_destination = os.path.join(home, 'PycharmProjects', 'Sketch', 'sketch_web', 'static', 'videos', '')

    file_name = original_name.split('.')[0]

    # .webm to .mp4 + audio fades
    subprocess.call(
        f"ffmpeg -i {originals_path}{original_name} -filter_complex 'afade=d=2, areverse, afade=d=4, areverse' {encoded_path}{original_name}_one.mp4",
        shell=True)

    # move original file
    os.rename(f"{originals_path}{original_name}", f"{originals_final_path}{original_name}")

    # audio filtering 200hz - 6000hz
    subprocess.call(
        f"ffmpeg -i {encoded_path}{original_name}_one.mp4 -af 'highpass=f=200, lowpass=f=6000' {encoded_path}{original_name}_two.mp4",
        shell=True)

    # deleting intermediary file
    os.remove(f"{encoded_path}{original_name}_one.mp4")

    encoded_file_name = file_name + '_final.mp4'

    # audio normalizing
    subprocess.call(
        f"ffmpeg-normalize {encoded_path}{original_name}_two.mp4 -o {encoded_path}{encoded_file_name} -c:a aac -b:a 192k",
        shell=True)

    # deleting intermediary file
    os.remove(f"{encoded_path}{original_name}_two.mp4")

    wav_file_name = file_name + '.wav'

    # REGISTER FILE NAMES
    video = Video.objects.get_or_create(name=encoded_file_name)

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

    # do something with the data
    notes_series = df.note.value_counts(normalize=True).head(5)
    notes_dict = notes_series.to_dict()

    Video.objects.filter(name=encoded_file_name).update(notes=json.dumps(notes_dict))

    # moving csvs to final destination
    os.rename(f"{csv_path}{csv_file_name}", f"{csv_final_path}{csv_file_name}")
