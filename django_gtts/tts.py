import re
import warnings
from six.moves import urllib
from io import BytesIO
import requests
import logging
from urllib3.exceptions import InsecureRequestWarning
from .gtts_token import Token

logger = logging.getLogger('django-gtts')


class gTTS:
    """ gTTS (Google Text to Speech): an interface to Google's Text to Speech API """

    # Google TTS API supports two read speeds
    # (speed <= 0.3: slow; speed > 0.3: normal; default: 1)
    class Speed:
        SLOW = 0.3
        NORMAL = 1

    GOOGLE_TTS_URL = 'https://translate.google.com/translate_tts'
    MAX_CHARS = 100  # Max characters the Google TTS API takes at a time
    LANGUAGES = {
        'af': 'Afrikaans',
        'sq': 'Albanian',
        'ar': 'Arabic',
        'hy': 'Armenian',
        'bn': 'Bengali',
        'ca': 'Catalan',
        'zh': 'Chinese',
        'zh-cn': 'Chinese (Mandarin/China)',
        'zh-tw': 'Chinese (Mandarin/Taiwan)',
        'zh-yue': 'Chinese (Cantonese)',
        'hr': 'Croatian',
        'cs': 'Czech',
        'da': 'Danish',
        'nl': 'Dutch',
        'en': 'English',
        'en-au': 'English (Australia)',
        'en-uk': 'English (United Kingdom)',
        'en-us': 'English (United States)',
        'eo': 'Esperanto',
        'fi': 'Finnish',
        'fr': 'French',
        'de': 'German',
        'el': 'Greek',
        'hi': 'Hindi',
        'hu': 'Hungarian',
        'is': 'Icelandic',
        'id': 'Indonesian',
        'it': 'Italian',
        'ja': 'Japanese',
        'km': 'Khmer (Cambodian)',
        'ko': 'Korean',
        'la': 'Latin',
        'lv': 'Latvian',
        'mk': 'Macedonian',
        'no': 'Norwegian',
        'pl': 'Polish',
        'pt': 'Portuguese',
        'ro': 'Romanian',
        'ru': 'Russian',
        'sr': 'Serbian',
        'si': 'Sinhala',
        'sk': 'Slovak',
        'es': 'Spanish',
        'es-es': 'Spanish (Spain)',
        'es-us': 'Spanish (United States)',
        'sw': 'Swahili',
        'sv': 'Swedish',
        'ta': 'Tamil',
        'th': 'Thai',
        'tr': 'Turkish',
        'uk': 'Ukrainian',
        'vi': 'Vietnamese',
        'cy': 'Welsh'
    }

    def __init__(self, text, lang='en', slow=False, debug=False, proxies=None):
        self.debug = debug

        assert lang.lower() in self.LANGUAGES, 'Language not supported: %s' % lang
        assert text, 'No text to speak'

        self.lang = lang.lower()
        self.text = text

        if proxies:
            self.proxies = proxies
        else:
            self.proxies = urllib.request.getproxies()

        # Read speed
        if slow:
            self.speed = self.Speed().SLOW
        else:
            self.speed = self.Speed().NORMAL

        # Split text in parts
        if self._len(text) <= self.MAX_CHARS:
            text_parts = [text]
        else:
            text_parts = self._tokenize(text, self.MAX_CHARS)

            # Clean
        def strip(x):
            return x.replace('\n', '').strip()

        text_parts = [strip(x) for x in text_parts]
        text_parts = [x for x in text_parts if len(x) > 0]
        self.text_parts = text_parts

        # Google Translate token
        self.token = Token(proxies=self.proxies)

    def save(self, savefile):
        """ Do the Web request and save to `savefile` """
        if type(savefile) == BytesIO:
            self.write_to_fp(savefile)
        else:
            with open(savefile, 'wb') as f:
                self.write_to_fp(f)
            f.close()

    def write_to_fp(self, fp):
        for idx, part in enumerate(self.text_parts):
            payload = {'ie': 'UTF-8',
                       'q': part,
                       'tl': self.lang,
                       'ttsspeed': self.speed,
                       'total': len(self.text_parts),
                       'idx': idx,
                       'client': 'tw-ob',
                       'textlen': self._len(part),
                       'tk': self.token.calculate_token(part)}
            headers = {
                "Referer": "https://translate.google.com/",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
            }
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
                try:
                    r = requests.get(
                        url=self.GOOGLE_TTS_URL,
                        params=payload,
                        headers=headers,
                        proxies=self.proxies,
                        verify=False,
                    )
                    if self.debug:
                        logger.debug("Headers: {}".format(r.request.headers))
                        logger.debug("Request url: {}".format(r.request.url))
                        logger.debug("Response: {}, Redirects: {}".format(r.status_code, r.history))
                    r.raise_for_status()
                    for chunk in r.iter_content(chunk_size=1024):
                        fp.write(chunk)

                except Exception as e:
                    logger.debug(e.message)
                    raise

    def _len(self, text):
        """ Get char len of `text`, after decoding if Python 2 """
        try:
            # Python 2
            return len(unicode(text))
        except NameError:
            # Python 3
            return len(text)

    def _tokenize(self, text, max_size):
        """ Tokenizer on basic punctuation """

        punc = "¡!()[]¿?.,،;:—。、：？！\n"
        punc_list = [re.escape(c) for c in punc]
        pattern = '|'.join(punc_list)
        parts = re.split(pattern, text)

        min_parts = []
        for p in parts:
            min_parts += self._minimize(p, " ", max_size)
        return min_parts

    def _minimize(self, thestring, delim, max_size):
        """ Recursive function that splits `thestring` in chunks
        of maximum `max_size` chars delimited by `delim`. Returns list. """

        if self._len(thestring) > max_size:
            idx = thestring.rfind(delim, 0, max_size)
            return [thestring[:idx]] + self._minimize(thestring[idx:], delim, max_size)
        else:
            return [thestring]


if __name__ == "__main__":
    proxies = dict(
        http='socks5://127.0.0.1:1086',
        https='socks5://127.0.0.1:1086',
    )
    tts = gTTS('hello', proxies=proxies)
    tts.save('hello.mp3')
