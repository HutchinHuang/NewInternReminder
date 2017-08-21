# -*- coding:utf-8 -*-
# This version is used for GUI main function.
import wx
from easy_GUI import MyWindow, MyPanel

# Open GUI
app = wx.App()
window = MyWindow(None, "小圆的实习小助手^_^")
frame = MyPanel(window)
window.Show(True)
app.MainLoop()

'''
# Now We Check The Inputs.
results = get_sxs(place=city, keyword=keyword, day=day, month=month, salary=salary, degree=degree, remain=remain)
print(results)
'''