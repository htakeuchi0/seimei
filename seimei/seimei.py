"""五格計算登録プログラム．

このモジュールは，人名と姓名判断における五格を計算し登録するためのプログラムです．
五格の数え方 (特に仮成数の扱い) や，ひらがな・カタカナの画数は [1] を参考にしました．
また，漢字の画数を求めるために [2] を利用しています．

実行例は以下のとおりです．

人名「田中 一郎」の登録
$ python seimei.py 田中 一郎

登録一覧表示
$ python seimei.py -s

登録削除
$ python seimei.py -r
$ python seimei.py -r 1 2 10 11

登録順変更
$ python seimei.py -m
$ python seimei.py -m 12uuuu

詳細表示
$ python seimei.py -i
$ python seimei.py -i 5

[1] たまごクラブ編, たまひよ 赤ちゃんのしあわせ名前事典 2020〜2021年版,
    株式会社ベネッセコーポレーション，東京，2019.
[2] 独立行政法人 情報処理推進機構, MJ文字情報API, http://mojikiban.ipa.go.jp/mji/,
    最終閲覧:2020年2月16日.
"""
# pylint: disable=R0902, R0914, C0103

import os
import argparse
import configparser
import urllib.request

from seimei_core import Seimei
from seimei_history import SeimeiHistory

def show(filepath):
    """履歴を表示する．

    Args:
        filepath: 履歴のファイルパス
    """
    history = SeimeiHistory(filepath)
    history.show()

def remove(filepath, remove_ids):
    """履歴を削除する．

    Args:
        filepath: 履歴のファイルパス
        remove_ids: 削除するIDのリスト
            空リストの場合は対話モード．
    """
    history = SeimeiHistory(filepath)

    if not remove_ids:
        history.show()
        print()
        input_ids = input('削除番号をスペース区切りで入力して下さい．\n'
                          '例えば，「1 2 3」で番号1, 2, 3の項目を削除します．\n'
                          'キャンセル時は「q」を入力して下さい．\n'
                          '> ')
        print()

        if input_ids.strip().lower() == 'q':
            print('終了します．')
            return

        input_ids = input_ids.strip()

        try:
            remove_ids = [int(input_id) for input_id in input_ids.split(' ')]

        except ValueError:
            len_history = len(history)
            raise RuntimeError('1以上{}以下の整数を指定して下さい．'.format(len_history))

    num_remove_ids = len(remove_ids)
    for i in range(num_remove_ids):
        remove_ids[i] -= 1

    len_history = len(history)
    if not all([0 <= remove_id < len_history for remove_id in remove_ids]):
        raise RuntimeError('1以上{}以下の整数を指定して下さい．'.format(len_history))

    remove_ids_str = ', '.join([str(remove_id+1) for remove_id in remove_ids])
    print('第{}番目の項目を削除します．'.format(remove_ids_str))
    print()

    history.remove(*remove_ids)
    history.save()
    history.show()

def move(filepath, move_str):
    """履歴の項目を移動する．

    Args:
        filepath: 履歴のファイルパス
        move_ids: 移動を表す文字列
            Noneの場合は対話モード．
    """
    history = SeimeiHistory(filepath)

    if move_str is None:
        history.show()
        print()
        move_str = input('番号と移動方向・移動量を入力して下さい．\n'
                         '移動方向は上，下をu, dで指定し，移動量はその個数で指定して下さい．\n'
                         '例えば，「4uuu」で4番目の項目を3個上に移動します．\n'
                         'キャンセル時は「q」を入力して下さい．\n'
                         '> ')
        print()

        if move_str.strip().lower() == 'q':
            print('終了します．')
            return

    move_str = move_str.strip()
    num_decimal_chars = 0
    for i, s in enumerate(move_str):
        if not s.isdecimal():
            num_decimal_chars = i
            break

    target_id = int(move_str[0:num_decimal_chars]) - 1
    size = len(history)
    if not 0 <= target_id < size:
        raise RuntimeError('先頭には1以上{}以下の整数を指定して下さい．'.format(size))

    if not move_str:
        raise RuntimeError(
            '{}文字目以降に移動方向 (uまたはd) を指定して下さい．'.format(num_decimal_chars+1))

    if not all([move_str[num_decimal_chars] == move_str[i]
                for i in range(num_decimal_chars, len(move_str))]):
        raise RuntimeError(
            '{}文字目以降は{}文字目と同じ文字にしてください．'.format(
                num_decimal_chars+2, num_decimal_chars+1))

    direction = None
    if move_str[num_decimal_chars] == 'd':
        direction = 1

    elif move_str[num_decimal_chars] == 'u':
        direction = -1

    if not direction:
        raise RuntimeError('移動方向はuまたはdを指定して下さい．')

    distance = len(move_str[num_decimal_chars:])
    target_move = direction * distance

    direction_str = '上' if direction == -1 else '下'
    print('第{}番目の項目を{}個{}に移動します．'.format(target_id+1, distance, direction_str))
    print()

    history.move(target_id, target_move)
    history.save()
    history.show()

