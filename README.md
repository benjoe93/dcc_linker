This tool was created to make communicateion easier between team members

The current setup only supports Unreal Engine, but this can be extended in the future.

## Unreal

This system relys on the **Remote Control API** (RC), that comes with Unreal.
We are creating a basic HTTP server that runs in the background and acts as a relay between the user and the editor.

In the editor we can create HTTP link, that can be shared with other team members. By clicking on the link, the
listening server will pick up the data stored in the URL, decodes these into a JSON payload and forwards it to the
editor, where the RC executes the requested functions.

## TODO:

## Instalation:
"# dcc_linker" 
"# dcc_linker" 
"# dcc_linker" 
