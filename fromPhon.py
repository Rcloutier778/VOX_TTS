import os
import pronouncing

from pydub import AudioSegment


PATH = r'C:\Users\Richard\Documents\Coding Projects\VOX_TTS'
SOUND_DIR = os.path.join(PATH,'VOX')
OUT_DIR = os.path.join(PATH,'VOX_out')
PHON_DIR = os.path.join(PATH,'VOX_phonetics')

def main():
    
    word='conditioner'
    phones = pronouncing.phones_for_word(word)[0].split(' ')
    newAudio = None
    for phon in phones:
        print(phon)
        
        phon_phon_dir = os.path.join(PHON_DIR, phon)
        if not os.path.exists(phon_phon_dir):
            print('%s doesn\'t exist!!!!'% phon)
            break
        phon_file = os.listdir(phon_phon_dir)[0]
        phonAudio = AudioSegment.from_wav(os.path.join(phon_phon_dir, phon_file))
        if not newAudio:
            newAudio = phonAudio
        else:
            newAudio += phonAudio
        
    newAudio.export(os.path.join(PATH,'test.wav'), format='wav')
    
    

if __name__=='__main__':
    main()