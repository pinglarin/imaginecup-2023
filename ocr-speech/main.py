from genericpath import exists
from fastapi import FastAPI

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

app = FastAPI()

@app.get("/sampleSpeech")
def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(subscription="0b3f3cff3bf54688b7c9dbee47aaed1c", region="southeastasia")
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(filename="ocr-speech/sample_sound.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    ret = ""
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        ret += "Recognized: {}".format(speech_recognition_result.text) + "\n\n"
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        ret += "No speech could be recognized: {}".format(speech_recognition_result.no_match_details) + "\n\n"
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        ret += "Speech Recognition canceled: {}".format(cancellation_details.reason) + "\n\n"
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            ret += "Error details: {}".format(cancellation_details.error_details) + "\n\n"
            ret += "Did you set the speech resource key and region values?" + "\n\n"

    return ret

@app.get("/displayFrame/{frameNum}")
async def displayFrame(frameNum):
    frameNum = int(frameNum)
    vidcap = cv2.VideoCapture('/Users/pinglarin/Documents/script_code/imaginecup-2023/ocr-speech/comVidCut_trim.mp4')
    vidcap.set(1, frameNum-1)
    res, frameImg = vidcap.read()

    res, im_png = cv2.imencode(".png", frameImg)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

@app.get("/frameOCR/{frameNum}")
async def frameOCR(frameNum):
    frameNum = int(frameNum)
    # frameNum = 100
    vidcap = cv2.VideoCapture('/Users/pinglarin/Documents/script_code/imaginecup-2023/ocr-speech/comVidCut_trim.mp4')
    
    # amount_of_frames = vidcap.get(cv2.CV_CAP_PROP_FRAME_COUNT)

    vidcap.set(1, frameNum-1)
    res, frameImg = vidcap.read()
    # print(frameImg, "A")
    is_success, buffer = cv2.imencode(".jpg", frameImg)
    # print(buffer, "B")
    
    io_buf = io.BytesIO(buffer)
    # print(io_buf, "C")
    b_handle = io_buf
    b_handle.seek(0)
    # print(b_handle, "C.5")
    b_br = io.BufferedReader(b_handle)
    # print(b_br, "C.9")

    ret = localocr(b_br)

    return ret

    # res, im_png = cv2.imencode(".png", frameImg)
    # return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

@app.get("/testimg")
async def testimg():
    
    frameImg=cv2.imread('testimg.png')
    # cv2.imshow(frameImg)
    res, im_png = cv2.imencode(".png", frameImg)
    im_png.seek(0)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

@app.get("/localOCR")
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
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                ret += ''.join(line.text) 
                ret += ' '.join(str(v) for v in line.bounding_box) 

    return ret

@app.get("/sampleOCR")
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

