import unittest
from django_gtts import TTSpeech


class TestTTS(unittest.TestCase):
    def setUp(self):
        self.text = """
            人民银行负责人在防范和处置非法集资法律政策宣传座谈会上表示，《处置非法集资条例》已列入国务院 2018 年立法工作计划，央行将配合司法部推动《处置非法集资条例》和《非存款类放贷组织条例》出台。以应对一些不法分子以代币发行融资 ICO、各类虚拟货币等互联网金融创新为幌子进行非法集资。下一步人民银行将会同互联网金融风险专项整治工作领导小组相关成员单位，继续做好互联网金融风险防范化解，积极稳妥推进专项整治工作。
        """

    def test_speech(self):
        tts = TTSpeech(text=self.text,)
        data = tts.text_to_speech(lang='zh')
        self.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
