# SkeletonForm
A simple database to record the state of skeletons from archaeological research and create a graphical report on the state of preservation.
Python 3 + wxPython 4.07 + SQLAlchemy 1.3.13 + ReportLab 3.5.34 + XlsxWriter 1.2.7.

The application uses ObjectListView, in this object is known problem (https://stackoverflow.com/questions/29302875/typeerror-in-string-requires-string-as-left-operand-not-int-with-objectlis )
, line 1457 in the ObjectListView.py file should be modified according to the suggestion.

Windows:

![Screen](/doc/screen.png)

![Screen](/doc/screen2.png)

Linux (Ubuntu 18.04):

 * pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 wxPython
 * apt install libsdl1.2debian
 
 While the program is running in Ubuntu 18.04 you may encounter GTK warnings displayed in the console. The problem is known (https://github.com/wxWidgets/Phoenix/issues/1297) but not solvable.
 
 ![Screen](/doc/screen_linux.png)
 
 ![Screen](/doc/screen_linux2.png)
 
 Skull report example:
 
 ![Screen](/doc/skull_report.png)
 
 
