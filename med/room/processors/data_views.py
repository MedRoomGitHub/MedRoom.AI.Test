import matplotlib.cm as cm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from sklearn.manifold import TSNE
import numpy as np
import pandas as pd
from med.room.processors.models import Transform


class DataVisualizer(Transform):

    def __init__(self, 
                model: object,
                title: str,
                model_similar: list,
                embedding_clusters: list,
                list_vocab: list,
                word_: list,
                words, 
                df
                ):
    
        self.model = model
        self.title = title
        self.model_similar = model_similar
        self.embedding_clusters = embedding_clusters
        self.list_vocab = list_vocab
        self.word_ = word_
        self.words = words
        self.df = df
        

    def tsne_plot_similar_words(title, labels, embedding_clusters, word_clusters, a=0.7, filename=None):
        plt.figure(figsize=(16, 9))
        colors = cm.rainbow(np.linspace(0, 1, len(labels)))
        for label, embeddings, words, color in zip(labels, embedding_clusters, word_clusters, colors):
            x = embeddings[:, 0]
            y = embeddings[:, 1]
            plt.scatter(x, y, c=color, alpha=a, label=label)
            for i, word in enumerate(words):
                plt.annotate(word, alpha=0.5, xy=(x[i], y[i]), xytext=(5, 2),
                            textcoords='offset points', ha='right', va='bottom', size=8)
        plt.legend(loc=4)
        plt.title(title)
        plt.grid(True)
        if filename:
            plt.savefig(filename, format='png', dpi=150, bbox_inches='tight')
        plt.show()


    def plo_similar_between_words(df):
        f, ax=plt.subplots(1, 1, figsize=(14,8))
        cmap = plt.cm.Blues
        mask = np.zeros_like(df)
        mask[np.triu_indices_from(mask)] = True
        sns.heatmap(df, cmap=cmap, mask=mask, square=True, ax=ax)
        _=plt.yticks(rotation=90)
        plt.xlabel('Words')
        _=plt.xticks(rotation=45)
        _=plt.title("Similarities between words")


    def dimensional_vector_words(model_wc, raw_words_of_interest, target_word):
        

        words_of_interest = []
        for woi in raw_words_of_interest:
            for word, _ in model_wc.most_similar(woi):
                words_of_interest.append(word)

        words_of_interest = list(set(words_of_interest))

        vectors = []
        for word in set(words_of_interest):
            vectors.append(model_wc[word])
            
        vectors = np.vstack(vectors) # turn vectors into a 2D array <words x 300dim>

        model = TSNE(n_components=2, perplexity=10, random_state=0)
        X_tsne = model.fit_transform(vectors)
        df_after_tsne = pd.DataFrame.from_records(X_tsne, columns=['x', 'y'])
        df_after_tsne['labels'] = words_of_interest

        # calculate similarity from a target word to all words, to use as our colour
        target_word = target_word
        similarities = []
        for woi in words_of_interest:
            similarity = min(max(0, model_wc.similarity(target_word, woi)), 1.0)
            similarities.append(similarity)

        # plot the T-SNE layout for words, darker words means more similar to our target
        plt.figure(figsize=(12,8))
        plt.xlim((min(X_tsne[:,0]), max(X_tsne[:,0])))
        plt.ylim((min(X_tsne[:,1]), max(X_tsne[:,1])))
        for idx in range(X_tsne.shape[0]):
            x, y = X_tsne[idx]
            label = words_of_interest[idx]
            color=str(min(0.6, 1.0-similarities[idx])) # convert to string "0.0".."1.0" as greyscale for mpl
            plt.annotate(s=label, xy=(x, y), color=color)
            #plt.annotate(s=label, xy=(x, y), weight=int(similarities[idx]*1000)) # use weight
        plt.tight_layout()
        plt.title("Word similarity (T-SNE) using vectors from {} words\nColoured by similarity to '{}'".format(len(words_of_interest), target_word))

