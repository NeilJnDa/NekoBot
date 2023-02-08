# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
import Neko_add
import Neko_Mouse_0
import win32api
sys.path.append("..")  # 加入上级目录

# 路径和配置文件的全局变量
current_path = os.path.abspath(".")
email_conf_path = os.path.join(current_path, "email.yml")
user_conf_path = os.path.join(current_path, "config.yml")
email_conf = Neko_add.get_yaml(email_conf_path)
user_conf = Neko_add.get_yaml(user_conf_path)


def confirm_save_email():
    # 获取新填入的content，直接保存即可，
    email_conf['content1'] = ui.textEdit.toPlainText()
    email_conf['content2'] = ui.textEdit_2.toPlainText()
    email_conf['sender_mail'] = ui.lineEdit.text()
    email_conf['sender_pass'] = ui.lineEdit_2.text()
    email_conf['from'] = ui.lineEdit_3.text()
    email_conf['subject'] = ui.lineEdit_4.text()
    email_conf['path'] = ui.textBrowser_2.toPlainText()
    # print('confirm_save_email')
    Neko_add.generate_yaml(email_conf_path, email_conf)


def confirm_save_accounts():
    # 一直都在编辑表格，要从表格转化为字典，需要构造新的字典然后保存。
    dict_template = {'name': None, 'enable': True, 'id': None, 'password': None, 'email': None}
    i, j = 0, 0
    save_accounts_conf = []
    for i in range(0, ui.tableWidget.rowCount()):
        temp = dict_template.copy()
        for key in temp.keys():
            if j == 1:
                if ui.tableWidget.cellWidget(i, j).isChecked():
                    temp[key] = True
                else:
                    temp[key] = False
                j += 1
            else:
                temp[key] = ui.tableWidget.item(i, j).text()
                j += 1
        j = 0
        save_accounts_conf.append(temp)
        i += 1

    Neko_add.generate_yaml(user_conf_path, save_accounts_conf)
    pass


def email_enable():
    if ui.radioButton.isChecked():
        email_conf['enable'] = True
    else:
        email_conf['enable'] = False
    pass


def restore_default():
    init()


def preview_email():
    content1 = ui.textEdit.toPlainText()
    content2 = ui.textEdit_2.toPlainText()
    # print(content1)
    ui.textBrowser.setText(content1 + '<p>' + '今日填报结果：自动填报已完成' + '</p>' + content2)


def init():
    # 文本框
    if email_conf['enable']:
        ui.radioButton.setChecked(True)
    else:
        ui.radioButton.setChecked(False)
    ui.lineEdit.setText(email_conf['sender_mail'])
    ui.lineEdit_2.setText(email_conf['sender_pass'])
    ui.lineEdit_3.setText(email_conf['from'])
    ui.lineEdit_4.setText(email_conf['subject'])
    ui.textEdit.setPlainText(email_conf['content1'])
    ui.textEdit_2.setPlainText(email_conf['content2'])
    ui.textBrowser_2.setText(email_conf['path'])
    # 文件路径横向滑动
    ui.textBrowser_2.setLineWrapMode(0)
    # 不显示滑动条
    ui.textBrowser_2.setHorizontalScrollBarPolicy(1)
    ui.textBrowser_2.setVerticalScrollBarPolicy(1)
    # 并将光标放在字符结束
    ui.textBrowser_2.moveCursor(ui.textBrowser_2.textCursor().End)
    # 预览
    ui.textBrowser.setText(email_conf['content1'] + '<p>' + '今日填报结果：自动填报已完成' + '</p>' + email_conf['content2'])
    # 表格
    table_init()


def table_init():
    # 表格
    ui.tableWidget.setRowCount(len(user_conf))
    if len(user_conf) > 0:
        ui.tableWidget.setColumnCount(len(user_conf[0]))
    else:
        ui.tableWidget.setColumnCount(0)
    ui.tableWidget.verticalHeader().setVisible(False)
    # 填充表格
    i, j = 0, 0
    for user in user_conf:
        for value in user.values():
            if j == 1:
                toggleButton = QPushButton()
                toggleButton.setFlat(True)
                toggleButton.setCheckable(True)
                if user['enable']:
                    # toggleButton.setDown(True)
                    toggleButton.setChecked(True)
                else:
                    # toggleButton.setDown(False)
                    toggleButton.setChecked(False)
                ui.tableWidget.setCellWidget(i, j, toggleButton)
                j += 1
            else:
                newItem = QTableWidgetItem(value)
                # 居中
                newItem.setTextAlignment(0x0004)
                ui.tableWidget.setItem(i, j, newItem)
                j += 1
        j = 0
        i += 1
    #  列宽适应内容
    ui.tableWidget.resizeColumnsToContents()


def new_user():
    ui.tableWidget.setRowCount(ui.tableWidget.rowCount() + 1)
    toggleButton = QPushButton()
    toggleButton.setFlat(True)
    toggleButton.setDown(True)
    toggleButton.setCheckable(True)
    ui.tableWidget.setCellWidget(ui.tableWidget.rowCount() - 1, 0, toggleButton)
    pass


def delete_user():
    delete_row = ui.tableWidget.currentRow()  # 获取当前选中的行
    ui.tableWidget.removeRow(delete_row)  # 删除指定行
    pass


def run_neko():
    confirm_save_accounts()
    confirm_save_email()
    neko_path = ui.textBrowser_2.toPlainText()
    try:
        win32api.ShellExecute(0, 'open', neko_path, '', '', 1)
    except:
        print("Error run exe")
    pass


def browse_choose():
    openfile_name = QFileDialog.getOpenFileName()
    # 文件名
    ui.textBrowser_2.setPlainText(str(openfile_name[0]))
    pass


def send_email():
    confirm_save_accounts()
    confirm_save_email()
    user_conf = Neko_add.get_yaml(user_conf_path)
    Neko_add.send_emails_to_all_manual(user_conf)
    pass


if __name__ == '__main__':

    # 打开窗口
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Neko_Mouse_0.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # 定义交互
    init()
    ui.pushButton.clicked.connect(lambda: confirm_save_email())
    ui.pushButton.clicked.connect(lambda: confirm_save_accounts())
    ui.pushButton_2.clicked.connect(lambda: new_user())
    ui.pushButton_4.clicked.connect(lambda: restore_default())
    ui.pushButton_3.clicked.connect(lambda: preview_email())
    ui.pushButton_5.clicked.connect(lambda: delete_user())
    ui.pushButton_6.clicked.connect(lambda: run_neko())
    ui.radioButton.toggled.connect(lambda: email_enable())
    ui.pushButton_7.clicked.connect(lambda: browse_choose())
    ui.pushButton_8.clicked.connect(lambda: send_email())
    # 退出
    sys.exit(app.exec_())
