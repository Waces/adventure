# Text Adventure game
# CopyLEFT 2018 - Waces F.
#---Imports---
import cmd
import textwrap
import sys
# import configparser # WIP to start
import os
from time import sleep

#---Some vars---
screenWidth = 80
jftsod = "Just for the sake of debugging/developing."

#---Syntax list--- with models that are a list of words that can mean one thing
yesModel = ('yes','y','ye','yep','yup','yus','yis','s','sim','yee','yy')
#(N 0, S 1, E 2, W 3, NE 4,SE 5,SW 6,NW 7, in 8, out 9, up 10, down 11
#(North, South, East, West,NE,SE,SW,NW,    in,  out,    up,    down
nothModel = ["north",'n']
southModel = ['south','s']
eastModel = ['east','e']
westModel = ['west','w']
nestModel = ['northeast','north east','ne']
sestModel = ["southeast","south east","se"]
swstModel = ["southwest","south west","sw"]
nwstModel = ["northwest","north west","nw"]
inModel = ["inside","in",'i']
outModel = ["outside", "out",'o']
upModel = ["up",'u']
downModel = ["down",'dw','d']

def repEl(li, ch, num, repl):
    last_found = 0
    for _ in range(num):
        last_found = li.index(ch, last+found+1)
    li[li.index(ch, last_found)] = repl

#Directions in the list, yes I could have just used tuples, but whatever
dirN,dirS,dirE,dirW,dirNE,dirSE,dirSW,dirNW,dirIn,dirOut,dirUp,dirDown = 0,1,2,3,4,5,6,7,8,9,10,11

# ---Player class---
class Player:
    def __init__(self, name, startPos):
        self.name = name
        self.position = startPos
        self.inventory = [] # Maybe change to/use dictionary to store name?
        self.reachable = () #Use? Nahhh, to remove
        #Add self.atributeName = value(s) to add more values to player


# Placeholder player:
# player = Player('Player', darkRoom0)
# player.inventory = ['readMe.md'] #Placeholder item

#---Objects class---
class Object:
    def __init__(self, name, grounDescription, shortDesc, takeBool):
        self.name = name
        self.words = () # Other words that mean it
        self.groundDesc = grounDescription # What shows when you enter room/look around if it still on the floor
        self.longDesc = ""
        self.shortDesc = shortDesc
        self.usable = False # If this object can be used
        self.useResult = ()
        self.readable = False
        self.texto = ""
        self.useVanish = False # If the object will disappear if used
        self.pickable = takeBool # If it can be picked by the player

#---Objects---
testObj = Object("testObj", "There is an undefined test object.", "A test object",True)
testObj.longDesc = "It is an object made to test the"
testObj.words = ['test object','testobj']

readMe = Object("readMe.md",
                "There is a paper note with some square cuts at the bottom.",
                "A paper note with square cuts at the bottom",
                True)
readMe.words = ['readme','note','readme.md']
readMe.readable = True
readMe.longDesc = "It is a note with some square cuts at the bottom."
readMe.texto = "It reads 'Hello World'."

woodTable = Object("Wooden table",
                   "There is a wooden table.",
                   "A wooden table",
                   False)
woodTable.longDesc = woodTable.shortDesc
woodTable.words = ['table','wooden table']

key0 = Object("Rusty key",
              "There is a rusty key laying in this place",
              "It's a rusty key",
              True)
key0.longDesc = "It is a, old rusty key, it may serve to open a door"
key0.words = ['key','rusty key']

lapTop = Object("Laptop",
                "I see a laptop laying on the floor",
                "A laptop laying on the floor that seems to be On",
                False)
lapTop.longDesc = "It's a laptop laying on the ground, and seems to be On. There's something displayed on its screen, two terminals, one running some text editor and the other running an unknown program."
lapTop.texto = "The time and date shown are 18:30-2-Feb-2000, on the first panel, it reads 'This is the end of the TEST.', on the other terminal panel, it reads\n'West of house\nThis is an open field west of a white house, with a boarded front door.\nThere is a small mailbox here', the bellow thext is obscured."
lapTop.readable = True
lapTop.words = ['laptop', 'computer','notebook','machine','dell inspiron 14r']

objReadMe = {'self':readMe,'name':readMe.name}
objWoodTable = {'self':woodTable,'name':woodTable.name}
objTest = {'self':testObj,'name':testObj.name}
objKey = {'self':key0,'name':key0.name}
objLaptop = {'self':lapTop,'name':lapTop.name}

# Directions (North, South, East, West, NE,ES,SW,WN, in, out, up, down)

