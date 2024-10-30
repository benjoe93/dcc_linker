import bpy


def make_cube() -> None:
    bpy.ops.mesh.primitive_cube_add(size=4)
    cube = bpy.context.active_object
    cube.location.z = 5
    print("YAAY!")


def make_monkey() -> None:
    bpy.ops.mesh.primitive_monkey_add()
    monkey = bpy.context.active_object
    monkey.location.y = 2


def make_sphere() -> None:
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.active_object
    sphere.location.y = 4
