import os
import fasttext
from gensim.models.wrappers.fasttext import FastText
from hangul_processor import Hangul


class HangulFastText:

    def __init__(self):
        self.fasttext = None
        self.hangul = Hangul()

    def _convert_word_to_jamo(self, word):
        if isinstance(word, str):
            return self.hangul.str_to_jamo(word)
        elif isinstance(word, list):
            return [self.hangul.str_to_jamo(w) for w in word]
        else:
            return word

    @staticmethod
    def _del_jamo_corpus(fname):
        os.remove(fname)

    def _generate_jamo_corpus(self, fname, postfix='_jamo'):
        with open(fname, 'r') as file_r:
            with open(fname + postfix, 'w') as file_w:
                for sent in file_r:
                    sent = sent.strip()
                    file_w.write('%s\n' % self._convert_word_to_jamo(sent))

    def train(self, input_txt, output_path, model='skipgram', lr=0.1, lr_update_rate=100, dim=100, ws=5, epoch=10,
              min_count=10, neg=5, loss='ns', bucket=2000000, minn=3, maxn=6, thread=8, t=1e-4, remove=True,
              postfix='_jamo'):
        self._generate_jamo_corpus(input_txt, postfix=postfix)

        input_txt += postfix
        if model == 'skipgram':
            ft = fasttext.skipgram(input_txt, output_path, lr=lr, dim=dim, ws=ws, epoch=epoch, min_count=min_count,
                                   neg=neg, loss=loss, bucket=bucket, minn=minn, maxn=maxn, thread=thread, t=t,
                                   lr_update_rate=lr_update_rate)
        elif model == 'cbow':
            ft = fasttext.cbow(input_txt, output_path, lr=lr, dim=dim, ws=ws, epoch=epoch, min_count=min_count,
                               neg=neg, loss=loss, bucket=bucket, minn=minn, maxn=maxn, thread=thread, t=t,
                               lr_update_rate=lr_update_rate)
        else:
            raise ValueError('model type must be either skipgram or cbow.')

        if remove:
            self._del_jamo_corpus(input_txt)

        self.load(output_path)

    def load(self, fname):
        self.fasttext = FastText.load_fasttext_format(fname)

    def most_similar(self, positive=[], negative=[], topn=10):
        self.fasttext.wv.init_sims()
        similars = self.fasttext.most_similar(positive=self._convert_word_to_jamo(positive),
                                              negative=self._convert_word_to_jamo(negative),
                                              topn=topn)
        return [(self.hangul.jamo_to_str(jamo), dist) for jamo, dist in similars]

    def similarity(self, word1, word2):
        return self.fasttext.similarity(self.hangul.str_to_jamo(word1), self.hangul.str_to_jamo(word2))
