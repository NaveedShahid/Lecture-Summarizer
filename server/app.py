import os
import time
from flask import Flask,request
from flask_cors import CORS
from google.cloud import storage
from google.cloud import speech
from google.oauth2 import service_account
from pymongo import MongoClient
from bson.objectid import ObjectId
from audio_transcriber import transcribe_audio 
from bart_summarizer import do_summarize
from keyword_extractor import extract_keywords
from config import GCS_BLOB_NAME, PATH_TO_GCP_JSON
import json

abs_path=os.getcwd()
app = Flask(__name__)
CORS(app)
key_name = PATH_TO_GCP_JSON

client = MongoClient('mongodb://localhost:27017')
db = client.transcriptionApp

@app.route('/recorded-audio', methods = ['POST'])

def audio():
    filename = request.headers['filename']
    speech_contexts = request.headers['speechContext']
    fn=filename+'.wav'
    audio_path= os.path.join('audio-files',fn)
    with open(audio_path, "wb") as f:
        data = request.get_data()
        f.write(data)
    transcript = transcribe_audio(audio_path,speech_contexts)
    print("Generating summary please wait.....")
    start=time.time()
    summary = do_summarize(transcript,'bart')
    end=time.time()
    print("Generating summary took {time} seconds.....\n".format(time=end-start))
    
    print("Extracting keywords....")
    keywords_summary = extract_keywords(summary) 
    
    # Query to db

    insert_transcript_into_db(filename,transcript,keywords_summary)
    delete_Blob(fn)
    return ''

# Get All transcripts

@app.route('/transcript', methods = ['GET'])

def get_transcripts():

    transcription = db.transcriptions
    result = list(transcription.find({}))
    return json.dumps(result, default=str)

# Delete a single transcript

@app.route('/transcript-delete/<id>',methods = ['DELETE'])

def delete_transcript(id):

    id = ObjectId(id)
    transcription = db.transcriptions
    transcription.delete_one({"_id" : id})

    return 'Deleted Successfully'

# Route for uploading a audio or text file and return the transcript + summary

@app.route('/upload-file',methods = ['POST'])

def upload_audio():

    filename = request.headers['filename']
    type = request.headers['type']
    type = type.split('/')
    type = type[1]
    # if text file
    file_path = os.path.join('audio-files',filename)
    if(type == 'plain'):
        data = request.get_data()
        with open(file_path, "wb") as f:
            f.write(data)
        with open(file_path,"r") as file:
            multipart_string = file.read()
            temp = multipart_string.split('Content-Type: text/plain')
            temp = temp[1]
            temp = temp.split('------')
            temp = temp[0]
            temp = temp.strip()
            with open(file_path,"w") as t:
                t.write(temp)
                
        with open(file_path,"r") as text_file:
            transcript = text_file.read()

        print("Generating summary please wait.....")
        start=time.time()
        summary = do_summarize(transcript,'bart')
        end=time.time()
        print("Generating summary took {time} seconds.....\n".format(time=end-start))
        print("Extracting keywords....")
        keywords_summary = extract_keywords(summary) 
        if len(filename.split('.'))>1:
            filename=filename.split('.')[0]
        insert_transcript_into_db(filename,transcript,keywords_summary)
        
    # else its an audio file
    else:
        data = request.get_data()
        with open(file_path, "wb") as f:
            f.write(data)
        transcript = transcribe_audio(file_path)
        print("Generating summary please wait.....")
        start=time.time()
        summary = do_summarize(transcript,'bart')
        end=time.time()
        print("Generating summary took {time} seconds.....\n".format(time=end-start))
        print("Extracting keywords....")
        keywords_summary = extract_keywords(summary) 
        if len(filename.split('.'))>1:
            filename=filename.split('.')[0]
        insert_transcript_into_db(filename,transcript,keywords_summary)

    return ''

# function to delete the audio blob from the cloud and from the local file system

def delete_Blob(audio_blob_name):
    os.remove(os.path.join(abs_path,'audio-files',audio_blob_name))

def insert_transcript_into_db(filename,transcript,keywords_summary):
    keywords_summary=''.join(keywords_summary)
    transcription = db.transcriptions
    transcription_object = {
        'transcription-name' : filename,
        'transcription-data' : transcript,
        'summary' : keywords_summary,  
    }
    insert_result = transcription.insert_one(transcription_object)

    return ''

if __name__ == '__main__':
    app.run(threaded=True)