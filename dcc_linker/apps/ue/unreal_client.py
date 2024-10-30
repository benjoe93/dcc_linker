from datetime import datetime

import unreal

from dcc_linker import Client, HostApps, Ports

c = Client(HostApps.unreal)


@unreal.uclass()
class DccLinkerClient(unreal.BlueprintFunctionLibrary):

    # Blender functions
    @unreal.ufunction(static=True, ret=bool, params=[])
    def blender_make_cube() -> bool:
        start = datetime.now()
        is_success = c.send_command(
            target=Ports.blender,
            func_name="make_cube",
        )
        end = datetime.now()
        print("TIME:", end - start)
        return is_success

    @unreal.ufunction(static=True, ret=bool, params=[])
    def blender_make_sphere() -> bool:
        start = datetime.now()
        is_success = c.send_command(
            target=Ports.blender,
            func_name="make_sphere",
        )
        end = datetime.now()
        print("TIME:", end - start)
        return is_success

    @unreal.ufunction(static=True, ret=bool, params=[])
    def blender_make_monkey() -> bool:
        start = datetime.now()
        is_success = c.send_command(
            target=Ports.blender,
            func_name="make_monkey",
        )
        end = datetime.now()
        print("TIME:", end - start)
        return is_success

    # Houdini functions
    @unreal.ufunction(static=True, ret=bool, params=[])
    def houdini_make_cube() -> bool:

        return c.send_command(
            target=Ports.houdini,
            func_name="make_box",
            parameters={},
        )
