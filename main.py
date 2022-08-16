import wx
import wx.xrc
import wx.html


class TestWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(210, 262), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_checkBox1 = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_checkBox1, 0, wx.ALL, 5)

        self.m_checkBox2 = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_checkBox2, 0, wx.ALL, 5)

        self.m_checkBox3 = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_checkBox3, 0, wx.ALL, 5)

        self.m_checkBox4 = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_checkBox4, 0, wx.ALL, 5)

        self.m_checkBox5 = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_checkBox5, 0, wx.ALL, 5)

        self.m_htmlWin1 = wx.html.HtmlWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                             wx.html.HW_SCROLLBAR_AUTO)
        bSizer1.Add(self.m_htmlWin1, 0, wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"MyButton", wx.Point(-1, -1), wx.DefaultSize, 0)

        self.m_button1.SetBitmapPosition(wx.BOTTOM)
        bSizer1.Add(self.m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
        super().__init__(
            None,
            title="My First App",
            size=wx.Size(350, 500)
        )


class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(210, 262), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_checkBox1 = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_checkBox1, 0, wx.ALL, 5)

        self.m_checkBox2 = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_checkBox2, 0, wx.ALL, 5)

        self.m_checkBox3 = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_checkBox3, 0, wx.ALL, 5)

        self.m_checkBox4 = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_checkBox4, 0, wx.ALL, 5)

        self.m_checkBox5 = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_checkBox5, 0, wx.ALL, 5)

        self.m_htmlWin1 = wx.html.HtmlWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                             wx.html.HW_SCROLLBAR_AUTO)
        bSizer1.Add(self.m_htmlWin1, 0, wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"MyButton", wx.Point(-1, -1), wx.DefaultSize, 0)

        self.m_button1.SetBitmapPosition(wx.BOTTOM)
        bSizer1.Add(self.m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass


if __name__ == '__main__':
    app = wx.App()
    window = TestWindow(MyFrame1)
    #window1 =
    window.Show()
    #window1.Show()
    app.MainLoop()
