
import re
import spacy
import unicodedata
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from med.room.utils import logger
import pandas as pd



NLTK_STOPWORDS = nltk.corpus.stopwords.words('portuguese')
PATH_SAVE = '/opt/med_room/datalake/transient'

class NedRoomClean: 

    def __init__(self):
      self.data_type =[]

    
    @classmethod
    def anonymizer(self, col, new_stopwords):

        stop_words = stopwords.words('portuguese')
        stop_words.pop(stop_words.index('não'))
        for i in new_stopwords:
            stop_words.append(i)

        col = unicodedata.normalize('NFD', col).encode('ascii', 'ignore').decode('utf-8')
        col = re.sub(' +', ' ', str(col).lower())
        col = re.sub('((http?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*', ' ', str(col).lower())
        col = re.sub('\S+@\S+', ' ', str(col).lower())
        col = re.sub('@\S+', ' ', str(col).lower())
        col = re.sub('\d', ' ', str(col).lower())
        col = re.sub('https:\S+', ' ', str(col).lower())
        col = re.sub('[^a-z0-9 ]+', ' ', str(col).lower())
        col = word_tokenize(col, language='portuguese')
        col_words = ' '.join([w for w in col if not w in stop_words])
        return col_words


    @classmethod
    def build_corpus(self, data):
        token_corpus = []
        for sentence in data:
            word_list = sentence.split(" ")
            token_corpus.append(word_list)
        return token_corpus
    



    @classmethod
    def save_file(self, df, filename):
        
        logger.info('save csf file')
        file_save = f'{filename}.csv'
        df.to_csv(f'{PATH_SAVE}/{file_save}', sep=';',encoding='utf-8',index=False)
        logger.info('Finishing Process')

        return df

    
    @classmethod
    def load_file(self, filename):

        logger.info('load csf file')
        file_save = f'{filename}.csv'

        df = pd.read_csv(f'{PATH_SAVE}/{file_save}', sep=';',encoding='utf-8')

        logger.info('Finishing Process')

        return df        
 



