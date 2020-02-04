import wx
import controller
import wx.lib.masked as masked


class RecordDialog(wx.Dialog):
    """
    dialog for edit and add record
    """

    def __init__(self, session, row=None, title="Add", addRecord=True):
        """
        Constructor
        """

        super().__init__(None, title="%s Record" % title)
        self.addRecord = addRecord
        self.selected_row = row
        self.session = session
        self.result = 0
        self.skeleton_id = None
        self.skeleton_dict = {}

        if row:
            site = self.selected_row.site
            location = self.selected_row.location
            skeleton = self.selected_row.skeleton
            observer = self.selected_row.observer
            obs_date = self.selected_row.obs_date
        else:
            site = location = skeleton = observer = obs_date = ""

        # GUI project
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        size = (100, -1)
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        # Site
        site_lbl = wx.StaticText(self, label="Site:", size=size)
        site_lbl.SetFont(font)
        self.site_txt = wx.TextCtrl(self, value=site, style=wx.TE_PROCESS_ENTER)
        self.site_txt.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        main_sizer.Add(self.row_builder(
            [site_lbl, self.site_txt]), 0, wx.ALL)

        # Location
        location_lbl = wx.StaticText(self, label="Location:", size=size)
        location_lbl.SetFont(font)
        self.location_txt = wx.TextCtrl(self, value=location, style=wx.TE_PROCESS_ENTER)
        self.location_txt.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        main_sizer.Add(self.row_builder(
            [location_lbl, self.location_txt]), 0, wx.ALL)

        # Skeleton
        skeleton_lbl = wx.StaticText(self, label="Skeleton:", size=size)
        skeleton_lbl.SetFont(font)
        self.skeleton_txt = wx.TextCtrl(self, value=skeleton, style=wx.TE_PROCESS_ENTER)
        self.skeleton_txt.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        main_sizer.Add(self.row_builder(
            [skeleton_lbl, self.skeleton_txt]), 0, wx.ALL)

        # Observer
        observer_lbl = wx.StaticText(self, label="Observer:", size=size)
        observer_lbl.SetFont(font)
        self.observer_txt = wx.TextCtrl(self, value=observer, style=wx.TE_PROCESS_ENTER)
        self.observer_txt.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        main_sizer.Add(self.row_builder(
            [observer_lbl, self.observer_txt]), 0, wx.ALL)

        # Observation date
        obs_date_lbl = wx.StaticText(
            self, label="Date:", size=size)
        obs_date_lbl.SetFont(font)
        #self.obs_date_txt = wx.TextCtrl(self, value=obs_date, style=wx.TE_PROCESS_ENTER)
        self.obs_date_txt = masked.TextCtrl(self, -1, "",
                                            mask="####-##-##",
                                            defaultValue=obs_date,
                                            validRequired=False,
                                            style=wx.TE_PROCESS_ENTER)
        self.obs_date_txt.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        main_sizer.Add(self.row_builder(
            [obs_date_lbl, self.obs_date_txt]), 0, wx.ALL)

        # buttons
        ok_btn = wx.Button(self, label="%s skeleton" % title)
        ok_btn.Bind(wx.EVT_BUTTON, self.on_record)
        btn_sizer.Add(ok_btn, 0, wx.ALL, 5)

        cancel_btn = wx.Button(self, wx.ID_CANCEL, "Cancel")
        cancel_btn.Bind(wx.EVT_BUTTON, self.on_close)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)
        main_sizer.Add(btn_sizer, 0, wx.CENTER)

        self.SetSizerAndFit(main_sizer)

    def onEnter(self, event):
        """ go to next crtl """
        event.EventObject.Navigate()

    def get_data(self):
        """
        Gets the data from the widgets in the dialog
        Also display an error message if required fields are empty
        """
        tmp_skeleton_dict = {}
        site = self.site_txt.GetValue()
        location = self.location_txt.GetValue()
        skeleton = self.skeleton_txt.GetValue()
        observer = self.observer_txt.GetValue()
        obs_date = self.obs_date_txt.GetValue()

        if site == "" or skeleton == "":
            show_message("Site and Skeleton are required!", "Error")
            return None

        tmp_skeleton_dict["site"] = site
        tmp_skeleton_dict["location"] = location
        tmp_skeleton_dict["skeleton"] = skeleton
        tmp_skeleton_dict["observer"] = observer
        tmp_skeleton_dict["obs_date"] = obs_date

        return tmp_skeleton_dict

    def on_add(self):
        """
        Add the record to the database
        """

        self.skeleton_dict = self.get_data()
        if self.skeleton_dict is None:
            return

        self.skeleton_id = controller.add_record(self.session, self.skeleton_dict)
        self.result = 1
        self.Close()

    def on_close(self, event):
        """
        Close the dialog
        """
        self.EndModal(wx.ID_CANCEL)

    def on_edit(self):
        """
        Edit a record in the database
        """
        self.skeleton_dict = self.get_data()
        controller.edit_record(
            self.session, self.selected_row.skeleton_id, self.skeleton_dict)
        self.selected_row.site = self.skeleton_dict['site']
        self.selected_row.location = self.skeleton_dict['location']
        self.selected_row.skeleton = self.skeleton_dict['skeleton']
        self.selected_row.observer = self.skeleton_dict['observer']
        self.selected_row.obs_date = self.skeleton_dict['obs_date']
        # show_message("Skeleton edited successfully!",
        #             "Success", wx.ICON_INFORMATION)
        self.Close()

    def on_record(self, event):
        """
        Add or edit a record
        """
        if self.addRecord:
            self.on_add()
        else:
            self.on_edit()

    def row_builder(self, widgets):
        """
        Helper function for building a row of widgets
        """
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl, txt = widgets
        sizer.Add(lbl, 0, wx.ALL, 5)
        sizer.Add(txt, 1, wx.ALL, 5)
        return sizer


def show_message(message, caption, flag=wx.ICON_ERROR):
    """
    Show a message dialog
    """
    msg = wx.MessageDialog(None, message=message,
                           caption=caption, style=flag)
    msg.ShowModal()
    msg.Destroy()


def ask_message(message, caption):
    """
    Ask a question message
    """
    msg = wx.MessageDialog(None, message=message, caption=caption,
                           style=wx.YES_NO | wx.NO_DEFAULT)
    if msg.ShowModal() == wx.ID_YES:
        return True
    else:
        return False
