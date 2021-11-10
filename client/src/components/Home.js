/* eslint-disable jsx-a11y/anchor-is-valid */
import { useState, useEffect } from 'react';
import RecordRTC from 'recordrtc';
import axios from 'axios';
import { Container, Row, Col } from 'react-bootstrap';
import VerticalModal from './layout/VerticalModal';


function Home() {
  const url = 'http://localhost:5000';

  // State Hooks

  let [audio, updateAudio] = useState();
  let [{ filename, speechContext, fileData }, setInputValue] = useState({
    filename: '',
    speechContext: '',
    fileData: null,
  });
  let [{ startButton, stopButton, pauseButton }, setDisabled] = useState({
    startButton: false,
    stopButton: false,
    pauseButton: false,
  });
  let [error, setError] = useState(false);
  let [recording, setRecording] = useState(null);
  let [timer, setTimer] = useState(0);
  let [intervalID, setIntervalID] = useState();
  let [modalShow, setModalShow] = useState(false);
  let [{ state, loading }, setState] = useState({ state: [], loading: false });
  let [pause, setPause] = useState(false);

  // Effect Hooks

  useEffect(() => {
    setState((prevValue) => ({ ...prevValue, loading: true }));

    axios.get(`${url}/transcript`).then((data) => {
      setState((prevValue) => ({
        ...prevValue,
        state: data.data,
        loading: false,
      }));
    });
  }, []);

  // Timer Variables
  const getSeconds = `0${timer % 60}`.slice(-2);
  const minutes = `${Math.floor(timer / 60)}`;
  const getMinutes = `0${minutes % 60}`.slice(-2);
  const getHours = `0${Math.floor(timer / 3600)}`.slice(-2);
const anime = require('animejs');

  // Functions

  const ModalHandler = (e, transcript_id) => {
    if (e === undefined) {
      setModalShow(false);
    } else {
      if (e.target.name === 'cancel') {
        setModalShow(false);
      } else {
        setModalShow(false);
        axios.delete(`${url}/transcript-delete/${transcript_id}`).then(() => {
          setState((prevValue) => ({ ...prevValue, loading: true }));

          axios.get(`${url}/transcript`).then((data) => {
            setState((prevValue) => ({
              ...prevValue,
              state: data.data,
              loading: false,
            }));
          });
        });
      }
    }
  };

  const transcriptDownload = (transcript, e) => {
    const blob = new Blob([transcript['transcription-data']], {
      type: 'text/plain',
    });
    e.target.download = transcript['transcription-name']+'-transcript';
    e.target.href = URL.createObjectURL(blob);
  };

  const summaryDownload = (transcript, e) => {
    const blob = new Blob([transcript['summary']], {
      type: 'text/plain',
    });
    e.target.download = transcript['transcription-name']+'-summary';
    e.target.href = URL.createObjectURL(blob);
  };

  const startRecording = () => {
    if (pause) {
      setPause((prevValue) => {
        pause = !prevValue;
      });
      setRecording(true);
      setDisabled({
        startButton: true,
      });
      setIntervalID(
        (intervalID = setInterval(() => {
          setTimer((timer) => timer + 1);
        }, 1000))
      );
      audio.resumeRecording();
    } else {
      if (filename.trim()) {
        setDisabled({
          startButton: true,
        });
        setError(false);
        setRecording(true);

        setIntervalID(
          (intervalID = setInterval(() => {
            setTimer((timer) => timer + 1);
          }, 1000))
        );

        navigator.mediaDevices
          .getUserMedia({
            audio: true,
          })
          .then((MediaStream) => {
            updateAudio(
              (audio = RecordRTC(MediaStream, {
                type: 'audio',
                mimeType: 'audio/webm',
                sampleRate: 44100, // this sampleRate should be the same in your server code
                numberOfAudioChannels: 1,
                recorderType: RecordRTC.StereoAudioRecorder,
              }))
            );

            audio.startRecording();
          });
      } else {
        setError(true);
      }
    }
  };

  const pauseRecording = () => {
    setPause(true);
    setRecording(false);
    setDisabled({
      startButton: false,
    });
    setTimer((prevValue) => (timer = prevValue));
    clearInterval(intervalID);
    audio.pauseRecording();
  };

  const stopRecording = () => {
    if (pause) {
      setPause((prevValue) => {
        pause = !prevValue;
      });
    }
    if (filename.trim()) {
      setDisabled({
        startButton: true,
        stopButton: true,
        pauseButton: true,
      });
      setError(false);
      setRecording(false);

      audio.stopRecording(() => {
        setTimer(0);
        clearInterval(intervalID);

        let data = audio.getBlob();
        axios
          .post(`${url}/recorded-audio`, data, {
            headers: {
              filename: filename,
              speechContext: speechContext,
            },
          })
          .then((data) => {
            setState((prevValue) => ({ ...prevValue, loading: true }));

            axios.get(`${url}/transcript`).then((data) => {
              setState((prevValue) => ({
                ...prevValue,
                state: data.data,
                loading: false,
              }));

              setInputValue((prevValue) => ({
                ...prevValue,
                filename: '',
                speechContext: '',
              }));
            });

            setDisabled({
              startButton: false,
              stopButton: false,
              pauseButton: false,
            });
            setRecording(null);
          })
          .catch((err) => {
            console.log(err);
            setDisabled({
              startButton: false,
              stopButton: false,
            });
            setRecording(null);
          });
      });
    } else {
      setDisabled((prevValue) => ({ ...prevValue, stopButton: false }));
      setError(true);
    }
  };

  const audioSubmitHandler = () => {
    setRecording(false);
    setDisabled({
      startButton: true,
      stopButton: true,
      pauseButton: true,
    });
    const formData = new FormData();
    formData.append('file', fileData);
    axios
      .post(`${url}/upload-file`, formData, {
        headers: {
          filename: fileData.name,
          type: fileData.type,
        },
      })
      .then((data) => {
        setRecording(null);
        setDisabled({
          startButton: false,
          stopButton: false,
          pauseButton: false,
        });

        setState((prevValue) => ({ ...prevValue, loading: true }));

        axios.get(`${url}/transcript`).then((data) => {
          setState((prevValue) => ({
            ...prevValue,
            state: data.data,
            loading: false,
          }));
        });
      });
  };

  return (
    <>
      <p className='header'>Lecture Summarizer</p>

      <Container>
        <Row>
          <Col xs={12} md={6}>
            <p className='left-section-content'>
              Start Recording Now To Generate Summaries
            </p>
            <p className='left-section-content lsc-child'>OR</p>
            <div className='left-section-upload-container'>
              <div className='audio-text'>
                <p>Upload Audio ( .mp3, .wav, .flac )</p>
                <p>Upload text file ( .txt )</p>
                <p>
                  Filename :{' '}
                  <span>{fileData !== null ? fileData.name : null}</span>{' '}
                </p>
              </div>
              <div className='audio-btn-container'>
                <label htmlFor='audioButton' className='audio-btn btn-1'>
                  Audio<i className='action-icon fa fa-upload'></i>
                </label>
                <input
                  onChange={(e) =>
                    setInputValue((prevValue) => ({
                      ...prevValue,
                      fileData: e.target.files[0],
                    }))
                  }
                  id='audioButton'
                  className='audio'
                  type='file'
                  name='audio'
                />
                <label htmlFor='audioButton' className='audio-btn btn-1'>
                  Text<i className='action-icon fa fa-upload'></i>
                </label>
                <input
                  onChange={(e) =>
                    setInputValue((prevValue) => ({
                      ...prevValue,
                      fileData: e.target.files[0],
                    }))
                  }
                  id='audioButton'
                  className='audio'
                  type='file'
                />
                <button
                  onClick={() => audioSubmitHandler()}
                  className='btn-1 audio-btn'
                >
                  Start Summarizing
                </button>
              </div>
            </div>
          </Col>
          <Col xs={12} md={6}>
            <div className='form'>
              <input
                className='input'
                placeholder='Enter File Name'
                name='filename'
                type='text'
                autoComplete='off'
                onChange={(e) => {
                  setInputValue((prevValue) => ({
                    ...prevValue,
                    filename: e.target.value,
                  }));
                }}
                value={filename}
              />
              <textarea
                className='speech-context'
                rows='3'
                type='text'
                placeholder='Enter Speech Contexts, example : Lecture 1, Physics, Law of motion'
                name='speechContext'
                onChange={(e) => {
                  setInputValue((prevValue) => ({
                    ...prevValue,
                    speechContext: e.target.value,
                  }));
                }}
                value={speechContext}
              ></textarea>
              <p className={error ? 'error-text' : 'error-text-none'}>
                Please enter a file name before proceeding.
              </p>
            </div>
            <div className='btn-container'>
              <button
                className='btn-1'
                onClick={() => startRecording()}
                disabled={startButton}
              >
                Start
                <i className='fa fa-microphone btn-1-icon'></i>
              </button>
              <button
                className='btn-1'
                onClick={() => pauseRecording()}
                disabled={pauseButton}
              >
                Pause
                <i className='fa fa-pause btn-1-icon'></i>
              </button>
              <button
                className='btn-1'
                onClick={() => stopRecording()}
                disabled={stopButton}
              >
                Stop
                <i className='fa fa-stop btn-1-icon'></i>
              </button>
            </div>

            <div className='status-container'>
              <i className='fa fa-clock-o'>
                <span className='clock-text'>{`${getHours}:${getMinutes}:${getSeconds}`}</span>
              </i>
              <p className='status-text'>
                Status :{' '}
                {recording === null
                  ? ''
                  : pause
                  ? 'Paused...'
                  : recording
                  ? 'Recording... '
                  : 'Processing...'}
              </p>
            </div>
          </Col>
          <Col xs={12}>
            <div className='text-list-header'>
              <p>Summarized Text Files</p>
            </div>
          </Col>
          <Col className='text-list-container' xs={12}>
            <div className='text-list-headings'>
              <p className='serial-header'>S.no</p>
              <p className='name-header'>Name</p>
              <p className='actions-header'>Actions</p>
            </div>
            {loading ? (
              <div>Loading...</div>
            ) : (
              state.map((transcription, index) => {
                return (
                  <div key={transcription['_id']} className='text-list'>
                    <p className='serial'>{index + 1}.</p>
                    <p className='name'>
                      {transcription['transcription-name']}
                    </p>
                    <p className='actions'>
                      <span className='action-space'></span>
                      <VerticalModal
                        show={modalShow}
                        onHide={(e) => ModalHandler(e, transcription['_id'])}
                      />
                      <a
                        onClick={(e) => summaryDownload(transcription, e)}
                        className='btn-1 btn-action btn-download'
                        download=''
                      >
                        Summary
                        <i className='action-icon fa fa-download'></i>
                      </a>
                      <a
                        onClick={(e) => transcriptDownload(transcription, e)}
                        className='btn-1 btn-action btn-download'
                        download=''
                      >
                        Transcript
                        <i className='action-icon fa fa-download'></i>
                      </a>
                      <button
                        className='btn-1 btn-action'
                        onClick={() => setModalShow(true)}
                      >
                        Delete
                        <i className='action-icon fa fa-trash'></i>
                      </button>
                    </p>
                  </div>
                );
              })
            )}
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default Home;
