from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.name)


class Video(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    notes = models.CharField(max_length=255)
    favorite = models.BooleanField(default=False)

    def __str__(self):
        if self.display_name == '':
            return str(self.name)
        else:
            return str(self.display_name)

class Album(models.Model):
    name = models.CharField(max_length=255, blank=True)
    year = models.IntegerField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    my_age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255, blank=True)
    duration = models.FloatField()
    tempo = models.FloatField()
    notes = models.CharField(max_length=255)

    def __str__(self):
        return str(self.filename)
