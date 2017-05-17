import os
import shutil
import unittest
from unittest import TestCase
from unittest.mock import patch, MagicMock
from hangul_fasttext import HangulFastText


class TestHangulFastText(TestCase):
    def setUp(self):
        self.hangul_ft = HangulFastText()
        self.temp_path = '/Users/hanseokjo/test/'
        self.temp_corpus_path = self.temp_path + 'temp_corpus'
        try:
            os.mkdir(self.temp_path)
        except FileExistsError:
            pass

        with open(self.temp_corpus_path, 'w') as f:
            sents = ['고기 먹고 싶다', '삼겹살에는 소주가 최고지']
            f.write('\n'.join(sents))

    def tearDown(self):
        shutil.rmtree(self.temp_path)
        self.hangul_ft = None

    def test__convert_word_to_jamo(self):
        tests = [
            ('나 고기 먹고 싶다', 'ㄴㅏ_ ㄱㅗ_ㄱㅣ_ ㅁㅓㄱㄱㅗ_ ㅅㅣㅍㄷㅏ_'),
            (['나', '고기', '먹고', '싶다'], ['ㄴㅏ_', 'ㄱㅗ_ㄱㅣ_', 'ㅁㅓㄱㄱㅗ_', 'ㅅㅣㅍㄷㅏ_'])
        ]

        for test, result in tests:
            with self.subTest(test=test):
                self.assertEqual(self.hangul_ft._convert_word_to_jamo(test), result)

    def test__del_jamo_corpus(self):
        fname = self.temp_path + 'test'
        with open(fname, 'w') as f:
            f.write('\n')

        self.hangul_ft._del_jamo_corpus(fname)
        self.assertFalse(os.path.isfile(fname))

    def test__generate_jamo_corpus(self):
        self.hangul_ft._generate_jamo_corpus(self.temp_corpus_path, postfix='_jamo')
        with open(self.temp_corpus_path + '_jamo', 'r') as f:
            tests = f.read().split('\n')

        results = [
            'ㄱㅗ_ㄱㅣ_ ㅁㅓㄱㄱㅗ_ ㅅㅣㅍㄷㅏ_',
            'ㅅㅏㅁㄱㅕㅂㅅㅏㄹㅇㅔ_ㄴㅡㄴ ㅅㅗ_ㅈㅜ_ㄱㅏ_ ㅊㅚ_ㄱㅗ_ㅈㅣ_'
        ]

        for test, result in zip(tests, results):
            with self.subTest(test=test):
                self.assertEqual(test, result)

    @patch('hangul_fasttext.HangulFastText.load')
    @patch('fasttext.skipgram')
    @patch('fasttext.cbow')
    def test_train(self, mock_cbow, mock_skipgram, mock_load):
        self.hangul_ft.train(input_txt=self.temp_corpus_path, output_path=self.temp_path+'ft', model='skipgram')
        mock_skipgram.assert_called_once_with(self.temp_corpus_path+'_jamo', self.temp_path+'ft', lr=0.1,
                                              lr_update_rate=100, dim=100, ws=5, epoch=10, min_count=10, neg=5,
                                              loss='ns', bucket=2000000, minn=3, maxn=6, thread=8, t=1e-4)

        self.hangul_ft.train(input_txt=self.temp_corpus_path, output_path=self.temp_path + 'ft', model='cbow')
        mock_cbow.assert_called_once_with(self.temp_corpus_path+'_jamo', self.temp_path+'ft', lr=0.1,
                                          lr_update_rate=100, dim=100, ws=5, epoch=10, min_count=10, neg=5,
                                          loss='ns', bucket=2000000, minn=3, maxn=6, thread=8, t=1e-4)

    @patch('gensim.models.wrappers.fasttext.FastText.load_fasttext_format')
    def test_load(self, mock_load):
        self.hangul_ft.load(self.temp_path+'_ft')
        mock_load.assert_called_once_with(self.temp_path+'_ft')

    def test_most_similar(self):
        positive = '긍정'
        negative = '부정'

        self.hangul_ft.fasttext = MagicMock()

        self.hangul_ft.most_similar(positive, negative)
        self.hangul_ft.fasttext.most_similar.assert_called_with(positive='ㄱㅡㅇㅈㅓㅇ', negative='ㅂㅜ_ㅈㅓㅇ', topn=10)

        positives = ['긍정긍', '긍정정']
        negatives = ['부정부', '부정정']

        self.hangul_ft.most_similar(positives, negatives)
        self.hangul_ft.fasttext.most_similar.assert_called_with(
            positive=['ㄱㅡㅇㅈㅓㅇㄱㅡㅇ', 'ㄱㅡㅇㅈㅓㅇㅈㅓㅇ'], negative=['ㅂㅜ_ㅈㅓㅇㅂㅜ_', 'ㅂㅜ_ㅈㅓㅇㅈㅓㅇ'], topn=10)

    def test_similarity(self):
        self.hangul_ft.fasttext = MagicMock()

        self.hangul_ft.similarity('긍정', '부정')
        self.hangul_ft.fasttext.similarity.assert_called_once_with('ㄱㅡㅇㅈㅓㅇ', 'ㅂㅜ_ㅈㅓㅇ')

if __name__ == '__main__':

    test_cases = [
        TestHangulFastText
    ]

    suite = unittest.TestSuite()
    for test_case in test_cases:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        suite.addTests(tests)

    runner = unittest.TextTestRunner()
    runner.run(suite)
