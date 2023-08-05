from pyssml.AmazonSpeech import AmazonSpeech
import boto3

polly_ = boto3.client('polly')
transcribe_ = boto3.client ('transcribe')

def polly (text, lang = 'ko-KR', voice_id = None):    
    if not voice_id:
        voice_id = lang == "ko-KR" and 'Seoyeon' or 'Joanna'
    response = polly_.synthesize_speech (
        Text = text,
        OutputFormat = 'mp3',
        VoiceId = voice_id,
        TextType = text.find ('</speak>') != -1 and 'ssml' or 'text'
    )
    stream = response.get ("AudioStream")
    return stream.read ()

# transcribe -----------------------------------------------
def upload_s3 (bucket, file):
    s3_.upload_file (file, bucket, file)
    return file

def transcribe (url, lang = 'ko-KR', job_name = 'TranscribeDemo', media_format = 'mp3'):
    transcribe_.start_transcription_job (
        TranscriptionJobName = job_name,
        LanguageCode = lang,
        MediaFormat = media_format,
        Media = {'MediaFileUri': url}
    )
    
