# SkeletonForm
A simple database to record the state of skeletons from archaeological research and create a graphical report on the state of preservation.
Python 3 + wxPython 4.07 + SQLAlchemy 1.3.13  ReportLab 3.5.34.

The application uses ObjectListView, in this object is known problem (https://stackoverflow.com/questions/29302875/typeerror-in-string-requires-string-as-left-operand-not-int-with-objectlis )
, line 1457 in the ObjectListView.py file should be modified according to the suggestion.

Windows:

![Screen](/doc/screen.png)

Linux (Ubuntu 18.04):

 * pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 wxPython
 * apt install libsdl1.2debian
 
 ![Screen](/doc/screen_linux.png)
 
 ![Screen](/doc/screen_linux2.png)