# Directions to 'not reachable' areas [wip to go with the 'go' commands]
class Blockage:
    blkgBool = True # Why does this even exists?
    def __init__(self, text):
        self.text = text #The text to say when you encounter it

wall = Blockage("There is a wall there.")
empty = Blockage("There is nothing there.")
ceiling = Blockage("There is the ceiling there.")
floor = Blockage("It is a solid floor.")
unknown = Blockage("I don't think it is possible.")
already = Blockage("I'm already here.")
blockageList = (wall,empty,ceiling,floor,unknown,already)
#---Door--- That only are used when there is a door to unlock
class Door:
    lockedText = "It seems to be locked"
    def __init__(self, lockedBool, r1, r2):
        self.name = "" #Name not needed
        self.locked = lockedBool
        self.lockedText = "There is a locked door here."
        self.connectedRooms = (r1,r2) #The 2 rooms that will be connected by this door
        self.keyItem = ()

#---Class Room---
class Room:
    def __init__(self, name, longDesc, shortDesc):
        self.name = name
        self.longDescription = longDesc
        self.shortDescription = shortDesc
        #                  The rooms/blockages in each direction
        #                   N,   S,   E,    W,  NE,  ES,  SW,  WN,  in,   out,  up,     down - 11
        self.connections = (wall,wall,wall,wall,wall,wall,wall,wall,empty,empty,ceiling,floor)
        self.items = [] # Make it like the inventory(?)

    def descItems(self):
        if len(self.items) > 0:
            for item in self.items:
                print("")
                print(item.groundDesc)


#---Rooms/Doors--- # Doors are placed after the two rooms you want to connect
darkRoom0 = Room("Dark room",
                "I'm in a room with a very dim light source that comes from above, there is a door to somewhere to the North.",
                "It is a room with dim light.")
dripRoom1 = Room("Puddle room",
                "I'm in a room with faded light and a puddle formed with water dripping from the ceiling, to the South there is a door to a dark room, to the West there is a door to somewhere and another door to the North.",
                "It's a room with water dripping from the ceiling.")
key_Room2 = Room("Strange room",
                "I'm in an oddly feeling room, there is a door to another room to the East",
                "It's an odd room, for some reason.")
finlRoom3 = Room("Marble room",
                "I'm in a room with marble beige walls, there is a door leading to another room to the South.",
                "It is a room with a laptop on the floor.")
lckdDoor0 = Door(True, finlRoom3, dripRoom1)
lckdDoor0.keyItem = key0

#                       (North0, South1, East2, West3, NE,ES,SW,WN, in, out, up, down)
darkRoom0.connections = (dripRoom1,wall,wall,wall,wall,wall,wall,wall,empty,unknown,ceiling,floor)
dripRoom1.connections = [lckdDoor0, darkRoom0, wall, key_Room2,wall,wall,wall,wall,already,unknown,ceiling,floor]
dripRoom1.items = [woodTable]

key_Room2.connections = (wall,wall,dripRoom1,wall,wall,wall,wall,wall,already,unknown,ceiling,floor)
key_Room2.items = [key0]

finlRoom3.connections = (wall,dripRoom1,wall,wall,wall,wall,wall,wall,empty,unknown,ceiling,floor)
finlRoom3.items = [lapTop]
# locked door list
lockedList = [lckdDoor0]

#--- Special uses for items

# Key
key0.usable = True
def k0r():
    if player.position == dripRoom1:
        #repEl(dripRoom1.connections, lckdDoor0, 0, finlRoom3)
        print("Please don't.")
    else:
        print("I can't use this here.")

key0.useResult = k0r
# Laptop
lapTop.usable = True
def l0t():
    write("On the strange program terminal, you write 'quit' and press enter.",0.05)
    print("")
    write("the program returns 'Are you sure you want to quit?', you write 'y' and press enter.", 0.05)
    print("")
    write("The program suddently exits-",0.04)
    sleep(1)
    print("")
    os.system("clear")
    exit()
lapTop.useResult = l0t
#---Map--- Model of game map
#  W← N↑ S↓ E→
#
#          [4]
#           ↑  Locked door (key on [3] )
#       [3][2]
#          [1] Start room
#

#---Call player---
player = Player('Player', darkRoom0) #Placeholder
player.inventory = [readMe]

