import json
from datetime import timedelta

from django import template

register = template.Library()

# TODO: rename to get_minutes
# TODO: only split the hour when it's 00
@register.filter(name="get_min")
def get_min(value):
    conversion = timedelta(seconds=value)
    return str(conversion)[2:]

# TODO: exclude the file extension in a more generic way
# TODO: exclude the band name in a more generic way (replace Theory of Mind)
@register.filter(name="display_album_name")
def display_album_name(value):
    value = value[:-4]
    result = ''.join([i for i in value if not i.isdigit() and i != '.'])
    return result[17:]


@register.filter(name="display_video_name")
def display_video_name(value):
    if (value.display_name and value.category):
        return value.display_name + ' - ' + value.category.name
    return value.display_name or value.category or 'sketch'


@register.filter(name="display_notes")
def display_notes(value):
    notes_dict = json.loads(value)
    notes_ls = [(k, round(v, 2)) for k, v in notes_dict.items()]
    sorted_by_second = sorted(notes_ls, key=lambda tup: tup[1], reverse=True)

    output = ''
    for k, v in sorted_by_second:
        output += "-> " + str(k) + ": " + str(int(v * 100)) + "%" + " "

    output = output.replace(")", "% ")
    output = output.replace("(", "-> ")
    output = output.replace("'", "")
    return output


@register.filter(name='display_notes_song')
def display_notes_song(value):
    output = ''.join([str(i) for i in value if i not in ["[", "]", "\""]])
    output = output.replace(",", " -->")
    return output
