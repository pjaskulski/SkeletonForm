import wx
import controller
import wx.lib.masked as masked
from datetime import datetime
import wx.propgrid as wxpg
from model import Skeleton


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
        # panel = wx.Panel(self)
        # fgs = wx.FlexGridSizer(5, 2, 10, 25)

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

        self.obs_date_txt = masked.TextCtrl(self, -1, "",
                                            mask="####-##-##",
                                            defaultValue=obs_date,
                                            validRequired=False,
                                            size=(200, -1),
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


class IntProperty2(wxpg.PGProperty):
    """\
    This is a simple re-implementation of wxIntProperty.
    """

    def __init__(self, label, name=wxpg.PG_LABEL, value=-1):
        wxpg.PGProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        """\
        This is not 100% necessary and in future is probably going to be
        automated to return class name.
        """
        return "IntProperty2"

    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrl")

    def ValueToString(self, value, flags):
        return str(value)

    def StringToValue(self, s, flags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        try:
            v = int(s)
            if self.GetValue() != v:
                return (True, v)
        except (ValueError, TypeError):
            if flags & wxpg.PG_REPORT_ERROR:
                wx.MessageBox("Cannot convert '%s' into a number." % s, "Error")
        return (False, None)

    def IntToValue(self, v, flags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        if (self.GetValue() != v):
            return (True, v)

        return (False, None)

    def ValidateValue(self, value, validationInfo):
        """ Let's limit the value to range -1 and 4.
        """
        # Just test this function to make sure validationInfo and
        # wxPGVFBFlags work properly.
        oldvfb__ = validationInfo.GetFailureBehavior()

        # Mark the cell if validation failed
        # validationInfo.SetFailureBehavior(wxpg.PG_VFB_MARK_CELL)

        if value == None or value < -1 or value > 1000:
            return False

        return True


class PreservationDialog(wx.Dialog):
    """
    dialog for edit state of preservation
    """

    def my_enum_prep(self, name, value=-1):
        return wxpg.EnumProperty(name, name,
                                 ['-1 -Not determined',
                                  '0  - None',
                                  '1  - up to 25%',
                                  '2  - up to 50%',
                                  '3  - up to 75%',
                                  '4  - up to 100%'],
                                 [-1, 0, 1, 2, 3, 4],
                                 value)

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
        data = rekord.__dict__

        data['vertebrae_remarks'] = rekord.vertebrae_remarks if rekord.vertebrae_remarks != None else ''
        for k, v in data.items():
            if v is None:
                data[k] = -1

        # GUI project
        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)

        self.pg = pg = wxpg.PropertyGrid(panel, style=wxpg.PG_SPLITTER_AUTO_CENTER)

        # SetPropertyValidator

        # Bg Colour for 0 column
        bgcCell = wx.Colour(219, 233, 255)

        # Add properties
        # Skull
        pg.Append(wxpg.PropertyCategory("Skull inventory"))

        pg.Append(self.my_enum_prep("Frontal", value=data['frontal']))
        pg.SetPropertyCell("Frontal", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Sphenoid", value=data['sphenoid']))
        pg.SetPropertyCell("Sphenoid", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Mandible", value=data['mandible']))
        pg.SetPropertyCell("Mandible", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Parietal left", value=data['parietal_l']))
        pg.SetPropertyCell("Parietal left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Parietal right", value=data['parietal_r']))
        pg.SetPropertyCell("Parietal right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Nasal left", value=data['nasal_l']))
        pg.SetPropertyCell("Nasal left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Nasal right", value=data['nasal_r']))
        pg.SetPropertyCell("Nasal right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Palatine left", value=data['palatine_l']))
        pg.SetPropertyCell("Palatine left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Palatine right", value=data['palatine_r']))
        pg.SetPropertyCell("Palatine right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Occipital", value=data['occipital']))
        pg.SetPropertyCell("Occipital", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Maxilla left", value=data['maxilla_l']))
        pg.SetPropertyCell("Maxilla left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Maxilla right", value=data['maxilla_r']))
        pg.SetPropertyCell("Maxilla right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Lacrimal left", value=data['lacrimal_l']))
        pg.SetPropertyCell("Lacrimal left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Lacrimal right", value=data['lacrimal_r']))
        pg.SetPropertyCell("Lacrimal right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Temporal left", value=data['temporal_l']))
        pg.SetPropertyCell("Temporal left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Temporal right", value=data['temporal_r']))
        pg.SetPropertyCell("Temporal right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Zygomatic left", value=data['zygomatic_l']))
        pg.SetPropertyCell("Zygomatic left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Zygomatic right", value=data['zygomatic_r']))
        pg.SetPropertyCell("Zygomatic right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Orbit left", value=data['orbit_l']))
        pg.SetPropertyCell("Orbit left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Orbit right", value=data['orbit_r']))
        pg.SetPropertyCell("Orbit right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ethmoid", value=data['ethmoid']))
        pg.SetPropertyCell("Ethmoid", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Thyroid", value=data['thyroid']))
        pg.SetPropertyCell("Thyroid", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Hyoid", value=data['hyoid']))
        pg.SetPropertyCell("Hyoid", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Calotte", value=data['calotte']))
        pg.SetPropertyCell("Calotte", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        # Post-cranial skeleton
        pg.Append(wxpg.PropertyCategory("Post-cranial skeleton inventory"))

        pg.Append(self.my_enum_prep("Ilium left", value=data['ilium_l']))
        pg.SetPropertyCell("Ilium left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ilium right", value=data['ilium_r']))
        pg.SetPropertyCell("Ilium right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Scapula left", value=data['scapula_l']))
        pg.SetPropertyCell("Scapula left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Scapula right", value=data['scapula_r']))
        pg.SetPropertyCell("Scapula right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Manubrium", value=data['manubrium']))
        pg.SetPropertyCell("Manubrium", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ischium left", value=data['ischium_l']))
        pg.SetPropertyCell("Ischium left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ischium right", value=data['ischium_r']))
        pg.SetPropertyCell("Ischium right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Patella left", value=data['patella_l']))
        pg.SetPropertyCell("Patella left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Patella right", value=data['patella_r']))
        pg.SetPropertyCell("Patella right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("C sterni", value=data['c_sterni']))
        pg.SetPropertyCell("C sterni", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Pubic left", value=data['pubic_l']))
        pg.SetPropertyCell("Pubic left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Pubic right", value=data['pubic_r']))
        pg.SetPropertyCell("Pubic right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("X process", value=data['x_process']))
        pg.SetPropertyCell("X process", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Sacrum", value=data['sacrum']))
        pg.SetPropertyCell("Sacrum", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Coccyx", value=data['coccyx']))
        pg.SetPropertyCell("Coccyx", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        # Long bones
        pg.Append(wxpg.PropertyCategory("Long bones"))

        pg.Append(self.my_enum_prep("Clavicle left D js", value=data['clavicle_l_djs']))
        pg.SetPropertyCell("Clavicle left D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Clavicle left D 1/3", value=data['clavicle_l_d13']))
        pg.SetPropertyCell("Clavicle left D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Clavicle left M 1/3", value=data['clavicle_l_m13']))
        pg.SetPropertyCell("Clavicle left M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Clavicle left P 1/3", value=data['clavicle_l_p13']))
        pg.SetPropertyCell("Clavicle left P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Clavicle left P js", value=data['clavicle_l_pjs']))
        pg.SetPropertyCell("Clavicle left P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Clavicle right D js", value=data['clavicle_r_djs']))
        pg.SetPropertyCell("Clavicle right D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Clavicle right D 1/3", value=data['clavicle_r_d13']))
        pg.SetPropertyCell("Clavicle right D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Clavicle right M 1/3", value=data['clavicle_r_m13']))
        pg.SetPropertyCell("Clavicle right M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Clavicle right P 1/3", value=data['clavicle_r_p13']))
        pg.SetPropertyCell("Clavicle right P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Clavicle right P js", value=data['clavicle_r_pjs']))
        pg.SetPropertyCell("Clavicle right P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Humerus left D js", value=data['humerus_l_djs']))
        pg.SetPropertyCell("Humerus left D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Humerus left D 1/3", value=data['humerus_l_d13']))
        pg.SetPropertyCell("Humerus left D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Humerus left M 1/3", value=data['humerus_l_m13']))
        pg.SetPropertyCell("Humerus left M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Humerus left P 1/3", value=data['humerus_l_p13']))
        pg.SetPropertyCell("Humerus left P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Humerus left P js", value=data['humerus_l_pjs']))
        pg.SetPropertyCell("Humerus left P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Humerus right D js", value=data['humerus_r_djs']))
        pg.SetPropertyCell("Humerus right D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Humerus right D 1/3", value=data['humerus_r_d13']))
        pg.SetPropertyCell("Humerus right D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Humerus right M 1/3", value=data['humerus_r_m13']))
        pg.SetPropertyCell("Humerus right M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Humerus right P 1/3", value=data['humerus_r_p13']))
        pg.SetPropertyCell("Humerus right P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Humerus right P js", value=data['humerus_r_pjs']))
        pg.SetPropertyCell("Humerus right P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Radius left D js", value=data['radius_l_djs']))
        pg.SetPropertyCell("Radius left D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Radius left D 1/3", value=data['radius_l_d13']))
        pg.SetPropertyCell("Radius left D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Radius left M 1/3", value=data['radius_l_m13']))
        pg.SetPropertyCell("Radius left M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Radius left P 1/3", value=data['radius_l_p13']))
        pg.SetPropertyCell("Radius left P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Radius left P js", value=data['radius_l_pjs']))
        pg.SetPropertyCell("Radius left P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Radius right D js", value=data['radius_r_djs']))
        pg.SetPropertyCell("Radius right D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Radius right D 1/3", value=data['radius_r_d13']))
        pg.SetPropertyCell("Radius right D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Radius right M 1/3", value=data['radius_r_m13']))
        pg.SetPropertyCell("Radius right M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Radius right P 1/3", value=data['radius_r_p13']))
        pg.SetPropertyCell("Radius right P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Radius right P js", value=data['radius_r_pjs']))
        pg.SetPropertyCell("Radius right P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ulna left D js", value=data['ulna_l_djs']))
        pg.SetPropertyCell("Ulna left D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ulna left D 1/3", value=data['ulna_l_d13']))
        pg.SetPropertyCell("Ulna left D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ulna left M 1/3", value=data['ulna_l_m13']))
        pg.SetPropertyCell("Ulna left M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ulna left P 1/3", value=data['ulna_l_p13']))
        pg.SetPropertyCell("Ulna left P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ulna left P js", value=data['ulna_l_pjs']))
        pg.SetPropertyCell("Ulna left P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ulna right D js", value=data['ulna_r_djs']))
        pg.SetPropertyCell("Ulna right D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ulna right D 1/3", value=data['ulna_r_d13']))
        pg.SetPropertyCell("Ulna right D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ulna right M 1/3", value=data['ulna_r_m13']))
        pg.SetPropertyCell("Ulna right M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ulna right P 1/3", value=data['ulna_r_p13']))
        pg.SetPropertyCell("Ulna right P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Ulna right P js", value=data['ulna_r_pjs']))
        pg.SetPropertyCell("Ulna right P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Femur left D js", value=data['femur_l_djs']))
        pg.SetPropertyCell("Femur left D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Femur left D 1/3", value=data['femur_l_d13']))
        pg.SetPropertyCell("Femur left D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Femur left M 1/3", value=data['femur_l_m13']))
        pg.SetPropertyCell("Femur left M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Femur left P 1/3", value=data['femur_l_p13']))
        pg.SetPropertyCell("Femur left P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Femur left P js", value=data['femur_l_pjs']))
        pg.SetPropertyCell("Femur left P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Femur right D js", value=data['femur_r_djs']))
        pg.SetPropertyCell("Femur right D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Femur right D 1/3", value=data['femur_r_d13']))
        pg.SetPropertyCell("Femur right D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Femur right M 1/3", value=data['femur_r_m13']))
        pg.SetPropertyCell("Femur right M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Femur right P 1/3", value=data['femur_r_p13']))
        pg.SetPropertyCell("Femur right P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Femur right P js", value=data['femur_r_pjs']))
        pg.SetPropertyCell("Femur right P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Tibia left D js", value=data['tibia_l_djs']))
        pg.SetPropertyCell("Tibia left D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Tibia left D 1/3", value=data['tibia_l_d13']))
        pg.SetPropertyCell("Tibia left D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Tibia left M 1/3", value=data['tibia_l_m13']))
        pg.SetPropertyCell("Tibia left M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Tibia left P 1/3", value=data['tibia_l_p13']))
        pg.SetPropertyCell("Tibia left P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Tibia left P js", value=data['tibia_l_pjs']))
        pg.SetPropertyCell("Tibia left P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Tibia right D js", value=data['tibia_r_djs']))
        pg.SetPropertyCell("Tibia right D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Tibia right D 1/3", value=data['tibia_r_d13']))
        pg.SetPropertyCell("Tibia right D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Tibia right M 1/3", value=data['tibia_r_m13']))
        pg.SetPropertyCell("Tibia right M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Tibia right P 1/3", value=data['tibia_r_p13']))
        pg.SetPropertyCell("Tibia right P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Tibia right P js", value=data['tibia_r_pjs']))
        pg.SetPropertyCell("Tibia right P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Fibula left D js", value=data['fibula_l_djs']))
        pg.SetPropertyCell("Fibula left D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Fibula left D 1/3", value=data['fibula_l_d13']))
        pg.SetPropertyCell("Fibula left D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Fibula left M 1/3", value=data['fibula_l_m13']))
        pg.SetPropertyCell("Fibula left M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Fibula left P 1/3", value=data['fibula_l_p13']))
        pg.SetPropertyCell("Fibula left P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Fibula left P js", value=data['fibula_l_pjs']))
        pg.SetPropertyCell("Fibula left P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Fibula right D js", value=data['fibula_r_djs']))
        pg.SetPropertyCell("Fibula right D js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Fibula right D 1/3", value=data['fibula_r_d13']))
        pg.SetPropertyCell("Fibula right D 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Fibula right M 1/3", value=data['fibula_r_m13']))
        pg.SetPropertyCell("Fibula right M 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Fibula right P 1/3", value=data['fibula_r_p13']))
        pg.SetPropertyCell("Fibula right P 1/3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Fibula right P js", value=data['fibula_r_pjs']))
        pg.SetPropertyCell("Fibula right P js", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metacarpals left 1st", value=data['metacarpals_l_1']))
        pg.SetPropertyCell("Metacarpals left 1st", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metacarpals left 2nd", value=data['metacarpals_l_2']))
        pg.SetPropertyCell("Metacarpals left 2nd", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metacarpals left 3rd", value=data['metacarpals_l_3']))
        pg.SetPropertyCell("Metacarpals left 3rd", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metacarpals left 4th", value=data['metacarpals_l_4']))
        pg.SetPropertyCell("Metacarpals left 4th", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metacarpals left 5th", value=data['metacarpals_l_5']))
        pg.SetPropertyCell("Metacarpals left 5th", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metacarpals right 1st", value=data['metacarpals_r_1']))
        pg.SetPropertyCell("Metacarpals right 1st", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metacarpals right 2nd", value=data['metacarpals_r_2']))
        pg.SetPropertyCell("Metacarpals right 2nd", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metacarpals right 3rd", value=data['metacarpals_r_3']))
        pg.SetPropertyCell("Metacarpals right 3rd", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metacarpals right 4th", value=data['metacarpals_r_4']))
        pg.SetPropertyCell("Metacarpals right 4th", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metacarpals right 5th", value=data['metacarpals_r_5']))
        pg.SetPropertyCell("Metacarpals right 5th", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metatarsals left 1st", value=data['metatarsals_l_1']))
        pg.SetPropertyCell("Metatarsals left 1st", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metatarsals left 2nd", value=data['metatarsals_l_2']))
        pg.SetPropertyCell("Metatarsals left 2nd", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metatarsals left 3rd", value=data['metatarsals_l_3']))
        pg.SetPropertyCell("Metatarsals left 3rd", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metatarsals left 4th", value=data['metatarsals_l_4']))
        pg.SetPropertyCell("Metatarsals left 4th", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metatarsals left 5th", value=data['metatarsals_l_5']))
        pg.SetPropertyCell("Metatarsals left 5th", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metatarsals right 1st", value=data['metatarsals_r_1']))
        pg.SetPropertyCell("Metatarsals right 1st", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metatarsals right 2nd", value=data['metatarsals_r_2']))
        pg.SetPropertyCell("Metatarsals right 2nd", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metatarsals right 3rd", value=data['metatarsals_r_3']))
        pg.SetPropertyCell("Metatarsals right 3rd", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metatarsals right 4th", value=data['metatarsals_r_4']))
        pg.SetPropertyCell("Metatarsals right 4th", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Metatarsals right 5th", value=data['metatarsals_r_5']))
        pg.SetPropertyCell("Metatarsals right 5th", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        # Vertebrae
        pg.Append(wxpg.PropertyCategory("Vertebrae"))

        pg.Append(wxpg.IntProperty("Vertebrae C 1", value=data['vertebrae_c_1']))
        pg.SetPropertyCell("Vertebrae C 1", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae C 2", value=data['vertebrae_c_2']))
        pg.SetPropertyCell("Vertebrae C 2", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae C 3", value=data['vertebrae_c_3']))
        pg.SetPropertyCell("Vertebrae C 3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae C 4", value=data['vertebrae_c_4']))
        pg.SetPropertyCell("Vertebrae C 4", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae C 5", value=data['vertebrae_c_5']))
        pg.SetPropertyCell("Vertebrae C 5", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae T 1", value=data['vertebrae_t_1']))
        pg.SetPropertyCell("Vertebrae T 1", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae T 2", value=data['vertebrae_t_2']))
        pg.SetPropertyCell("Vertebrae T 2", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae T 3", value=data['vertebrae_t_3']))
        pg.SetPropertyCell("Vertebrae T 3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae T 4", value=data['vertebrae_t_4']))
        pg.SetPropertyCell("Vertebrae T 4", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae T 5", value=data['vertebrae_t_5']))
        pg.SetPropertyCell("Vertebrae T 5", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae L 1", value=data['vertebrae_l_1']))
        pg.SetPropertyCell("Vertebrae L 1", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae L 2", value=data['vertebrae_l_2']))
        pg.SetPropertyCell("Vertebrae L 2", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae L 3", value=data['vertebrae_l_3']))
        pg.SetPropertyCell("Vertebrae L 3", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae L 4", value=data['vertebrae_l_4']))
        pg.SetPropertyCell("Vertebrae L 4", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Vertebrae L 5", value=data['vertebrae_l_5']))
        pg.SetPropertyCell("Vertebrae L 5", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.StringProperty("Vertebrae remarks", value=data['vertebrae_remarks']))
        pg.SetPropertyCell("Vertebrae remarks", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        # Ribs
        pg.Append(wxpg.PropertyCategory("Ribs"))

        pg.Append(wxpg.IntProperty("Ribs left whole", value=data['ribs_l_whole']))
        pg.SetPropertyCell("Ribs left whole", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Ribs left S end", value=data['ribs_l_send']))
        pg.SetPropertyCell("Ribs left S end", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Ribs left V end", value=data['ribs_l_vend']))
        pg.SetPropertyCell("Ribs left V end", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Ribs left Frag.", value=data['ribs_l_frag']))
        pg.SetPropertyCell("Ribs left Frag.", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Ribs right whole", value=data['ribs_r_whole']))
        pg.SetPropertyCell("Ribs right whole", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Ribs right S end", value=data['ribs_r_send']))
        pg.SetPropertyCell("Ribs right S end", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Ribs right V end", value=data['ribs_r_vend']))
        pg.SetPropertyCell("Ribs right V end", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Ribs right Frag.", value=data['ribs_r_frag']))
        pg.SetPropertyCell("Ribs right Frag.", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Ribs unknown whole", value=data['ribs_u_whole']))
        pg.SetPropertyCell("Ribs unknown whole", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Ribs unknown S end", value=data['ribs_u_send']))
        pg.SetPropertyCell("Ribs unknown S end", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Ribs unknown V end", value=data['ribs_u_vend']))
        pg.SetPropertyCell("Ribs unknown V end", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Ribs unknown Frag.", value=data['ribs_u_frag']))
        pg.SetPropertyCell("Ribs unknown Frag.", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        # Phalanges
        pg.Append(wxpg.PropertyCategory("Phalanges"))

        pg.Append(wxpg.IntProperty("Phalanges hand proximal", value=data['phalanges_hand_p']))
        pg.SetPropertyCell("Phalanges hand proximal", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Phalanges hand medial", value=data['phalanges_hand_m']))
        pg.SetPropertyCell("Phalanges hand medial", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Phalanges hand distal", value=data['phalanges_hand_d']))
        pg.SetPropertyCell("Phalanges hand distal", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Phalanges foot proximal", value=data['phalanges_foot_p']))
        pg.SetPropertyCell("Phalanges foot proximal", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Phalanges foot medial", value=data['phalanges_foot_m']))
        pg.SetPropertyCell("Phalanges foot medial", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Phalanges foot distal", value=data['phalanges_foot_d']))
        pg.SetPropertyCell("Phalanges foot distal", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        # Carpals - tarsals
        pg.Append(wxpg.PropertyCategory("Carpals - tarsals"))

        pg.Append(self.my_enum_prep("Scaphoid left", value=data['scaphoid_l']))
        pg.SetPropertyCell("Scaphoid left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Scaphoid right", value=data['scaphoid_r']))
        pg.SetPropertyCell("Scaphoid right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Lunate left", value=data['lunate_l']))
        pg.SetPropertyCell("Lunate left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Lunate right", value=data['lunate_r']))
        pg.SetPropertyCell("Lunate right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Triquetral left", value=data['triquetral_l']))
        pg.SetPropertyCell("Triquetral left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Triquetral right", value=data['triquetral_r']))
        pg.SetPropertyCell("Triquetral right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Pisiform left", value=data['pisiform_l']))
        pg.SetPropertyCell("Pisiform left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Pisiform right", value=data['pisiform_r']))
        pg.SetPropertyCell("Pisiform right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Trapezium left", value=data['trapezium_l']))
        pg.SetPropertyCell("Trapezium left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Trapezium right", value=data['trapezium_r']))
        pg.SetPropertyCell("Trapezium right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Trapezoid left", value=data['trapezoid_l']))
        pg.SetPropertyCell("Trapezoid left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Trapezoid right", value=data['trapezoid_r']))
        pg.SetPropertyCell("Trapezoid right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Capitate left", value=data['capitate_l']))
        pg.SetPropertyCell("Capitate left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Capitate right", value=data['capitate_r']))
        pg.SetPropertyCell("Capitate right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Hamate left", value=data['hamate_l']))
        pg.SetPropertyCell("Hamate left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Hamate right", value=data['hamate_r']))
        pg.SetPropertyCell("Hamate right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Sesamoids hand", value=data['sesamoids_hand']))
        pg.SetPropertyCell("Sesamoids hand", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Talus left", value=data['talus_l']))
        pg.SetPropertyCell("Talus left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Talus right", value=data['talus_r']))
        pg.SetPropertyCell("Talus right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Calcaneus left", value=data['calcaneus_l']))
        pg.SetPropertyCell("Calcaneus left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Calcaneus right", value=data['calcaneus_r']))
        pg.SetPropertyCell("Calcaneus right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("1st Cun left", value=data['cun_1_l']))
        pg.SetPropertyCell("1st Cun left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("1st Cun right", value=data['cun_1_r']))
        pg.SetPropertyCell("1st Cun right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("2nd Cun left", value=data['cun_2_l']))
        pg.SetPropertyCell("2nd Cun left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("2nd Cun right", value=data['cun_2_r']))
        pg.SetPropertyCell("2nd Cun right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("3rd Cun left", value=data['cun_3_l']))
        pg.SetPropertyCell("3rd Cun left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("3rd Cun right", value=data['cun_3_r']))
        pg.SetPropertyCell("3rd Cun right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Navicular left", value=data['navicular_l']))
        pg.SetPropertyCell("Navicular left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Navicular right", value=data['navicular_r']))
        pg.SetPropertyCell("Navicular right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Cuboid left", value=data['cuboid_l']))
        pg.SetPropertyCell("Cuboid left", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(self.my_enum_prep("Cuboid right", value=data['cuboid_r']))
        pg.SetPropertyCell("Cuboid right", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        pg.Append(wxpg.IntProperty("Sesamoids foot", value=data['sesamoids_foot']))
        pg.SetPropertyCell("Sesamoids foot", 0, text=wx.propgrid.PG_LABEL, bgCol=bgcCell)

        topsizer.Add(pg, 1, wx.EXPAND)

        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, -1, "&Save")
        btn_ok.Bind(wx.EVT_BUTTON, self.on_save_preservation)
        rowsizer.Add(btn_ok, 1)
        btn_cancel = wx.Button(panel, -1, "&Cancel")
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel_preservation)
        rowsizer.Add(btn_cancel, 1)
        topsizer.Add(rowsizer, 0, wx.EXPAND)

        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.SetSize((400, 600))

        pg.AddActionTrigger(wx.propgrid.PG_ACTION_NEXT_PROPERTY,
                            wx.WXK_RETURN)
        pg.DedicateKey(wx.WXK_RETURN)
        self.pg.SelectProperty('Frontal', True)
        self.pg.SetFocus()

    def on_save_preservation(self, event):
        self.skeleton_dict = self.get_preservation_data()

        controller.edit_preservation(
            self.session, self.selected_row.skeleton_id, self.skeleton_dict)
        self.Close()

    def on_cancel_preservation(self, event):
        self.EndModal(wx.ID_CANCEL)

    def get_preservation_data(self):
        d = self.pg.GetPropertyValues(inc_attributes=True)

        data = {}
        data['frontal'] = d['Frontal']
        data['parietal_l'] = d['Parietal left']
        data['parietal_r'] = d['Parietal right']
        data['occipital'] = d['Occipital']
        data['temporal_l'] = d['Temporal left']
        data['temporal_r'] = d['Temporal right']
        data['sphenoid'] = d['Sphenoid']
        data['nasal_l'] = d['Nasal left']
        data['nasal_r'] = d['Nasal right']
        data['maxilla_l'] = d['Maxilla left']
        data['maxilla_r'] = d['Maxilla right']
        data['zygomatic_l'] = d['Zygomatic left']
        data['zygomatic_r'] = d['Zygomatic right']
        data['mandible'] = d['Mandible']
        data['palatine_l'] = d['Palatine left']
        data['palatine_r'] = d['Palatine right']
        data['lacrimal_l'] = d['Lacrimal left']
        data['lacrimal_r'] = d['Lacrimal right']
        data['orbit_l'] = d['Orbit left']
        data['orbit_r'] = d['Orbit right']
        data['ethmoid'] = d['Ethmoid']
        data['thyroid'] = d['Thyroid']
        data['hyoid'] = d['Hyoid']
        data['calotte'] = d['Calotte']

        data['ilium_l'] = d['Ilium left']
        data['ilium_r'] = d['Ilium right']
        data['scapula_l'] = d['Scapula left']
        data['scapula_r'] = d['Scapula right']
        data['manubrium'] = d['Manubrium']
        data['ischium_l'] = d['Ischium left']
        data['ischium_r'] = d['Ischium right']
        data['patella_l'] = d['Patella left']
        data['patella_r'] = d['Patella right']
        data['c_sterni'] = d['C sterni']
        data['pubic_l'] = d['Pubic left']
        data['pubic_r'] = d['Pubic right']
        data['x_process'] = d['X process']
        data['sacrum'] = d['Sacrum']
        data['coccyx'] = d['Coccyx']

        data['clavicle_l_djs'] = d['Clavicle left D js']
        data['clavicle_l_d13'] = d['Clavicle left D 1/3']
        data['clavicle_l_m13'] = d['Clavicle left M 1/3']
        data['clavicle_l_p13'] = d['Clavicle left P 1/3']
        data['clavicle_l_pjs'] = d['Clavicle left P js']
        data['clavicle_r_djs'] = d['Clavicle right D js']
        data['clavicle_r_d13'] = d['Clavicle right D 1/3']
        data['clavicle_r_m13'] = d['Clavicle right M 1/3']
        data['clavicle_r_p13'] = d['Clavicle right P 1/3']
        data['clavicle_r_pjs'] = d['Clavicle right P js']

        data['humerus_l_djs'] = d['Humerus left D js']
        data['humerus_l_d13'] = d['Humerus left D 1/3']
        data['humerus_l_m13'] = d['Humerus left M 1/3']
        data['humerus_l_p13'] = d['Humerus left P 1/3']
        data['humerus_l_pjs'] = d['Humerus left P js']
        data['humerus_r_djs'] = d['Humerus right D js']
        data['humerus_r_d13'] = d['Humerus right D 1/3']
        data['humerus_r_m13'] = d['Humerus right M 1/3']
        data['humerus_r_p13'] = d['Humerus right P 1/3']
        data['humerus_r_pjs'] = d['Humerus right P js']

        data['radius_l_djs'] = d['Radius left D js']
        data['radius_l_d13'] = d['Radius left D 1/3']
        data['radius_l_m13'] = d['Radius left M 1/3']
        data['radius_l_p13'] = d['Radius left P 1/3']
        data['radius_l_pjs'] = d['Radius left P js']
        data['radius_r_djs'] = d['Radius right D js']
        data['radius_r_d13'] = d['Radius right D 1/3']
        data['radius_r_m13'] = d['Radius right M 1/3']
        data['radius_r_p13'] = d['Radius right P 1/3']
        data['radius_r_pjs'] = d['Radius right P js']

        data['ulna_l_djs'] = d['Ulna left D js']
        data['ulna_l_d13'] = d['Ulna left D 1/3']
        data['ulna_l_m13'] = d['Ulna left M 1/3']
        data['ulna_l_p13'] = d['Ulna left P 1/3']
        data['ulna_l_pjs'] = d['Ulna left P js']
        data['ulna_r_djs'] = d['Ulna right D js']
        data['ulna_r_d13'] = d['Ulna right D 1/3']
        data['ulna_r_m13'] = d['Ulna right M 1/3']
        data['ulna_r_p13'] = d['Ulna right P 1/3']
        data['ulna_r_pjs'] = d['Ulna right P js']

        data['femur_l_djs'] = d['Femur left D js']
        data['femur_l_d13'] = d['Femur left D 1/3']
        data['femur_l_m13'] = d['Femur left M 1/3']
        data['femur_l_p13'] = d['Femur left P 1/3']
        data['femur_l_pjs'] = d['Femur left P js']
        data['femur_r_djs'] = d['Femur right D js']
        data['femur_r_d13'] = d['Femur right D 1/3']
        data['femur_r_m13'] = d['Femur right M 1/3']
        data['femur_r_p13'] = d['Femur right P 1/3']
        data['femur_r_pjs'] = d['Femur right P js']

        data['tibia_l_djs'] = d['Tibia left D js']
        data['tibia_l_d13'] = d['Tibia left D 1/3']
        data['tibia_l_m13'] = d['Tibia left M 1/3']
        data['tibia_l_p13'] = d['Tibia left P 1/3']
        data['tibia_l_pjs'] = d['Tibia left P js']
        data['tibia_r_djs'] = d['Tibia right D js']
        data['tibia_r_d13'] = d['Tibia right D 1/3']
        data['tibia_r_m13'] = d['Tibia right M 1/3']
        data['tibia_r_p13'] = d['Tibia right P 1/3']
        data['tibia_r_pjs'] = d['Tibia right P js']

        data['fibula_l_djs'] = d['Fibula left D js']
        data['fibula_l_d13'] = d['Fibula left D 1/3']
        data['fibula_l_m13'] = d['Fibula left M 1/3']
        data['fibula_l_p13'] = d['Fibula left P 1/3']
        data['fibula_l_pjs'] = d['Fibula left P js']
        data['fibula_r_djs'] = d['Fibula right D js']
        data['fibula_r_d13'] = d['Fibula right D 1/3']
        data['fibula_r_m13'] = d['Fibula right M 1/3']
        data['fibula_r_p13'] = d['Fibula right P 1/3']
        data['fibula_r_pjs'] = d['Fibula right P js']

        data['metacarpals_l_1'] = d['Metacarpals left 1st']
        data['metacarpals_l_2'] = d['Metacarpals left 2nd']
        data['metacarpals_l_3'] = d['Metacarpals left 3rd']
        data['metacarpals_l_4'] = d['Metacarpals left 4th']
        data['metacarpals_l_5'] = d['Metacarpals left 5th']
        data['metacarpals_r_1'] = d['Metacarpals right 1st']
        data['metacarpals_r_2'] = d['Metacarpals right 2nd']
        data['metacarpals_r_3'] = d['Metacarpals right 3rd']
        data['metacarpals_r_4'] = d['Metacarpals right 4th']
        data['metacarpals_r_5'] = d['Metacarpals right 5th']

        data['metatarsals_l_1'] = d['Metatarsals left 1st']
        data['metatarsals_l_2'] = d['Metatarsals left 2nd']
        data['metatarsals_l_3'] = d['Metatarsals left 3rd']
        data['metatarsals_l_4'] = d['Metatarsals left 4th']
        data['metatarsals_l_5'] = d['Metatarsals left 5th']
        data['metatarsals_r_1'] = d['Metatarsals right 1st']
        data['metatarsals_r_2'] = d['Metatarsals right 2nd']
        data['metatarsals_r_3'] = d['Metatarsals right 3rd']
        data['metatarsals_r_4'] = d['Metatarsals right 4th']
        data['metatarsals_r_5'] = d['Metatarsals right 5th']

        data['vertebrae_c_1'] = d['Vertebrae C 1']
        data['vertebrae_c_2'] = d['Vertebrae C 2']
        data['vertebrae_c_3'] = d['Vertebrae C 3']
        data['vertebrae_c_4'] = d['Vertebrae C 4']
        data['vertebrae_c_5'] = d['Vertebrae C 5']
        data['vertebrae_t_1'] = d['Vertebrae T 1']
        data['vertebrae_t_2'] = d['Vertebrae T 2']
        data['vertebrae_t_3'] = d['Vertebrae T 3']
        data['vertebrae_t_4'] = d['Vertebrae T 4']
        data['vertebrae_t_5'] = d['Vertebrae T 5']
        data['vertebrae_l_1'] = d['Vertebrae L 1']
        data['vertebrae_l_2'] = d['Vertebrae L 2']
        data['vertebrae_l_3'] = d['Vertebrae L 3']
        data['vertebrae_l_4'] = d['Vertebrae L 4']
        data['vertebrae_l_5'] = d['Vertebrae L 5']
        data['vertebrae_remarks'] = d['Vertebrae remarks']

        data['ribs_l_whole'] = d['Ribs left whole']
        data['ribs_l_send'] = d['Ribs left S end']
        data['ribs_l_vend'] = d['Ribs left V end']
        data['ribs_l_frag'] = d['Ribs left Frag.']
        data['ribs_r_whole'] = d['Ribs right whole']
        data['ribs_r_send'] = d['Ribs right S end']
        data['ribs_r_vend'] = d['Ribs right V end']
        data['ribs_r_frag'] = d['Ribs right Frag.']
        data['ribs_u_whole'] = d['Ribs unknown whole']
        data['ribs_u_send'] = d['Ribs unknown S end']
        data['ribs_u_vend'] = d['Ribs unknown V end']
        data['ribs_u_frag'] = d['Ribs unknown Frag.']

        data['phalanges_hand_p'] = d['Phalanges hand proximal']
        data['phalanges_hand_m'] = d['Phalanges hand medial']
        data['phalanges_hand_d'] = d['Phalanges hand distal']
        data['phalanges_foot_p'] = d['Phalanges foot proximal']
        data['phalanges_foot_m'] = d['Phalanges foot medial']
        data['phalanges_foot_d'] = d['Phalanges foot distal']

        data['scaphoid_l'] = d['Scaphoid left']
        data['scaphoid_r'] = d['Scaphoid right']
        data['lunate_l'] = d['Lunate left']
        data['lunate_r'] = d['Lunate right']
        data['triquetral_l'] = d['Triquetral left']
        data['triquetral_r'] = d['Triquetral right']
        data['pisiform_l'] = d['Pisiform left']
        data['pisiform_r'] = d['Pisiform right']
        data['trapezium_l'] = d['Trapezium left']
        data['trapezium_r'] = d['Trapezium right']
        data['trapezoid_l'] = d['Trapezoid left']
        data['trapezoid_r'] = d['Trapezoid right']
        data['capitate_l'] = d['Capitate left']
        data['capitate_r'] = d['Capitate right']
        data['hamate_l'] = d['Hamate left']
        data['hamate_r'] = d['Hamate right']
        data['sesamoids_hand'] = d['Sesamoids hand']

        data['talus_l'] = d['Talus left']
        data['talus_r'] = d['Talus right']
        data['calcaneus_l'] = d['Calcaneus left']
        data['calcaneus_r'] = d['Calcaneus right']
        data['cun_1_l'] = d['1st Cun left']
        data['cun_1_r'] = d['1st Cun right']
        data['cun_2_l'] = d['2nd Cun left']
        data['cun_2_r'] = d['2nd Cun right']
        data['cun_3_l'] = d['3rd Cun left']
        data['cun_3_r'] = d['3rd Cun right']
        data['navicular_l'] = d['Navicular left']
        data['navicular_r'] = d['Navicular right']
        data['cuboid_l'] = d['Cuboid left']
        data['cuboid_r'] = d['Cuboid right']
        data['sesamoids_foot'] = d['Sesamoids foot']

        return data


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
