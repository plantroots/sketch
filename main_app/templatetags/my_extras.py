import json
from datetime import timedelta
from os.path import splitext

from django import template

register = template.Library()


@register.filter(name="get_minutes")
def get_minutes(value):
    conversion = timedelta(seconds=value)
    # if a song has less than an hour, show only the minutes
    if str(conversion)[0] == "0":
        return str(conversion)[2:]
    else:
        return str(conversion)


@register.filter(name="display_song_name")
def display_song_name(value):
    # removing the extension from the filename
    value = splitext(value)[0]
    result = ''.join([i for i in value if not i.isdigit() and i != '.'])
    result = result.replace("Theory of Mind - ", "")
    return result


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
