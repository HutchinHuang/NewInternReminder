# -*- coding:utf-8 -*-
# This is the main GUI of my little program using wxPython
import wx
import wx.adv
import sys
import shelve
import time
from datetime import datetime
from getIntern import send_intern_mail

seconds_per_day = 86400  # Define a constant value

# Use shelve to get parameter changing rules.
# This shelve is created in file "change_input.py".
with shelve.open("shelve/para_change_dict") as slvFile:
    city_dict = slvFile["city"]
    salary_dict = slvFile["salary"]
    degree_dict = slvFile["degree"]
    remain_dict = slvFile["remain"]
    day_dict = slvFile["day"]
    month_dict = slvFile["month"]
    frequency_dict = slvFile["frequency"]
    

class MyWindow(wx.Frame):
    def __init__(self, parent, name):
        wx.Frame.__init__(self, parent, title=name, size=(360, 480))
        # self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        # A Status Bar
        self.CreateStatusBar()
        # A menu
        file_menu = wx.Menu()
        menu_about = file_menu.Append(wx.ID_ABOUT, "1.    Info", "对软件的简单介绍")
        file_menu.AppendSeparator()  # Add A Separate Line
        menu_exit = file_menu.Append(wx.ID_EXIT, "2.    Exit", "退出软件（不推荐）")
        # A menu bar
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "Click Here To Start :")
        self.SetMenuBar(menu_bar)
        # Event Handling
        self.Bind(wx.EVT_MENU, self.about_clicked, menu_about)
        self.Bind(wx.EVT_MENU, self.exit_clicked, menu_exit)
        # Show
        self.Show()

    def about_clicked(self, evt):
        # First we create and fill the info object
        info = wx.adv.AboutDialogInfo()
        info.Name = "小圆的实习小助手"
        info.Version = "15.5.3"
        info.Copyright = "(c) 2015.05.03 - For Ever.   无法无天公司出品\n"
        info.Description = "希望这个小东西能帮老婆找到心仪的实习机会。\n\n" \
                           "亲爱的小圆：\n" \
                           "你只需要填选自己对实习的要求和关键词，\n" \
                           "就可以让这个小程序在后台自动运转了，\n" \
                           "然后它就会以你指定的频次检测实习更新，\n" \
                           "并给你的邮箱发送相关内容的邮件。\n\n" \
                           "Best Wishes  &  Forever Love."

        info.Developers = ["大英雄和清", "Hutchin."]
        # Then we call wx.AboutBox giving it that info object
        wx.adv.AboutBox(info)

    def exit_clicked(self, evt):
        sys.exit()


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Create A Grid Sizer
        grid = wx.GridBagSizer(hgap=20, vgap=10)  # rowNum=8, colNum=2, verticalGap=5, HorizontalGap=5

        # A Save Button
        self.saveButton = wx.Button(self, label="确认信息，开始发送邮件", size=(150, 22))
        self.Bind(wx.EVT_BUTTON, self.click_save, self.saveButton)
        grid.Add(self.saveButton, (11, 2))

        # 2 Input Text Field

        # (a) Key Word Input
        self.key = "请在此处输入一个关键词"
        self.word_1 = wx.StaticText(self, label="实习类别或公司名称:")
        self.input_1 = wx.TextCtrl(self, value="请在此处输入一个关键词", size=(150, 22))
        self.Bind(wx.EVT_TEXT, self.text_event_1, self.input_1)
        grid.Add(self.word_1, (1, 1))
        grid.Add(self.input_1, (1, 2))

        # (b) E-mail Address Input
        self.mail = "18017531553@163.com"
        self.word_2 = wx.StaticText(self, label="请输入常用邮箱地址:")
        self.input_2 = wx.TextCtrl(self, value="18017531553@163.com", size=(150, 22))
        self.Bind(wx.EVT_TEXT, self.text_event_2, self.input_2)
        grid.Add(self.word_2, (9, 1))
        grid.Add(self.input_2, (9, 2))

        # 7 combobox Controls

        # No.1 - City (Place)
        self.city = None
        self.label_1 = wx.StaticText(self, label="请选择您的实习地点：")
        self.lst_1 = ['全国', '北京', '上海', '深圳', '广州', '天津', '成都', '重庆', '杭州', '南京', '青岛', '苏州', '沈阳', '武汉', '西安', '香港', '厦门']
        self.box_1 = wx.ComboBox(self, size=(150, 22), choices=self.lst_1, style=wx.CB_READONLY)
        grid.Add(self.label_1, (2, 1))
        grid.Add(self.box_1, (2, 2))
        self.Bind(wx.EVT_COMBOBOX, self.combox_event_1, self.box_1)

        # No.2 - Day
        self.day = None
        self.label_2 = wx.StaticText(self, label="请选择每周实习天数：")
        self.lst_2 = ['任意', '1天', '2天', '3天', '4天', '5天']
        self.box_2 = wx.ComboBox(self, size=(150, 22), choices=self.lst_2, style=wx.CB_READONLY)
        grid.Add(self.label_2, (3, 1))
        grid.Add(self.box_2, (3, 2))
        self.Bind(wx.EVT_COMBOBOX, self.combox_event_2, self.box_2)

        # No.3 - Month
        self.month = None
        self.label_3 = wx.StaticText(self, label="请选择连续实习月数：")
        self.lst_3 = ['任意', '1个月', '2个月', '3个月', '4个月', '5个月', '6个月', '8个月', '10个月', '12个月']
        self.box_3 = wx.ComboBox(self, size=(150, 22), choices=self.lst_3, style=wx.CB_READONLY)
        grid.Add(self.label_3, (4, 1))
        grid.Add(self.box_3, (4, 2))
        self.Bind(wx.EVT_COMBOBOX, self.combox_event_3, self.box_3)

        # No.4 - salary
        self.salary = None
        self.label_4 = wx.StaticText(self, label="请选择每日工资要求：")
        self.lst_4 = ['任意', '50元以下', '50-100元', '100-150元', '150-200元', '200-300元', '300元以上']
        self.box_4 = wx.ComboBox(self, size=(150, 22), choices=self.lst_4, style=wx.CB_READONLY)
        grid.Add(self.label_4, (5, 1))
        grid.Add(self.box_4, (5, 2))
        self.Bind(wx.EVT_COMBOBOX, self.combox_event_4, self.box_4)

        # No.5 - degree
        self.degree = None
        self.label_5 = wx.StaticText(self, label="请选择最低学历要求：")
        self.lst_5 = ['任意', '大专', '本科', '硕士', '博士']
        self.box_5 = wx.ComboBox(self, size=(150, 22), choices=self.lst_5, style=wx.CB_READONLY)
        grid.Add(self.label_5, (6, 1))
        grid.Add(self.box_5, (6, 2))
        self.Bind(wx.EVT_COMBOBOX, self.combox_event_5, self.box_5)

        # No.6 - remain
        self.remain = None
        self.label_6 = wx.StaticText(self, label="请选择是否要求留用：")
        self.lst_6 = ['任意', '可以留用', '不能留用', '可能留用']
        self.box_6 = wx.ComboBox(self, size=(150, 22), choices=self.lst_6, style=wx.CB_READONLY)
        grid.Add(self.label_6, (7, 1))
        grid.Add(self.box_6, (7, 2))
        self.Bind(wx.EVT_COMBOBOX, self.combox_event_6, self.box_6)

        # No.7 - frequency
        self.frequency = None
        self.frequency_word = "每天提醒一次"
        self.label_7 = wx.StaticText(self, label="请选择邮件告知频次：")
        self.lst_7 = ['每天提醒一次', '每3天提醒一次', '每周提醒一次']
        self.box_7 = wx.ComboBox(self, size=(150, 22), choices=self.lst_7, style=wx.CB_READONLY)
        grid.Add(self.label_7, (8, 1))
        grid.Add(self.box_7, (8, 2))
        self.Bind(wx.EVT_COMBOBOX, self.combox_event_7, self.box_7)

        # set sizer
        self.SetSizerAndFit(grid)
    
    # No.1 city
    def combox_event_1(self, event):
        self.city = city_dict[str(event.GetString())]

    # No.2 day
    def combox_event_2(self, event):
        self.day = day_dict[str(event.GetInt())]
        # GetInt() returns the number of the choice by order, starting from 0.

    # No.3 month
    def combox_event_3(self, event):
        self.month = month_dict[str(event.GetInt())]
    
    # No.4 salary
    def combox_event_4(self, event):
        self.salary = salary_dict[str(event.GetInt())]

    # No.5 degree 
    def combox_event_5(self, event):
        self.degree = degree_dict[str(event.GetInt())]

    # No.6 remain
    def combox_event_6(self, event):
        self.remain = remain_dict[str(event.GetInt())]
    
    # No.7 frequency
    def combox_event_7(self, event):
        self.frequency = frequency_dict[str(event.GetInt())]
        self.frequency_word = event.GetString()
    
    # textBox No.1 keyword 
    def text_event_1(self, event):
        self.key = event.GetString()

    # textBox No.2 mail
    def text_event_2(self, event):
        self.mail = event.GetString()

    def click_save(self, event):
        # print(self.city, self.day, self.month, self.salary, self.degree, self.remain, self.frequency)
        # print(self.key, self.mail)
        dlg = wx.MessageDialog(self, '第一封邮件即将发送！\n\n第一封邮件的内容将包括符合您要求的所有实习链接。\n\n今后，将会以{}的频率给您推送新增加的实习链接。'.format(self.frequency_word),
                               '请您再次确认邮件地址：{}'.format(self.mail),
                               style=wx.OK | wx.CANCEL
                               )
        if dlg.ShowModal() == wx.ID_OK:  # "OK" is clicked.
            return_flag = send_intern_mail(keyword=self.key, place=self.city, day=self.day, month=self.month, salary=self.salary, degree=self.degree, remain=self.remain, from_nick="大英雄", from_name="pku_hhq@163.com", from_code="kobe24", to_nick="Fighting!", to_name="pku_hhq@163.com")
            if return_flag:  # The e-mail has been sent successfully.
                dlg_true = wx.MessageDialog(self, '第一封邮件已经发送成功！还请您稍后查收。', 'Yeah!!!', style=wx.OK)
                dlg_true.ShowModal()
                dlg_true.Destroy()
                dlg.Destroy()  # Turn the dialogue off before looping to send emails every week or every several days.

                while True:  # Send emails by certain frequency.
                    time.sleep(seconds_per_day * self.frequency)  # One day has 86400 seconds.
                    new_flag = send_intern_mail(keyword=self.key, place=self.city, day=self.day, month=self.month, salary=self.salary, degree=self.degree, remain=self.remain, from_nick="大英雄", from_name="pku_hhq@163.com", from_code="kobe24", to_nick="Fighting!", to_name="pku_hhq@163.com")
                    if not new_flag:  # The email has not been sent successfully.
                        dlg_false = wx.MessageDialog(self, '非常抱歉，邮件发送失败了！您可以尝试再次点击发送按钮重新发送，或联络开发者：pku_hhq@163.com。', 'Oops!!!', style=wx.OK)
                        dlg_false.ShowModal()
                        dlg_false.Destroy()
                        break
            else:
                dlg_false = wx.MessageDialog(self, '非常抱歉，第一封邮件发送失败！您可以尝试重新发送或者联络开发者：pku_hhq@163.com。', 'Oops!!!', style=wx.OK)
                dlg_false.ShowModal()
                dlg_false.Destroy()
        dlg.Destroy()

    
if __name__ == '__main__':
    app = wx.App()
    window = MyWindow(None, "小圆的实习小助手^_^")
    frame = MyPanel(window)
    window.Show(True)
    app.MainLoop()
