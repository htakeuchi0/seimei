"""五格計算の履歴を管理するクラスを含むモジュール．
"""

# pylint: disable=R0902, R0914, C0103, R0801

import os
from fileio import FileIO

class SeimeiHistory(FileIO):
    """姓名の履歴を管理するクラス．

    Attributes:
        history: 履歴
        filepath: 履歴を保存するファイルパス
    """
    def __init__(self, filepath=None):
        """初期化．

        Args:
            filepath: 履歴が保存されているファイルパス
        """
        self.history = []
        self.filepath = filepath
        if filepath is not None:
            self.load(filepath)

    def __len__(self):
        return len(self.history)

    def get_filepath(self):
        return self.filepath

    def add(self, family, given, gokaku_dict, char_kakusuu_dict):
        """履歴に姓名を追加する．

        Args:
            family: 姓
            given: 名
            gokaku_dict: 五格の辞書
            char_kakusuu_dicr: 姓名に含まれる文字の画数の辞書
        """
        for item in self.history:
            # 姓より名を優先して判断する．
            if item[1] == given and item[0] == family:
                return

        self.history.append([family, given, gokaku_dict, char_kakusuu_dict])

    def save_csv(self, filepath):
        """履歴をCSV形式で保存する．

        Args:
            filepath: 保存先のファイルのパス
        """
        if not os.path.exists(filepath):
            return

        with open(filepath, 'w') as f:
            f.write('# 姓, 名, 天格, 人格, 地格, 外格, 総格, 画数...\n')
            for item in self.history:
                family = item[0]
                given = item[1]
                save_list = [family, given]

                gokaku_dict = item[2]
                save_list.append(str(gokaku_dict['天格']))
                save_list.append(str(gokaku_dict['人格']))
                save_list.append(str(gokaku_dict['地格']))
                save_list.append(str(gokaku_dict['外格']))
                save_list.append(str(gokaku_dict['総格']))

                char_kakusuu_dict = item[3]
                for char in family:
                    save_list.append(str(char_kakusuu_dict[char]))

                for char in given:
                    save_list.append(str(char_kakusuu_dict[char]))

                save_str = ','.join(save_list) + '\n'
                f.write(save_str)

    def load_csv(self, filepath):
        """CSV形式のファイルから履歴を読み込む．

        Args:
            filepath: 読み込むファイルのパス
        """
        if not os.path.exists(filepath):
            return

        with open(filepath, 'r') as f:  # pylint: disable=R0801
            for line in f:
                line = line.strip()
                if not line:
                    # 空行は飛ばす
                    continue

                if line[0] == '#':
                    # コメント行は飛ばす
                    continue

                load_list = line.split(',')

                # 姓名
                family = load_list[0].strip()
                given = load_list[1].strip()

                len_family = len(family)
                len_given = len(given)

                # 五格
                gokaku_dict = {'天格': int(load_list[2].strip()),
                               '人格': int(load_list[3].strip()),
                               '地格': int(load_list[4].strip()),
                               '外格': int(load_list[5].strip()),
                               '総格': int(load_list[6].strip())}

                idx0 = 7
                idx1 = idx0 + len_family
                idx2 = idx1 + len_given

                # 画数
                char_kakusuu_dict = {}
                char_kakusuu_dict.update({char.strip(): int(kakusuu.strip()) for char, kakusuu
                                          in zip(family, load_list[idx0:idx1])})
                char_kakusuu_dict.update({char.strip(): int(kakusuu.strip()) for char, kakusuu
                                          in zip(given, load_list[idx1:idx2])})

                self.add(family, given, gokaku_dict, char_kakusuu_dict)

    def show(self):
        """標準出力する．
        """
        print('\n'.join(['|{:3d}|{}{}|{}|{}|'.format(
            i+1,
            '{} {}'.format(item[0], item[1]),
            ' '*(11 - (2*len(item[0]) + 2*len(item[1]) + 1)),
            ', '.join(['{}: {:2d}'.format(key, val) for key, val in item[2].items()]),
            ', '.join(['{}: {:2d}'.format(key, val) for key, val in item[3].items()]))
                         for i, item in enumerate(self.history)]))

    def remove(self, *remove_ids):
        """履歴を削除する．

        Args:
            remove_ids: 削除する項目のインデックス (複数選択可能)
        """
        # インデックスが変わらないようにインデックスの大きい項目から削除する
        sorted_remove_ids = sorted(remove_ids)
        for remove_id in sorted_remove_ids[::-1]:
            self.history.pop(remove_id)

    def move(self, idx, move_val):
        """履歴の項目を移動する．

        Args:
            idx: 削除する項目のインデックス
            move_val: 移動方向 (正負) と移動量 (絶対値)
        """
        if move_val == 0:
            return

        dest_idx = idx + move_val

        # 先頭より前になる場合は先頭にする
        dest_idx = dest_idx if dest_idx >= 0 else 0

        # 末尾より後になる場合は末尾にする
        last_idx = len(self) - 1
        dest_idx = dest_idx if dest_idx <= last_idx else last_idx

        # 移動する
        if dest_idx > idx:
            for i in range(idx, dest_idx):
                self.history[i], self.history[i+1] = self.history[i+1], self.history[i]

        else:
            for i in range(idx, dest_idx, -1):
                self.history[i], self.history[i-1] = self.history[i-1], self.history[i]
