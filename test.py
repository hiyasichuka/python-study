# -*- mode:python;coding:utf-8 -*-
import random
import sys
import tkinter
import time
from typing import Any, List, Type

QA_INTERVAL = 300
DEBUG = False

def abort_process(event: tkinter.Event) -> None:
    u'''強制終了
    '''
    sys.exit(1)

class QAFrame(tkinter.Frame):
    u'''問題表示クラス'''
    def __init__(self, window: tkinter.Tk,
                 *args: Any, **kwargs: Any) -> None:
        tkinter.Frame.__init__(self, window, *args, **kwargs)
    def result(self) -> bool:
        return False
class AnsEntry(tkinter.Entry):
    u'''回答入力
    '''
    def __init__(self, frame: tkinter.Frame,
                 status: tkinter.StringVar, trueAns: str) -> None:
        tkinter.Entry.__init__(self, frame)
        self.status = status
        self.trueAns = trueAns
        self.stringVar = tkinter.StringVar()
        self.stringVar.trace('w', self._updated)
        self.configure(textvariable=self.stringVar)
    def _updated(self, *args: Any) -> None:
        self.status.set("updated: {0}".format(args[0]))
        if args[0] != self.stringVar._name:
            return
        s = self.stringVar.get()
        if s == self.trueAns:
            self._success()
        else:
            self._ng()
    def _success(self) -> None:
        self.status.set("OK")
    def _ng(self) -> None:
        self.status.set("NG")
    def result(self) -> bool:
        return str(self.status.get()) == "OK"
class QACalcAddFrame(QAFrame):
    u'''簡単な足し算の問題を出す
    '''
    def __init__(self, window: tkinter.Tk,
                 *args: Any, **kwargs: Any) -> None:
        QAFrame.__init__(self, window, *args, **kwargs)
        self.pack()
        a = random.randrange(0, 20)
        b = random.randrange(0, 20)
        qtext =  '{0} + {1} ='.format(a, b)
        status = tkinter.StringVar()
        statusLabel = tkinter.Label(self, textvariable=status)
        questionLabel = tkinter.Label(self, text=qtext)
        self.ansEntry = AnsEntry(self, status, str(a + b))
        statusLabel.grid(column=0, row=0,)
        questionLabel.grid(column=1, row=0)
        self.ansEntry.grid(column=2, row=0)
    def result(self) -> bool:
        u'''回答内容が正しいなら文字列 'OK' を返す。
        '''
        return self.ansEntry.result()
class SummaryFrame(tkinter.Frame):
    u'''結果表示
    '''
    def __init__(self, window: tkinter.Tk,
                 qainstances: List[QAFrame], *args: Any, **kwargs: Any) -> None:
        tkinter.Frame.__init__(self, window, *args, **kwargs)
        self.window = window
        self.qainstances = qainstances
        self.after(1000, self._check)
        self.status = tkinter.StringVar()
        statusLabel = tkinter.Label(self, textvariable=self.status)
        statusLabel.pack()
    def _check(self) -> None:
        ngcount = sum([(0 if qainstance.result() else 1)
                       for qainstance in self.qainstances])
        if ngcount == 0:
            self.status.set('おわり！！！'.format(ngcount))
            self.after(1000, self.window.destroy)
        else:
            self.status.set('のこり {0} もん'.format(ngcount))
            self.after(1000, self._check)

# 問題を3つ出す
QACLASSES: List[Type[QAFrame]] = [QACalcAddFrame,QACalcAddFrame,QACalcAddFrame]

def display_qa() -> None:
    # メイン関数
    window = tkinter.Tk()
    time.sleep(1)
    window.attributes('-fullscreen', True)
    window.title("test window")
    qainstances = []
    for qaclass in QACLASSES:
        qa = qaclass(window, pady=10, padx=10)
        qainstances.append(qa)
    summary = SummaryFrame(window, qainstances)
    summary.pack()
    # デバッグ用
    if DEBUG:
        button = tkinter.Button(window, text="exit")
        button.pack()
        button.bind("<ButtonPress>", abort_process)
    window.mainloop()

if __name__ == '__main__':
    display_qa()