"""ファイルの読み書きの機能をもつクラスを含むモジュール
"""

# pylint: disable=R0902, R0914, C0103

class FileIO:
    """ファイルの読み書きに関する機能をもつインタフェースクラス．

    以下の機能をもつ．
    * 既定のファイルパスを返す機能
    * 保存する機能
    * CSV形式で保存する機能
    * 読み込む機能
    * CSV形式のファイルから読み込む機能
    """
    def get_filepath(self):
        """ファイルパスを返す．
        """
        raise NotImplementedError

    def save(self, filepath=None):
        """ファイルに保存する．

        Args:
            filepath: 保存先のファイルのパス
                省略時は既定のファイルパスとなる．
        """
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
        """ファイルから読み込む．

        Args:
            filepath: 読み込むファイルのパス
                省略時は既定のファイルパスとなる．
        """
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
