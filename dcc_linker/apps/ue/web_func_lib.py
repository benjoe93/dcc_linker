import json
import urllib.parse

import unreal

PORT: int = 9999


def conver_dict(func_name: str, params: dict) -> str:
    param_str: str = json.dumps(params)
    return f"{func_name}&{urllib.parse.quote(param_str)}"


@unreal.uclass()
class WebFuncLib(unreal.BlueprintFunctionLibrary):
    @unreal.ufunction(params=[str, unreal.Vector, unreal.Rotator], ret=None, static=True)
    def set_level_and_cam(map_name: str, cam_loc: unreal.Vector, cam_rot: unreal.Rotator) -> None:
        les: unreal.LevelEditorSubsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        ues: unreal.UnrealEditorSubsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)

        ues.set_level_viewport_camera_info(cam_loc, cam_rot)
        conf_key: unreal.Name = les.get_active_viewport_config_key()
        les.editor_set_game_view(True, unreal.Name("None"))
        les.editor_set_game_view(False, conf_key)
        # if les.load_level(map_name):
        #     unreal.log("Level Loaded!")

    @unreal.ufunction(params=[unreal.Array(str)], ret=None, static=True)
    def select_assets(assets: list[str]) -> None:

        unreal.EditorAssetLibrary.sync_browser_to_objects(assets)

    @unreal.ufunction(params=[unreal.Array(str)], ret=None, static=True)
    def select_actors(actor_path: list[str]) -> None:
        eas: unreal.EditorActorSubsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        les: unreal.LevelEditorSubsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)

        actors: list[unreal.Actor] = []
        for p in actor_path:
            actor: unreal.Actor = eas.get_actor_reference(p)
            actors.append(actor)

        eas.set_selected_level_actors(actors)
        conf_key: unreal.Name = les.get_active_viewport_config_key()
        les.editor_set_game_view(True, unreal.Name("None"))
        les.editor_set_game_view(False, conf_key)


def get_level_and_cam() -> str:
    # get current level name
    ues: unreal.UnrealEditorSubsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    current_level: unreal.World = ues.get_editor_world()
    level_name: str = current_level.get_full_name().split(" ")[1].split(".")[0]

    # get camera details
    cam_loc: unreal.Vector
    cam_rot: unreal.Rotator
    cam_loc, cam_rot = ues.get_level_viewport_camera_info()

    params: dict = {}
    params["map_name"] = level_name
    params["cam_loc"] = {"X": cam_loc.x, "Y": cam_loc.y, "Z": cam_loc.z}
    params["cam_rot"] = {"Pitch": cam_rot.pitch, "Yaw": cam_rot.yaw, "Roll": cam_rot.roll}

    url_params: str = conver_dict("set_level_and_cam", params=params)
    url: str = f"http://localhost:{PORT}/?{url_params}"

    unreal.log(f"URL: {url}")
    return url


def get_selected_assets() -> str:
    # get selected assets
    selected_assets: list[str] = []
    assets_data: list[unreal.AssetData] = unreal.EditorUtilityLibrary.get_selected_asset_data()
    for data in assets_data:
        selected_assets.append(str(data.package_name))

    if not selected_assets:
        # TODO: Build error message UI
        return ""

    params: dict = {}
    params["assets"] = selected_assets

    url_params: str = conver_dict("select_assets", params=params)
    url: str = f"http://localhost:{PORT}/?{url_params}"

    unreal.log(f"URL: {url}")
    return url


def get_selected_actors() -> str:
    eas: unreal.EditorActorSubsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    selected_actors: list[unreal.Actor] = eas.get_selected_level_actors()

    if not selected_actors:
        return ""

    actor_paths: list[str] = []
    for actor in selected_actors:
        path: str = actor.get_path_name().split(":")[1]
        actor_paths.append(path)

    params: dict = {}
    params["actor_path"] = actor_paths
    url_params: str = conver_dict("select_actors", params=params)
    url: str = f"http://localhost:{PORT}/?{url_params}"

    unreal.log(f"URL: {url}")
    return url
