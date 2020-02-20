import json, pygame, math, random

ask_for_file_out = True
ask_for_file_in = True

"""
Graphical + Textual Worldbuilding Application

Saves output to json-file

 - click a location to add a room
 - 'q' + click room prints json info about the room
 - 'e' + click room 1, then click room 2, to add exits from room 1 to 2
 - 'm' + click room, then click somewhere else, to move room
 - 'i' + click room to set the items of room
 - 'a' + 'i' + click room to add to the items of room
 - 's' + click room to make room the starting room
 - 't' + click room to make room the treasure room

"""

alphabet = "abcdefghijklmnopqrstuvwxyz"

def pressed(l):
	if l not in alphabet: return None
	else: return pygame.key.get_pressed()[97+alphabet.index(l)]
	
def dist(p1,p2):
	return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))
	
def build_world():
	
	if ask_for_file_out: output_filename = input("Enter output file name (without extension): ")
	else: output_filename = "world"
	
	rooms = []
	room_ids = []
	exits = []
		
	if ask_for_file_in: 
		load_filename = input("Enter load file name (without extension or suffix) or type 'none': ")
		if load_filename != "none":
			with open(load_filename+"-reuse.json", "r") as f_in:
				loaded = json.load(f_in)
			rooms = loaded.get("rooms")
			room_ids = [room.get("id") for room in rooms]
			exits_provisional = [[room,ex.get("room id")] for room in rooms for ex in room.get("exits")]
			for ex in exits_provisional:
				for room in rooms:
					if room.get("id") == ex[1]:
						exits.append((ex[0],room))
						
	pygame.init()
	
	SCREENSIZE = (1500,1000)
	RADIUS = 50
	screen = pygame.display.set_mode(SCREENSIZE)
	background = pygame.Surface(screen.get_size())
	background.fill((255,255,255))
	background = background.convert()
	screen.blit(background, (0, 0))
	
	
	
	def clicked():
		for room in rooms:
			if dist(room.get("position"),pygame.mouse.get_pos()) < RADIUS:
				return room
		return None
	
	mainloop = True
	
	exit_from = None
	move_from = None
	starting_room = None
	treasure_room = None

	while mainloop:
		color = (0,0,0)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mainloop = False 
			if event.type == pygame.MOUSEBUTTONDOWN:
				if exit_from is not None:
					c = clicked()
					if c is not None:
						if dist(c.get("position"),pygame.mouse.get_pos()) < RADIUS:
							aliases = input("Enter comma separated aliases for the exit from "+exit_from.get("id")+" to "+c.get("id")+": ").split(",")
							if aliases != [""]:
								for alias in list(set(aliases)):
									exit_from.get("exits").append({"name":alias,"room id":c.get("id")})
								exits.append((exit_from,c))
							exit_from = None
							move_from = None
							
				if move_from is not None:
					too_close = False
					for room in rooms:
						if dist(room.get("position"),pygame.mouse.get_pos()) < RADIUS*3: too_close = True
					if not too_close: 
						move_from.update({"position":pygame.mouse.get_pos()})
						exit_from = None
						move_from = None
				else:
					if pressed("q"):
						c = clicked()
						if c is not None: print(json.dumps(c, indent = 4))
					elif pressed("e"):
						exit_from = clicked()
					elif pressed("m"):
						move_from = clicked()
					elif pressed("i"):
						c = clicked()
						if c is not None: 
							if pressed("a"):
								items = input("Enter comma separated new items for "+c.get("id")+": ").split(",")
								c.update({"items":list(set(items+c.get("items")))})
							else:
								items = input("Enter comma separated items for "+c.get("id")+": ").split(",")
								c.update({"items":list(set(items))})
					elif pressed("s"):
						c = clicked()
						if c is not None: starting_room = c.get("id")
					elif pressed("t"):
						for room in rooms:
							if dist(room.get("position"),pygame.mouse.get_pos()) < RADIUS:
								treasure_room = room.get("id")
					else:
						too_close = False
						for room in rooms:
							if dist(room.get("position"),pygame.mouse.get_pos()) < RADIUS*3: too_close = True
						if not too_close: 
							identifier = None
							while identifier is None or identifier in room_ids:
								identifier = input("Enter new room id: ")
							description = input("Enter "+identifier+" description: ")
							rooms.append({"id":identifier,"description":description,"exits":[],"index":len(rooms),"position":pygame.mouse.get_pos(),"color":(random.randint(30,255),random.randint(30,255),random.randint(30,255))})
							room_ids.append(identifier)
				
		background = pygame.Surface(SCREENSIZE)
		background.fill(color)
		
		for ex in exits:
			if ex[0] == move_from: 
				pygame.draw.line(background,(255,255,255),pygame.mouse.get_pos(),ex[1].get("position"),3)
			elif ex[1] == move_from: 
				pygame.draw.line(background,(255,255,255),ex[0].get("position"),pygame.mouse.get_pos(),3)
			else: pygame.draw.line(background,(255,255,255),ex[0].get("position"),ex[1].get("position"),3)
			
		if exit_from is not None:
			pygame.draw.line(background,(255,255,255),exit_from.get("position"),pygame.mouse.get_pos(),3)

		for room in rooms:
			if room == move_from:
				pygame.draw.circle(background,room.get("color"),pygame.mouse.get_pos(),RADIUS)
			else: pygame.draw.circle(background,room.get("color"),room.get("position"),RADIUS)
			
		screen.blit(background, (0,0))		
		pygame.display.flip()
		
	pygame.quit()

	if rooms != []:
		if starting_room is None:
			starting_room = rooms[0].get("id")
			
		if treasure_room is None:
			treasure_room = rooms[0].get("id")
			
		world = {"rooms":rooms,"start room":starting_room,"treasure room":treasure_room}

		with open(output_filename+"-reuse.json","w") as f:
			json.dump(world, f, indent = 4)
			
		for room in rooms:
			room.pop("index")
			room.pop("position")
			room.pop("color")
	
		world = {"rooms":rooms,"start room":starting_room,"treasure room":treasure_room}

		with open(output_filename+".json","w") as f:
			json.dump(world, f, indent = 4)
			
		print("Resulting world: ")
		print(json.dumps(world, indent = 4))
		

build_world()
