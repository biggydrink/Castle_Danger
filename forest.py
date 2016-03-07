__author__ = 'abutz'

import random
import time
import sys

# ~~~~~~~~~~~~~~~~~~~~~~~~ Define the classes ~~~~~~~~~~~~~~~~~~~~~~~~

class Room:
    """
    Rooms are the basic building blocks of the game. Each one has its own setting (description) that the player can
    read when they "enter" the room, and every room should be mapped to at least one other room via the self.north,
    self.south, etc variables. Each room has a default mob (monster) type that is created when the room is created.
    That mob is also added to self.moblist to keep track of what mobs are in what room, and to help access the mob's
    data.
    """

    def __init__(self,name,exits,setting,defaultMobType):
        self.name = name
        self.exits = exits
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.setting = setting
        self.defaultMobType = defaultMobType
        self.mobList = []
        self.createMob()

#inventory function shows list of items
# use items
#

    def __str__(self):
        return "This room is the " + self.name

    def getSetting(self):
        """
        Gets the description of the room that the player will see in the game. Used in the setting() function.
        """
        description = self.setting + "\n"
        if self.mobList != []:
            for mob in self.mobList:
                description += mob.setting
        return description

    def getExits(self):
        """
        Returns the possible exits from this room as a string. Used as part of the game's basic info/prompt screen
        in prompt()
        """
        exitstring = ""
        for i in range(len(self.exits)):
            exitstring += str(self.exits[i])
        return exitstring

    def getName(self):
        """
        Returns the name of the room. Used in prompt()
        """
        return self.name

    def createMob(self):
        """
        Create a mob in this room.
        """
        if self.defaultMobType != None:
            mob = Monster(self.defaultMobType)
            self.mobList.append(mob)
#           mob.addRoom(self)

    def behave(self):
        """
        Runs the mob's behavior method. These are located in the Monster class, and can be plugged in as a starting
        variable for the mob to determine it's normal behavior.
        """
        for mob in self.mobList:
            mob.funcBehave()

class Character:
    """
    The player's character. Stats are currently HP, attack, and defense, although these could be expanded upon.
    The player also has a dictionary of equipped items and a dictionary of inventory items. Dictionaries are used
    instead of lists so that the item.name can be displayed
    """

    def __init__(self, name):
        self.name = name
        self.maxhp = random.randint(100, 120)
        self.hp = self.maxhp
        self.attack = random.randint(13, 18)
        self.defense = random.randint(3, 7)
        self.equippedDict = {}
        self.inventoryDict = {}

    def die(self):
        print("Oh no, you are dying...")
        print("You have died.")
        print("You can try again, if you want to improve on your FAILURE.")
        sys.exit()

