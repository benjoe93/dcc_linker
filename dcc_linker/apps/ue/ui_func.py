import unreal

from .web_func_lib import get_level_and_cam, get_selected_actors, get_selected_assets

tool_menus: unreal.ToolMenus = unreal.ToolMenus.get()


@unreal.uclass()
class LevelCamerMenuEntry(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context) -> None:
        get_level_and_cam()


@unreal.uclass()
class ActorSelectionMenuEntry(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context) -> None:
        get_selected_actors()


@unreal.uclass()
class AssetSelectionMenuEntry(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context) -> None:
        get_selected_assets()


def get_menu_obj() -> None:
    file_menu: unreal.ToolMenu = tool_menus.find_menu("LevelEditor.MainMenu.File")
    print(file_menu)


def list_menus(num: int = 1000) -> None:
    menu_names: set[str] = set()
    for i in range(num):
        obj: unreal.ToolMenu = unreal.find_object(None, f"/Engine/Transient.ToolMenus_0:RegisteredMenu_{i}")
        if not obj:
            continue

        menu_names.add(str(obj.menu_name))

    print(*sorted(list(menu_names)), sep="\n")


def add_tech_art_menu() -> unreal.ToolMenu:
    main_menu: unreal.ToolMenu = tool_menus.find_menu("LevelEditor.MainMenu")
    main_menu.add_sub_menu("TechArt", "TechArtMenu", "TechArt", "Tech Art")
    tool_menus.refresh_all_widgets()
    tech_art_menu: unreal.ToolMenu = tool_menus.find_menu("LevelEditor.MainMenu.TechArt")
    tech_art_menu.add_section(
        section_name="TA Script",
        label="Tech Art Script",
    )

    return tech_art_menu


def add_ta_menu_entry(
    owner: unreal.ToolMenu, script_obj: unreal.ToolMenuEntryScript, name: str, lable: str, tool_tip: str = ""
) -> None:
    script_obj = script_obj
    script_obj.init_entry(
        owner_name=owner.menu_name,
        menu=owner.menu_name,
        section="NewScripts",
        name=name,
        label=lable,
        tool_tip=tool_tip,
    )
    script_obj.register_menu_entry()


def costruct_tech_art_menu() -> None:
    menu = add_tech_art_menu()

    add_ta_menu_entry(
        menu,
        LevelCamerMenuEntry(),
        "LvlCamLoc",
        "Get Level & Camera Loc",
        "Creates a link for the current level and camera location",
    )

    add_ta_menu_entry(
        menu,
        ActorSelectionMenuEntry(),
        "ActorSelection",
        "Get Selected Actors",
        "Creates a link for the currently selected actors",
    )

    add_ta_menu_entry(
        menu,
        AssetSelectionMenuEntry(),
        "AssetSelection",
        "Get Selected Assets",
        "Creates a link for the currently selected assets",
    )
