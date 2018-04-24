from tts import gTTS
from io import BytesIO
from hashlib import md5
from django.core.files.storage import get_storage_class
from django.conf import settings


class TTSpeech(object):

    def __init__(self, text):
        self.text = text
        storage = get_storage_class()
        self.s = storage()

    def text_to_speech(self, text, lang):
        tts = gTTS(text=text, lang=lang)
        output = BytesIO()
        tts.save(output)
        filename = md5(output).hexdigest()

        return filename

