import wx
import controller
import wx.lib.masked as masked
from datetime import datetime
import wx.propgrid as wxpg


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
            site = location = skeleton = observer = ""
            obs_date = datetime.today().strftime('%Y-%m-%d')

        # GUI project
        #panel = wx.Panel(self)
        #fgs = wx.FlexGridSizer(5, 2, 10, 25)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        size = (100, -1)
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        # Site
        site_lbl = wx.StaticText(self, label="Site:", size=size)
        site_lbl.SetFont(font)
        self.site_txt = wx.TextCtrl(
            self, value=site, style=wx.TE_PROCESS_ENTER, size=(300, -1))
        self.site_txt.SetMaxLength(50)
        self.site_txt.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        main_sizer.Add(self.row_builder(
            [site_lbl, self.site_txt]), 0, wx.ALL)

        # Location
        location_lbl = wx.StaticText(self, label="Location:", size=size)
        location_lbl.SetFont(font)
        self.location_txt = wx.TextCtrl(
            self, value=location, style=wx.TE_PROCESS_ENTER, size=(300, -1))
        self.location_txt.SetMaxLength(50)
        self.location_txt.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        main_sizer.Add(self.row_builder(
            [location_lbl, self.location_txt]), 0, wx.ALL)

        # Skeleton
        skeleton_lbl = wx.StaticText(self, label="Skeleton:", size=size)
        skeleton_lbl.SetFont(font)
        self.skeleton_txt = wx.TextCtrl(
            self, value=skeleton, style=wx.TE_PROCESS_ENTER, size=(300, -1))
        self.skeleton_txt.SetMaxLength(50)
        self.skeleton_txt.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        main_sizer.Add(self.row_builder(
            [skeleton_lbl, self.skeleton_txt]), 0, wx.ALL)

        # Observer
        observer_lbl = wx.StaticText(self, label="Observer:", size=size)
        observer_lbl.SetFont(font)
        self.observer_txt = wx.TextCtrl(
            self, value=observer, style=wx.TE_PROCESS_ENTER, size=(300, -1))
        self.observer_txt.SetMaxLength(50)
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
        self.obs_date_txt.SetMaxLength(10)
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

        self.skeleton_id = controller.add_record(
            self.session, self.skeleton_dict)
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


