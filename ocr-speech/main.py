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
    


@app.get("/sampleOCR")
async def ocr():
    subscription_key = "37cf6d8217354a25b5bad0cc9a738599"
    endpoint = "https://ocr-computer-vision-imaginecup-2023.cognitiveservices.azure.com/"

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    print("===== Read File - remote =====")
    # Get an image with text
    read_image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"

    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read(read_image_url,  raw=True)

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

