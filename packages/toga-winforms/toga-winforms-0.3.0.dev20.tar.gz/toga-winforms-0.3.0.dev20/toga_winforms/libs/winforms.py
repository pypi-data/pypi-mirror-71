import ctypes

import clr

clr.AddReference("System.Windows.Forms")

import System.Windows.Forms as WinForms  # noqa: E402, F401

from System import Action  # noqa: E402, F401
from System import Convert  # noqa: E402, F401
from System import DateTime as WinDateTime  # noqa: E402, F401
from System import Environment  # noqa: E402, F401
from System import Single  # noqa: E402, F401
from System import Threading  # noqa: E402, F401
from System import Uri  # noqa: E402, F401

from System.Drawing import Drawing2D  # noqa: E402, F401
from System.Drawing import Font as WinFont  # noqa: E402, F401
from System.Drawing import Icon as WinIcon  # noqa: E402, F401
from System.Drawing import Image as WinImage  # noqa: E402, F401
from System.Drawing import ContentAlignment, Size, Point, PointF  # noqa: E402, F401
from System.Drawing import FontFamily, FontStyle, SystemFonts  # noqa: E402, F401
from System.Drawing import StringFormat  # noqa: E402, F401
from System.Drawing import Text, Color, Bitmap  # noqa: E402, F401
from System.Drawing import Graphics  # noqa: E402, F401
from System.Drawing import Pen, SolidBrush  # noqa: E402, F401
from System.Drawing import Rectangle, RectangleF  # noqa: E402, F401
from System.Drawing.Drawing2D import GraphicsPath, FillMode, Matrix  # noqa: E402, F401

from System.Threading.Tasks import Task  # noqa: E402, F401


user32 = ctypes.windll.user32
# shcore dll not exist on some Windows versions
# win_version should be checked to ensure proper usage
try:
    shcore = ctypes.windll.shcore
except OSError:
    shcore = None
win_version = Environment.OSVersion.Version
