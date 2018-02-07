#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 测试地址 http://artimages.clevelandart.org/zoomify/96FD7F716EC5BBECFD99AFEC8746E128/TileGroup0/4-9-5.jpg
import sys
import download
import merge
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLabel, QPushButton,
                             QLineEdit, QGridLayout,
                             QTextEdit, QFileDialog)
from PyQt5.QtGui import (QFont)
from PyQt5.QtCore import (QThread, pyqtSignal)


class DownloadThread(QThread):
    _signal = pyqtSignal(int, str)

    def __init__(self, code, start_img, start_path, save_img_name,
                 http_proxy, https_proxy):
        super(DownloadThread, self).__init__()
        self.code = code
        self.start_img = start_img
        self.start_path = start_path
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.save_img_name = save_img_name
    
    def run(self):
        download.init(self.code, self.start_img, self.start_path, 
                      self.http_proxy, self.https_proxy, self.callback)
        download.download()
        print("1")
        merge.merge(self.start_path, self.save_img_name+".jpg", 
                    self.callback)
        print("3")

    def callback(self, errorcode, text):
        print("4")
        self._signal.emit(errorcode, text)
    
        
class MerageImage(QWidget): 
    def __init__(self):
        super(MerageImage, self).__init__()
        self.initUI()

    # 初始化界面    
    def initUI(self):
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle("获取图片")
        grid = QGridLayout()
        grid.setSpacing(10)
        self.img_code_lable = QLabel('图片编码', self)
        self.img_code_edit = QLineEdit(self)
        grid.addWidget(self.img_code_lable, 1, 0)
        grid.addWidget(self.img_code_edit, 1, 1)
        self.start_img_label = QLabel('第一张图片', self)
        self.start_img_edit = QLineEdit(self)
        grid.addWidget(self.start_img_label, 2, 0)
        grid.addWidget(self.start_img_edit, 2, 1)
        self.save_dir_path_label = QLabel('保存路径', self)
        self.save_dir_path_edit = QLineEdit(self)
        self.file_open = QPushButton('打开', self)
        self.file_open.clicked.connect(self.openDir)
        grid.addWidget(self.save_dir_path_label, 3, 0)
        grid.addWidget(self.save_dir_path_edit, 3, 1)
        grid.addWidget(self.file_open, 3, 2)
        self.save_img_name_label = QLabel('保存图片名称', self)
        self.save_img_name_edit = QLineEdit(self)
        grid.addWidget(self.save_img_name_label, 4, 0)
        grid.addWidget(self.save_img_name_edit, 4, 1)
        self.http_proxy_label = QLabel('HTTP', self)
        self.http_proxy_edit = QLineEdit(self)
        self.http_proxy_edit.setText('socks5://127.0.0.1:1080')
        grid.addWidget(self.http_proxy_label, 5, 0)
        grid.addWidget(self.http_proxy_edit, 5, 1)
        self.https_proxy_label = QLabel('HTTPS', self)
        self.https_proxy_edit = QLineEdit(self)
        self.https_proxy_edit.setText('socks5://127.0.0.1:1080')
        grid.addWidget(self.https_proxy_label, 6, 0)
        grid.addWidget(self.https_proxy_edit, 6, 1)
        self.comfirm_btn = QPushButton('下载', self)
        self.comfirm_btn.clicked.connect(self.comfirmClick)
        grid.addWidget(self.comfirm_btn, 7, 0)
        self.download_info = QTextEdit(self)
        self.download_info.setReadOnly(True)
        grid.addWidget(self.download_info, 8, 0, 1, 2)
        self.setLayout(grid)
        self.show()
        self.activateWindow()

    # 按钮点击事件
    def comfirmClick(self):
        self.img_code = self.img_code_edit.text()
        self.start_img = self.start_img_edit.text()
        self.dir_path = self.save_dir_path_edit.text()
        self.save_img_name = self.save_img_name_edit.text()
        self.http_proxy = self.http_proxy_edit.text()
        self.https_proxy = self.https_proxy_edit.text()
        if not self.checkInput():
            return
        else:
            self.comfirm_btn.setEnabled(False)
            self.infoOutput('[INFO]:下载开始')
            self.downloadThread = DownloadThread(self.img_code, 
                                                 self.start_img, 
                                                 self.dir_path,
                                                 self.save_img_name, 
                                                 self.http_proxy, 
                                                 self.https_proxy)
            self.downloadThread._signal.connect(self.callback)
            self.downloadThread.start()

    # 打开文件夹
    def openDir(self):
        filename = QFileDialog.getExistingDirectory(self, 'open file', './')
        self.save_dir_path_edit.setText(filename)
    
    # 下载/合并回调输出信息
    def callback(self, errorcode, text):
        if errorcode == 0:
            self.comfirm_btn.setEnabled(True)
        elif errorcode == 1:
            self.infoOutput('[INFO]:'+text)
        else:
            self.infoOutput('[ERROR]:'+text)

    # 输出信息
    def infoOutput(self, text):
        self.download_info.append(text)

    # 检测输入是否合法                              
    def checkInput(self):
        if not self.img_code:
            self.infoOutput('[ERROR]:请输入图片编码')
            return False
        elif not self.start_img:
            self.infoOutput('[ERROR]:请输入第一张图片名称')
            return False
        elif not self.dir_path:
            self.infoOutput('[ERROR]:请输入保存路径')
            return False
        elif not self.save_img_name:
            self.infoOutput('[ERROR]:请输入保存名')
            return False
        else:
            return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont('宋体', 12))
    merageImage = MerageImage()
    sys.exit(app.exec_())