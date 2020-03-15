"""姓名登録履歴フレームを含むモジュール．
"""
# pylint: disable=R0902, R0903, R0913, R0914, C0103

import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
from tkinter import messagebox
import numpy as np

from seimei.seimei_history import SeimeiHistory
from gui.append import AppendFrame

class SeimeiFrame(tk.Frame):
    """姓名登録履歴を表示するためのフレーム．

    Attributes:
        master: マスタ
        history: 姓名データ
        kakusuu_dict_path: 文字と画数の辞書ファイルのパス
        header_label: ヘッダラベル
        info_header_label: 詳細情報ヘッダラベル
        tree: 履歴表示部
        view_frame: 詳細表示フレーム
        view: 詳細情報
        view_item: 詳細表示している項目
        font_family: フォント種類
        note_label: ノートの説明ラベル
        note: ノート
        button_frame: ボタン配置用フレーム
        up_button: 上移動ボタン
        down_button: 下移動ボタン
        remove_button: 削除ボタン
        append_button: 追加ボタン
        footer_frame: フッタ用フレーム
        save: 保存ボタン
        ok: OKボタン
        cancel: キャンセルボタン
    """
    def __init__(self, history_path, kakusuu_dict_path, master=None):
        """初期化をする．

        Args:
            history_path: 姓名データファイルへのパス
            kakusuu_dict_path: 画数履歴フィアルのパス
            master: マスタ
        """
        super().__init__(master)
        self.master = master
        self.history = SeimeiHistory(history_path)
        self.kakusuu_dict_path = kakusuu_dict_path
        self.view_item = None
        self.font_family = 'IPAゴシック' if os.name == 'posix' else 'ＭＳ ゴシック'

        self.header_label = None
        self.info_header_label = None
        self.tree = None
        self.view_frame = None
        self.view = None
        self.note_label = None
        self.note = None

        self.button_frame = None
        self.up_button = None
        self.down_button = None
        self.remove_button = None
        self.append_button = None
        self.footer_frame = None
        self.save = None
        self.ok = None
        self.cancel = None

        self.master.title('Seimei')
        self.pack()
        self.create_widgets()
        ttk.Style().configure('Treeview', font=(self.font_family))

    def create_widgets(self):
        """構成要素を生成する．
        """
        self.create_header()
        self.create_tree()
        self.create_buttons()
        self.create_view()
        self.create_footer()
        self.bind_keys()
        self.tree.focus_set()

    def bind_keys(self):
        """ショートカットキーを設定する．
        """
        self.master.bind('<Control-Key-a>', self.on_append)
        self.master.bind('<Control-Key-r>', self.on_remove)
        self.master.bind('<Control-Key-s>', self.on_save)
        self.master.bind('<Key-colon><Key-w>', self.on_colon_w)
        self.master.bind('<Control-Key-w>', self.on_cancel)
        self.master.bind('<Key-colon><Key-q>', self.on_colon_q)
        self.master.bind('<Control-Key-k>', self.on_up)
        self.master.bind('<Control-Key-j>', self.on_down)
        self.master.bind('<Key-g><Key-g>', self.on_focus_top)
        self.master.bind('<Key-d><Key-d>', self.on_remove)
        self.master.bind('<Key-G>', self.on_focus_last)
        self.master.bind('<Key-j>', self.on_focus_down)
        self.master.bind('<Key-k>', self.on_focus_up)

    def create_header(self):
        """ヘッダを生成する．
        """
        self.header_label = tk.Label(self, text='登録履歴',
                                     font=Font(family=self.font_family))
        self.header_label.grid(row=0, column=0, padx=5, pady=5)
        self.info_header_label = tk.Label(self, text='詳細',
                                          font=Font(family=self.font_family))
        self.info_header_label.grid(row=0, column=3, padx=5, pady=5)

    def create_tree(self):
        """表を生成する．
        """
        indices = [i for i in range(8)]
        self.tree = ttk.Treeview(self, column=indices, show='headings', height=30)
        self.tree.grid(row=1, column=0)

        width_of = lambda i: 35 if i == 0 else 75
        for i in indices:
            self.tree.column(i, width=width_of(i))

        header = ['', '姓', '名', '天格', '人格', '地格', '外格', '総格']
        for i, text in zip(indices, header):
            self.tree.heading(i, text=text)

        vscrollbar = ttk.Scrollbar(self,
                                   orient=tk.VERTICAL,
                                   command=self.tree.yview)
        self.tree.configure(yscroll=vscrollbar.set)
        vscrollbar.grid(row=1, column=1, sticky=tk.NS)

        self.tree.bind('<Double-Button-1>', self.show_data)

        self.tree.bind('<Key-Return>', self.show_data)
        self.tree.bind('<Key-space>', self.show_data)

        self.update_view()

        items = self.tree.get_children()
        if items:
            item = items[0]
            self.tree.selection_set(item)
            self.tree.focus(item)

    def create_view(self):
        """表示テキストエリアを生成する．
        """
        self.view_frame = tk.Frame(self)
        self.view_frame.grid(row=1, column=3, rowspan=3, padx=5, pady=5, sticky=tk.NS)

        self.view = tk.Text(self.view_frame, state=tk.DISABLED,
                            font=Font(family=self.font_family, size='15'))
        self.view.grid(row=0, column=0, columnspan=2, sticky=tk.NS)

        vscrollbar = ttk.Scrollbar(self.view_frame,
                                   orient=tk.VERTICAL,
                                   command=self.view.yview)
        self.view.configure(yscroll=vscrollbar.set)
        vscrollbar.grid(row=0, column=2, sticky=tk.NS)

        self.note_label = tk.Label(self.view_frame, text='ノート', height=2, anchor=tk.W,
                                   font=Font(family=self.font_family))
        self.note_label.grid(row=1, column=0, sticky=tk.EW)

        self.note_save = tk.Button(self.view_frame, text='ノート保存',
                                   font=Font(family=self.font_family),
                                   command=self.on_note_save)
        self.note_save.grid(row=1, column=1, columnspan=2, sticky=tk.E)
        self.note_save.bind('<Key-Return>', self.on_note_save)

        self.note = tk.Text(self.view_frame, height=3, font=Font(family=self.font_family))
        self.note.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        self.note.bind('<Control-Key-bracketleft>', self.on_focus_tree)
        self.note.bind('<Key-Escape>', self.on_focus_tree)

        vscrollbar_note = ttk.Scrollbar(self.view_frame,
                                        orient=tk.VERTICAL,
                                        command=self.note.yview)
        self.note.configure(yscroll=vscrollbar_note.set)
        vscrollbar_note.grid(row=2, column=2, sticky=tk.NS)

    def on_focus_tree(self, event):
        """履歴にフォーカスする．

        Args:
            event: イベント情報
        """
        self.tree.focus_set()

    def on_note_save(self, event=None):
        """ノートにキー入力されたときの処理する．
        """
        item = self.view_item
        if item:
            item.note = self.note.get('1.0', 'end').replace('\n', '\\n')

    def create_buttons(self):
        """ボタンを生成する．
        """
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=2)

        self.up_button = tk.Button(self.button_frame, text='△', command=self.on_up,
                                   font=Font(family=self.font_family))
        self.up_button.grid(row=0, padx=5, pady=5, sticky=tk.EW)
        self.up_button.bind('<Key-Return>', self.on_up)

        self.down_button = tk.Button(self.button_frame, text='▽', command=self.on_down,
                                     font=Font(family=self.font_family))
        self.down_button.grid(row=1, padx=5, pady=5, sticky=tk.EW)
        self.down_button.bind('<Key-Return>', self.on_down)

        self.remove_button = tk.Button(self.button_frame, text='×', command=self.on_remove,
                                       font=Font(family=self.font_family))
        self.remove_button.grid(row=2, padx=5, pady=5, sticky=tk.EW)
        self.remove_button.bind('<Key-Return>', self.on_remove)

        self.append_button = tk.Button(self.button_frame, text='＋', command=self.on_append,
                                       font=Font(family=self.font_family))
        self.append_button.grid(row=3, padx=5, pady=5, sticky=tk.EW)
        self.append_button.bind('<Key-Return>', self.on_append)

    def create_footer(self):
        """保存・OK・キャンセルボタンを生成する．
        """
        self.footer_frame = tk.Frame(self, height=30)
        self.footer_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.save = tk.Button(self.footer_frame, width=10, text='保存', command=self.on_save,
                              font=Font(family=self.font_family))
        self.save.grid(row=0, column=1, padx=10)
        self.save.bind('<Key-Return>', self.on_save)

        self.ok = tk.Button(self.footer_frame, width=10, text='OK', command=self.on_ok,
                            font=Font(family=self.font_family))
        self.ok.grid(row=0, column=2, padx=10)
        self.ok.bind('<Key-Return>', self.on_ok)

        self.cancel = tk.Button(self.footer_frame, width=10, text='キャンセル',
                                command=self.on_cancel,
                                font=Font(family=self.font_family))
        self.cancel.grid(row=0, column=3, padx=10)
        self.cancel.bind('<Key-Return>', self.on_cancel)

    def show_data(self, event):
        """名前情報を表示する．
        """
        items = self.tree.selection()
        if not items:
            return

        item = items[0]
        idx = self.tree.item(item)['values'][0] - 1
        self.view_item = self.history[idx]

        self.view.configure(state=tk.NORMAL)
        self.view.delete('1.0', 'end')
        self.view.insert('end', str(self.history[idx]))

        self.view.configure(state=tk.DISABLED)

        self.note.delete('1.0', 'end')
        self.note.insert('end', self.history[idx].note.replace('\\n', '\n'))

    def update_view(self):
        """表示データを更新する．
        """
        self.tree.delete(*self.tree.get_children())
        for i, item in enumerate(self.history):
            family = item.family
            given = item.given
            tenkaku = item.gokaku_dict['天格']
            jinkaku = item.gokaku_dict['人格']
            tikaku = item.gokaku_dict['地格']
            gaikaku = item.gokaku_dict['外格']
            soukaku = item.gokaku_dict['総格']
            self.tree.insert('', 'end', values=(i+1, family, given, tenkaku,
                                                jinkaku, tikaku, gaikaku, soukaku))

    def on_save(self, event=None):
        """保存する．

        Args:
            event: キーイベント情報

        Returns:
            保存する場合はTrue
        """
        res = messagebox.askokcancel(title='確認', message='保存してよろしいですか？')
        if res:
            self.history.save()

        return res

    def on_ok(self, event=None):
        """保存して終了する。

        Args:
            event: キーイベント情報
        """
        res = self.on_save()
        if res:
            self.master.destroy()

    def on_cancel(self, event=None):
        """保存する．

        Args:
            event: キーイベント情報
        """
        res = messagebox.askokcancel(title='確認', message='終了してよろしいですか？')
        if res:
            self.master.destroy()

    def on_colon_w(self, event):
        """:wキーに対する処理を行う．

        Args:
            event: キーイベント情報
        """
        if self.master.focus_get() != self.note:
            self.on_save(event)

    def on_colon_q(self, event):
        """:qキーに対する処理を行う．

        Args:
            event: キーイベント情報
        """
        if self.master.focus_get() != self.note:
            self.on_cancel(event)

    def on_up(self, event=None):
        """選択項目を上に移動する．

        Args:
            event: キーイベント情報
        """
        indices = []
        for item in self.tree.selection():
            idx = self.tree.item(item)['values'][0] - 1
            indices.append(idx)

        if not indices:
            return

        moved = self.history.move_up(*indices)
        if not moved:
            return

        self.update_view()
        sorted_indices = iter(np.sort(indices))

        items = []
        try:
            idx = next(sorted_indices)
            for item in self.tree.get_children():
                tree_idx = self.tree.item(item)['values'][0] - 1
                if tree_idx == idx - 1:
                    items.append(item)
                    idx = next(sorted_indices)

        except StopIteration:
            pass

        self.tree.selection_set(*items)
        for item in items:
            self.tree.focus(item)

        self.tree.see(items[0])

    def on_down(self, event=None):
        """選択項目を下に移動する．

        Args:
            event: キーイベント情報
        """
        indices = []
        for item in self.tree.selection():
            idx = self.tree.item(item)['values'][0] - 1
            indices.append(idx)

        if not indices:
            return

        moved = self.history.move_down(*indices)
        if not moved:
            return

        self.update_view()
        sorted_indices = iter(np.sort(indices))

        items = []
        try:
            idx = next(sorted_indices)
            for item in self.tree.get_children():
                tree_idx = self.tree.item(item)['values'][0] - 1
                if tree_idx == idx + 1:
                    items.append(item)
                    idx = next(sorted_indices)

        except StopIteration:
            pass

        self.tree.selection_set(*items)
        for item in items:
            self.tree.focus(item)

        self.tree.see(items[-1])

    def on_remove(self, envet=None):
        """項目を削除する．

        Args:
            event: キーイベント情報
        """
        if self.focus_get() == self.note:
            return

        indices = []
        for item in self.tree.selection():
            idx = self.tree.item(item)['values'][0] - 1
            indices.append(idx)

        if not indices:
            return

        res = messagebox.askokcancel(title='確認', message='削除してよろしいですか？')
        if not res:
            return

        self.history.remove(*indices)
        self.update_view()

    def on_append(self, event=None):
        """項目を追加する．

        Args:
            event: キーイベント情報
        """
        if self.focus_get() == self.note:
            return

        dlg = tk.Toplevel()
        frame = AppendFrame(self.kakusuu_dict_path, dlg)
        dlg.grab_set()
        dlg.focus_set()
        dlg.wait_window(dlg)

        item = frame.item
        if not item:
            return

        self.history.add(item)
        self.update_view()
        self.on_focus_last()

    def on_focus_up(self, event=None):
        """フォーカスを一つ上に移動する．

        Args:
            event: キーイベント情報
        """
        if self.focus_get() == self.note:
            return

        select_items = self.tree.selection()
        if not select_items:
            items = self.tree.get_children()
            if not items:
                return

            item = items[0]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            return

        item = select_items[0]
        idx = self.tree.item(item)['values'][0] - 1
        if idx == 0:
            return

        idx -= 1
        target_item = None
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] - 1 == idx:
                target_item = item
                break

        if not target_item:
            return


        self.tree.selection_set(target_item)
        self.tree.focus(target_item)
        self.tree.see(target_item)

    def on_focus_down(self, event=None):
        """フォーカスを一つ下に移動する．

        Args:
            event: キーイベント情報
        """
        if self.focus_get() == self.note:
            return

        select_items = self.tree.selection()
        if not select_items:
            items = self.tree.get_children()
            if not items:
                return

            item = items[0]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            return

        item = select_items[-1]
        idx = self.tree.item(item)['values'][0] - 1
        if idx == len(self.history) - 1:
            return

        idx += 1
        target_item = None
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] - 1 == idx:
                target_item = item
                break

        if not target_item:
            return

        self.tree.selection_set(target_item)
        self.tree.focus(target_item)
        self.tree.see(target_item)
        
    def on_focus_top(self, event=None):
        """フォーカスを一番上に移動する．

        Args:
            event: キーイベント情報
        """
        items = self.tree.get_children()
        if not items:
            return

        item = items[0]
        self.tree.selection_set(item)
        self.tree.focus(item)
        self.tree.see(item)
        
    def on_focus_last(self, event=None):
        """フォーカスを一番下に移動する．

        Args:
            event: キーイベント情報
        """
        items = self.tree.get_children()
        if not items:
            return

        item = items[-1]
        self.tree.selection_set(item)
        self.tree.focus(item)
        self.tree.see(item)
