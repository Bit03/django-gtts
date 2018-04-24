from .tts import gTTS
from io import BytesIO
from hashlib import md5
# from django.core.files.storage import get_storage_class
# from django.conf import settings


class TTSpeech(object):

    def __init__(self, text, proxies=dict()):
        self.text = text
        if proxies:
            self.proxies = proxies
        else:
            self.proxies = None
        # storage = get_storage_class()
        # self.s = storage()

    def text_to_speech(self, lang):
        tts = gTTS(text=self.text, lang=lang, proxies=self.proxies)
        output = BytesIO()
        tts.save(output)
        return output


if __name__ == "__main__":
    tts = TTSpeech(text='您好')
