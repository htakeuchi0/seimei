"""五格計算の履歴を管理するクラスを含むモジュール．
"""

# pylint: disable=R0902, R0914, C0103, R0801

import os
import numpy as np
from seimei.fileio import CSVFileIO
from seimei.seimei_item import SeimeiItem

class SeimeiHistory(CSVFileIO):
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

    def add(self, item):
        """履歴に姓名を追加する．

        Args:
            item: 姓名データ
        """
        for history_item in self.history:
            # 姓より名を優先して判断する．
            if history_item.given == item.given and history_item.family == item.family:
                return

        self.history.append(item)

    def __iter__(self):
        return iter(self.history)

    def __getitem__(self, key):
        return self.history[key]

    def save_csv(self, filepath):
        """履歴をCSV形式で保存する．

        Args:
            filepath: 保存先のファイルのパス
        """
        if not os.path.exists(filepath):
            return

        with open(filepath, 'w') as f:
            f.write(('# 姓, 名, 天格, 人格, 地格, 外格, 総格, '
                     '五行：天格, 五行：人格, 五行：地格, 五行運勢, 画数...\n'))
            for item in self.history:
                family = item.family
                given = item.given
                save_list = [family, given]

                gokaku_dict = item.gokaku_dict
                save_list.append(str(gokaku_dict['天格']))
                save_list.append(str(gokaku_dict['人格']))
                save_list.append(str(gokaku_dict['地格']))
                save_list.append(str(gokaku_dict['外格']))
                save_list.append(str(gokaku_dict['総格']))

                gogyo_dict = item.gogyo_dict
                save_list.append(str(gogyo_dict['天格']))
                save_list.append(str(gogyo_dict['人格']))
                save_list.append(str(gogyo_dict['地格']))
                save_list.append(str(gogyo_dict['運勢']))

                char_kakusuu_dict = item.char_kakusuu_dict
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
                if CSVFileIO.is_continue(line):
                    continue

                if line.count(',') < 6:
                    raise RuntimeError("ファイル形式が不正です．")

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

                # 陰陽五行
                gogyo_dict = {'天格': load_list[7].strip(),
                              '人格': load_list[8].strip(),
                              '地格': load_list[9].strip(),
                              '運勢': load_list[10].strip()}

                idx0 = 11
                idx1 = idx0 + len_family
                idx2 = idx1 + len_given

                if len(load_list) < idx2:
                    raise RuntimeError("ファイル形式が不正です．")

                # 画数
                char_kakusuu_dict = {}
                char_kakusuu_dict.update({char.strip(): int(kakusuu.strip()) for char, kakusuu
                                          in zip(family, load_list[idx0:idx1])})
                char_kakusuu_dict.update({char.strip(): int(kakusuu.strip()) for char, kakusuu
                                          in zip(given, load_list[idx1:idx2])})

                self.add(SeimeiItem(family, given, char_kakusuu_dict, gokaku_dict, gogyo_dict))

    def show(self):
        """標準出力する．
        """
        print('\n'.join(['|{:3d}|{}{}|{}|{}|'.format(
            i+1,
            '{} {}'.format(item.family, item.given),
            ' '*(11 - (2*len(item.family) + 2*len(item.given) + 1)),
            ', '.join(['{}: {:2d}'.format(key, val) for key, val in item.gokaku_dict.items()]),
            ', '.join(['{}: {:2d}'.format(key, val) for key, val
                       in item.char_kakusuu_dict.items()]))
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
            idx: 移動する項目のインデックス
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

    def move_up(self, *indices):
        """指定されたインデックスの履歴の項目をひとつ上に移動する．

        Args:
            indices: 移動対象のインデックス

        Returns:
            移動したときTrue
        """
        sorted_indices = np.sort(np.array(indices))
        if sorted_indices[0] < 0 or sorted_indices[-1] >= len(self):
            raise RuntimeError('インデックスが不正です．')

        if sorted_indices[0] == 0:
            return False

        for idx in sorted_indices:
            self.move(idx, -1)

        return True

    def move_down(self, *indices):
        """指定されたインデックスの履歴の項目をひとつ下に移動する．

        Args:
            indices: 移動対象のインデックス

        Returns:
            移動したときTrue
        """
        sorted_indices = np.sort(np.array(indices))
        if sorted_indices[0] < 0 or sorted_indices[-1] >= len(self):
            raise RuntimeError('インデックスが不正です．')

        if sorted_indices[-1] == len(self) - 1:
            return False

        for idx in sorted_indices[::-1]:
            self.move(idx, +1)

        return True
