# seimei

## 概要

人名と姓名判断における五格を計算し登録するためのプログラムです．    
五格とは，天格，人格，地格，外格，総格の総称です．

このプログラムでは，以下のように五格を計算できます．    
```
$ python seimei/seimei.py 田中 一郎

[姓名]
- 姓: 田中
- 名: 一郎

[画数]
- 田:  5
- 中:  4
- 一:  1
- 郎:  9

[姓名判断]
- 天格:  9
- 人格:  5
- 地格: 10
- 外格: 14
- 総格: 19

[陰陽五行]
- 天格: 水
- 人格: 土
- 地格: 水
- 運勢: 凶
```
計算した名前と五格は履歴ファイルに保存され，それら履歴を表示することもできます．

五格の数え方 (特に仮成数の扱い) や，ひらがな・カタカナの画数は [1] を参考にしました．    
また，漢字の画数を求めるために [2] を利用しています．

## 動作環境

以下の環境で動作確認をしています．

* OS: Linux (Ubuntu 18.04.4 LTS)
* Python: Python 3.7.5

## インストール

以下のいずれかのコマンドで必要なライブラリをインストールできます．
* `$ make`
* `$ make init`
* `$ pip install -r requirements.txt`

venv環境を作成するための簡単なスクリプトファイルも同梱しています．    
これを使うと，以下のコマンドでvenv環境の作成とライブラリのインストールができます．
```
$ source makeenv.sh
$ source activate
$ make
```

## 使い方

### ヘルプの表示

以下のコマンドでヘルプが表示できます．    
* `$ python seimei/seimei.py -h`
* `$ python seimei/seimei.py --help`

### 使用例

コマンド実行例を記載します．

#### 名前の登録
```
$ python seimei/seimei.py 田中 一郎

[姓名]
- 姓: 田中
- 名: 一郎

[画数]
- 田:  5
- 中:  4
- 一:  1
- 郎:  9

[姓名判断]
- 天格:  9
- 人格:  5
- 地格: 10
- 外格: 14
- 総格: 19

[陰陽五行]
- 天格: 水
- 人格: 土
- 地格: 水
- 運勢: 凶
```

#### 履歴の表示
```
$ python seimei/seimei.py -s
|  1|田中 一郎  |天格:  9, 人格:  5, 地格: 10, 外格: 14, 総格: 19|田:  5, 中:  4, 一:  1, 郎:  9|
|  2|佐藤 太郎  |天格: 25, 人格: 22, 地格: 13, 外格: 16, 総格: 38|佐:  7, 藤: 18, 太:  4, 郎:  9|
```

#### 履歴の削除
```
$ python seimei/seimei.py -r
|  1|田中 一郎  |天格:  9, 人格:  5, 地格: 10, 外格: 14, 総格: 19|田:  5, 中:  4, 一:  1, 郎:  9|
|  2|佐藤 太郎  |天格: 25, 人格: 22, 地格: 13, 外格: 16, 総格: 38|佐:  7, 藤: 18, 太:  4, 郎:  9|

削除番号をスペース区切りで入力して下さい．
例えば，「1 2 3」で番号1, 2, 3の項目を削除します．
キャンセル時は「q」を入力して下さい．
> 2

第2番目の項目を削除します．

|  1|田中 一郎  |天格:  9, 人格:  5, 地格: 10, 外格: 14, 総格: 19|田:  5, 中:  4, 一:  1, 郎:  9|
```

#### 履歴の移動
```
$ python seimei/seimei.py -m
|  1|田中 一郎  |天格:  9, 人格:  5, 地格: 10, 外格: 14, 総格: 19|田:  5, 中:  4, 一:  1, 郎:  9|
|  2|佐藤 太郎  |天格: 25, 人格: 22, 地格: 13, 外格: 16, 総格: 38|佐:  7, 藤: 18, 太:  4, 郎:  9|

番号と移動方向・移動量を入力して下さい．
移動方向は上，下をu, dで指定し，移動量はその個数で指定して下さい．
例えば，「4uuu」で4番目の項目を3個上に移動します．
キャンセル時は「q」を入力して下さい．
> 2u

第2番目の項目を1個上に移動します．

|  1|佐藤 太郎  |天格: 25, 人格: 22, 地格: 13, 外格: 16, 総格: 38|佐:  7, 藤: 18, 太:  4, 郎:  9|
|  2|田中 一郎  |天格:  9, 人格:  5, 地格: 10, 外格: 14, 総格: 19|田:  5, 中:  4, 一:  1, 郎:  9|
```

## 設定ファイル

履歴ファイルの配置場所はデフォルトではカレントディレクトリになります．    
ファイルの配置場所は，`config.ini`という名前の設定ファイルから設定できます．    
設定ファイルに設定できる項目は以下のとおりです．

```
[Paths]
seimei_history = (名前履歴ファイルのパス)
kakusuu_dict   = (画数保存ファイルのパス)
```

名前履歴ファイルは，`-s` オプションで表示される履歴が保存されるファイルです．    
画数保存ファイルは，一度使った漢字とその画数をローカルに保存しておくためのファイルです．    

設定例は以下のとおりです．

```
[Paths]
seimei_history=/path/to/name.csv
kakusuu_dict=/path/to/kakusuu.csv
```

設定ファイルを配置したディレクトリからpythonコマンドを実行するか，     
起動時に `-c` オプションで設定ファイルのパスを指定してください (ヘルプ参照)．

## 画数保存ファイル

画数保存ファイルとは，一度使った漢字とその画数を保存しておくためのファイルですが，    
画数保存ファイルに画数が保存されることで，    
すでに画数を調べた実績がある漢字の画数が，初回より高速に求まるという利点があります．

例として，画数保存ファイル・名前履歴ファイルを削除して，    
`田中 一郎`, `中田 一郎` を続けて登録した場合の実行時間は以下のとおりです．

```
$ time python seimei/seimei.py 田中 一郎
(略)

real	0m2.083s
user	0m0.558s
sys	0m0.533s

$ time python seimei/seimei.py 中田 一郎
(略)

real	0m0.098s
user	0m0.182s
sys	0m0.326s
```

実行時間が 1/10 未満になっていることがわかります．

## 参考文献
[1] たまごクラブ編, たまひよ 赤ちゃんのしあわせ名前事典 2020〜2021年版, 株式会社ベネッセコーポレーション，東京，2019.    
[2] 独立行政法人 情報処理推進機構, MJ文字情報API, http://mojikiban.ipa.go.jp/mji/, 最終閲覧:2020年2月16日.
