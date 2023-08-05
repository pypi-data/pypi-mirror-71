import os
import wave
import sys
from google.cloud import speech
from google.cloud import translate
from google.cloud import texttospeech
import requests

"""
Getting CREDENTIAL File:

1. console.cloud.google.com
2. create and download JSON file at "Credentials > Service Account Key" from your project
"""

translate_client = None
speech_client = None
    
class OverSizeError (Exception):
    pass

def get_translate (text, lang = 'en'):
    global translate_client
    if translate_client is None:
        translate_client = translate.Client()
    translation = translate_client.translate(text, target_language=lang)
    # translation = {'translatedText': 'Hello', 'detectedSourceLanguage': 'ko', 'input': '안녕'}
    return translation['translatedText']

def get_speech (audio_clip_path, lang = 'en-US'):
    global speech_client
    if speech_client is None:
        speech_client = speech.SpeechClient ()
        
    if os.path.getsize(audio_clip_path) > 100000000:
        raise OverSizeError
        
    with wave.open(audio_clip_path,'rb') as temp:
        frequency = temp.getframerate()
    with open(audio_clip_path,'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content = content)
    config = speech.types.RecognitionConfig (
        encoding = speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = frequency,
        language_code = lang
    )
    response=speech_client.recognize(config, audio)
    
    if not response.results:
        return ''             
    for result in response.results:
        # Applying Google cloud speech api and recording its result on the database.
        alternatives =result.alternatives
        alternative = alternatives[0].transcript
        if alternative:
            return alternative    
    return ''

def synth_speech (text, lang = 'en-US', voice_name = None):
    if voice_name is None:
        if lang == 'en-US':
            voice_name = 'en-US-Wavenet-E'
        elif lang == 'ko-KR':
            voice_name = 'ko-KR-Wavenet-D'
        else:
            voice_name = '{}-Wavenet-A'.format (lang)

    client = texttospeech.TextToSpeechClient()
    if text.find ('</speak>') != -1:
        synthesis_input = texttospeech.types.SynthesisInput (ssml = text)
    else:
        synthesis_input = texttospeech.types.SynthesisInput (text = text)
    voice = texttospeech.types.VoiceSelectionParams (
        language_code = lang,
        name = voice_name
    )
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    return response.audio_content


if __name__ == '__main__':
    '''
    print (get_translate ("안녕하세요?"))
    print (get_translate ("Who are you?", "ko"))
    
    print (get_speech ("test-music.wav"))
    print (get_speech ("test-voice.wav"))
    '''
    set_credential ('/home/ubuntu/sns/peperone-api/apiserve/services/helpers/google-credential.json')
    mp3 = synth_speech ("<speak> <emphasis level=\"strong\">To be</emphasis> <break time=\"200ms\"/> or not to be, <break time=\"400ms\"/> <emphasis level=\"moderate\">that</emphasis> is the question.<break time=\"400ms\"/> Whether ‘tis nobler in the mind to suffer The slings and arrows of outrageous fortune,<break time=\"200ms\"/> Or to take arms against a sea of troubles And by opposing end them. </speak>")
    with open ('out.mp3', 'wb') as f:
        f.write (mp3)
