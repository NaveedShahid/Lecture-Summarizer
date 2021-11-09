1. Install linux packages
2. 
	``$ sudo apt-get install ffmpeg``
	
	``$ sudo apt-get install poppler-utils``

2. For conda installation(optional):
	
	``$ conda env create -f environment.yml``

3. Install pip packages with
 	
	``$ pip install -r requirements.txt``
	
	``$ python summarizer.py --install True``
4. Run tests for mp3 file
	
	``$ python summarizer.py --audio_file path_to_mp3``
5. Run tests for text file
	
	``$ python summarizer.py --text_file path_to_transcript``
6. Run tests for microphone recording
	
	``$ python summarizer.py --record True``

**Note**: For summarizing an audio file or live audio, the google API credentials need to be replaced with working ones. More info at [GCP Speech-to-text](https://console.cloud.google.com/speech)

**Note** : For now summarizer and other models require large amount of disk space (download on first run 1.63 GB bart model, 483 MB stanford nlp library, 367 MB elmo model, Pytorch and transformers almost 1.5-2 GB)
	be patient on the first run
	
**Note** : Summarizer uses cpu and gpu resources if available (GPU recommended) and memory upto 5 GB when running. atleast 8-12 GB RAM recommended

**Note** : If GPU is not installed the summarizer will still run but will take upto 5 minutes for a 2 minute audio

**Note** : For using GPU make sure NVIDIA GPU is installed with drivers and pytorch using  

	``$ pip install torch==1.7.0+cu110 torchvision==0.8.1+cu110 torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html``