class Monster:

    def __init__(self, name):
        self.name = name
        self.funcBehave = self.defaultBehavior
        self.inventoryList = []
        self.equippedList = []
        if name == "Ladybug":
            self.hp = 20
            self.attack = 5
            self.defense = 0
            self.setting = "There is a ladybug here." #change this to a description of the ladybug/monster
        if name == "Super Ladybug":
            self.hp = 50
            self.attack = 8
            self.defense = 2
            self.setting = "Whoa, a giant ladybug is here!! How did it get so huge? Why does it have a sword?!?"
            self.createItem("Longsword")
            self.createItem("Polkadot shirt")
            self.createItem("Polkadot pants")
            self.createItem("Potion")
            self.funcBehave = self.attackBehavior
        if name == "Will'o Wisp":
            self.hp = 45
            self.attack = 10
            self.defense = 1
            self.setting = "There's a Will'o Wisp here."
            self.createItem("Potion")
        if name == "Swamp Thing":
            self.hp = 100
            self.attack = 12
            self.defense = 5
            self.setting = "The Swamp Thing from the movie is here!"
            self.createItem("Oozy shirt")
            self.createItem("Oozy pants")
            self.createItem("Green sword")
            self.createItem("Potion")
            self.funcBehave = self.attackBehavior
        if name == "Volcano Golem":
            self.hp = 75
            self.attack = 8
            self.defense = 10
            self.setting = "A volcano golem is here."
            self.createItem("Potion")
        if name == "Black Dragon":
            self.hp = 200
            self.attack = 15
            self.defense = 15
            self.setting = "A... a black dragon is here. GULP."
            self.createItem("Charred leather vest")
            self.createItem("Charred leather pants")
            self.createItem("Blackened Sword")
            self.createItem("Mega potion")
            self.createItem("Mega potion")
            self.funcBehave = self.attackBehavior
        if name == "Foppish Palace Guard":
            self.hp = 125
            self.attack = 15
            self.defense = 15
            self.setting = "A foppish palace guard is here, fixing his hair in the mirror."
            self.createItem("Potion")
        if name == "The Corrupt and Nasty King (of destruction-ness and killing)":
            self.hp = 400
            self.attack = 20
            self.defense = 20
            self.setting = "The Corrupt and Nasty King (of destruction-ness and killing) is here, waiting for you to FINISH HIM"
            self.createItem("Shiny new breastplate")
            self.createItem("Shiny new legplates")
            self.funcBehave = self.attackBehavior

    def defaultBehavior(self):
        print(self.name + " watches you.")

    def attackBehavior(self):
        print(self.name + " attacks you!")
        attack()

    def createItem(self, item):
        new_item = Item(item)
        self.inventoryList.append(new_item)

    def die(self):
        currentroom.mobList.remove(self)
        print(self.name + " has died!")
        for item in self.inventoryList:
            global player
            player.inventoryDict[item.name] = item
            print("You got a " + item.name)


class Item:
    def __init__(self,name):
        self.name = name
        if self.name == "Balloon animal sword":
            self.setting = \
                (
                "It's a \"sword\" made out of those skinny balloons that balloon animals are made out"
                "of. You really should probably find something else to use if you can.."
                ),
            self.attack = 1
            self.defense = 0
            self.hp = 0
        if self.name == "Longsword":
            self.setting = "Finally, a sword! This should be useful. Don't ask why ladybugs have these."
            self.attack = 4
            self.defense = 0
            self.hp = 0
        if self.name == "Shabby Shirt":
            self.setting = "A pretty shabby shirt. Should probably shrug this off shoon. Soon."
            self.attack = 0
            self.defense = 1
            self.hp = 0
        if self.name == "Flimsy Pants":
            self.setting = "Flimsy pants. I mean, you really don't want to be wearing something so flimsy, right??"
            self.attack = 0
            self.defense = 1
            self.hp = 5
        if self.name == "Polkadot shirt" or self.name == "Polkadot pants":
            self.setting = "It's black polkadots on a red background. Well, you got it from a ladybug, right?"
            self.attack = 0
            self.defense = 2
            self.hp = 5
        if self.name == "Oozy shirt":
            self.setting = "Well, it came from a swamp thingy, right? Still better than your shabby shirt."
            self.attack = 0
            self.defense = 4
            self.hp = 10
        if self.name == "Oozy pants":
            self.setting = "Well, it came from a swamp thingy, right? Debatably better than your flimsy pants. Kind of gross, really."
            self.attack = 0
            self.defense = 4
            self.hp = 10
        if self.name == "Green sword":
            self.setting = "There's no reason a green sword should be better than a longsword, but it is."
            self.attack = 8
            self.defense = 0
            self.hp = 5
        if self.name == "Charred leather vest":
            self.setting = "A leather vest that looks pretty cooked. Durable though."
            self.attack = 0
            self.defense = 6
            self.hp = 15
        if self.name == "Charred leather pants":
            self.setting = "Some leather pants that look pretty cooked. Cuz you're on FIRE!! I mean not for real though, don't worry."
            self.attack = 0
            self.defense = 6
            self.hp = 15
        if self.name == "Blackened Sword":
            self.setting = "This sword used to be shinier, but its previous owner was a 10 packs-a-day smoker."
            self.attack = 11
            self.defense = 0
            self.hp = 0
        if self.name == "Shiny new breastplate" or self.name == "Shiny new legplates":
            self.setting = "Some actual armor. Finally!"
            self.attack = 0
            self.defense = 8
            self.hp = 20
        if self.name == "Potion":
            self.setting = "Gotta drink that potion."
            self.attack = 0
            self.defense = 0
            self.hp = 50
        if self.name == "Mega potion":
            self.setting = "MOAR POTION"
            self.attack = 0
            self.defense = 0
            self.hp = 150

