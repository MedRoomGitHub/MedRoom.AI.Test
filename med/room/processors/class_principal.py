from med.room.processors.transform_data import NedRoomClean
from med.room.processors.models import Transform
from med.room.utils import logger


class CallMethods(NedRoomClean):

    def __init__(self, 
                filename: str,
                column_text: list,
                additional_stop_words: list,
                especifc_word_similar: str,
                list_of_relationship_positive: list,
                list_of_relationship_negative: list):
        
        
        self.filename = filename
        self.column_text = column_text
        self.additional_stop_words = additional_stop_words
        self.especifc_word_similar = especifc_word_similar
        self.list_of_relationship_positive = list_of_relationship_positive
        self.list_of_relationship_negative = list_of_relationship_negative


        super().__init__()

    @classmethod
    def call_processors(self,
                        filename,
                        column_text,
                        additional_stop_words,
                        especifc_word_similar,
                        list_of_relationship_positive,
                        list_of_relationship_negative):
        
        logger.info('Start Process to Similary Words')

        logger.info('Load DataFrame')
        dataset = NedRoomClean.load_file(filename=filename)

        logger.debug(f'Numbers of columns and Rows {dataset.shape}')
        logger.debug(f'Columns Name {dataset.columns}')

        logger.info('Start Process to Transform Data')
        for index, i in enumerate(column_text):
            dataset[f'{column_text[index]}_clean'] = dataset[column_text[index]].apply(lambda x: NedRoomClean.anonymizer(x, additional_stop_words))
            logger.debug(f'column created: \n {dataset[f"{column_text[index]}_clean"]}')

                    
        logger.info('Convert Text to Tokens')
        for index, i in enumerate(column_text):
            dataset[f'{column_text[index]}_token'] = NedRoomClean.build_corpus(dataset[f'{column_text[index]}_clean'])
            logger.debug(f'column created: \n {dataset[f"{column_text[index]}_token"]}')


        logger.debug(f'concat two columns from text {column_text}')
        dataset['concatenado'] = dataset[f'{column_text[0]}_token'] + dataset[f'{column_text[1]}_token']
        logger.debug(f'consolideted column: \n {dataset["concatenado"]}')

        logger.info('Extract Features from Similar Words')
        model = Transform.createModel_word2vec(dataset['concatenado'], min_count=1, window=10)

        logger.debug(f'Visualize Vocabulary Similars \n {list(model.wv.vocab)}')

        logger.info('List of silimar Words')
        model_similar, word_clusters = Transform.get_similar_words(model=model)
        logger.debug(f'list of specific words \n {model_similar}')

        
        similar = [(item[0],round(item[1],2)) for item in model.most_similar(especifc_word_similar)]
        logger.info(f'Word selected: {especifc_word_similar} List of search specific similar words: {similar}')


        logger.info('Word Embedding')
        embeddings_en_2d = Transform.word_embedding(model)
        logger.debug(f"Word Embedding Results: \n {embeddings_en_2d} ")


        w2v_vocab = set(model.wv.vocab)
        logger.info(f"Loaded {w2v_vocab} words in vocabulary {len(w2v_vocab)}")

        logger.debug('build matrix with similar words')
        matrix_words, dataframe_matrix = Transform.build_matrix_similar_words(model=model)
        logger.debug(f"matrix of similars: n\ {matrix_words}")

        logger.debug('build relationship words positive e negative correlation')
        print_info = Transform.relationship_words(model, list_of_relationship_negative=list_of_relationship_negative, list_of_relationship_positive=list_of_relationship_positive)
        logger.debug(f'relationship words: \n {print_info}')

        logger.info("Finishing Process")

        return dataset, model_similar, matrix_words, dataframe_matrix, model, embeddings_en_2d, print_info, similar, word_clusters
    




      