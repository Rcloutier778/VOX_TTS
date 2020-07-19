

from nltk.corpus import wordnet as wn
import num2words
import os
import functools


LONG_PAUSE = '_period'
SHORT_PAUSE = '_comma'

PATH = r"C:\Users\Richard\Documents\Coding Projects\VOX_TTS"

STYLE = None

OVERRIDES = {'too':'to'}

@functools.lru_cache(1024)
def get_words():
    return [word[:-4] for word in os.listdir(os.path.join(PATH,STYLE))] + list(OVERRIDES)

def isvalid(word):
    return word.lower() in get_words()


def convert_word(word):

    result = []

    # Quotes
    word = word.replace('\'', '').replace('"', '')

    #Dash
    if '-' in word:
        result.extend(convert_word(word.split('-',1)[0]))
        result.extend(convert_word(word.split('-', 1)[1]))
        return result

    # Misc chars
    for char in ['_', '=']:
        word = word.replace(char, '')

    # Pauses
    if any(word.endswith(x) for x in ['.', ',', ';', ':','!','?']):
        result.extend(convert_word(word[:-1]))

        # Long pause
        if any(word.endswith(x) for x in ['.', ':','!','?']):
            result.append(LONG_PAUSE)
        # short pause
        else:
            result.append(SHORT_PAUSE)
        return result

    # Numbers
    if word.isnumeric():
        for w in num2words.num2words(int(word)).split(' '):
            result.extend(convert_word(w))
        return result

    if not isvalid(word):
        checked = []
        for ss in wn.synsets(word):
            ss_name = ss.name().split('.',1)[0]
            if isvalid(ss_name):
                result.append(ss_name)
                print('Using %s as synonym for %s (%d checked)' % (ss_name, word, len(checked) + 1, ))
                break
            checked.append(ss_name)
            for ss_ln in [x for x in ss.lemma_names() if x not in checked]:
                if isvalid(ss_ln):
                    result.append(ss_ln)
                    print('Using %s as synonym for %s (%d checked)' % (ss_ln, word, len(checked) + 1,))
                    return result
                checked.append(ss_ln)
        # FIXME
        raise RuntimeError('%s is not a valid word and none of the following synonyms were valid words\n%s' % (word, str(checked),))
        return result
    
    result.append(word)
    return result

def create_sentance(words):
    import winsound
    path = os.path.join(PATH, STYLE)
    for word in words:
        word = OVERRIDES[word] if word in OVERRIDES else word
        winsound.PlaySound(os.path.join(path, word.lower() + '.wav'), 0)
        

def main(line='', style='VOX'):
    # style is VOX (Black Mesa)  /  HECU (Military)  /  BOTH (both...)
    global STYLE
    assert style in ['VOX','HECU', 'BOTH']
    STYLE = style
    print('Using %s style'%style)
    
    if not line:
        line = input("What do you want VOX to say? ")
        
    line = line.strip().lower()
    
    if not any(line.endswith(x) for x in ['.','?','!']):
        line += '.'
        
    words = []
    for word in line.strip().split(' '):
        if not word:
            continue
        words.extend(convert_word(word))
    
            
    print(words)
    
    create_sentance(words)
    
    



if __name__ == '__main__':
    main()
