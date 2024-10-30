# TODO: Sort this out to be dynamic

try:
    from . import blender

    print("blender")
except ImportError:
    pass
try:
    from . import ue

    print("ue")
except ImportError:
    pass
try:
    from . import houdini

    print("houdini")
except ImportError:
    pass
