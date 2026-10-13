# EN to JP phonemes for VPR
# reads a .vpr file and outputs .jp.vpr

import json
import csv
import io
import zipfile
import sys
import argparse
from pathlib import Path

# replaces the voice with this specific vb's info, if you set REPLACE_VB to True
REPLACE_VB = False
vb_comp_id = ''  # it will complain if you don't set this (it's a serial i think) but it should fix itself when opening
vb_name = 'MIKU_V4X_Original_EVEC'

def convert(data, args, language, phonemes_stage_1, phonemes_stage_2):
    # set voice used in vpr
    if REPLACE_VB:
        for voice in data["voices"]:
            voice["compID"] = vb_comp_id
            voice["name"] = vb_name

    for track in data["tracks"]:
        for part in track["parts"]:
            if REPLACE_VB:
                if "voice" in part:
                    # set language and voice ID for whole part
                    part["voice"]["langID"] = language
                    part["voice"]["compID"] = vb_comp_id
            if "notes" in part:
                for note in part["notes"]:
                    note["langID"] = language  # language ID
                    
                    # lock the phonemes
                    note["isProtected"] = True
                    
                    phonemes = note["phoneme"].split(" ")
                    
                    # pre-split phoneme renaming
                    for phoneme_in, phoneme_out in phonemes_stage_1.items():
                        phonemes = [p.replace(phoneme_in, phoneme_out) for p in phonemes]
                    
                    if args.japanese:
                        phonemes = [phoneme for row in phonemes for phoneme in row] # split to individual characters
                        phonemes = [phoneme for phoneme in phonemes if phoneme != ':'] # remove straggling ':'
                    
                    # post-split phoneme renaming
                    for phoneme_in, phoneme_out in phonemes_stage_2.items():
                        phonemes = [p.replace(phoneme_in, phoneme_out) for p in phonemes]

                    # in some cases there are duplicate phonemes beside each other
                    # such as an r-coloured vowel beside an r, for an example
                    # this cleans out duplicates by comparing phonemes to the one before it
                    # and refusing to add it to the string if it's the same one
                    phoneme_input = " ".join(phonemes)
                    phoneme_raw = phoneme_input[0]
                    for x in range(1,len(phoneme_input)):
                        if phoneme_input[x] != phoneme_input[x-1]: # checks if phoneme is different than the previous
                            phoneme_raw += phoneme_input[x]
                    note["phoneme"] = phoneme_raw
                    # print(note["phoneme"]) # if you want to print out each individual phoneme I guess

    return json.dumps(data, indent=4)

def main(args):
    input_path = Path(args.file)
    language = 0
    csv_path = "phonemes.csv"

    print("File: ", input_path)

    # since VPRs are just zip files in disguise with a sequence.json inside,
    # we can just copy all the files to a new zip except for the sequence.json,
    # modify that json file, and add it in at the end
    output_path = input_path.with_suffix(".jp.vpr")
    if args.english:
        output_path = input_path.with_suffix(".en.vpr")
        language = 1
        csv_path = "phonemes-jpn.csv"

    # read csv file so phonemes can be easily edited by user
    with open(csv_path, 'r') as f:
        reader = csv.reader(f, delimiter=';', skipinitialspace=True)
        phonemes_stage_1 = {} # multi-char phonemes to replace before splitting
        phonemes_stage_2 = {} # replacements after splitting all characters up
        stage = 1
        for k, v in reader:
        
            # looks for break in csv file, skips
            if stage == 0:
                stage = 2
            elif k == 'BREAK1':
                stage = 0
        
            # first half of csv file is for stage 1, second half for stage 2
            if stage == 1:
                phonemes_stage_1[k] = v
            elif stage == 2:
                phonemes_stage_2[k] = v

    print("Multi-char phonemes to replace: ", phonemes_stage_1)
    print("Phonemes to replace: ", phonemes_stage_2)
    
    with zipfile.ZipFile(input_path, mode="r") as input_vpr:
        with zipfile.ZipFile(output_path, mode="w") as output_vpr:
            # go through all file entries
            for entry in input_vpr.infolist():
                if entry.filename == "Project/sequence.json":
                    with input_vpr.open("Project/sequence.json", "r") as binary:
                        with io.TextIOWrapper(binary, encoding="utf-8") as f:  # wrap it to explicitly decode UTF-8
                            data = json.load(f)  # load-then-close
                    output_vpr.writestr(entry.filename, convert(data, args, language, phonemes_stage_1, phonemes_stage_2).encode('utf-8'))
                    print("Translated yay!!!!")
                else:
                    # if it's not a sequence.json copy the file as-is
                    output_vpr.writestr(entry.filename, input_vpr.read(entry.filename))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(__file__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-e", "--english", action="store_true", help="Convert Japanese phonemes to English ones.")
    parser.add_argument("-j", "--japanese", action="store_true", help="Convert English phonemes to Japanese ones.")
    parser.add_argument("-f", "--file", type=str, default="song.vpr", help="Project file")
    args = parser.parse_args() # either manually input the VPR filename here or pass it as a command line argument

    main(args)