class PreservationDialog(wx.Dialog):
    """
    dialog for edit state of preservation
    """

    def __init__(self, session, row, title="State of preservation"):
        """
        Constructor
        """

        super().__init__(None, title="{}: {}".format(title, row.skeleton))
        self.selected_row = row
        self.session = session
        self.result = 0
        self.skeleton_id = row.skeleton_id
        skeleton_dict = {}

        rekord = controller.find_skeleton(self.session, self.skeleton_id)
        data = {}
        data['frontal'] = rekord.frontal if rekord.frontal != None else 0
        data['sphenoid'] = rekord.sphenoid if rekord.sphenoid != None else 0
        data['mandible'] = rekord.mandible if rekord.mandible != None else 0
        data['ethmoid'] = rekord.ethmoid if rekord.ethmoid != None else 0
        data['parietal_l'] = rekord.parietal_l if rekord.parietal_l != None else 0
        data['parietal_r'] = rekord.parietal_r if rekord.parietal_r != None else 0
        data['nasal_l'] = rekord.nasal_l if rekord.nasal_l != None else 0
        data['nasal_r'] = rekord.nasal_r if rekord.nasal_r != None else 0
        data['palatine_l'] = rekord.palatine_l if rekord.palatine_l != None else 0
        data['palatine_r'] = rekord.palatine_r if rekord.palatine_r != None else 0
        data['thyroid'] = rekord.thyroid if rekord.thyroid != None else 0
        data['occipital'] = rekord.occipital if rekord.occipital != None else 0
        data['maxilla_l'] = rekord.maxilla_l if rekord.maxilla_l != None else 0
        data['maxilla_r'] = rekord.maxilla_r if rekord.maxilla_r != None else 0
        data['lacrimal_l'] = rekord.lacrimal_l if rekord.lacrimal_l != None else 0
        data['lacrimal_r'] = rekord.lacrimal_r if rekord.lacrimal_r != None else 0
        data['hyoid'] = rekord.hyoid if rekord.hyoid != None else 0
        data['temporal_l'] = rekord.temporal_l if rekord.temporal_l != None else 0
        data['temporal_r'] = rekord.temporal_r if rekord.temporal_r != None else 0
        data['zygomatic_l'] = rekord.zygomatic_l if rekord.zygomatic_l != None else 0
        data['zygomatic_r'] = rekord.zygomatic_r if rekord.zygomatic_r != None else 0
        data['orbit_l'] = rekord.orbit_l if rekord.orbit_l != None else 0
        data['orbit_r'] = rekord.orbit_r if rekord.orbit_r != None else 0
        data['calotte'] = rekord.calotte if rekord.calotte != None else 0

        data['ilium_l'] = rekord.ilium_l if rekord.ilium_l != None else 0
        data['ilium_r'] = rekord.ilium_r if rekord.ilium_r != None else 0

        # GUI project
        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)

        self.pg = pg = wxpg.PropertyGrid(panel)

        # Add properties
        pg.Append(wxpg.PropertyCategory("Skull inventory"))
        #pg.Append( wxpg.StringProperty("String",value="") )
        pg.Append(wxpg.IntProperty("Frontal", value=data['frontal']))
        pg.Append(wxpg.IntProperty("Sphenoid", value=data['sphenoid']))
        pg.Append(wxpg.IntProperty("Mandible", value=data['mandible']))
        pg.Append(wxpg.IntProperty("Parietal left", value=data['parietal_l']))
        pg.Append(wxpg.IntProperty("Parietal right", value=data['parietal_r']))
        pg.Append(wxpg.IntProperty("Nasal left", value=data['nasal_l']))
        pg.Append(wxpg.IntProperty("Nasal right", value=data['nasal_r']))
        pg.Append(wxpg.IntProperty("Palatine left", value=data['palatine_l']))
        pg.Append(wxpg.IntProperty("Palatine right", value=data['palatine_r']))
        pg.Append(wxpg.IntProperty("Occipital", value=data['occipital']))
        pg.Append(wxpg.IntProperty("Maxilla left", value=data['maxilla_l']))
        pg.Append(wxpg.IntProperty("Maxilla right", value=data['maxilla_r']))
        pg.Append(wxpg.IntProperty("Lacrimal left", value=data['lacrimal_l']))
        pg.Append(wxpg.IntProperty("Lacrimal right", value=data['lacrimal_r']))
        pg.Append(wxpg.IntProperty("Temporal left", value=data['temporal_l']))
        pg.Append(wxpg.IntProperty("Temporal right", value=data['temporal_r']))
        pg.Append(wxpg.IntProperty("Zygomatic left", value=data['zygomatic_l']))
        pg.Append(wxpg.IntProperty("Zygomatic right", value=data['zygomatic_r']))
        pg.Append(wxpg.IntProperty("Orbit left", value=data['orbit_l']))
        pg.Append(wxpg.IntProperty("Orbit right", value=data['orbit_r']))
        pg.Append(wxpg.IntProperty("Ethmoid", value=data['ethmoid']))
        pg.Append(wxpg.IntProperty("Thyroid", value=data['thyroid']))
        pg.Append(wxpg.IntProperty("Hyoid", value=data['hyoid']))
        pg.Append(wxpg.IntProperty("Calotte", value=data['calotte']))

        pg.Append(wxpg.PropertyCategory("Post-cranial skeleton inventory"))
        pg.Append(wxpg.IntProperty("Ilium left", value=data['ilium_l']))
        pg.Append(wxpg.IntProperty("Ilium right", value=data['ilium_r']))

        # Long bones
        # Vertebrae
        # Ribs
        # Phalanges
        #Carpals - tarsals

        topsizer.Add(pg, 1, wx.EXPAND)

        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, -1, "Save")
        btn_ok.Bind(wx.EVT_BUTTON, self.on_save_preservation)
        rowsizer.Add(btn_ok, 1)
        btn_cancel = wx.Button(panel, -1, "Cancel")
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel_preservation)
        rowsizer.Add(btn_cancel, 1)
        topsizer.Add(rowsizer, 0, wx.EXPAND)

        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def on_save_preservation(self, event):
        self.skeleton_dict = self.get_preservation_data()
        # controller.edit_preservation(
        #    self.session, self.selected_row.skeleton_id, self.skeleton_dict)
        self.Close()

    def on_cancel_preservation(self, event):
        self.EndModal(wx.ID_CANCEL)

    def get_preservation_data(self):
        d = self.pg.GetPropertyValues(inc_attributes=True)
        print(d)
        return d


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
