import os
import sys

# Temperory import of the package. In the future this should be installed into the venv of Blender
linker_path: str = r"D:\dev\unreal\ToolsTest\Plugins\WebHook\Content\Python"
if linker_path not in sys.path:
    sys.path.append(linker_path)

import hou

from dcc_linker import DccRequestHandler, HostApps, MainThreadManager, Ports, Server

mtm = MainThreadManager(app=HostApps.houdini)

s = Server(("", Ports.houdini), DccRequestHandler, main_manager=mtm)
s.start_server_on_thread()

# registers the thread poller in the main program loop
hou.ui.addEventLoopCallback(mtm.main_thread_poller)
