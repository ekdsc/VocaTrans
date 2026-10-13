# VocaTrans

Small program for quickly translating English phonemes in Vocaloid .VPR files to Japanese ones.

Program pulls phonemes to replace from the included phonemes.csv file - feel free to edit it based on what you prefer. A good reference list of equivalent phonemes can be found [here](https://vocaloid.fandom.com/wiki/English_-_Japanese). **Make sure the .csv is in the same folder as the .exe file or the program won't work.**

You will need to manually change the voicebank to a Japanese one when you reopen the file in Vocaloid editor. The phonemes are set to locked in the editor, if you need them to be regenerated you will need to unlock the phonemes for each note. You will probably also need to still tinker with the pronunciations, but this automates a lot of the repetitive aspects of retuning English words for a Japanese Vocaloid.

**EXE downloads are here** (Windows only): https://github.com/ekdsc/VocaTrans/releases

For running the Python code directly, no additional pip libraries are needed.

To use the interactive GUI: `python3 vocagui.py`

To use as a command-line tool: `python3 vocatrans.py -f <input_file>` where `<input_file>` is the directory and filename of the input VPR file.

The resulting output file is the input filename (in the same directory), but `.vpr` is replaced with `.jp.vpr`.

Converting Japanese phonemes to English ones is also possible. On the command line you can specify `-e`, and there is a checkbox on the command line.