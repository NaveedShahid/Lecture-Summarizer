import time
import nltk
nltk.download('wordnet')
nltk.download('stopwords')

from bart_summarizer import do_summarize
from embeddings import sent_emb_sif, word_emb_elmo
from model.method import SIFRank, SIFRank_plus
from stanfordcorenlp import StanfordCoreNLP
from transcriber import record
from audio_transcriber import transcribe_audio
import sys
import time
import requests
import argparse
import os
import zipfile

parser = argparse.ArgumentParser(description='Summarization')
parser.add_argument('--text_file', metavar='PATH', default=None,
                    help='path to text file')
parser.add_argument('--model', default="bart", choices=["bart", "presumm"],
                    help='machine learning model choice')
parser.add_argument('--record',default=False,
                    help='record audio from microphone')
parser.add_argument("--audio_file", metavar='PATH', default=None,
                    help="path to the mp3 file")
parser.add_argument("--install", default=False,
                    help="install pre requisites")              
args = parser.parse_args()

def main():

    opt_file = "auxiliary_data/elmo_2x4096_512_2048cnn_2xhighway_options.json"
    wgt_file = "auxiliary_data/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"
    stanfordCoreNlp_path='./'
    model = args.model

    if not os.path.exists(wgt_file):
        url = 'https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5'
        r = requests.get(url, allow_redirects=True)
        with open(wgt_file, 'wb') as file:
            file.write(r.content)
            
    if not os.path.exists(stanfordCoreNlp_path):
        url2 = 'https://downloads.cs.stanford.edu/nlp/software/stanford-corenlp-4.2.0.zip'
        r2 = requests.get(url2, allow_redirects=True)
        with open('stanford-corenlp-4.2.0.zip', 'wb') as file2:
            file2.write(r2.content)
            
        with zipfile.ZipFile('stanford-corenlp-4.2.0.zip', 'r') as zip_ref:
            os.mkdir(stanfordCoreNlp_path)
            zip_ref.extractall(stanfordCoreNlp_path)
            os.remove('stanford-corenlp-4.2.0.zip')
                        		
    if args.install:
        sys.exit()
    if args.text_file is not None:
        with open(args.text_file) as f:
            text = f.read()
    elif args.record:
        text = record()
    elif args.audio_file is not None:
        text = transcribe_audio(args.audio_file)
    else:
        print("Please specify a text file or set the record argument to true")
        sys.exit()
    
    print("Generating summary please wait.....")
    start=time.time()
    summary = do_summarize(text,model)
    end=time.time()
    print("Generating summary took {time} seconds.....\n".format(time=end-start))
    
    print("Extracting keywords....")
    porter = nltk.PorterStemmer()
    ELMO = word_emb_elmo.WordEmbeddings(opt_file, wgt_file)
    SIF = sent_emb_sif.SentEmbeddings(ELMO, lamda=1.0)
    en_model = StanfordCoreNLP(r'stanford-corenlp-4.2.0',quiet=True)
    elmo_layers_weight = [0.0, 1.0, 0.0]
    altered_paragraphs=[]
    for para in summary:
        words = len(para.split()) 
        if words>6:
            keyphrases_ = SIFRank_plus(para, SIF, en_model, N=15, elmo_layers_weight=elmo_layers_weight)
            keyphrase=keyphrases_[0]
            new_line=str(keyphrase[0]).title()+": "+para+'\n'
            altered_paragraphs.append(new_line)
            
    with open("summary_keywords.txt",'w+') as f:
        print("Writing generated summaries to text file....")
        f.writelines(altered_paragraphs)
        f.close()
        print("Done")
if __name__=='__main__':
    main()

          
    