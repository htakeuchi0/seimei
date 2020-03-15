"""姓名登録フレームを含むモジュール．
"""
# pylint: disable=R0902, R0903, R0913, R0914, C0103
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
from seimei.seimei_core import Seimei
from tkinter import messagebox

class AppendFrame(tk.Frame):
    """姓名を登録するためのフレーム．

    Attributes:
        master: マスタ
        item: 姓名データ
        font_family: フォント種類
        family_label: 姓ラベル
        given_label: 名ラベル
        family_entry: 姓テキストボックス
        given_entry: 名テキストボックス
        view_button: 表示ボタン
        view_frame: 表示フレーム
        view: 表示テキストエリア
        note_label: ノートの説明ラベル
        note: ノート
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
        self.font_family = 'IPAゴシック' if os.name == 'posix' else 'ＭＳ ゴシック'

        self.family_label = None
        self.given_label = None
        self.family_entry = None
        self.given_entry = None
        self.view_button = None
        self.view_frame = None
        self.view = None
        self.note_label = None
        self.note = None

        self.error_message = None
        self.error = None
        self.footer_frame = None
        self.ok = None
        self.cancel = None

        self.master.title('新規登録')
        self.pack()
        self.create_widgets()

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
        self.master.bind('<Control-Key-s>', self.on_ok)
        self.master.bind('<Key-colon><Key-w><Key-q>', self.on_colon_wq)
        self.master.bind('<Control-Key-w>', self.on_cancel)
        self.master.bind('<Key-colon><Key-q>', self.on_colon_q)
        self.family_entry.focus_set()

    def create_family_label(self):
        """姓ラベルを生成する．
        """
        self.family_label = tk.Label(self, text='姓', font=Font(family=self.font_family))
        self.family_label.grid(row=0, column=0, padx=10, pady=1)

    def create_given_label(self):
        """名ラベルを生成する．
        """
        self.given_label = tk.Label(self, text='名', font=Font(family=self.font_family))
        self.given_label.grid(row=0, column=1, padx=10, pady=1)

    def create_family_entry(self):
        """姓テキストボックスを生成する．
        """
        self.family_entry = tk.Entry(self, font=Font(family=self.font_family))
        self.family_entry.grid(row=1, column=0, padx=10, pady=1)
        self.family_entry.bind('<Key-Return>', self.focus_given_entry)
        self.family_entry.bind('<Control-Key-bracketleft>', self.focus_master)
        self.family_entry.bind('<Key-Escape>', self.focus_master)

    def create_given_entry(self):
        """名テキストボックスを生成する．
        """
        self.given_entry = tk.Entry(self, font=Font(family=self.font_family))
        self.given_entry.grid(row=1, column=1, padx=10, pady=1)
        self.given_entry.bind('<Key-Return>', self.focus_view_button)
        self.given_entry.bind('<Control-Key-bracketleft>', self.focus_master)
        self.given_entry.bind('<Key-Escape>', self.focus_master)

    def focus_master(self, event):
        self.master.focus_set()

    def create_view_button(self):
        """表示ボタンを生成する．
        """
        self.view_button = tk.Button(self, command=self.show_name_data, text='表示',
                                     font=Font(family=self.font_family))
        self.view_button.grid(row=1, column=2, padx=10, pady=1)
        self.view_button.bind('<Key-Return>', self.show_name_data)

    def create_view(self):
        """表示テキストエリアを生成する．
        """
        self.view_frame = tk.Frame(self)
        self.view_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.view = tk.Text(self.view_frame, width=40, height=23, state=tk.DISABLED,
                            font=Font(family=self.font_family, size='15'))
        self.view.grid(row=0, column=0)

        vscrollbar = ttk.Scrollbar(self.view_frame,
                                   orient=tk.VERTICAL,
                                   command=self.view.yview)
        self.view.configure(yscroll=vscrollbar.set)
        vscrollbar.grid(row=0, column=1, sticky=tk.NS)

        self.note_label = tk.Label(self.view_frame, text='ノート', height=2,
                                   font=Font(family=self.font_family),
                                   anchor=tk.W)
        self.note_label.grid(row=1, column=0, sticky=tk.EW)

        self.note = tk.Text(self.view_frame, width=30, height=3,
                            font=Font(family=self.font_family))
        self.note.grid(row=2, column=0, sticky=tk.EW)
        self.note.bind('<Control-Key-bracketleft>', self.on_focus_ok)
        self.note.bind('<Key-Escape>', self.on_focus_ok)

        vscrollbar_note = ttk.Scrollbar(self.view_frame,
                                        orient=tk.VERTICAL,
                                        command=self.note.yview)
        self.note.configure(yscroll=vscrollbar_note.set)
        vscrollbar_note.grid(row=2, column=1, sticky=tk.NS)

    def on_focus_ok(self, event):
        """OKボタンにフォーカスする．

        Args:
            event: イベント情報
        """
        self.ok.focus_set()

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

        self.ok = tk.Button(self.footer_frame, width=10, command=self.on_ok, text='OK',
                            font=Font(family=self.font_family))
        self.ok.grid(row=0, column=1, padx=10)
        self.ok.bind('<Key-Return>', self.on_ok)

        self.cancel = tk.Button(self.footer_frame, width=10, command=self.on_cancel,
                                text='キャンセル',
                                font=Font(family=self.font_family))
        self.cancel.grid(row=0, column=2, padx=10)
        self.cancel.bind('<Key-Return>', self.on_cancel)

    def focus_given_entry(self, event):
        """名テキストボックスにフォーカスを移す．

        Args:
            event: キーイベント情報
        """
        self.given_entry.focus_set()

    def focus_view_button(self, event):
        """表示ボタンにフォーカスを移す．

        Args:
            event: キーイベント情報
        """
        self.view_button.focus_set()

    def show_name_data(self, event=None):
        """名前情報を表示する．

        Args:
            event: キーイベントの場合の情報
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
            self.error_message.set(e)

        self.view.configure(state=tk.DISABLED)
        self.ok.focus_set()

    def on_ok(self, event=None):
        """OKボタンが押されたときの処理を行う．

        Args:
            event: キーイベント情報
        """
        family = self.family_entry.get()
        given = self.given_entry.get()

        try:
            name = Seimei(family, given, kakusuu_path=self.kakusuu_dict_path)
            self.item = name.data()
            self.item.note = self.note.get('1.0', 'end')
            self.master.destroy()

        except Exception as e:
            self.error_message.set(e)

    def on_cancel(self, event=None):
        """キャンセルボタンが押されたときの処理を行う．

        Args:
            event: キーイベント情報
        """
        res = messagebox.askokcancel(title='確認', message='終了してよろしいですか？')
        if res:
            self.master.destroy()

    def on_colon_wq(self, event):
        """:wqキーに対する処理を行う．

        Args:
            event: キーイベント情報
        """
        focus = self.master.focus_get()
        if focus != self.note and \
                focus != self.family_entry and \
                focus != self.given_entry:
            self.on_ok(event)

    def on_colon_q(self, event):
        """:qキーに対する処理を行う．

        Args:
            event: キーイベント情報
        """
        focus = self.master.focus_get()
        if focus != self.note and \
                focus != self.family_entry and \
                focus != self.given_entry:
            self.on_cancel(event)
