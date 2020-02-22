"""画数を管理するクラスを含むモジュール．
"""
# pylint: disable=R0902, R0914, C0103

import os
from fileio import CSVFileIO

class Kakusuu(CSVFileIO):
    """画数を管理するクラス．

    Attributes:
        dict: 文字と画数の辞書
        filepath: 出力先ファイルパス
    """
    def __init__(self, filepath=None, kana=None):
        """初期化．

        Args:
            filepath: 辞書情報が格納されているファイルのパス
            kana: ひらがな・カタカナの設定ファイルのパス
        """
        self.filepath = filepath
        self.dict = {}
        if filepath is not None:
            self.load(filepath)

        if kana is not None:
            kakusuu = Kakusuu.kana_load(kana)
            self.dict.update(kakusuu)


    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __contains__(self, item):
        return item in self.dict

    def get_filepath(self):
        return self.filepath

    def save_csv(self, filepath):
        """CSV形式で保存する．

        Args:
            filepath: 保存先ファイルパス
        """
        with open(filepath, 'w') as f:
            for key, val in self.dict.items():
                line = '{},{}\n'.format(key, val)
                f.write(line)

    def load_csv(self, filepath):
        """CSV形式のファイルから読み込む．

        Args:
            filepath: 保存先ファイルパス
        """
        if not os.path.exists(filepath):
            return

        self.dict = {}
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if CSVFileIO.is_continue(line):
                    continue

                if line.count(',') != 1:
                    raise RuntimeError("ファイル形式が不正です．")

                key, val = line.split(',')
                key = key.strip()
                val = val.strip()
                self.dict[key] = int(val)

    @staticmethod
    def kana_load(kana):
        """ひらがな・カタカナの画数データを読み込む．

        Args:
            kana: ひらがな・カタカナの画数データのファイルパス
        """
        kakusuu_dict = {}
        if not os.path.exists(kana):
            return kakusuu_dict

        hiragana = ('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめも'
                    'やゆよらりるれろわゐゑをん')

        katakana = ('アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモ'
                    'ヤユヨラリルレロワヰヱヲン')

        kigou = ('ーゝゞ々')

        seion_h = ('かきくけこさしすせそたちつてとはひふへほ')
        dakuon_h = ('がぎぐげござじずぜぞだぢづでどばびぶべぼ')

        dakuon_dict = {}
        dakuon_dict.update({key: val for key, val in zip(dakuon_h, seion_h)})

        seion_k = ('カキクケコサシスセソタチツテトハヒフヘホ')
        dakuon_k = ('ガギグゲゴザジズゼゾダヂヅデドバビブベボ')
        dakuon_dict.update({key: val for key, val in zip(dakuon_k, seion_k)})

        seion2_h = ('はひふへほ')
        handakuon_h = ('ぱぴぷぺぽ')
        dakuon_dict.update({key: val for key, val in zip(handakuon_h, seion2_h)})

        seion2_k = ('ハヒフヘホ')
        handakuon_k = ('パピプペポ')
        dakuon_dict.update({key: val for key, val in zip(handakuon_k, seion2_k)})

        small_dict = {}
        large_h = 'あいうえおやゆよわ'
        small_h = 'ぁぃぅぇぉゃゅょゎ'
        small_dict.update({key: val for key, val in zip(small_h, large_h)})

        large_k = 'アイウエオヤユヨワケ'
        small_k = 'ァィゥェォャュョヮヶ'
        small_dict.update({key: val for key, val in zip(small_k, large_k)})

        with open(kana, 'r') as f:
            kakusuu = f.readline()
            kakusuu_dict.update({key: int(val) for key, val in zip(hiragana, kakusuu)})

            kakusuu = f.readline()
            kakusuu_dict.update({key: int(val) for key, val in zip(katakana, kakusuu)})

            kakusuu = f.readline()
            kakusuu_dict.update({key: int(val) for key, val in zip(kigou, kakusuu)})

            dakuon_kakusuu = 2
            handakuon_kakusuu = 1
            kakusuu_dict.update({key: kakusuu_dict[dakuon_dict[key]] + dakuon_kakusuu
                                 for key in dakuon_h})
            kakusuu_dict.update({key: kakusuu_dict[dakuon_dict[key]] + dakuon_kakusuu
                                 for key in dakuon_k})
            kakusuu_dict.update({key: kakusuu_dict[dakuon_dict[key]] + handakuon_kakusuu
                                 for key in handakuon_h})
            kakusuu_dict.update({key: kakusuu_dict[dakuon_dict[key]] + handakuon_kakusuu
                                 for key in handakuon_k})

            kakusuu_dict.update({key: kakusuu_dict[small_dict[key]] for key in small_h})
            kakusuu_dict.update({key: kakusuu_dict[small_dict[key]] for key in small_k})

        return kakusuu_dict
