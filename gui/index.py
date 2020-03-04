"""姓名登録履歴フレームを含むモジュール．
"""
# pylint: disable=R0902, R0903, R0913, R0914, C0103

import tkinter as tk
import tkinter.ttk as ttk
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
        button_frame: ボタン配置用フレーム
        up_button: 上移動ボタン
        down_button: 下移動ボタン
        remove_button: 削除ボタン
        append_button: 追加ボタン
        footer_frame: フッタ用フレーム
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

        self.header_label = None
        self.info_header_label = None
        self.tree = None
        self.view_frame = None
        self.view = None
        self.button_frame = None
        self.up_button = None
        self.down_button = None
        self.remove_button = None
        self.append_button = None
        self.footer_frame = None
        self.ok = None
        self.cancel = None
        self.pack()
        self.create_widgets()

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
        self.master.bind('<Control-Key-s>', self.on_ok)
        self.master.bind('<Key-colon><Key-w><Key-q>', self.on_ok)
        self.master.bind('<Key-Escape>', self.on_cancel)
        self.master.bind('<Key-bracketleft>', self.on_cancel)
        self.master.bind('<Key-colon><Key-q>', self.on_cancel)

    def create_header(self):
        """ヘッダを生成する．
        """
        self.header_label = tk.Label(self, text='登録履歴')
        self.header_label.grid(row=0, column=0, padx=5, pady=5)
        self.info_header_label = tk.Label(self, text='詳細')
        self.info_header_label.grid(row=0, column=3, padx=5, pady=5)

    def create_tree(self):
        """表を生成する．
        """
        indices = [i for i in range(8)]
        self.tree = ttk.Treeview(self, column=indices, show='headings', height=20)
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
        self.tree.bind('<Control-Key-k>', self.on_up)
        self.tree.bind('<Control-Key-j>', self.on_down)
        self.tree.bind('<Key-j>', self.on_focus_down)
        self.tree.bind('<Key-k>', self.on_focus_up)
        self.tree.bind('<Key-g><Key-g>', self.on_focus_top)
        self.tree.bind('<Key-d><Key-d>', self.on_remove)
        self.tree.bind('<Key-G>', self.on_focus_last)
        self.tree.bind('<Key-Return>', self.show_data)

        self.update_view()
        item = self.tree.get_children()[0]
        self.tree.selection_set(item)
        self.tree.focus(item)

    def create_view(self):
        """表示テキストエリアを生成する．
        """
        self.view_frame = tk.Frame(self)
        self.view_frame.grid(row=1, column=3, rowspan=3, padx=5, pady=5)

        self.view = tk.Text(self.view_frame, width=60, height=25, state=tk.DISABLED)
        self.view.grid(row=0, column=0)

        vscrollbar = ttk.Scrollbar(self.view_frame,
                                   orient=tk.VERTICAL,
                                   command=self.view.yview)
        self.view.configure(yscroll=vscrollbar.set)
        vscrollbar.grid(row=0, column=1, sticky=tk.NS)

    def create_buttons(self):
        """ボタンを生成する．
        """
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=2)

        self.up_button = tk.Button(self.button_frame, text='△', command=self.on_up)
        self.up_button.grid(row=0, padx=5, pady=5)
        self.up_button.bind('<Key-Return>', self.on_up)

        self.down_button = tk.Button(self.button_frame, text='▽', command=self.on_down)
        self.down_button.grid(row=1, padx=5, pady=5)
        self.down_button.bind('<Key-Return>', self.on_down)

        self.remove_button = tk.Button(self.button_frame, text='×', command=self.on_remove)
        self.remove_button.grid(row=2, padx=5, pady=5)
        self.remove_button.bind('<Key-Return>', self.on_remove)

        self.append_button = tk.Button(self.button_frame, text='＋', command=self.on_append)
        self.append_button.grid(row=3, padx=5, pady=5)
        self.append_button.bind('<Key-Return>', self.on_append)

    def create_footer(self):
        """OK・キャンセルボタンを生成する．
        """
        self.footer_frame = tk.Frame(self, height=30)
        self.footer_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.ok = tk.Button(self.footer_frame, width=10, text='OK', command=self.on_ok)
        self.ok.grid(row=0, column=1, padx=10)
        self.ok.bind('<Key-Return>', self.on_ok)

        self.cancel = tk.Button(self.footer_frame, width=10, text='キャンセル',
                                command=self.on_cancel)
        self.cancel.grid(row=0, column=2, padx=10)
        self.cancel.bind('<Key-Return>', self.on_cancel)

    def show_data(self, event):
        """名前情報を表示する．
        """
        # item = self.tree.identify('item', event.x, event.y)
        item = self.tree.selection()[0]
        idx = self.tree.item(item)['values'][0] - 1

        self.view.configure(state=tk.NORMAL)
        self.view.delete('1.0', 'end')
        self.view.insert('end', str(self.history[idx]))

        self.view.configure(state=tk.DISABLED)

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

    def on_ok(self, event=None):
        """保存する．

        Args:
            event: キーイベント情報
        """
        res = messagebox.askokcancel(title='確認', message='保存してよろしいですか？')
        if res:
            self.history.save()
            self.master.destroy()

    def on_cancel(self, event=None):
        """保存する．

        Args:
            event: キーイベント情報
        """
        res = messagebox.askokcancel(title='確認', message='終了してよろしいですか？')
        if res:
            self.master.destroy()

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
        if not self.tree.selection():
            if not self.tree.get_children():
                return

            item = self.tree.get_children()[0]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            return

        item = self.tree.selection()[0]
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
        if not self.tree.selection():
            if not self.tree.get_children():
                return

            item = self.tree.get_children()[0]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            return

        item = self.tree.selection()[0]
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
        item = self.tree.get_children()[0]
        self.tree.selection_set(item)
        self.tree.focus(item)
        self.tree.see(item)
        
    def on_focus_last(self, event=None):
        """フォーカスを一番下に移動する．

        Args:
            event: キーイベント情報
        """
        item = self.tree.get_children()[-1]
        self.tree.selection_set(item)
        self.tree.focus(item)
        self.tree.see(item)
