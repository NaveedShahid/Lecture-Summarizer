#Summarization Settings
MAX_WORDS_PER_LINE=15 #Number of words required to consider a line for summarization. Otherwise skip line
SUMMARY_RATIO=0.1 #Length of the summary relative to original text length (30% or 0.3 default)
MAX_LINES_PER_PARA=30 #Number of lines to cluster into a paragraph for summarization

#Keyword Extraction Settings
STANFORD_CORE_NLP_PATH='stanford-corenlp-4.2.0' #Path to Stanford core NLP library
ELMO_OPTIONS_FILE= "auxiliary_data/elmo_2x4096_512_2048cnn_2xhighway_options.json" #ELMO Options file path
ELMO_WEIGHTS_FILE= "auxiliary_data/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5" #ELMO Model Weights file path

#Google's Speech-to-text Settings
PATH_TO_GCP_JSON= "dazzling-ego-297009-6e03c87d770b.json"
STT_MODEL='video'
STT_LANGUAGE="en-US"  
STT_RATE=16000
INTERIM_RESULTS=False
GCS_BLOB_NAME = "audio_1_new"
