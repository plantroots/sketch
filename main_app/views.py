import os
from os import listdir
from os.path import isfile, join
from pathlib import Path

from django.shortcuts import render, redirect
from main_app import forms
from main_app.models import Category
from main_app.models import Video
from main_app.tasks import encode_video


# Create your views here.

def index(request):
    videos = Video.objects.all()
    videos_dict = {'videos': videos}
    return render(request, "main_app/index.html", context=videos_dict)


def video_focus(request, id):
    video = Video.objects.get(id=id)
    form_one = forms.CommentForm(instance=video)

    if request.method == "POST":
        form_one = forms.CommentForm(request.POST, instance=video)
        if form_one.is_valid():
            form_one.save(commit=True)
        else:
            print("Error! Form invalid!")
    return render(request, 'main_app/video_focus.html', {'form_one': form_one, 'video': video})


def favourites(request):
    videos = Video.objects.filter(favorite=True)
    videos_dict = {'videos': videos}
    return render(request, "main_app/index.html", context=videos_dict)


def themes(request):
    category = Category.objects.get(name="Theme")
    videos = Video.objects.filter(category=category.id)
    videos_dict = {'videos': videos}
    return render(request, "main_app/index.html", context=videos_dict)


def harmony(request):
    category = Category.objects.get(name="Harmony")
    videos = Video.objects.filter(category=category.id)
    videos_dict = {'videos': videos}
    return render(request, "main_app/index.html", context=videos_dict)


def songs(request):
    category = Category.objects.get(name="Song")
    videos = Video.objects.filter(category=category.id)
    videos_dict = {'videos': videos}
    return render(request, "main_app/index.html", context=videos_dict)


def other(request):
    category = Category.objects.get(name="other")
    videos = Video.objects.filter(category=category.id)
    videos_dict = {'videos': videos}
    return render(request, "main_app/index.html", context=videos_dict)


def encoder(request):
    home = str(Path.home())
    originals_path = os.path.join(home, "Videos", "Webcam", "")
    onlyfiles = [f for f in listdir(originals_path) if isfile(join(originals_path, f))]
    for f in onlyfiles:
        encode_video.delay(f)
    return redirect('/')


def delete_video(request, id):
    video = Video.objects.get(id=id)
    home = str(Path.home())
    final_destination = os.path.join(home, 'PycharmProjects', 'Sketch', 'sketch_web', 'static', 'videos', '')

    # deleting mp4
    os.remove(f"{final_destination}{video.name}")

    csv_final_path = os.path.join(home, "PycharmProjects", "Sketch", "sketch_web", "data", "csvs", "Originals", "")

    # deleting csv
    os.remove(f"{csv_final_path}{video.name.split('_final')[0] + '.f0.csv'}")

    # deleting from DB
    Video.objects.filter(id=id).delete()
    return redirect('/')
