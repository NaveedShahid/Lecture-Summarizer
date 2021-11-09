import nltk
nltk.download('wordnet')
nltk.download('stopwords')
import logging
import json
from alive_progress import alive_bar
from embeddings import sent_emb_sif, word_emb_elmo
from model.method import SIFRank, SIFRank_plus
from stanfordcorenlp import StanfordCoreNLP
from config import MAX_WORDS_PER_LINE, STANFORD_CORE_NLP_PATH, ELMO_WEIGHTS_FILE, ELMO_OPTIONS_FILE

def extract_keywords(summary):
    altered_paragraphs={}
    logging.info("Loading keyword extraction model....")            
    porter = nltk.PorterStemmer()
    ELMO = word_emb_elmo.WordEmbeddings(ELMO_OPTIONS_FILE, ELMO_WEIGHTS_FILE)
    SIF = sent_emb_sif.SentEmbeddings(ELMO, lamda=1.0)
    en_model = StanfordCoreNLP(STANFORD_CORE_NLP_PATH,quiet=False)
    elmo_layers_weight = [0.0, 1.0, 0.0]
    with alive_bar(len(summary),title='Keyword Extraction',calibrate=20, spinner='twirls') as bar:
        for para in summary:
            bar()
            words = list(para)
            words = [w.replace('%', 'percent') for w in words]
            para="".join(words)
            if len(para.split())>MAX_WORDS_PER_LINE:
                logging.info("Extracting keywords....")
                keyphrases_ = SIFRank_plus(para, SIF, en_model, N=15, elmo_layers_weight=elmo_layers_weight)
                keyphrase_=keyphrases_[0]
                keyphrase = keyphrase_[0]
                if keyphrase in altered_paragraphs.keys():
                    old_line=altered_paragraphs.get(keyphrase)
                    new_line=old_line+" "+para
                    altered_paragraphs[keyphrase]=new_line
                else:
                    altered_paragraphs.update({keyphrase:para}) 
            else:
                altered_paragraphs.update({"Untitled":para})
    new_summ=[]
    for item in altered_paragraphs.items():
        head=item[0]
        body=item[1]
        new_summ.append(str(head+":\n\t"+body+"\n\n"))
        

    del summary
    return new_summ