"""姓名を管理するクラスを含むモジュール．
"""
# pylint: disable=R0902, R0903, R0913, R0914, C0103

import urllib.request
import json
import numpy as np

from seimei.kakusuu import Kakusuu
from seimei.seimei_history import SeimeiHistory
from seimei.seimei_item import SeimeiItem

class Seimei:
    """姓名を管理するクラス．

    Attributes:
        family: 姓
        given: 名
        history_path: 履歴を格納するファイルのパス
        kakusuu_path: 画数を格納するファイルのパス
        history: 履歴
        kakusuu: キャッシュされている画数の辞書
        kakusuu_family: 姓に含まれる文字の画数リスト
        kakusuu_given: 姓に含まれる文字の画数リスト
    """
    def __init__(self, family, given=None, history_path=None, kakusuu_path=None):
        """初期化．

        Args:
            family: 姓または「姓 名」の形式の文字列
            given: 名．ただし，familyを「姓 名」で指定した場合は省略可
            history_path: 履歴が保存されているファイルのパス
            kakusuu_path: 画数が保存されているファイルのパス
        """
        if given is None and (' ' in family):
            family, given = family.split(' ')

        if family is None or (isinstance(family, str) and not family):
            raise RuntimeError('姓が空白です．')

        if given is None or (isinstance(given, str) and not given):
            raise RuntimeError('名が空白です．')

        self.family = family
        self.given = given
        self.history_path = history_path
        self.kakusuu_path = kakusuu_path
        self.history = SeimeiHistory(history_path)
        self.kakusuu = Kakusuu(kakusuu_path)
        self.kakusuu_family, self.kakusuu_given = self.get_kakusuu_list()

    def get_kakusuu_list(self):
        """姓・名の各文字の画数を返す．

        Returns:
            kakusuu_family: 姓に含まれる文字の画数リスト
            kakusuu_family: 名に含まれる文字の画数リスト
        """
        kakusuu_family = np.array([self.get_kakusuu(char) for char in self.family])
        kakusuu_given = np.array([self.get_kakusuu(char) for char in self.given])
        return kakusuu_family, kakusuu_given

    def tenkaku(self):
        """天格を返す．

        Returns:
            天格
        """
        len_family = len(self.family)
        len_given = len(self.given)
        kaseisuu = 0

        if len_family < len_given:
            kaseisuu = len_given - len_family

        return np.sum(self.kakusuu_family) + kaseisuu

    def jinkaku(self):
        """人格を返す．

        Returns:
            人格
        """
        return self.kakusuu_family[-1] + self.kakusuu_given[0]

    def tikaku(self):
        """地格を返す．

        Returns:
            地格
        """
        len_family = len(self.family)
        len_given = len(self.given)
        kaseisuu = 0

        if len_family > len_given:
            kaseisuu = len_family - len_given

        return np.sum(self.kakusuu_given) + kaseisuu

    def gaikaku(self):
        """外格を返す．

        Returns:
            外格
        """
        len_family = len(self.family)
        len_given = len(self.given)

        kaseisuu = np.abs(len_family - len_given)

        given_kakusuu = np.sum(self.kakusuu_given[1:]) if len_given > 1 else 0
        return np.sum(self.kakusuu_family[:-1]) + given_kakusuu + kaseisuu

    def soukaku(self):
        """総格を返す．

        Returns:
            総格
        """
        return np.sum(self.kakusuu_family) + np.sum(self.kakusuu_given)

    @staticmethod
    def genso(kakusuu):
        """画数に対応する陰陽五行の元素を返す．

        Args:
            kakusuu: 漢字の画数

        Returns:
            元素ID (木:0, 火:1, 土:2, 金:3, 水:4)
        """
        bit = kakusuu % 10
        if bit == 0:
            bit = 10

        genso_val = (bit - 1) // 2

        return genso_val

    @staticmethod
    def genso_str(kakusuu):
        """画数に対応する陰陽五行の元素を返す．

        Args:
            kakusuu: 漢字の画数

        Returns:
            画数に対応する陰陽五行の元素
        """
        genso_tbl = '木火土金水'
        genso_idx = Seimei.genso(kakusuu)
        return genso_tbl[genso_idx]

    @staticmethod
    def gogyo(tenkaku, jinkaku, tikaku):
        """天格・人格・地格から，三才吉凶表に基づく運勢を返す．

        Args:
            tenkaku: 天格
            jinkaku: 人格
            tikaku: 地格

        Returns:
            三才吉凶表にもとづく運勢 (大吉，中吉，凶）
        """
        # 木火土金水の元素がそれぞれ0から4に対応するとして，
        # 天格・人格・地格に対応する元素を対応する番号に変換し，
        # 各番号をその順に並べた数字を5進数3桁の整数とみなしたとき，
        # インデックスがその整数となる文字が運勢を表す．
        # 運勢は凶，中吉，大吉がそれぞれ0から2に対応する．
        # 例えば，天格，人格，地格が9, 5, 10ならば，
        # 対応する元素は水，土，水なので，番号に変換して並べると424になる．
        # これを5進数とみなすと十進数で114となり，
        # 先頭をインデックスを0とするとインデックスが114の値は0なので凶とわかる．
        sansai_kikkyo_tbl = ('2220021200010000010020001'
                             '2220022000022100000000000'
                             '1100021200022200022000000'
                             '0010000000012200020000020'
                             '2120000000000100020000000')

        unsei_tbl = ['凶', '中吉', '大吉']

        tenkaku_genso = Seimei.genso(tenkaku)
        jinkaku_genso = Seimei.genso(jinkaku)
        tikaku_genso = Seimei.genso(tikaku)
        idx = 5*(tenkaku_genso + 5*jinkaku_genso) + tikaku_genso
        unsei_idx = int(sansai_kikkyo_tbl[idx])
        return unsei_tbl[unsei_idx]

    def save(self, history_path=None, kakusuu_path=None):
        """登録内容をファイルに保存する．

        Args:
            history_path: 履歴を保存するファイルのパス.
                省略時は初期化時に指定されたファイルパスとなり，
                読み込んだファイルに上書きされる．

            kakusuu_path: 画数を保存するファイルのパス
                省略時は初期化時に指定されたファイルパスとなり，
                読み込んだファイルに上書きされる．
        """
        history_path = history_path if history_path is not None else self.history_path
        kakusuu_path = kakusuu_path if kakusuu_path is not None else self.kakusuu_path
        self.history.save(history_path)
        self.kakusuu.save(kakusuu_path)

    @staticmethod
    def get_hex(char):
        """文字をUnicodeコードポイントの16進文字列に変換して返す．

        Args:
            char: 文字

        Returns:
            16進文字列
        """
        # 文字列に変換
        letter = str(char)

        # Unicodeコードポイントに変換
        decimal = ord(letter)

        # 0x付き16進文字列に変換
        hex_str = hex(decimal)
        return hex_str

    def get_kakusuu(self, char):
        """文字の画数を返す．

        Args:
            char: 文字 (複数文字不可)

        Reutrns:
            文字の画数
        """
        if len(char) > 1:
            raise RuntimeError('ひとつの文字を指定して下さい．')

        # キャッシュされている場合は結果を返す
        if char in self.kakusuu:
            return self.kakusuu[char]

        # IPAが公開している文字情報取得APIから画数を取得
        request_url = "https://mojikiban.ipa.go.jp/mji/q?UCS=%"
        hex_str = Seimei.get_hex(char)
        request_url = request_url.replace('%', hex_str)

        req = urllib.request.Request(request_url)

        try:
            with urllib.request.urlopen(req) as res:
                body = json.load(res)

        except urllib.error.URLError:
            raise urllib.error.URLError('画数取得時にネットワーク接続エラーが発生しました．')

        if 'results' in body:
            kakusuu = body['results'][0]['総画数']
            self.kakusuu[char] = kakusuu
            return kakusuu

        raise NotImplementedError('未対応の文字が含まれています．')

    def data(self):
        """名前情報を計算して返す．

        Returns:
            名前情報
        """
        name = self.family + self.given

        full_kakusuu = np.concatenate([self.kakusuu_family, self.kakusuu_given])
        char_kakusuu_dict = {char: kakusuu for char, kakusuu in zip(name, full_kakusuu)}

        tenkaku_value = self.tenkaku()
        jinkaku_value = self.jinkaku()
        tikaku_value = self.tikaku()
        gaikaku_value = self.gaikaku()
        soukaku_value = self.soukaku()
        gokaku_dict = {'天格': tenkaku_value,
                       '人格': jinkaku_value,
                       '地格': tikaku_value,
                       '外格': gaikaku_value,
                       '総格': soukaku_value}

        tenkaku_genso = Seimei.genso_str(tenkaku_value)
        jinkaku_genso = Seimei.genso_str(jinkaku_value)
        tikaku_genso = Seimei.genso_str(tikaku_value)
        gogyo_unsei = Seimei.gogyo(tenkaku_value, jinkaku_value, tikaku_value)
        gogyo_dict = {'天格': tenkaku_genso,
                      '人格': jinkaku_genso,
                      '地格': tikaku_genso,
                      '運勢': gogyo_unsei}

        item = SeimeiItem(self.family, self.given, char_kakusuu_dict,
                          gokaku_dict, gogyo_dict)

        return item

    def show_name_status(self):
        """名前情報を標準出力する．
        """
        item = self.data()
        item.show()
        self.history.add(item)
