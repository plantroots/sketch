import os
from os import listdir
from os.path import isfile, join

from django.shortcuts import render, redirect
from main_app import forms
from main_app.models import Category, Video, Album, Song
from main_app.tasks import encode_video
from main_app.tasks import scan
from sketch_web.settings import STATIC_DIR, AUDIO_DIR, VIDEO_DIR


def index(request):
    videos = Video.objects.all()
    albums = Album.objects.order_by('year').all()
    context = {'videos': videos, 'albums': albums}
    return render(request, "main_app/index.html", context=context)


def video_focus(request, id):
    video = Video.objects.get(id=id)
    albums = Album.objects.order_by('year').all()
    form = forms.CommentForm(instance=video)

    if request.method == "POST":
        form = forms.CommentForm(request.POST, instance=video)
        if form.is_valid():
            form.save(commit=True)
        else:
            print("Error! Form invalid!")
    return render(request, 'main_app/video_focus.html', {'form_one': form, 'video': video, 'albums': albums})


def favourites(request):
    videos = Video.objects.filter(favorite=True)
    albums = Album.objects.order_by('year').all()
    context = {'videos': videos, 'albums': albums}
    return render(request, "main_app/index.html", context=context)


def encoder(request):
    originals_path = os.path.join(VIDEO_DIR, "")
    onlyfiles = [f for f in listdir(originals_path) if isfile(join(originals_path, f))]
    for f in onlyfiles:
        encode_video.delay(f)
    return redirect('/')


def delete_video(request, id):
    video = Video.objects.get(id=id)
    video_path = os.path.join(STATIC_DIR, 'videos', '')

    # deleting mp4
    os.remove(f"{video_path}{video.name}")

    csv_path = os.path.join(AUDIO_DIR, "Originals", "")

    # deleting csv
    os.remove(f"{csv_path}{video.name.split('_final')[0] + '.f0.csv'}")

    # deleting from DB
    Video.objects.filter(id=id).delete()
    return redirect('/')


def album_scan(request):
    album_path = os.path.join(STATIC_DIR, "sounds", "")
    onlyfiles = [f for f in listdir(album_path) if isfile(join(album_path, f))]

    for f in onlyfiles:
        scan.delay(f)
    return redirect('/')


def album_focus(request, id):
    albums = Album.objects.order_by('year').all()
    album = Album.objects.filter(id=id).get()
    song_objects = Song.objects.filter(album_id=id).order_by('order').all()
    return render(request, 'main_app/album_focus.html',
                  context={'songs': song_objects, 'album': album, 'albums': albums})


def category_view(request, name):
    category = Category.objects.get(name=name)
    videos = Video.objects.filter(category=category.id)
    albums = Album.objects.order_by('year').all()
    context = {'videos': videos, 'albums': albums}
    return render(request, "main_app/index.html", context=context)


def themes(request):
    return category_view(request, "Theme")


def harmony(request):
    return category_view(request, "Harmony")


def songs(request):
    return category_view(request, "Song")


def other(request):
    return category_view(request, "other")
