import random
import joblib
import nltk
from nltk.stem import lancaster, WordNetLemmatizer
from tensorflow.keras.models import load_model


class TransformTokenizer:
    """ 'All in one' tokenizer. Tokenize and normalize (lemmatize or stem) a text corpus, depending on the given mode
    A RegEx can be used for the tokenisation.
    It's possible to use a custom lemmatizer/stemmer, defaults are WordNetLemmatizer or LancasterStemmer
    It's also possible to remove a custom list of stop words, or nltk stopwords for a given langage
    """
    def __init__(self, mode='lemma', normalizer=None, regex_pattern=None,
                 sw='english', used_postags=[]):
        """
        args:
            mode: {'lemma', 'stem'}, default='lemma' - normalization mode
            transformer: obj default=None - optional custom normalizer
            regexp_pattern: str, default=None - optional regxp for tokenization
            sw_lang: str, default='english' - stop words langage
            rmv_postags: list(str) - unused postags, to remove in the corpus
        """
        if mode and mode not in ['lemma', 'stem']:
            raise ValueError(":mode: must be 'lemma', 'stem' or None only.")
        # defines normalizer (custom or default) depending on the given mode
        self.mode = mode
        self.normalizer = normalizer or WordNetLemmatizer() if self.mode == 'lemma' else lancaster.LancasterStemmer()
        # defines regexptokenizer if pattern
        self.regexptokenizer = nltk.RegexpTokenizer(regex_pattern) if regex_pattern else None
        # defines stop words
        if sw and type(sw) == str:
            self.stop_words = nltk.corpus.stopwords.words(sw)
        elif sw and type(sw) == list:
            self.stop_words = sw
        self.used_postags = used_postags

    def __call__(self, doc):
        """
        args:
            doc: str - text document to tokenize
        output:
            list - tokenized document
        """
        # tokenization
        if self.regexptokenizer:
            tokens = self.regexptokenizer.tokenize(doc)
        else:
            tokens = nltk.word_tokenize(doc)
        # unused POStags removal
        if self.used_postags and tokens:
            postags = nltk.pos_tag(tokens)
            tokens = [x[0] for x in postags if (x[1] in self.used_postags) and (x[0] not in self.stop_words)]
        # Normalisation + stop words removal
        if self.mode == 'lemma':
            tokens = [self.normalizer.lemmatize(tkn) for tkn in tokens]
        elif self.mode == 'stem':
            tokens = [self.normalizer.stem(tkn) for tkn in tokens]
        return tokens


class Chatbot:
    def __init__(self, vect_resp_path, model_path, pred_threshold):
        """Chatbot initialisation : loads vectorizers, model, responses and inits threshold
        args:
            vect_resp_path: str - Path of the vectorizers+responses object
            model_path: str - Path of the vectorizers+responses object
            pred_threshold: float - Predictions theshold
        """
        # loading fitted vectorizers and the responses
        self.vectorizer, self.label_binarizer, self.responses = joblib.load(vect_resp_path)
        # loading model
        self.model = load_model(model_path)
        # define threshold
        self.pred_threshold = pred_threshold
        print('#### Vectorizers, model and responses loaded ####')

    def predict_intents(self, input):
        """ Predict the label (intent) of a user input for a given model.
        inputs:
            input: str - user sentence
        output:
            return_list: list(dict) - contain the list of results sorted by probability
        """
        input_vect = self.vectorizer.transform([input])
        preds = self.model.predict(input_vect.toarray())[0]
        results = [[i, r] for i, r in enumerate(preds) if r > self.pred_threshold]
        if not results:
            return [{'intent': 'noanswer'}]
        # sorting strength probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.label_binarizer.classes_[r[0]], "probability": str(r[1])})
        return return_list

    def get_response(self, intent):
        """ Returns a random response for a given intent
        inputs:
            intent: str - predicted intents of a user input
        output:
            result : str - The chatbot answers to display
        """
        resp = self.responses['responses'][self.responses['label'] == intent]
        result = random.choice(list(resp)[0])
        return result
