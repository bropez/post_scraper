"""Text to Speech maker

This script creates an .mp3 audio file in the specified directory with a 
specified file name. 

This script requires that `gTTS` be installed within the Python environment
you are running this script in.

This file can also be imported as a module and contains the following
functions:
    * tts - Creates a text to speech audio file of a given string
"""


from gtts import gTTS
import time

import os


def tts(mytext: str, directoryname: str, filename: str):
    """Creates a text to speech audio file of a given string

    Args:
        mytext (str): The text to be turned into an audio file
        directoryname (str): The directory to save the audio in
        filename (str): The name of the file to save as

    Returns:
        None
    """
    language = 'en'
    myobj = gTTS(mytext, language)
    try:
        myobj.save('{}/sounds/{}.mp3'.format(directoryname, filename))
    except:
        time.sleep(10)
        myobj.save('{}/sounds/{}.mp3'.format(directoryname, filename))
    


if __name__ == '__main__':
    os.mkdir('tester_dir')
    os.mkdir('tester_dir/sounds')

    tts('testing this out.', 'tester_dir', 'tester')
