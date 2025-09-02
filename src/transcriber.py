import whisper

class Transcriber:
    def __init__(self, weight="base"):
        self.model = whisper.load_model(weight)

    def transcribe_audio(self, audio_data, language='en'):
        result = self.model.transcribe(audio_data, language=language)
        return result["text"]