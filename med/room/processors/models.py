
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import word2vec
from sklearn.manifold import TSNE
import numpy as np
from med.room.processors.transform_data import NedRoomClean
import pandas as pd
from med.room.utils import logger




class Transform(NedRoomClean):

    def __init__(self, 
                text_words: str,
                especifc_word_similar: str,
                list_of_relationship_positive: list,
                list_of_relationship_negative: list,
                min_count: int,
                window: int):
        

        self.text_words = text_words
        self.especifc_word_similar = especifc_word_similar
        self.list_of_relationship_positive = list_of_relationship_positive
        self.list_of_relationship_negative = list_of_relationship_negative
        self.min_count = min_count
        self.window = window


    @classmethod
    def createModel_word2vec(self, text, min_count=None,window=None):
        model = word2vec.Word2Vec(text, min_count=min_count, window=window)
        return model
    

    @classmethod
    def get_similar_words(self, model):

        text_words = [x for x in model.wv.vocab]
        embedding_clusters = []
        word_clusters = []
        for word in text_words:
            embeddings = []
            words = []
            for similar_word, _ in model.most_similar(word, topn=30):
                words.append(similar_word)
                embeddings.append(model[similar_word])
            embedding_clusters.append(embeddings)
            word_clusters.append(words)
            similar = model.most_similar
                
        return similar, word_clusters
    
    

    @classmethod
    def word_embedding(self, model):

        text_words = [x for x in model.wv.vocab]
        embedding_clusters = []
        word_clusters = []
        for word in text_words:
            embeddings = []
            words = []
            for similar_word, _ in model.most_similar(word, topn=30):
                words.append(similar_word)
                embeddings.append(model[similar_word])
            embedding_clusters.append(embeddings)
            word_clusters.append(words)

        embedding_clusters = np.array(embedding_clusters)
        n, m, k = embedding_clusters.shape
        tsne_model_en_2d = TSNE(perplexity=10, n_components=2, init='pca', n_iter=3500, random_state=32)
        embeddings_en_2d = np.array(tsne_model_en_2d.fit_transform(embedding_clusters.reshape(n * m, k))).reshape(n, m, 2)

        return embeddings_en_2d


    @classmethod
    def model_keys(self, model):
        list_vocab = [x for x in model.wv.vocab]
        return list_vocab
    

    @classmethod
    def build_matrix_similar_words(self, model):
        words = [x for x in model.wv.vocab]
        similarities = np.zeros((len(words), len(words)), dtype=np.float_)
        for idx1, word1 in enumerate(words):
            for idx2, word2 in enumerate(words):
                # note KeyError is possible if word doesn't exist
                sim = model.similarity(word1, word2)
                similarities[idx1, idx2] = sim
                
        df = pd.DataFrame.from_records(similarities, columns=words)
        df.index = words
        return words, df
    

    @classmethod
    def relationship_words(self, model, list_of_relationship_positive, list_of_relationship_negative):
        return model.most_similar(positive=list_of_relationship_positive, negative=list_of_relationship_negative)
    

    @classmethod
    def target_source_sentences(self, model, target_sentence, w2v_vocab):

        for i in target_sentence:
            sentences = [x for x in model.wv.vocab]
            sentences_similarity = np.zeros(len(sentences))

            target_sentence_words = [w for w in i.split() if w in w2v_vocab]
            for idx, sentence in enumerate(sentences):
                sentence_words = [w for w in sentence.split() if w in w2v_vocab]
                sim = model.n_similarity(target_sentence_words, sentence_words)
                sentences_similarity[idx] = sim

            result = list(zip(sentences_similarity, sentences))
            result.sort(key=lambda item:item[0], reverse=True)
            logger.info(f"Target: {target_sentence}")
            logger.info(result)      

        return target_sentence, result
    
