from multiprocessing import Pool

from datetime import datetime, timedelta

# Machine learning classification libraries
from sklearn import preprocessing
from sklearn.svm import SVC, SVR, NuSVC, LinearSVC
from sklearn.metrics import scorer
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neural_network import MLPClassifier

# For data manipulation
import pandas as pd
import numpy as np

import os
from scipy.io import wavfile
import pronouncing
import random
import aligner.align as align
from collections import defaultdict
import pprint
from pydub import AudioSegment

PATH = r'C:\Users\Richard\Documents\Coding Projects\VOX_TTS'
SOUND_DIR = os.path.join(PATH,'VOX')
OUT_DIR = os.path.join(PATH,'VOX_out')
PHON_DIR = os.path.join(PATH,'VOX_phonetics')

def parseTextGrid(fname):
    name = fname.split('.', 1)[0]
    phonDict = defaultdict(list)
    with open(os.path.join(OUT_DIR, fname), 'r') as f:
        lines = f.read().split('"IntervalTier"\n"phone"\n',1)[1].split('"IntervalTier"',1)[0].strip().split('\n')[3:]
        for indx in range(0, len(lines), 3):
            start, end, phon = lines[indx:indx + 3]
            phonDict[phon.replace('"', '').replace("'", '')].append([float(start), float(end), "%s.wav" % name])

    phonDict=dict(phonDict)
    return phonDict

def main():
    '''
    fs,data = wavfile.read(os.path.join(PATH, 'biological.wav'))

    newdata = []
    for i in data:
        newdata.append(0 if not random.randint(0,100) else i)
    
    newdata = np.asarray(newdata)
    scaled = np.int16(newdata/np.max(np.abs(newdata)) * 32767)
    
    wavfile.write(os.path.join(PATH,'testwav.wav'), fs, scaled)
    
    return
    '''
    
    '''
    files = {}
    for fname in [x for x in os.listdir(SOUND_DIR) if not x.startswith('_')]:
        fs, data = wavfile.read(os.path.join(SOUND_DIR,fname))
        files[fname[:-4]] = [fs,data,pronouncing.phones_for_word(fname[:-4])]
        align.main(os.path.join(SOUND_DIR,fname), os.path.join(OUT_DIR, fname))
    print('Done reading files')
    '''
    if not os.path.exists(PHON_DIR):
        os.mkdir(PHON_DIR)
    phonDict = defaultdict(list)
    
    
    do_total = True
    
    
    totalAudio = None
    if do_total:
        phonDict = parseTextGrid(os.path.join(PATH,'total.TextGrid'))
        totalAudio = AudioSegment.from_wav(os.path.join(PATH,'total.wav'))
    else:
        for fname in sorted(os.listdir(OUT_DIR)):
            tmpRes = parseTextGrid(fname)
            for phon in tmpRes:
                phonDict[phon].extend(tmpRes[phon])
    if 'sp' in phonDict:
        del phonDict['sp']
    pprint.pprint(phonDict)
    print(phonDict['D'])
    
    for phon in phonDict:
        phon_phon_dir = os.path.join(PHON_DIR, phon)
        if not os.path.exists(phon_phon_dir):
            os.mkdir(phon_phon_dir)
        for start, end, fname in phonDict[phon]:
            start, end = start * 1000.0, end * 1000.0
            try:
                audio = AudioSegment.from_wav(os.path.join(SOUND_DIR,fname)) if not do_total else totalAudio
                newAudio = audio[start:end]
                d = sorted(os.listdir(phon_phon_dir))
                newFilename = "%d.wav" % (0 if not d else int(d[-1].split('.',1)[0])+1)
                newAudio.export(os.path.join(phon_phon_dir,newFilename), format="wav",bitrate='16')
            except Exception:
                pass

def createTotal():
    naudio = None
    res = []
    skipwords = 'FOXTROT'
    for i in [x for x in os.listdir(SOUND_DIR) if not x.startswith('_') and x.upper().split('.',1)[0] not in skipwords]:
        if pronouncing.phones_for_word(i.split('.', 1)[0]):
            if not naudio:
                naudio = AudioSegment.from_wav(os.path.join(SOUND_DIR, i))
            else:
                naudio += AudioSegment.from_wav(os.path.join(SOUND_DIR, '_comma.wav'))
                naudio += AudioSegment.from_wav(os.path.join(SOUND_DIR, i))
            res.append(i.split('.', 1)[0].upper())
    naudio.export(os.path.join(PATH, 'total.wav'), format='wav')
    with open(os.path.join(PATH, 'total.txt'), 'w+') as f:
        f.write('\n'.join(res))


if __name__ == '__main__':
    main()