#---Cmd class--- # Don't even ask me how this works
class userInput(cmd.Cmd):
    prompt = "\n»" # Some good exmaples I found: > » 🠶 $

    def default(self, arg): #What to say when there is no known command
        print("Sorry, I can't understand that | Type 'help' for command list")

    def do_quit(self, arg):
        """Quit the game."""
        print('\nAre you sure? All unsaved progress will be lost.')
        quiOpt = input('[yes/no]»')
        if quiOpt.lower() in yesModel:
            return True


    def help_save(self):
        print("Save system is [WIP].")

    def do_look(self, arg): # WIP
        """Use 'look around' to show what's around you,
        use 'look inventory' to show your items and
        use 'look at [object]' to look at an specific object."""
        lookAt = arg.split()

        if arg.lower() == 'around':
            print(player.position.longDescription)
            pr = player.position
            pr.descItems()
        elif arg.lower() == 'inventory':
            if len(player.inventory) > 0:
                print("In your inventory you have:")
                for item in player.inventory:
                    print('|',item.name)
            else:
                print("Inventory is empty.")
        elif len(lookAt) > 0 and lookAt[0] == 'at':
            if len(lookAt) > 1:
                pr = player.position
                lookAt.pop(0)
                lit = ' '.join(lookAt)
                inRes = 7
                gdRes = 7
                #print(player.inventory)
                #player.lookObIn(lit)
                #pr.lookObGd(lit)
                for i in player.inventory:
                    #print(i)
                    #print(i.name)
                    ene = {'ld':i.longDesc,'wd':i.words}
                    #print(ene)
                    if lit in ene['wd']:
                        print(ene['ld'])
                        inRes = 10
                for i in pr.items:
                    #print(i)
                    #print(i.name)
                    ene = {'ld':i.longDesc,'wd':i.words}
                    #print(ene)
                    if lit in ene['wd']:
                        print(ene['ld'])
                        gdRes = 20
                if inRes + gdRes == 14:
                    print("I can't seem to find this item.")

            else:
                print("Look at what?")

        else:
            print("Look what?")

    def do_go(self, arg): # WIP
        """This command moves the player to a certain direction.
The directions are North, South, East, West, Notheast,
Southeast, Southwest, Northwest, In, Out, Up and Down"""
#(N 0, S 1, E 2, W 3, NE 4,SE 5,SW 6,NW 7, in 8, out 9, up 10, down 11
        goDir = arg.lower() #lower() to make everything lowercase
        doGoDir = 100 # failsafe, kinda

        if goDir in nothModel: # Directions:
            doGoDir = dirN
            goTex = "north"
        if goDir in southModel:
            doGoDir = dirS
            goTex = "south"
        if goDir in eastModel:
            doGoDir = dirE
            goTex = "east"
        if goDir in westModel:
            doGoDir = dirW
            goTex = "west"
        if goDir in nestModel:
            doGoDir = dirNE
            goTex = "north east"
        if goDir in sestModel:
            doGoDir = dirSE
            goTex = "south east"
        if goDir in swstModel:
            doGoDir = dirSW
            goTex = "south west"
        if goDir in nwstModel:
            doGoDir = dirNW
            goTex = "north west"
        if goDir in inModel:
            doGoDir = dirIn
            goTex = "inside"
        if goDir in outModel:
            doGoDir = dirOut
            goTex = "out"
        if goDir in upModel:
            doGoDir = dirUp
            goTex = "up"
        if goDir in downModel:
            doGoDir = dirDown
            goTex = "down"



        if doGoDir < 100: #the, kinda, ailsafe
            if player.position.connections[doGoDir] not in blockageList:
                if player.position.connections[doGoDir] in lockedList: #if it's a locked door
                    print(player.position.connections[doGoDir].lockedText)
                else: #If it's a valid room
                    player.position = player.position.connections[doGoDir]
                    print("You go",goTex, "and get to", player.position.name)
                    print(player.position.longDescription)
                    pr = player.position
                    pr.descItems()
            else: #Print the blockage text
                print(player.position.connections[doGoDir].text)
        else:
            print("Invalid direction, please use 'help go' to see list of directions.")

    def do_take(self, arg):
        """This takes an item from the room you are, if it is able to be taken."""
        pr = player.position
        #print(len(pr.items))
        if len(pr.items) > 0:
           for i in pr.items:
               #print(i.words)
               if arg in i.words:
                   if i.pickable == True:
                       player.inventory.append(i)
                       print("You got %s" %i.name)
                       pr.items.pop(pr.items.index(i))
                   else:
                       print("It's better to keep this where it is.")
               else:
                   if pr.items.index(i) == len(pr.items)-1:
                       print("I can't find this item.")
        elif len(pr.items) < 1:
            print("I can't find this item.")

    def do_drop(self, arg):
        """This drops an item from the your inventory to the room you are."""
        pr = player.position
        #print(len(pr.items))
        if len(player.inventory) > 0:
           for i in player.inventory:
               #print(i.words)
               if arg in i.words:
                   pr.items.append(i)
                   print("You dropped %s" %i.name)
                   player.inventory.pop(player.inventory.index(i))
               else:
                   if player.inventory.index(i) == len(player.inventory)-1:
                       print("I don't think I have this item.")
        elif len(player.inventory) < 1:
            print("I don't have anything to drop.")

    def do_use(self, arg):
        """Interact with something on the room or your inventory."""
        if len(arg) > 0:
            pr = player.position
            lit = arg
            inRes = 7
            gdRes = 7
            #print(player.inventory)
            #player.lookObIn(lit)
            #pr.lookObGd(lit)
            for i in player.inventory:
                #print(i)
                #print(i.name)
                ene = {'ld':i.usable ,'wd':i.words,'rs':i.useResult}
                #print(ene)
                if lit in ene['wd']:
                    if ene['ld'] == True:
                        i.useResult()
                    else:
                        print("I can't use this.")
                    inRes = 10
            for i in pr.items:
                #print(i)
                #print(i.name)
                ene = {'ld':i.usable ,'wd':i.words,'rs':i.useResult}
                #print(ene)
                if lit in ene['wd']:
                    if ene['ld'] == True:
                        i.useResult()
                    else:
                        print("I can't use this.")
                    gdRes = 20
            if inRes + gdRes == 14:
                print("I can't seem to find this.")
        else:
            print("Use what?")

    def do_unlock(self, arg): #WIP
        """Unlock things that need to be unlocked, use 'unlock <thing> with <item>'. WIP"""
        unLocc = arg.split()
        if len(unLocc) == 3 and unLocc[1] == 'with':
            if unLocc[0] == 'door':
                for i in player.position.connections:
                    if i in lockedList:
                        enn = i
                        for k in player.inventory:
                            if unLocc[2] in k.words:
                                #print(k.name)
                                #print(i)
                                #print(enn.keyItem.name)
                                if k == enn.keyItem:
                                    repEl(player.position.connections, i, player.position.connections.index(i), i.connectedRooms[0])
                                    print('You use %s, and the door unlocks.' %k.name)
                                else:
                                    print("I can't open this door with %s" %k.name)


        else:
            print("Sorry, but I can't undestand that. Type 'help unlock' to see how to use this")

    def do_read(self, arg):
        """Read the text of something that has text"""
        if len(arg) > 0:
            pr = player.position
            lit = arg
            inRes = 7
            gdRes = 7
            #print(player.inventory)
            #player.lookObIn(lit)
            #pr.lookObGd(lit)
            for i in player.inventory:
                #print(i)
                #print(i.name)
                ene = {'ld':i.readable ,'wd':i.words,'rs':i.longDesc}
                #print(ene)
                if lit in ene['wd']:
                    if ene['ld'] == True:
                        print(i.texto)
                    else:
                        print("I can't read this.")
                    inRes = 10
            for i in pr.items:
                #print(i)
                #print(i.name)
                ene = {'ld':i.readable ,'wd':i.words,'rs':i.longDesc}
                #print(ene)
                if lit in ene['wd']:
                    if ene['ld'] == True:
                        print(i.texto)
                    else:
                        print("I can't read this.")
                    gdRes = 20
            if inRes + gdRes == 14:
                print("I can't seem to find this.")
        else:
            print("Use what?")

    def do_ttuff(self, arg): #jftsod
        """Just for testing something"""
        write("Somebody once told me the world is gonna roll me.", 0.05)

    def do_clear(self, arg):
        """Use this to clear the screen."""
        os.system('clear')

    do_exit = do_quit
    do_pick = do_take
    do_get = do_take

#---Text wrap stuff---
def write(text, time):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        sleep(time)


#---Title screen---
def titleScreen():
    os.system('clear')
    print("  ╔═════════════╗")
    print("  |  adv≡nture  |")
    print("  ╚═════════════╝")
    write("   ~Bottom text~ \n",0.08)
    print("")
    sleep(0.08)
    print(" [start|help|quit]")
    write(" By Waces-----2018",0.08)

if __name__ == '__main__':
    sleep(1.08)
    os.system('clear')
    #titleScreen()
    #sleep(0.08)
    write("Just look around", 0.08)
    print("")
    userInput().cmdloop()
    print('\nThanks for playing!')
    sleep(2)
    os.system('clear')
