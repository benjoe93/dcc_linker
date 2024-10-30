# This is an example file to show how to create Blueprint Function Libraries in python.
# You can find function examples that show how to achive certain node setups.

import unreal


@unreal.ustruct()
class OutStruct(unreal.StructBase):
    """
    This struct is used to enable a ufunction to have multiple outputs
    For function example look at func_multi() bellow
    """

    integer = unreal.uproperty(int)
    string = unreal.uproperty(str)
    boolean = unreal.uproperty(bool)
    map = unreal.uproperty(unreal.Map(str, float))
    array = unreal.uproperty(unreal.Array(int))


@unreal.ustruct()
class PTData(unreal.StructBase):
    """
    This struct is used to enable a ufunction to have multiple outputs
    For function example look at func_multi() bellow
    """

    ID = unreal.uproperty(int)
    Transform = unreal.uproperty(unreal.Transform)
    metadata = unreal.uproperty(unreal.Map(str, str))


@unreal.uclass()
class FunctionLibraryName(unreal.BlueprintFunctionLibrary):
    """
    @unreal.ufunction() paramers:
        static: Is it a static function? For Function Libs this is always **True**
        ret: The return type of the function
        parms: List of the types of input parameters
    """

    @unreal.ufunction(static=True, ret=None, params=[])
    def func_no_input() -> None:
        """
        Base static function with no input and output
        """
        pass

    @unreal.ufunction(static=True, ret=str, params=[])
    def func_output() -> str:
        """
        Base static function with output
        The type of the output is changed in ret=...
        """
        pass
        return ""

    @unreal.ufunction(static=True, ret=unreal.Map(str, str), params=[])
    def func_complex_output() -> dict[str, str]:
        """
        Base static function with complex output
        """
        out = unreal.Map(str, str)
        out["one"] = "One"
        out["two"] = "Two"
        return out

    @unreal.ufunction(
        static=True,
        ret=None,
        params=[int, str, float, bool, unreal.Array(int), unreal.Map(str, int), unreal.StaticMesh],
    )
    def func_inputs(
        integer: int,
        string: str,
        floating: float,
        boolian: bool,
        int_array: list[int],
        map: dict[str, int],
        static_mesh: unreal.StaticMesh,
    ) -> None:
        """
        Base static function with inputs
        """
        pass

    @unreal.ufunction(pure=True, static=True, ret=str, params=[int])
    def func_pure(integer: int) -> str:
        """
        Base static function with inputs
        """
        return "string"

    @unreal.ufunction(pure=True, static=True, ret=OutStruct, params=[])
    def func_multi():
        """
        Static function with 'multiple' outputs
        For this to work the outputs need to be wrapped in a unreal.ustruct()

        Find the struct up in the file
        """
        out_map = unreal.Map(str, float)
        out_map["one"] = 3.14159265

        struct = OutStruct()
        struct.integer = 1
        struct.string = "hello"
        struct.boolean = True
        struct.map = out_map
        struct.array = [1, 2, 5]

        return struct

    @unreal.ufunction(pure=True, static=True, ret=bool, params=[unreal.Array(PTData)])
    def func_multi(PtsData: list[PTData]):
        """
        Static function with 'multiple' outputs
        For this to work the outputs need to be wrapped in a unreal.ustruct()

        Find the struct up in the file
        """
        return True
