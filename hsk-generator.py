import pandas as pd
from hskDicts import HSK
import re
import zhon.pinyin
from unidecode import unidecode 
import random

carddeck = pd.DataFrame(columns=["hanzi", "pinyin", "definition", "example_sentence", "difficulty"])

acc2tone = {'ā': '1', 'ē': '1', 'ī': '1', 'ō': '1', 'ū': '1', 'ǖ': '1',
    'á': '2', 'é': '2', 'í': '2', 'ó': '2', 'ú': '2', 'ǘ': '2', 'ḿ': '2', 'ń': '2',
    'ǎ': '3', 'ě': '3', 'ǐ': '3', 'ǒ': '3', 'ǔ': '3', 'ǚ': '3', 'ň': '3',
    'à': '4', 'è': '4', 'ì': '4', 'ò': '4', 'ù': '4', 'ǜ': '4', 'ǹ': '4'}

accented="".join([a for a in acc2tone])

def accented2tones(sentence):
   """
   Credit:  calculatrix - www.chinese-forums.com
   """
   lastposition = 0
   retval = ""
   for match in re.finditer(zhon.pinyin.acc_syl,sentence,re.IGNORECASE):
      retval += sentence[lastposition:match.start()]
      pinyin = sentence[match.start():match.end()]
      m = re.findall('[%s]' % accented, pinyin)
      tone = acc2tone.get(m[0],"") if len(m) > 0 else ""
      umlaut = re.findall("[üǖǘǚǜ]",pinyin)
      pinyin = pinyin.replace(umlaut[0],"ü")+tone if len(umlaut) > 0 else unidecode(pinyin)+tone
      retval += pinyin
      lastposition = match.end()
   retval += sentence[lastposition:]
   return retval 

hsk1 = HSK.hsk1

for i,word in enumerate(hsk1['words']):
    try: 
        ex_sentence = random.choice([sent['hanzi'] for sent in hsk1['localizedSentences'] if word['hanzi'] in sent['hanzi']]) 
    except: 
        ex_sentence = "..."
    #carddeck.loc[i] = [word['hanzi'],accented2tones(word['pinyinToneSpace']),word['def'],ex_sentence,'Easy']
    carddeck.loc[i] = [word['hanzi'],(word['pinyinToneSpace']),word['def'],ex_sentence,'Easy']

carddeck.to_csv("hsk1_flashcards.csv", sep=",", index=False)