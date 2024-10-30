from dcc_linker import Client, Ports

c = Client()

# c.send_command(Ports.blender, "make_cube")
c.send_command(Ports.blender, "make_sphere")
# c.send_command(Ports.blender, "make_monkey")
