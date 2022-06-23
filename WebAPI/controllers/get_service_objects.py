from Service import *
from Service import nlpEngine, preprocess


class GetServiceObject:
    def __init__(self):
        pass

    @staticmethod
    def get_preprocess_object():
        try:
            preprocess_object = preprocess.PreProcess
            return preprocess_object
        except Exception as e:
            print(e)
            return str(e)

    @staticmethod
    def get_nlp_engine_object():
        try:
            nlp_engine_object = nlpEngine.NLPEngine()
            return nlp_engine_object
        except Exception as e:
            print(e)
            return str(e)
