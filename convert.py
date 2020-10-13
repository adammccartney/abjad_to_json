#!/usr/bin/python

"""Script imports a definition.py file, which contains dictionaries of 
   abjad.PitchSegments

   data structures are retained

   all segments are converted to hertz values

   The output is a JSON file containing dictionaries in the json format 

   definition.py needs to be in pwd

   v0.1
   a few kinks to be ironed out: 
   1. trailing commas are not totally conforming to json standard
   2. no general case
   """

import abjad
import re

from definition import chord_voice as chord_voice
from definition import melody_voice as melody_voice
from definition import tremolo_voice as tremolo_voice

""" Module variables """
colors = ["blue", "green", "red", "black"]
phrases = ["p1", "p2", "p3"]
partials = [1, 2, 3, 4, 5, 6, 8, 10]
octaves = [0, 1, 2, 3, 4, 5, 6, 7, 8]

def rewrite_chord_voice_dict():
    open_bracket = f"{{ \n"
    dict_content = f"{open_bracket}"
    for color in colors:
        top_key = f"\"{color}\" : {{ \n"
        dict_content += top_key
        for octave in octaves:
            val = chord_voice[color][octave].hertz
            json_val_entry = f"{octave} : {val} , \n"
            dict_content += json_val_entry
            if octave != octaves[-1]:
                close_top_key = ""
            elif (octave == octaves[-1]) and (color != colors[-1]):
                close_top_key = f"}}, \n"
            elif (octave == octaves[-1]) and (color == colors[-1]):
                close_top_key = f"}} \n"
            dict_content += close_top_key
    close_bracket = f"}} \n"
    dict_content += close_bracket
    return dict_content

def rewrite_melody_voice_dict():
    open_bracket = f"{{ \n"
    dict_content = f"{open_bracket}"
    for color in colors[:-2]:
        top_key = f"\"{color}\" : {open_bracket}"
        dict_content += top_key
        for phrase in phrases:
            mid_key = f"\"{phrase}\" : {open_bracket}"
            dict_content += mid_key
            for partial in partials:
                val = melody_voice[color][phrase][partial].hertz
                json_val_entry = f"{partial} : {val} "
                dict_content += json_val_entry
                if partial != partials[-1]:
                    close_mid_key = f", MID \n"
                elif (partial == partials[-1]) and (phrase != phrases[2]):
                    close_mid_key = f"\n}} , MID\n"
                elif (partial == partials[-1]) and (phrase == phrases[2]):
                    close_mid_key = f"\n}} MID\n"
                dict_content += close_mid_key
        if color == colors[0]:
            close_top_key = f"}}, \n"
        elif color == colors[1]:
            close_top_key = f"}} \n"
        dict_content += close_top_key
    close_bracket = f"}}"
    dict_content += close_bracket
    return dict_content

def rewrite_tremolo_voice_dict():
    open_bracket = f"{{ \n"
    dict_content = f"{open_bracket}"
    for color in colors[:-2]:
        top_key = f"\"{color}\" : {open_bracket}"
        dict_content += top_key
        for octave in octaves[1:-2]:
            mid_key = f"{octave} : {open_bracket}"
            dict_content += mid_key
            for phrase in phrases:
                val = tremolo_voice[color][octave][phrase].hertz
                json_val_entry = f"\"{phrase}\" : {val} "
                dict_content += json_val_entry
                if phrase != phrases[-1]:
                    close_mid_key = f",\n"
                elif (phrase == phrases[-1]) and (octave != octaves[6]): #hard
                    close_mid_key = f"\n}} , \n"
                elif (phrase == phrases[-1]) and (octave == octaves[6]):
                    close_mid_key = f"\n}} \n"
                dict_content += close_mid_key
        if color == colors[0]:
            close_top_key = f"}}, \n"
        elif color == colors[1]:
            close_top_key = f"}} \n"
        dict_content += close_top_key
    close_bracket = f"}}"
    dict_content += close_bracket
    return dict_content

def get_chord_voice_pitches_as_hertz():
    chord_dict = rewrite_chord_voice_dict()
    melody_dict = rewrite_melody_voice_dict()
    tremolo_dict = rewrite_tremolo_voice_dict()
    hertz_dicts = [chord_dict, melody_dict, tremolo_dict]
    return hertz_dicts

def reformat_dicts_as_json(hertz_dicts):
    formatted_hertz_dicts = []
    for hertz_dict in hertz_dicts:
        formatted = replace_all_square_brackets(hertz_dict)
        formatted_hertz_dicts.append(formatted)
    return formatted_hertz_dicts

def replace_all_square_brackets(segment_string):
    string = segment_string
    pattern = r"([\[])((\d+)[\.](\d)+[,]?[ ]?)+([\]])"
    matches = re.findall(pattern, string)
    open_curly = "{ "
    close_curly = " }"
    for match in matches:
        p1 = match[0]
        p2 = match[4]
        string = string.replace(p1, open_curly)
        string = string.replace(p2, close_curly)
    return string

if __name__ == '__main__':
    import sys
    reformatted_dicts = get_chord_voice_pitches_as_hertz()
    chord_dict_file = open('chord_voice.json', 'w')
    chord_dict_file.write(reformatted_dicts[0])
    chord_dict_file.close()
    melody_dict_file = open('melody_voice.json', 'w')
    melody_dict_file.write(reformatted_dicts[1])
    melody_dict_file.close()
    tremolo_dict_file = open('tremolo_voice.json', 'w')
    tremolo_dict_file.write(reformatted_dicts[2])
    tremolo_dict_file.close()
