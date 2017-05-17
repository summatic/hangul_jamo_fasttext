import unittest
from unittest import TestCase
from hangul_processor import Hangul


class TestHangul(TestCase):
    def setUp(self):
        self.hangul = Hangul()

    def test__is_kor_char(self):
        test = [
            ('*', False),
            ('A', False),
            ('쀍', True)
        ]

        for char, result in test:
            with self.subTest(char=char):
                self.assertEqual(self.hangul._is_kor_char(char), result)

    def test__is_complete_char(self):
        test = [
            (['ㅇ', 'ㅏ', 'ㄴ'], True),
            (['ㅇ', 'ㅏ', '_'], True),
            (['ㅏ', 'ㅇ', 'ㄴ'], False),
            (['ㅋ', 'ㅋ', 'ㅋ'], False),
            (['_', 'ㅁ', 'ㅓ'], False)
        ]

        for jamo_list, result in test:
            with self.subTest(jamo_list=jamo_list):
                self.assertEqual(self.hangul._is_complete_char(jamo_list), result)

    def test_char_to_jamo(self):
        test = [
            ('a', ['a']),
            ('#', ['#']),
            ('헿', ['ㅎ', 'ㅔ', 'ㅎ']),
            ('크', ['ㅋ', 'ㅡ', '_'])
        ]

        for char, result in test:
            with self.subTest(char=char):
                self.assertEqual(self.hangul.char_to_jamo(char), result)

    def test_str_to_jamo(self):
        test = [
            ('안녕하세요', 'ㅇㅏㄴㄴㅕㅇㅎㅏ_ㅅㅔ_ㅇㅛ_'),
            ('안녕하세요?', 'ㅇㅏㄴㄴㅕㅇㅎㅏ_ㅅㅔ_ㅇㅛ_?'),
            ('안녕-하세요?', 'ㅇㅏㄴㄴㅕㅇ-ㅎㅏ_ㅅㅔ_ㅇㅛ_?'),
            ('그때는 집중에 도움이 된다 생각했다.', 'ㄱㅡ_ㄸㅐ_ㄴㅡㄴ ㅈㅣㅂㅈㅜㅇㅇㅔ_ ㄷㅗ_ㅇㅜㅁㅇㅣ_ ㄷㅚㄴㄷㅏ_ ㅅㅐㅇㄱㅏㄱㅎㅐㅆㄷㅏ_.')
            ]

        for string, jamo in test:
            with self.subTest(string=string):
                self.assertEqual(self.hangul.str_to_jamo(string), jamo)

    def test_jamo_to_char(self):
        test = [
            (['ㅇ', 'ㅏ', 'ㄴ'], '안'),
            (['ㅇ', 'ㅏ', '_'], '아')
        ]

        for jamo, char in test:
            with self.subTest(jamo=jamo):
                self.assertEqual(self.hangul.jamo_to_str(jamo), char)

    def test_jamo_to_str(self):
        test = [
            ('ㅇㅏㄴㄴㅕㅇㅎㅏ_ㅅㅔ_ㅇㅛ_', '안녕하세요'),
            ('ㅇㅏㄴㄴㅕㅇㅎㅏ_ㅅㅔ_ㅇㅛ_?', '안녕하세요?'),
            ('ㅇㅏㄴㄴㅕㅇ-ㅎㅏ_ㅅㅔ_ㅇㅛ_?', '안녕-하세요?'),
            ('ㄱㅡ_ㄸㅐ_ㄴㅡㄴ ㅈㅣㅂㅈㅜㅇㅇㅔ_ ㄷㅗ_ㅇㅜㅁㅇㅣ_ ㄷㅚㄴㄷㅏ_ ㅅㅐㅇㄱㅏㄱㅎㅐㅆㄷㅏ_.', '그때는 집중에 도움이 된다 생각했다.'),
            ('ㅁㅕㅊㅅㅣ_?ㅇㅑ_', '몇시?야'),
            ('ㅇㅏ_ㄴㅏ_ㄱㅗ_', '아나고'),
            ('ㄲㅏㅁㅈㅏㅇ?', '깜장?'),
            ('?ㅇㅡㅇ', '?응'),
            ('ㅁㅝ_ㄹㅐ_????', '뭐래????')
        ]

        for jamo, string in test:
            with self.subTest(jamo=jamo):
                self.assertEqual(self.hangul.jamo_to_str(jamo), string)

if __name__ == '__main__':

    test_cases = [
        TestHangul
    ]

    suite = unittest.TestSuite()
    for test_case in test_cases:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        suite.addTests(tests)

    runner = unittest.TextTestRunner()
    runner.run(suite)
