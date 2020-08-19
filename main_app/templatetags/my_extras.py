import json
from datetime import timedelta

from django import template

register = template.Library()


@register.filter(name="get_min")
def get_min(value):
    conversion = timedelta(seconds=value)
    return str(conversion)[2:]


@register.filter(name="display_album_name")
def display_album_name(value):
    value = value[:-4]
    result = ''.join([i for i in value if not i.isdigit() and i != '.'])
    return result[17:]


@register.filter(name="display_video_name")
def display_video_name(value):
    if (value.display_name and value.category):
        return value.display_name + ' - ' + value.category.name
    return value.display_name or value.category or 'default'


@register.filter(name="display_notes")
def display_notes(value):
    d_one = json.loads(value)
    d_two = dict((k, round(v, 2)) for k, v in d_one.items())
    my_ls = [(k, v) for k, v in d_two.items()]
    sorted_by_second = sorted(my_ls, key=lambda tup: tup[1], reverse=True)

    my_str = ''
    for k, v in sorted_by_second:
        my_str += "-> " + str(k) + ": " + str(int(v * 100)) + "%" + " "

    my_str = my_str.replace(")", "% ")
    my_str = my_str.replace("(", "-> ")
    my_str = my_str.replace("'", "")
    return my_str


@register.filter(name='display_notes_song')
def display_notes_song(value):
    output = ''.join([str(i) for i in value if i not in ["[", "]", "\""]])
    output = output.replace(",", " -->")
    return output
