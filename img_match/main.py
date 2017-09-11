#! env python
# -*- coding: utf-8 -*-

import wx
import sys,os
import cv2

# 変数の宣言
filepath = ""
folderpath = ""
text1 = ""
button_1 = ""

class MainFrame(wx.Frame):

    # イベント
    def click_button_1(self, event):
        global filepath
        global button_1
        # ファイル選択ダイアログを作成
        dialog = wx.FileDialog(None, u'比較ファイルを選択してください')
        # ファイル選択ダイアログを表示
        dialog.ShowModal()
        # 選択したファイルパスを取得する
        filepath = dialog.GetPath()
        self.SetStatusText(os.path.basename(filepath))
        # 終了処理
        cv2.destroyAllWindows()

    def click_button_2(self, event):
        global folderpath
        # フォルダ選択ダイアログを作成
        dialog = wx.DirDialog(None, u'画像フォルダを選択してください')
        # フォルダ選択ダイアログを表示
        dialog.ShowModal()
        # 選択したフォルダパスを取得する
        folderpath = dialog.GetPath()
        self.SetStatusText(folderpath)

    def click_button_3(self, event):
        global filepath
        global folderpath
        global text1
        TARGET_FILE = os.path.basename(filepath)
        IMG_DIR = folderpath + "/"
        IMG_SIZE = (200, 200)
        TargetImgSizeX = 0
        TargetImgSizeY = 0
        ComparingImgSizeX = 0
        ComparingImgSizeY = 0
        winName = ""

        target_img_path = IMG_DIR + TARGET_FILE
        target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
        TargetImgSizeX = target_img.shape[0]
        TargetImgSizeY = target_img.shape[1]
        target_img = cv2.resize(target_img, IMG_SIZE)
        # target_img = cv2.resize(target_img, (TargetImgSizeX*2, TargetImgSizeY*2))
        bw = cv2.adaptiveThreshold(target_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 10)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        detector = cv2.ORB_create()
        # detector = cv2.AKAZE_create()
        # (target_kp, target_des) = detector.detectAndCompute(target_img, None)
        (target_kp, target_des) = detector.detectAndCompute(bw, None)

        print('TARGET_FILE: %s' % (TARGET_FILE))

        files = os.listdir(IMG_DIR)
        text1.Clear()
        # 終了処理
        cv2.destroyAllWindows()
        for file in files:
            if file == '.DS_Store' or file == TARGET_FILE:
                continue

            comparing_img_path = IMG_DIR + file
            winName = os.path.basename(comparing_img_path)
            try:
                comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
                ComparingImgSizeX = comparing_img.shape[0]
                ComparingImgSizeY = comparing_img.shape[1]
                comparing_img = cv2.resize(comparing_img, IMG_SIZE)
                # comparing_img = cv2.resize(comparing_img, (ComparingImgSizeX*2, ComparingImgSizeY*2))
                bw2 = cv2.adaptiveThreshold(comparing_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 10)
                (comparing_kp, comparing_des) = detector.detectAndCompute(bw2, None)
                matches = bf.match(target_des, comparing_des)
                dist = [m.distance for m in matches]
                ret = sum(dist) / len(dist)
            except cv2.error:
                ret = 100000

            print(file, ret)
            text1.AppendText(file + " : " + str(ret) + "\n")
            cv2.namedWindow('output' + winName, cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
            cv2.imshow('output' + winName, bw2)

    def __init__(self):
         wx.Frame.__init__(self, None, wx.ID_ANY, "Main")
         self.InitializeComponents()

    def InitializeComponents(self):
        global text1
        global button_1
        self.CreateStatusBar()
        # ボタンの作成
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour("#AFAFAF")
        button_1 = wx.Button(panel, wx.ID_ANY, u"比較ファイル")
        button_2 = wx.Button(panel, wx.ID_ANY, u"画像フォルダ")
        button_3 = wx.Button(panel, wx.ID_ANY, u"実行")
        # panel2 = wx.Panel(frame, wx.ID_ANY)
        # panel2.SetBackgroundColour("#000000")
        text1 = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_MULTILINE)

        # イベントの設定
        button_1.Bind(wx.EVT_BUTTON, self.click_button_1)
        button_2.Bind(wx.EVT_BUTTON, self.click_button_2)
        button_3.Bind(wx.EVT_BUTTON, self.click_button_3)

        # ボタンレイアウト
        layout = wx.GridBagSizer()
        layout.Add(button_1, (0,0), (1,1), flag=wx.EXPAND)
        layout.Add(button_2, (0,1), (1,1), flag=wx.EXPAND)
        layout.Add(button_3, (0,2), (1,1), flag=wx.EXPAND)
        layout.Add(text1, (1,0), (3,3), flag=wx.EXPAND)
        layout.AddGrowableRow(0)
        layout.AddGrowableRow(1)
        layout.AddGrowableRow(2)
        layout.AddGrowableRow(3)
        layout.AddGrowableCol(0)
        layout.AddGrowableCol(1)
        layout.AddGrowableCol(2)
        panel.SetSizer(layout)

if __name__ == '__main__':
    app = wx.App()
    MainFrame().Show(True)
    app.MainLoop()
