import wx
import os
import controller
import dialogs
import platform
from ObjectListView import ObjectListView, ColumnDefn
from wx.lib.wordwrap import wordwrap
from model import olvSkeleton
from sheet import SheetExport


APP_NAME = 'SkeletonForm'


class SkeletonPanel(wx.Panel):
    """
    Skeleton panel widget
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.db_name = ""
        self.skeleton_results = []
        self.session = None
        self.parent = parent
        # self.session = controller.connect_to_database()

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

        # create the search related widgets
        categories = ["Site", "Location", "Observer", "Skeleton"]
        search_label = wx.StaticText(self, label=" Filter By:")
        search_label.SetFont(font)
        search_sizer.Add(search_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        search_sizer.AddSpacer(5)

        if platform.system().lower() == 'linux':
            self.categories = wx.ComboBox(
                self, value="Skeleton", choices=categories, style=wx.CB_READONLY, size=(150, -1))
        else:
            self.categories = wx.ComboBox(
                self, value="Skeleton", choices=categories, style=wx.CB_READONLY)

        search_sizer.Add(self.categories, 0, wx.ALL, 5)

        search_sizer.AddSpacer(5)

        if platform.system().lower() == 'linux':
            self.search_ctrl = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER, size=(200, 27))
        else:
            self.search_ctrl = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER, size=(200, -1))

        # self.search_ctrl.ShowCancelButton(True)
        self.search_ctrl.SetDescriptiveText('Filter')
        self.search_ctrl.Bind(wx.EVT_TEXT_ENTER, self.search)
        search_sizer.Add(self.search_ctrl, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        search_sizer.AddSpacer(5)

        self.show_all_btn = wx.Button(self, label="Show All")
        self.show_all_btn.Bind(wx.EVT_BUTTON, self.on_show_all)
        search_sizer.Add(self.show_all_btn, 0, wx.ALL, 5)

        lfont = self.GetFont()
        lfont.SetPointSize(10)
        self.skeleton_results_olv = ObjectListView(
            self, style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL)
        self.skeleton_results_olv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDoubleClick)
        self.skeleton_results_olv.EnableBellOnNoMatch(on=False)
        self.skeleton_results_olv.SetFont(lfont)
        self.skeleton_results_olv.SetEmptyListMsg("No Records Found")
        self.update_skeleton_results()

        # create the button row
        self.add_record_btn = wx.Button(self, label="&Add")
        self.add_record_btn.Bind(wx.EVT_BUTTON, self.add_record)
        btn_sizer.Add(self.add_record_btn, 0, wx.ALL, 5)

        self.edit_record_btn = wx.Button(self, label="&Edit")
        self.edit_record_btn.Bind(wx.EVT_BUTTON, self.edit_record)
        btn_sizer.Add(self.edit_record_btn, 0, wx.ALL, 5)

        self.pre_record_btn = wx.Button(self, label="&Preservation")
        self.pre_record_btn.Bind(wx.EVT_BUTTON, self.edit_preservation)
        btn_sizer.Add(self.pre_record_btn, 0, wx.ALL, 5)

        self.delete_record_btn = wx.Button(self, label="&Delete")
        self.delete_record_btn.Bind(wx.EVT_BUTTON, self.delete_record)
        btn_sizer.Add(self.delete_record_btn, 0, wx.ALL, 5)

        self.report_btn = wx.Button(self, label="&Create a report")
        self.report_btn.Bind(wx.EVT_BUTTON, self.create_report)
        btn_sizer.Add(self.report_btn, 0, wx.ALL, 5)

        self.controls_state(False)

        main_sizer.Add(search_sizer)
        main_sizer.Add(self.skeleton_results_olv, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(main_sizer)

    def controls_state(self, state):
        self.add_record_btn.Enable(state)
        self.edit_record_btn.Enable(state)
        self.pre_record_btn.Enable(state)
        self.delete_record_btn.Enable(state)
        self.report_btn.Enable(state)
        self.show_all_btn.Enable(state)
        self.search_ctrl.Enable(state)

    def on_open_file(self, event):
        wildcard = "DATABASE files (*.db)|*.db"
        with wx.FileDialog(self, "Choose a file", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.db_name = dialog.GetPath()
                # zapis w ostatnio używanych plikach
                self.parent.filehistory.AddFileToHistory(dialog.GetPath())
                self.parent.filehistory.Save(self.parent.config)
                self.parent.config.Flush()
                if self.session != None:
                    self.skeleton_results_olv.DeleteAllItems()
                    self.parent.SetTitle("{}: ".format(APP_NAME))
                    self.session.close()

                self.session = controller.connect_to_database(self.db_name)
                self.parent.SetTitle("{}: ".format(APP_NAME) + self.db_name)
                self.controls_state(True)
                self.show_all_records()

    def on_create_file(self, event):
        wildcard = "DATABASE files (*.db)|*.db"
        with wx.FileDialog(self, "Create a file", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.db_name = dialog.GetPath()
                # zapis w ostatnio używanych plikach
                self.parent.filehistory.AddFileToHistory(dialog.GetPath())
                self.parent.filehistory.Save(self.parent.config)
                self.parent.config.Flush()
                if self.session != None:
                    self.skeleton_results_olv.DeleteAllItems()
                    self.parent.SetTitle("{}: ".format(APP_NAME))
                    self.session.close()

                self.session = controller.connect_to_database(self.db_name)
                self.parent.SetTitle("{}: ".format(APP_NAME) + self.db_name)
                self.controls_state(True)
                self.show_all_records()

    def add_record(self, event):
        """
        Add a record to the database
        """
        with dialogs.RecordDialog(self.session) as dlg:
            dlg.CenterOnScreen()
            dlg.ShowModal()
            if dlg.result == 1:
                data = {}
                data['skeleton_id'] = dlg.skeleton_id
                data['site'] = dlg.skeleton_dict['site']
                data['location'] = dlg.skeleton_dict['location']
                data['skeleton'] = dlg.skeleton_dict['skeleton']
                data['observer'] = dlg.skeleton_dict['observer']
                data['obs_date'] = dlg.skeleton_dict['obs_date']

                new_skeleton = olvSkeleton(data)
                self.skeleton_results_olv.AddObject(new_skeleton)
                idx = self.skeleton_results_olv.GetIndexOf(new_skeleton)
                self.skeleton_results_olv.Select(idx)
                self.skeleton_results_olv.SelectObject(new_skeleton)

        self.skeleton_results_olv.SetFocus()

    def edit_skeleton(self):
        selected_row = self.skeleton_results_olv.GetSelectedObject()
        active_row = self.skeleton_results_olv.GetIndexOf(selected_row)
        if selected_row is None:
            dialogs.show_message('No record selected!', 'Error')
            return

        with dialogs.RecordDialog(self.session, selected_row, title='Modify', addRecord=False) as dlg:
            dlg.CenterOnScreen()
            dlg.ShowModal()
            if dlg.result == 1:
                self.skeleton_results_olv.RefreshObject(selected_row)

        self.skeleton_results_olv.SetFocus()

    def edit_record(self, event):
        """
        Edit a record
        """
        self.edit_skeleton()

    def onDoubleClick(self, event):
        self.edit_skeleton()

    def delete_record(self, event):
        """
        Delete a record
        """
        selected_row = self.skeleton_results_olv.GetSelectedObject()
        row_index = self.skeleton_results_olv.GetIndexOf(selected_row)
        if selected_row is None:
            dialogs.show_message('No record selected!', 'Error')
            return

        info = 'Delete current record?\n\nSite: {}\nLocation: {}\nSkeleton: {}'.format(selected_row.site,
                                                                                       selected_row.location,
                                                                                       selected_row.skeleton)
        if dialogs.ask_message(info, 'Delete record'):
            controller.delete_record(self.session, selected_row.skeleton_id)
            self.skeleton_results_olv.RemoveObject(selected_row)
            if row_index > 0:
                row_index -= 1

        self.skeleton_results_olv.Select(row_index)
        self.skeleton_results_olv.SetFocus()

    def edit_preservation(self, event):
        selected_row = self.skeleton_results_olv.GetSelectedObject()
        active_row = self.skeleton_results_olv.GetIndexOf(selected_row)
        if selected_row is None:
            dialogs.show_message('No record selected!', 'Error')
            return

        with dialogs.PreservationDialog(self.session, selected_row) as dlg:
            dlg.CenterOnScreen()
            dlg.ShowModal()

        self.skeleton_results_olv.SetFocus()

    def show_all_records(self, active_row=0):
        """
        Updates the record list to show all of them
        """
        self.skeleton_results = controller.get_all_records(self.session)
        self.update_skeleton_results(active_row)

    def create_report(self, event):
        """
        generating a skeleton report
        """
        filename = ""
        wildcard = "PDF files (*.pdf)|*.pdf"
        with wx.FileDialog(None, "Create a report", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetPath()

        if filename == "":
            return

        my_id = self.skeleton_results_olv.GetSelectedObject().skeleton_id
        rekord = controller.find_skeleton(self.session, my_id)
        if rekord == None:
            dialogs.show_message('No record was found', 'Error')
            return

        data = {}
        data['site'] = rekord.site
        data['location'] = rekord.location
        data['skeleton'] = rekord.skeleton
        data['observer'] = rekord.observer
        data['obs_date'] = rekord.obs_date
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

        report = SheetExport()
        result = report.export_sheet(filename, data)
        if result != '':
            dialogs.show_message('Problems occurred during the creation of the report:\n{}'.format(result), 'Error')

        self.skeleton_results_olv.SetFocus()

    def search(self, event):
        """
        Searches database based on the user's filter
        choice and keyword
        """
        filter_choice = self.categories.GetValue()
        keyword = self.search_ctrl.GetValue()
        self.skeleton_results = controller.search_records(
            self.session, filter_choice, keyword)
        self.update_skeleton_results()

    def on_show_all(self, event):
        """
        Updates the record list to show all the records
        """
        self.show_all_records()

    def update_skeleton_results(self, active_row=0):
        """
        Updates the ObjectListView's contents
        """
        self.skeleton_results_olv.SetColumns([
            ColumnDefn("Site", "left", 350, "site",
                       isSpaceFilling=True, minimumWidth=50),
            ColumnDefn("Location", "left", 150,
                       "location", isSpaceFilling=True, minimumWidth=50),
            ColumnDefn("Skeleton", "left", 150,
                       "skeleton", isSpaceFilling=True, minimumWidth=50),
            ColumnDefn("Observer", "left", 150,
                       "observer", isSpaceFilling=True, minimumWidth=50),
            ColumnDefn("Observation date", "center", 80,
                       "obs_date", isSpaceFilling=True, minimumWidth=50)
        ])
        self.skeleton_results_olv.SetObjects(self.skeleton_results)
        if self.skeleton_results_olv.GetItemCount() > 0:
            self.skeleton_results_olv.Select(active_row)
        self.skeleton_results_olv.SetFocus()


class SkeletonFrame(wx.Frame):
    """
    The top level frame widget
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__(None, title=APP_NAME, size=(800, 600))
        self.panel = SkeletonPanel(self)
        self.filehistory = wx.FileHistory(8)
        self.config = wx.Config(APP_NAME, style=wx.CONFIG_USE_LOCAL_FILE)
        self.create_menu()
        self.SetMinSize(wx.Size(400, 300))
        self.Show()

    def on_exit(self, event):
        self.Destroy()

    def on_about(self, event):
        info = wx.adv.AboutDialogInfo()
        info.Name = APP_NAME
        info.Version = "0.1 Beta"
        info.Copyright = "(C) 2020 Piotr Jaskulski"
        description = "A simple database to record the state of skeletons from archaeological "
        description += "research and create a graphical report on the state of preservation. "
        info.Description = wordwrap(description, 350, wx.ClientDC(self.panel))
        info.WebSite = ("https://github.com/pjaskulski/SkeletonForm", "APP_NAME")
        info.Developers = ["Piotr Jaskulski"]
        info.License = wordwrap("MIT", 500, wx.ClientDC(self.panel))
        wx.adv.AboutBox(info)

    def on_file_history(self, event):
        fileNum = event.GetId() - wx.ID_FILE1
        path = self.filehistory.GetHistoryFile(fileNum)
        self.filehistory.AddFileToHistory(path)
        self.panel.db_name = path

        if self.panel.session != None:
            self.panel.skeleton_results_olv.DeleteAllItems()
            self.panel.parent.SetTitle("{}: ".format(APP_NAME))
            self.panel.session.close()

        self.panel.session = controller.connect_to_database(self.panel.db_name)
        self.SetTitle("{}: ".format(APP_NAME) + self.panel.db_name)
        self.panel.controls_state(True)
        self.panel.show_all_records()

    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()

        self.filehistory.Load(self.config)

        create_db_menu_item = file_menu.Append(wx.ID_NEW, 'Create DB\tCtrl+N', 'Create database file')
        open_db_menu_item = file_menu.Append(wx.ID_OPEN, 'Open DB\tCtrl+O', 'Open database file')

        # ostatnio używane pliki
        recent = wx.Menu()
        self.filehistory.UseMenu(recent)
        self.filehistory.AddFilesToMenu()
        file_menu.Append(wx.ID_ANY, "&Recent Files", recent)

        file_menu.AppendSeparator()
        exit_menu_item = file_menu.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Quit application')

        menu_bar.Append(file_menu, "&File")
        self.Bind(wx.EVT_MENU, self.panel.on_open_file, open_db_menu_item)
        self.Bind(wx.EVT_MENU, self.panel.on_create_file, create_db_menu_item)
        self.Bind(wx.EVT_MENU_RANGE, self.on_file_history, id=wx.ID_FILE1, id2=wx.ID_FILE9)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_menu_item)

        help_menu = wx.Menu()
        about_menu_item = help_menu.Append(wx.ID_ANY, 'About', 'About Application')
        menu_bar.Append(help_menu, "Help")
        self.Bind(wx.EVT_MENU, self.on_about, about_menu_item)

        self.SetMenuBar(menu_bar)


if __name__ == "__main__":
    app = wx.App(False)
    frame = SkeletonFrame()
    app.MainLoop()