def info(filepath, info_idx):
    """履歴の項目の詳細を表示する．

    Args:
        filepath: 履歴のファイルパス
        info_idx: 詳細を表示する項目のインデックス．
            Noneの場合は対話モード．
    """
    history = SeimeiHistory(filepath)

    if not info_idx:
        history.show()
        print()
        input_idx = input('詳細を表示する番号を入力して下さい．\n'
                          '例えば，「5」で番号5の項目を表示します．\n'
                          'キャンセル時は「q」を入力して下さい．\n'
                          '> ')
        print()

        if input_idx.strip().lower() == 'q':
            print('終了します．')
            return

        input_idx = input_idx.strip()

        try:
            info_idx = int(input_idx)

        except ValueError:
            len_history = len(history)
            raise RuntimeError('1以上{}以下の整数を指定して下さい．'.format(len_history))

    info_idx -= 1

    len_history = len(history)
    if not 0 <= info_idx < len_history:
        raise RuntimeError('1以上{}以下の整数を指定して下さい．'.format(len_history))

    print('第{}番目の項目の詳細を表示します．'.format(info_idx+1))
    history[info_idx].show()

def append(family, given, seimei_history_path, kakusuu_dict_path):
    """姓名を登録する．

    Args:
        family: 姓
        given: 名
        seimei_history_path: 履歴の保存先ファイルパス
        kakusuu_dict_path: 画数辞書の保存先ファイルパス
    """
    if not family:
        raise RuntimeError('姓を指定して下さい．')

    if not given:
        raise RuntimeError('「姓 名」の書式で指定して下さい．')

    name = Seimei(family, given, seimei_history_path, kakusuu_dict_path)
    name.show_name_status()
    name.save()

def create_default_files():
    """デフォルトの履歴・画数ファイルを生成する．
    """
    default_seimei_csv = 'name.csv'
    if not os.path.exists(default_seimei_csv):
        with open(default_seimei_csv, 'w'):
            pass

    default_kakusuu_csv = 'kakusuu.csv'
    if not os.path.exists(default_kakusuu_csv):
        with open(default_kakusuu_csv, 'w'):
            pass

def parse():
    """コマンドライン引数を解析する．

    Returns:
        解析結果
    """
    parser = argparse.ArgumentParser(description='五格計算登録プログラム．',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('family', nargs='?', type=str, help='姓')
    parser.add_argument('given', nargs='?', type=str, help='名')
    parser.add_argument('--config', '-c', action='store', default='config.ini', type=str,
                        help='設定ファイル．省略時は config.ini になります．')
    parser.add_argument('--show', '-s', action='store_true', help='表示モード．')
    parser.add_argument('--remove', '-r', action='store', nargs='*', default=None, type=int,
                        help=('削除モード．\n'
                              '表示モードの一番左の番号をスペース区切りで指定してください．\n'
                              '例えば，「-r 1 2 3」で1, 2, 3番目の項目が削除されます．\n'
                              '「-r」だけの場合は対話モードになります．'))
    parser.add_argument('--move', '-m', action='store', type=str, nargs='*',
                        help=('移動モード．\n'
                              '表示モードの一番左の番号，移動方向，移動量を指定してください．\n'
                              '移動方向は上，下をそれぞれu, d, 移動量はその文字の個数です．\n'
                              '例えば，「m 10uu」で10番目の項目をを2個上に，\n'
                              '「-m 2dddd」で2番目の項目を4個下に移動します．\n'
                              '「-m」だけの場合は対話モードになります．'))
    parser.add_argument('--info', '-i', action='store', nargs='*', default=None, type=int,
                        help=('詳細モード．\n'
                              '表示モードの一番左の番号をひとつ指定してください．\n'
                              '例えば，「-i 5」で5番目の項目の詳細が表示されます．\n'
                              '「-i」だけの場合は対話モードになります．'))
    args = parser.parse_args()
    return args

def config_default_values():
    """設定ファイルが読み込めないときの既定値を返す．

    Returns:
        seimei_history: 姓名の履歴ファイルパス
        kakusuu_dict: 文字と画数の辞書ファイルのパス
    """
    seimei_history = 'name.csv'
    kakusuu_dict = 'kakusuu.csv'
    return seimei_history, kakusuu_dict


def config_parse(config_path):
    """設定ファイルを解析する．

    Args:
        config_path: 設定ファイルのパス．

    Returns:
        seimei_history: 姓名の履歴ファイルパス
        kakusuu_dict: 文字と画数の辞書ファイルのパス
    """
    if not os.path.exists(config_path):
        return config_default_values()

    config = configparser.ConfigParser()
    config.read(config_path)

    if 'Paths' not in config:
        return config_default_values()

    config_paths = config['Paths']
    seimei_history = config_paths.get('seimei_history', 'name.csv')
    kakusuu_dict = config_paths.get('kakusuu_dict', 'kakusuu.csv')

    return seimei_history, kakusuu_dict

def main():
    """プログラムを起動する．
    """
    create_default_files()
    args = parse()
    try:
        seimei_history, kakusuu_dict = config_parse(args.config)

        if args.show:
            # 表示モード
            show(seimei_history)

        elif args.remove is not None:
            # 削除モード
            remove(seimei_history, args.remove)

        elif args.move is not None:
            # 移動モード
            move_str = args.move[0] if args.move else None
            move(seimei_history, move_str)

        elif args.info is not None:
            info_idx = args.info[0] if args.info else None
            info(seimei_history, info_idx)

        else:
            # 追加モード
            append(args.family, args.given, seimei_history, kakusuu_dict)

    except RuntimeError as e:
        print('ERROR: {}'.format(e.args[0]))

    except ValueError as e:
        print('ERROR: {}'.format(e.args[0]))

    except FileNotFoundError as e:
        print('ERROR: {}'.format(e.args[0]))

    except urllib.error.URLError as e:
        print('ERROR: {}'.format(e.args[0]))

if __name__ == '__main__':
    main()