# command class? each command gets a method, then make a dict/list and link the user commands to the methods. make them upper()

# ~~~~~~~~~~~~~~~~~~~~~~~~ Create the rooms ~~~~~~~~~~~~~~~~~~~~~~~~

Starter = Room("Deep Dark Forest",  # name
               ["N", "S", "E", "W"],  # exits
               "You are at the edge of a deep, dark forest to the north, a swampy swamp to the east, a volcano to the \n"
               "south, and a big fancy-looking palace to the west. \n"
               "(Hint: Head north first, then east, then south, and then west.)",  # setting
               None)  # mobs

# Dark Forest rooms

DarkForest0 = Room("Deeper Into the Deep Dark Forest",  # name
                   ["N", "S"],  # exits
                   "You're moving deeper into the forest. It looks like the trail leads north and south.",  # setting
                   "Ladybug")  # mobs

DarkForest1 = Room("Even Deeper Into the Deep Dark Forest",
                   ["N", "S"],
                   "Continuing on the trail deeper into the forest. It's starting to get a little darker, and the \n"
                   "trees are looking a little bigger",
                   "Ladybug",)

DarkForest2 = Room("So Deep Into the Deep Dark Forest",
                   ["N", "S"],
                   "This forest really is deep!",
                   "Ladybug",)

DarkForest3 = Room("Pretty Deep Now Into the Deep Dark Forest",
                   ["N", "S"],
                   "It's starting to get dark now too.",
                   "Ladybug",)

DarkForest4 = Room("Definitely Very Deep Now Into the Deep Dark Forest",
                   ["N", "S"],
                   (
                   "You're quite deep into the forest now. The trees are so massive and so thick that it's pretty \n"
                   "dark. You think you can see a little bit of a clearing ahead to the north though."
                   ),
                   "Ladybug",)

DarkForestEnd = Room("A Clearing in the Deep Dark Forest",
                     ["S"],
                     "You've found a clearing way into the forest. Looks like something big might have knocked down\n"
                     "these trees.",
                     "Super Ladybug",)

DarkForestRooms = [DarkForest0, DarkForest1, DarkForest2, DarkForest3, DarkForest4, DarkForestEnd]

# Swampy Place rooms

SwampyPlace0 = Room("Entering the Swampy Swamp",  # name
                    ["E", "W"],  # exits
                    "You're entering a murky swamp. There is a path though--looks like it's taking you further east.",  # setting
                    "Will'o Wisp")  # mobs

SwampyPlace1 = Room("The Swampy Swamp",
                    ["E", "W"],
                    "Further into the swampy swamp. There are lots of mosquitoes around!",
                    "Will'o Wisp")

SwampyPlace2 = Room("The Swampy Swamp",
                    ["E", "W"],
                    "You continue to trudge through the swampy swamp. It's pretty... swampy.",
                    "Will'o Wisp")



SwampyPlace3 = Room("The Swampy Swamp",
                    ["E", "W"],
                    "You find yourself in yet more of the swampy swampy swamp.",
                    "Will'o Wisp")

SwampyPlace4 = Room("The Swampy Swamp",
                    ["E", "W"],
                    "You're starting to get sick of the muck in this swampy swamp. But, there you are, in the thick of it",
                    "Will'o Wisp")

SwampyPlace5 = Room("The Swampy Swamp",
                    ["E", "W"],
                    "Swampy swamp swamp swamp, swampy swampy swamp swampy, swampy swampy swampy swamp. Swamp.",
                    "Will'o Wisp")

SwampyPlace6 = Room("The Swampy Swamp",
                    ["E", "W"],
                    "FINALLY, it looks like you might be coming to a clearing up ahead. Either that, or it's the \n"
                    "swampiest area you've found yet!",
                    "Will'o Wisp")

