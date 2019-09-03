from gtts import gTTS
import time

import os


def tts(mytext, directoryname, filename):
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
