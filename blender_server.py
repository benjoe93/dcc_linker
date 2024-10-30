import os
import sys

# Temperory import of the package. In the future this should be installed into the venv of Blender
linker_path: str = r"D:\dev\unreal\ToolsTest\Plugins\WebHook\Content\Python"
if linker_path not in sys.path:
    sys.path.append(linker_path)

import bpy

from dcc_linker import DccRequestHandler, HostApps, MainThreadManager, Ports, Server

mtm = MainThreadManager(app=HostApps.blender)

s = Server(("", Ports.blender), DccRequestHandler, main_manager=mtm)
s.start_server_on_thread()

# registers the thread poller in the main program loop
bpy.app.timers.register(mtm.main_thread_poller)
