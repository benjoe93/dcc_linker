import hou


def make_box():
    network = hou.node("/obj/")
    geo = network.createNode("geo")
    geo.createNode("box")