SwampyPlaceEnd = Room("The Swampy Swamp",
                      ["W"],
                      "Foiled again! Actually this is the swampiest area you've come across yet!",
                      "Swamp Thing")

SwampyPlaceRooms = [SwampyPlace0, SwampyPlace1, SwampyPlace2, SwampyPlace3, SwampyPlace4, SwampyPlace5, SwampyPlace6,
                    SwampyPlaceEnd]

VolcanoArea0 = Room("Entering the Volcano",  # name
                    ["N", "S"],  # exits
                    "You've entered the realm of the volcano. It's quite a blasted landscape, just long fields of \n"
                    "almost nothing but black, jagged rock.",  # setting
                    "Volcano Golem")  # mobs

VolcanoArea1 = Room("The Volcano",
                    ["N", "S"],
                    "Your footsteps make a crunching sound as you walk across the cooled lava landscape.",
                    "Volcano Golem")

VolcanoArea2 = Room("The Volcano",
                    ["N", "S"],
                    "Your footsteps make a crunching sound as you walk across the cooled lava landscape.",
                    "Volcano Golem")

VolcanoArea3 = Room("The Volcano",
                    ["N", "S"],
                    "Your footsteps make a crunching sound as you walk across the cooled lava landscape.",
                    "Volcano Golem")

VolcanoArea4 = Room("The Volcano",
                    ["N", "S"],
                    "Your footsteps make a crunching sound as you walk across the cooled lava landscape. It's \n"
                    "starting to get pretty hot.",
                    "Volcano Golem")

VolcanoArea5 = Room("The Volcano",
                    ["N", "S"],
                    "It's REALLY hot now, you're not sure if you can go much farther. There's a cave further to the \n"
                    "south.",
                    "Volcano Golem")

VolcanoAreaEnd = Room("The Volcano",
                      ["N"],
                      "Inside the cave there's treasure everywhere, rubies and gold and all the wealth you can \n"
                      "imagine. Too bad there's no money in this game.",
                      "Black Dragon")


VolcanoAreaRooms = [VolcanoArea0, VolcanoArea1, VolcanoArea2, VolcanoArea3, VolcanoArea3, VolcanoArea4, VolcanoArea5,
                    VolcanoAreaEnd]

FancyPalace0 = Room("Entering the Fancy Palace",  # name
                    ["E", "W"],  # exits
                    "As you walk into the palace, you become acutely aware of your sweaty, unkempt nature. I mean, \n"
                    "it's understandable, but really, you DO look out of place. You try to wipe your feet on the \n"
                    "welcome mat.",  # setting
                    "Foppish Palace Guard")  # mobs

FancyPalace1 = Room("The Fancy Palace",
                    ["E", "W"],
                    "You find yourself distracted by the giant tapestries and other fancy furnishings in this place.",
                    "Foppish Palace Guard")

FancyPalace2 = Room("The Fancy Palace",
                    ["E", "W"],
                    "You find yourself distracted by the giant tapestries and other fancy furnishings in this place. \n"
                    "It's really quite... fancy.",
                    "Foppish Palace Guard")

FancyPalace3 = Room("The Fancy Palace",
                    ["E", "W"],
                    "You find yourself distracted by the giant tapestries and other fancy furnishings in this place. \n"
                    "It's really quite... fancy.",
                    "Foppish Palace Guard")

FancyPalace4 = Room("The Fancy Palace",
                    ["E", "W"],
                    "You find yourself distracted by the giant tapestries and other fancy furnishings in this place. \n"
                    "It's really quite... fancy.",
                    "Foppish Palace Guard")

FancyPalace5 = Room("The Fancy Palace",
                    ["E", "W"],
                    "You didn't think it was possible, but this place starts to get MORE fancy (and pretentious).",
                    "Foppish Palace Guard")

FancyPalace6 = Room("The Fancy Palace",
                    ["E", "W"],
                    "It's getting really opulent in here. Somebody apparently thinks they are a pretty big deal.",
                    "Foppish Palace Guard")

