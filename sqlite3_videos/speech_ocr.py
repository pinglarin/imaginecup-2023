from genericpath import exists
from fastapi import FastAPI
from fastapi import Response
import moviepy.editor as mp

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import azure.cognitiveservices.speech as speechsdk

from array import array
import os
from PIL import Image
import sys
import time
import cv2
import io
import numpy as np
from starlette.responses import StreamingResponse
from pydub import AudioSegment
import json
import subprocess


# app = FastAPI()


# @app.get("/sampleSpeech")
def recognize_from_long_file():

    # path = "media_files/comVidCutMP3.mp3" # ocr-speech/
    path = "comvideos/comVidCutMP4.mp4" # ocr-speech/
    # path = "sample_sound.mp3"
    name, extension = os.path.splitext(path)
    print("A")
    if (extension != '.wav'):
        # command = "ffmpeg -i " + path + " -ab 160k -ac 2 -ar 44100 -vn " + name + '_wav' + '.wav'
        # subprocess.call(command, shell=True)
        print("B")

        clip = mp.VideoFileClip(path) #.subclip(0,20)
        temppath = "tempaudio.mp3"
        clip.audio.write_audiofile(temppath)

        newpath = name + '_wav' + '.wav'
        os.system("mpg123 -w " + newpath + " " + temppath)
        path = newpath
        # sound = AudioSegment.from_mp3("/path/to/file.mp3")
        # sound.export("/output/path/file.wav", format="wav")
        # raw_audio = AudioSegment.from_file(path, format="mp3")
        # path = name + '_wav' + '.wav'
        # raw_audio.export(path, format="wav")
        print("convert to wav")
    print("C")
    

    speech_config = speechsdk.SpeechConfig(subscription="0b3f3cff3bf54688b7c9dbee47aaed1c", region="southeastasia")
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(filename=path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config) ####
    
    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    all_results = []
    # one_speech_result = {id: 0, 'text': "", offset}
    def handle_final_result(evt):
        ret = evt.result # + " " + evt.result.offset + " " + evt.result.duration
        all_results.append(ret)

    speech_recognizer.recognized.connect(handle_final_result)
    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    print("Printing all results:")
    print(all_results)
    return all_results

    # if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
    #     # ret = speech_recognition_result
    #     ret += "Recognized: {}".format(speech_recognition_result.text) + "\n\n"
    # elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
    #     ret += "No speech could be recognized: {}".format(speech_recognition_result.no_match_details) + "\n\n"
    # elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = speech_recognition_result.cancellation_details
    #     ret += "Speech Recognition canceled: {}".format(cancellation_details.reason) + "\n\n"
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         ret += "Error details: {}".format(cancellation_details.error_details) + "\n\n"
    #         ret += "Did you set the speech resource key and region values?" + "\n\n"

    # return ret
    # return Response(content=ret, media_type="application/json")

# @app.get("/displayFrame/{frameNum}")
async def displayFrame(frameNum):
    frameNum = int(frameNum)
    vidcap = cv2.VideoCapture('/Users/pinglarin/Documents/script_code/imaginecup-2023/ocr-speech/comVidCut_trim.mp4')
    vidcap.set(1, frameNum-1)
    res, frameImg = vidcap.read()

    res, im_png = cv2.imencode(".png", frameImg)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

# @app.get("/vidOCR/{vidID}")
async def vidOCR(path):
    print("start vid ocr")
    json_list = []
    count = 0
    # path = 'uploadedVideoes/'#"/Users/pinglarin/Documents/script_code/imaginecup-2023/ocr-speech/media_files/"
    cap = cv2.VideoCapture(path) # cv2.VideoCapture(path + vidID + '.mp4') # comVidCutMP4_trim_2.mp4
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("total frame count:", total_frame)
    if (total_frame <= 0): 
        print("Video Not Found")
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        # cv2.imshow('frame') # , gray
        b_br = cvtVidcapToIOBuffer(frame)
        frame_ocr_result = localocr(b_br)
        frame_result_loaded = json.loads(frame_ocr_result)
        json_list.append(frame_result_loaded)
        print("current frame:", count)
        count += 10000 # around five minutes
        cap.set(cv2.CAP_PROP_POS_FRAMES, count)
        
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    json_output = json.dumps(json_list)
    return Response(content=json_output, media_type="application/json")

def cvtVidcapToIOBuffer(frameImg):
    is_success, buffer = cv2.imencode(".jpg", frameImg)
    io_buf = io.BytesIO(buffer)
    # print(io_buf, "C")
    b_handle = io_buf
    b_handle.seek(0)
    # print(b_handle, "C.5")
    b_br = io.BufferedReader(b_handle)
    return b_br

# @app.get("/frameOCR/{frameNum}")
async def frameOCR(frameNum):
    # uuid, video_name, lecture_name, studentid, lecturerid
    frameNum = int(frameNum)
    # frameNum = 100
    vidcap = cv2.VideoCapture('/Users/pinglarin/Documents/script_code/imaginecup-2023/ocr-speech/comVidCut_trim.mp4')
    
    # amount_of_frames = vidcap.get(cv2.CV_CAP_PROP_FRAME_COUNT)

    vidcap.set(1, frameNum-1)
    res, frameImg = vidcap.read()
    # print(frameImg, "A")
    
    b_br = cvtVidcapToIOBuffer(frameImg)
    # print(b_br, "C.9")

    ret = localocr(b_br)
    
    ############# convert into short json ver.
    data = json.loads(ret)
    # created_time = data['created_date_time']
    # all_sentence = ""
    # for line in data['analyze_result']['read_results'][0]['lines']:
    #     all_sentence += line['text'] + " "
    # print(all_sentence)
    # output = {}
    # output['created_time'] = created_time
    # output['sentences'] = all_sentence
    # json_output = json.dumps(output)
    # print(data['analyze_result']['read_results'])

    return Response(content=ret, media_type="application/json")

    # res, im_png = cv2.imencode(".png", frameImg)
    # return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


# @app.get("/localOCR")
def localocr(img): # async
    subscription_key = "37cf6d8217354a25b5bad0cc9a738599"
    endpoint = "https://ocr-computer-vision-imaginecup-2023.cognitiveservices.azure.com/"

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    print("===== Read File - local =====")

    # read_image_path = "/Users/pinglarin/Documents/script_code/imaginecup-2023/ocr-speech/testimg.png"
    # read_image = open(read_image_path, "rb")
    print(img)
    # Call API with image and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(img, raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    print(read_operation_location)
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower () not in ['notstarted', 'running']:
            break
        print ('Waiting for result...')
        time.sleep(10)

    ret = ""

    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        # print(json.dumps(read_result.as_dict()))
        ret = json.dumps(read_result.as_dict())
        
        # for text_result in read_result.analyze_result.read_results:
        #     print(text_result)
        #     for line in text_result.lines:
        #         ret += ''.join(line.text) 
                
        #         ret += ' '.join(str(v) for v in line.bounding_box) 
                

    return ret

# @app.get("/sampleOCR")
def ocr(img): # async
    subscription_key = "37cf6d8217354a25b5bad0cc9a738599"
    endpoint = "https://ocr-computer-vision-imaginecup-2023.cognitiveservices.azure.com/"

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    print("===== Read File - remote =====")
    # Get an image with text
    # if 'img' in locals():
    read_image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"

    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read(read_image_url,  raw=True) # _in_stream
    print(computervision_client, read_response.headers)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    ret = ""

    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                ret += ''.join(line.text) + "\n\n"
                ret += ' '.join(str(v) for v in line.bounding_box) + "\n\n"

    return ret

    # uvicorn main:app --reload

