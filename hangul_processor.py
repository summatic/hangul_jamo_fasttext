from queue import Queue

class Hangul:

    def __init__(self, non_jongsung='_'):
        self.non_jongsung = non_jongsung
        self._kor_char_begin = 44032
        self._kor_char_end = 55203

        self._chosung_base = 21*28
        self._jungsung_base = 28

        self._chosung_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ',
                              'ㅌ', 'ㅍ', 'ㅎ']
        self._jungsung_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ',
                               'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
        self._jongsung_list = [self.non_jongsung, 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ',
                               'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ',  'ㅎ']

    def _is_kor_char(self, c):
        return self._kor_char_begin <= ord(c) <= self._kor_char_end

    def _is_complete_char(self, jamo_list):
        try:
            cho, jung, jong = jamo_list
        except ValueError:
            return False
        return cho in self._chosung_list and jung in self._jungsung_list and jong in self._jongsung_list

    def char_to_jamo(self, c):
        if not self._is_kor_char(c):
            return [c]

        num = ord(c) - self._kor_char_begin

        cho = num // self._chosung_base
        jung = (num - cho * self._chosung_base) // self._jungsung_base
        jong = num - cho * self._chosung_base - jung * self._jungsung_base

        return [self._chosung_list[cho], self._jungsung_list[jung], self._jongsung_list[jong]]

    def str_to_jamo(self, string):
        return ''.join([''.join(self.char_to_jamo(c)) for c in string])

    def jamo_to_char(self, jamo_list):
        cho_idx = self._chosung_list.index(jamo_list[0])
        jung_idx = self._jungsung_list.index(jamo_list[1])
        jong_idx = self._jongsung_list.index(jamo_list[2])
        return chr(self._kor_char_begin + self._chosung_base*cho_idx + self._jungsung_base*jung_idx + jong_idx)

    def jamo_to_str(self, jamo_string):
        string_queue = Queue(maxsize=1000)
        check_queue = list()
        for c in jamo_string:
            string_queue.put(c)

        result = []
        while string_queue.qsize() > 0 or len(check_queue) > 0:
            if self._is_complete_char(check_queue):
                result.append(self.jamo_to_char(check_queue))
                check_queue = list()
            elif len(check_queue) < 3:
                if string_queue.empty():
                    result.append(check_queue[0])
                    del check_queue[0]
                else:
                    check_queue.append(string_queue.get())
            else:
                result.append(check_queue[0])
                del check_queue[0]
        return ''.join(result)