FancyPalace7 = Room("The Fancy Palace",
                    ["E", "W"],
                    "The fanciest doors you've ever seen are straight ahead of you.",
                    "Foppish Palace Guard")

FancyPalaceEnd = Room("The Fancy Palace",
                      ["E"],
                      "You've reached the throme room of the Fancy Palace. This is the fanciest fancy pants place \n"
                      "you've ever seen or even heard of.",
                      "The Corrupt and Nasty King (of destruction-ness and killing)")

FancyPalaceRooms = [FancyPalace0, FancyPalace1, FancyPalace2, FancyPalace3, FancyPalace4, FancyPalace5, FancyPalace6,
                    FancyPalace7, FancyPalaceEnd]

# ~~~~~~~~~~~~~~~~~~~~~~~~ Mapping the rooms ~~~~~~~~~~~~~~~~~~~~~~~~

# Starter map
Starter.north = DarkForest0
Starter.south = VolcanoArea0
Starter.east = SwampyPlace0
Starter.west = FancyPalace0

#Deep Dark Forest map
DarkForest0.north = DarkForest1
DarkForest0.south = Starter
DarkForest1.north = DarkForest2
DarkForest1.south = DarkForest0
DarkForest2.north = DarkForest3
DarkForest2.south = DarkForest1
DarkForest3.north = DarkForest4
DarkForest3.south = DarkForest2
DarkForest4.north = DarkForestEnd
DarkForest4.south = DarkForest3
DarkForestEnd.south = DarkForest4

#Swampy Swamp map
SwampyPlace0.east = SwampyPlace1
SwampyPlace0.west = Starter
SwampyPlace1.east = SwampyPlace2
SwampyPlace1.west = SwampyPlace0
SwampyPlace2.east = SwampyPlace3
SwampyPlace2.west = SwampyPlace1
SwampyPlace3.east = SwampyPlace4
SwampyPlace3.west = SwampyPlace2
SwampyPlace4.east = SwampyPlace5
SwampyPlace4.west = SwampyPlace3
SwampyPlace5.east = SwampyPlace6
SwampyPlace5.west = SwampyPlace4
SwampyPlace6.east = SwampyPlaceEnd
SwampyPlace6.west = SwampyPlace5
SwampyPlaceEnd.west = SwampyPlace6

#The Volcano map
VolcanoArea0.north = Starter
VolcanoArea0.south = VolcanoArea1
VolcanoArea1.north = VolcanoArea0
VolcanoArea1.south = VolcanoArea2
VolcanoArea2.north = VolcanoArea1
VolcanoArea2.south = VolcanoArea3
VolcanoArea3.north = VolcanoArea2
VolcanoArea3.south = VolcanoArea4
VolcanoArea4.north = VolcanoArea3
VolcanoArea4.south = VolcanoArea5
VolcanoArea5.north = VolcanoArea4
VolcanoArea5.south = VolcanoAreaEnd
VolcanoAreaEnd.north = VolcanoArea5

#Fancy Palace map
FancyPalace0.east = Starter
FancyPalace0.west = FancyPalace1
FancyPalace1.east = FancyPalace0
FancyPalace1.west = FancyPalace2
FancyPalace2.east = FancyPalace1
FancyPalace2.west = FancyPalace3
FancyPalace3.east = FancyPalace2
FancyPalace3.west = FancyPalace4
FancyPalace4.east = FancyPalace3
FancyPalace4.west = FancyPalace5
FancyPalace5.east = FancyPalace4
FancyPalace5.west = FancyPalace6
FancyPalace6.east = FancyPalace5
FancyPalace6.west = FancyPalace7
FancyPalace7.east = FancyPalace6
FancyPalace7.west = FancyPalaceEnd
FancyPalaceEnd.east = FancyPalace7


roomlist = [Starter, DarkForestRooms, SwampyPlaceRooms, VolcanoAreaRooms, FancyPalaceRooms]

global currentroom
currentroom = Starter

# attack gives list of creatures in room, cna choose which to attack?

