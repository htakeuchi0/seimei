"""ファイルの読み書きの機能をもつクラスを含むモジュール
"""

# pylint: disable=R0902, R0914, C0103

class FileIO:
    """CSVファイルの読み書きに関する機能をもつインタフェースクラス．

    以下の機能をもつ．
    * 既定のファイルパスを返す機能
    * 保存する機能
    * 読み込む機能
    """
    def get_filepath(self):
        """ファイルパスを返す．
        """
        raise NotImplementedError

    def save(self, filepath=None):
        """ファイルに保存する．

        Args:
            filepath: 保存先のファイルのパス
                省略時は既定 (get_filepath) のファイルパスとなる．
        """
        raise NotImplementedError

    def load(self, filepath):
        """ファイルから読み込む．

        Args:
            filepath: 読み込むファイルのパス
                省略時は既定 (get_filepath) のファイルパスとなる．
        """
        raise NotImplementedError


class CSVFileIO(FileIO):
    """CSVファイルの読み書きに関する機能をもつインタフェースクラス．

    save, loadメソッドはCSV向けデフォルト実装である．
    CSVFileIO以外のインタフェースも実装する場合は，
    各ファイル形式が扱えるsaveメソッドをオーバーロード実装すること

    以下の機能をもつ．
    * FileIOインタフェースの機能
    * CSV形式で保存する機能
    * CSV形式のファイルから読み込む機能
    """
    def save(self, filepath=None):
        filepath = filepath if filepath is not None else self.get_filepath()

        if not '.' in filepath:
            self.save_csv(filepath)

        ext = filepath.rsplit('.', 1)[-1]
        ext = ext.strip().lower()
        if ext == 'csv':
            self.save_csv(filepath)
            return

        raise NotImplementedError('未対応のファイルフォーマットです')

    def save_csv(self, filepath):
        """CSV形式でファイルに保存する．

        Args:
            filepath: 保存先のファイルのパス
        """
        raise NotImplementedError

    def load(self, filepath):
        filepath = filepath if filepath is not None else self.get_filepath()

        if not '.' in filepath:
            self.load_csv(filepath)

        ext = filepath.rsplit('.', 1)[-1]
        ext = ext.strip().lower()
        if ext == 'csv':
            self.load_csv(filepath)
            return

        raise NotImplementedError('未対応のファイルフォーマットです')

    def load_csv(self, filepath):
        """CSV形式のファイルから読み込む．

        Args:
            filepath: 保存先のファイルのパス
        """
        raise NotImplementedError

    @staticmethod
    def is_continue(line):
        """読み飛ばす行のときTrueを返す．

        Args:
            line: 前後の空白削除済みの行

        Returns:
            読み飛ばす行のときTrue
        """
        if not line:
            # 空行は飛ばす
            return True

        if line[0] == '#':
            # コメント行は飛ばす．
            return True

        return False
