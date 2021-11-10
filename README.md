# Lecture-Summarizer
Summarize a live audio lecture, a text file or an audio file using BART transformer model.

1. Install linux packages
2. ``$ sudo apt-get install ffmpeg``  
   ``$ sudo apt-get install poppler-utils``  
   
3. For conda installation(optional):   
   ``$ conda env create -f environment.yml``

4. Install pip packages with  
  	``$ pip install -r requirements.txt``    
    Change directory to /server and run	  
    ``$ python summarizer.py --install True``
6. Run tests for mp3 file  
 ``$ python summarizer.py --audio_file path_to_mp3``
8. Run tests for text file	  
``$ python summarizer.py --text_file path_to_transcript``
10. Run tests for microphone recording    
``$ python summarizer.py --record True``
12. Once the summarizer is working as usual, cd to the client directory and run   
``npm install``   
14. This command requires node.js installed
15. After npm install finishes, open a react front-end in the default browser by running   
``npm start``
17. To start the Flask backend, cd to the server directory and run   
``python app.py`` 

![Alt Text](https://github.com/NaveedShahid/Lecture-Summarizer/blob/main/client/public/app.gif)

19. The server stores the transcripts and summaries in a MongoDB database. Make sure MongoDB is installed. Run   
``mongo``  
in cmd to start MongoDB server.
21. Try out the Lecture Summarizer  

**Note**: For summarizing an audio file or live audio, the google API credentials need to be replaced with working ones. More info at [GCP Speech-to-text](https://console.cloud.google.com/speech)

**Note** : For now summarizer and other models require large amount of disk space (download on first run 1.63 GB bart model, 483 MB stanford nlp library, 367 MB elmo model, Pytorch and transformers almost 1.5-2 GB)
	be patient on the first run
	
**Note** : Summarizer uses cpu and gpu resources if available (GPU recommended) and memory upto 5 GB when running. atleast 8-12 GB RAM recommended

**Note** : If GPU is not installed the summarizer will still run but will take upto 5 minutes for a 2 minute audio

**Note** : For using GPU make sure NVIDIA GPU is installed with drivers and pytorch using  
	``$ pip install torch==1.7.0+cu110 torchvision==0.8.1+cu110 torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html``