# ~~~~~~~~~~~~~~~~~~~~~~~~ Creating functions ~~~~~~~~~~~~~~~~~~~~~~~~

def create_player():
    global player
    player = Character(input("What is your name, Mr/Ms Would-be Hero?: "))
    if player.name == "Mr. Would-be Hero" or player.name == "Ms. Would-be Hero":
        print("Wow, just TOO unoriginal, I'm sorry - try again.")
        player = Character(input("What is your name, Mr/Ms Would-be Hero?: "))
    print("OK " + player.name + "! Let's go on a totally radical adventure!")

def setting():
    print(currentroom.getSetting())
    currentroom.behave()

def prompt():
    print("<" + currentroom.getName() + " : " + str(player.hp) + "/" + str(player.maxhp) + "HP : " + currentroom.getExits() + ">", end="")

def inputcommand():
    while True:
        command = input(" ")
        commandlist = command.split()
        if len(commandlist) > 1 and commandlist[0].upper() in commandsDict:
            if len(commandlist) > 3:
                argument = commandlist[1] + " " + commandlist[2] + " " + commandlist[3]
            elif len(commandlist) > 2:
                argument = commandlist[1] + " " + commandlist[2]
            else:
                argument = commandlist[1]
            commandsDict[commandlist[0].upper()](argument)
            prompt()
        elif commandlist[0].upper() in commandsDict:
            commandsDict.get(commandlist[0].upper())()
            prompt()
        else:
            print("Um, wait what?", end=" ")
            prompt()

def gonorth():
    global currentroom
    if currentroom.north == None:
        print("You can't go that way from here.")
    else:
        currentroom = currentroom.north
        setting()

def gosouth():
    global currentroom
    if currentroom.south == None:
        print("You can't go that way from here.")
    else:
        currentroom = currentroom.south
        setting()

def goeast():
    global currentroom
    if currentroom.east == None:
        print("You can't go that way from here.")
    else:
        currentroom = currentroom.east
        setting()

def gowest():
    global currentroom
    if currentroom.west == None:
        print("You can't go that way from here.")
    else:
        currentroom = currentroom.west
        setting()

def attack():
    global player
    monster_attacked = currentroom.mobList[0]
    while player.hp > 0 and monster_attacked.hp > 0:
        player.hp -= monster_attacked.attack - player.defense
        if player.hp > player.maxhp:
            player.hp = player.maxhp
        monster_attacked.hp -= player.attack - monster_attacked.defense

        if monster_attacked.attack > 18: mobattackstring = "HARD!!"
        elif monster_attacked.attack > 14: mobattackstring = "omg so hard"
        elif monster_attacked.attack > 12: mobattackstring = "...ouch!"
        elif monster_attacked.attack > 10: mobattackstring = "pretty hard."
        elif monster_attacked.attack > 7: mobattackstring = "kinda hard."
        elif monster_attacked.attack > 5: mobattackstring = "kinda."
        else: mobattackstring = "a little bit."

        if player.attack > 18: playerattackstring = "HARD!!"
        elif player.attack > 14: playerattackstring = "omg so hard"
        elif player.attack > 12: playerattackstring = "...ouch!"
        elif player.attack > 10: playerattackstring = "pretty hard."
        elif player.attack > 7: playerattackstring = "kinda hard."
        elif player.attack > 5: playerattackstring = "kinda."
        else: playerattackstring = "a little bit."

        print(monster_attacked.name + " hits you " + mobattackstring)
        print("You hit " + monster_attacked.name + " " + playerattackstring)
        prompt()
        print("\n")
        if monster_attacked.hp > 0 and player.hp > 0:
            time.sleep(2)
    if monster_attacked.hp <= 0:
        monster_attacked.die()
    if player.hp <= 0:
        player.die()

def look(argument=0):
    invlist = list(player.inventoryDict.keys())
    eqlist = list(player.equippedDict.keys())
    if argument == 0:
        setting()
    elif argument in invlist:
        itemref = player.inventoryDict.get(argument)
        print(itemref.setting)
    elif argument in eqlist:
        itemref = player.equippedDict.get(argument)
        print(itemref.setting)
    else:
        print("Look at what?")

