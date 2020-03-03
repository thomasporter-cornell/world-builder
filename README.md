# world-builder

This is a python script to build text adventure jsons for A2 and the GOOD SCOPE of A3, according to my implementation. 
It is a combined graphical and terminal interface, so keep both windows open and be ready to switch between them.

Requires pygame. 

You may save and load a world to continue projects. 
It produces two files, filename.json, and filename-reuse.json. 
Make manual edits in the -reuse version, but run the game with the regular version.

Commands:

 - click a location to add a room
 - 'q' + click room prints json info about the room
 - 'e' + click room 1, then click room 2, to add exits from room 1 to 2
 - 'm' + click room, then click somewhere else, to move room
 - 'i' + click room to add items to a room
 - 's' + click room to make room the starting room
 - 't' + click room to make room the treasure room
 - Save by exiting the pygame window, NOT THE TERMINAL.

The code is not elegant, and there is no error handling. It is just a quick and dirty tool for building a world edits will have to be made in the file, as will adding compatibility with A3 excellent scope. 

Also you may want to go into the code and edit the dimensions (screensize and radius) so it fits on your computer.
