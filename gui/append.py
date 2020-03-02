"""姓名登録フレームを含むモジュール．
"""
# pylint: disable=R0902, R0903, R0913, R0914, C0103

import tkinter as tk
import tkinter.ttk as ttk
from seimei.seimei_core import Seimei

class AppendFrame(tk.Frame):
    """姓名を登録するためのフレーム．

    Attributes:
        master: マスタ
        item: 姓名データ
        family_label: 姓ラベル
        given_label: 名ラベル
        family_entry: 姓テキストボックス
        given_entry: 名テキストボックス
        view_button: 表示ボタン
        view_frame: 表示フレーム
        view: 表示テキストエリア
        error_message: エラーメッセージ
        error: エラーラベル
        footer_frame: フッタ用フレーム
        ok: OKボタン
        cancel: キャンセルボタン
    """
    def __init__(self, kakusuu_dict_path, master=None):
        """初期化をする．

        Args:
            kakusuu_dict_path: 画数履歴フィアルのパス
            master: マスタ
        """
        super().__init__(master)
        self.kakusuu_dict_path = kakusuu_dict_path
        self.master = master
        self.item = None

        self.family_label = None
        self.given_label = None
        self.family_entry = None
        self.given_entry = None
        self.view_button = None
        self.view_frame = None
        self.view = None
        self.error_message = None
        self.error = None
        self.footer_frame = None
        self.ok = None
        self.cancel = None

        self.pack()
        self.create_widgets()
        self.focus_set()

    def create_widgets(self):
        """構成要素を生成する．
        """
        self.create_family_label()
        self.create_given_label()
        self.create_family_entry()
        self.create_given_entry()
        self.create_view_button()
        self.create_view()
        self.create_error()
        self.create_footer()

    def create_family_label(self):
        """姓ラベルを生成する．
        """
        self.family_label = tk.Label(self, text='姓')
        self.family_label.grid(row=0, column=0, padx=10, pady=1)

    def create_given_label(self):
        """名ラベルを生成する．
        """
        self.given_label = tk.Label(self, text='名')
        self.given_label.grid(row=0, column=1, padx=10, pady=1)

    def create_family_entry(self):
        """姓テキストボックスを生成する．
        """
        self.family_entry = tk.Entry(self)
        self.family_entry.grid(row=1, column=0, padx=10, pady=1)

    def create_given_entry(self):
        """名テキストボックスを生成する．
        """
        self.given_entry = tk.Entry(self)
        self.given_entry.grid(row=1, column=1, padx=10, pady=1)

    def create_view_button(self):
        """表示ボタンを生成する．
        """
        self.view_button = tk.Button(self, command=self.show_name_data)
        self.view_button['text'] = '表示'
        self.view_button.grid(row=1, column=2, padx=10, pady=1)

    def create_view(self):
        """表示テキストエリアを生成する．
        """
        self.view_frame = tk.Frame(self)
        self.view_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.view = tk.Text(self.view_frame, width=60, height=25, state=tk.DISABLED)
        self.view.grid(row=0, column=0)

        vscrollbar = ttk.Scrollbar(self.view_frame,
                                   orient=tk.VERTICAL,
                                   command=self.view.yview)
        self.view.configure(yscroll=vscrollbar.set)
        vscrollbar.grid(row=0, column=1, sticky=tk.NS)

    def create_error(self):
        """エラーラベルを生成する．
        """
        self.error_message = tk.StringVar()

        self.error = tk.Label(self, textvariable=self.error_message, fg='red')
        self.error.grid(row=3, column=0, columnspan=3)

    def create_footer(self):
        """OK・キャンセルボタンを生成する．
        """
        self.footer_frame = tk.Frame(self, height=30)
        self.footer_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.ok = tk.Button(self.footer_frame, width=10, command=self.on_ok)
        self.ok['text'] = 'OK'
        self.ok.grid(row=0, column=1, padx=10)

        self.cancel = tk.Button(self.footer_frame, width=10, command=self.master.destroy)
        self.cancel['text'] = 'キャンセル'
        self.cancel.grid(row=0, column=2, padx=10)

    def show_name_data(self):
        """名前情報を表示する．
        """
        family = self.family_entry.get()
        given = self.given_entry.get()

        try:
            name = Seimei(family, given, kakusuu_path=self.kakusuu_dict_path)
            self.view.configure(state=tk.NORMAL)
            self.view.delete('1.0', 'end')
            item = name.data()
            self.view.insert('end', str(item))
            self.error_message.set('')

        except Exception as e:
            self.error_message.set(e.args[0])

        self.view.configure(state=tk.DISABLED)

    def on_ok(self):
        """OKボタンが押されたときの処理を行う．
        """
        family = self.family_entry.get()
        given = self.given_entry.get()

        try:
            name = Seimei(family, given, kakusuu_path=self.kakusuu_dict_path)
            self.item = name.data()
            self.master.destroy()

        except Exception as e:
            self.error_message.set(e.args[0])