def inventory():
    if len(player.inventoryDict) == 0:
        print("You are carrying:")
        print("Wait... you aren't carrying anything.")
    else:
        print("You are carrying:")
        invlist = list(player.inventoryDict.keys())
        for item in invlist:
            print(item)
#        for item in player.inventoryDict:
#            print(item.name)

def equip(item=0):
    """
    With no arguments, shows a list of currently equipped items.
    With an argument, equips an item.
    """
    if item == 0:
        eqkeylist = list(player.equippedDict.keys())
        print("You are wearing: ")
        if len(eqkeylist) == 0:
            print("Nothing!")
        else:
            for item in eqkeylist:
                print(item)
    elif item == "Potion" or item == "Mega potion":
        print("Um, you can't equip a potion, smarty pants.")
    else:
        invkeylist = list(player.inventoryDict.keys())
        if item in invkeylist:
            itemref = player.inventoryDict.get(item) # gets itemref so we can use it to reference the object itself
            player.equippedDict[itemref.name] = itemref # adds the object to the equipped dictionary
            player.maxhp += itemref.hp
            player.attack += itemref.attack
            player.defense += itemref.defense
            print("You equip your " + itemref.name + ".")
            player.inventoryDict.pop(item) # removes item from inventory
        else:
            print("You aren't carrying that item.")

def unequip(item=0):
    """
    Unequips an item.
    Removes it from the equipped dictionary and adds it to the inventory dictionary.
    """
    if item == 0:
        print("Unequip what?")
    else:
        keylist = list(player.equippedDict.keys())
        if item in keylist:
            itemref = player.equippedDict.get(item) # creates a reference to the object itself
            player.equippedDict.pop(item) # removes the item from the equipped dictionary
            player.inventoryDict[itemref.name] = itemref # adds the item to the inventory dictionary
            player.maxhp -= itemref.hp
            if player.hp > player.maxhp:
                player.hp = player.maxhp
            player.attack -= itemref.attack
            player.defense -= itemref.defense
            print("You unequip your " + itemref.name + ".")
        else:
            print("You don't have that item equipped.")

def drop(item=0):
    """
    Removes an item from inventory.
    """
    if item == 0:
        print("Drop what?")
    else:
        keylist = list(player.inventoryDict.keys())
        if item in keylist:
            itemref = player.inventoryDict.get(item)
            player.inventoryDict.pop(item) # remove item from inventory)
            print("You drop your " + itemref.name + ".")
        else:
            print("You don't have that item.")

def use(item=0):
    """
    Gets a one-time use out of the item.
    """
    if item == 0:
        print("Use what?")
    else:
        keylist = list(player.inventoryDict.keys())
        if item in keylist:
            itemref = player.inventoryDict.get(item) # creates reference to the object
            player.hp += itemref.hp
            if player.hp > player.maxhp:
                player.hp = player.maxhp
            player.attack += itemref.attack
            player.defense += itemref.defense
            player.inventoryDict.pop(item) # removes the item from the inventory dictionary

def stats():
    print("HP: " + str(player.hp) + "/" + str(player.maxhp))
    print("Attack: " + str(player.attack))
    print("Defense: " + str(player.defense))

def mainscreen():
    setting()
    prompt()
    inputcommand()

def main():
    create_player()
    mainscreen()

# ~~~~~~~~~~~~~~~~~~~~~~~~ Creating dictionaries ~~~~~~~~~~~~~~~~~~~~~~~~

commandsDict = {"N": gonorth, #"NORTH": gonorth,
                "S": gosouth, #"SOUTH": gosouth,
                "E": goeast, #EAST": goeast,
                "W": gowest, #"WEST": gowest(),
                "ATTACK": attack,
                "LOOK": look, "L": look,
                "INVENTORY": inventory, "INV": inventory,
                "EQUIP": equip,
                "UNEQUIP": unequip,
                "STATS": stats,
                "USE": use,
                "DROP": drop}



main()