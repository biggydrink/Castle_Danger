"""
Castle Danger.py
Author: Andrew Butz
Date: 05/14/2014

This is a little text RPG I built during my first semester at Minneapolis Technical & Community College for my final
project in Programming Logic & Design. It is not actually a very good game, but it did teach me a lot about Python,
and I feel that it's a good base to work from if I want to go further with the project.

Enjoy!
"""

import random  # used to get random stats for the player's character. May be used in the future for attack()
import time  # used to slow down the game's combat
import colorama  # used to provide (ANSI) color support, supposed to work on any platform

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

    def __str__(self):
        return colorama.Style.RESET_ALL + "This room is the " + self.name

    def getSetting(self):
        """
        Gets the description of the room that the player will see in the game. Used in the setting() function.
        """
        description = self.setting + "\n"
        if self.mobList != []:
            for mob in self.mobList:
                description += colorama.Fore.YELLOW + mob.setting
        return description

    def getExits(self):
        """
        Returns the possible exits from this room as a string. Used as part of the game's basic info/prompt screen
        in prompt()
        """
        exitstring = ""
        for i in range(len(self.exits)):
            exitstring += str(self.exits[i])
        return colorama.Style.RESET_ALL + exitstring

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
    instead of lists so that we can easily create a list of items by name (by creating a list of the dictionary's keys),
    and so we can easily access each item object's data using its name as a reference. This comes in handy when
    we want to display a list of items in inventory or equipped ( inventory() or equip() ) and when we need to access
    a specific item's data by using the item's name as an argument in a function call, as in look().
    """
    def __init__(self, name):
        """
        Stats are currently randomized from a limited range.
        """
        self.name = name
        self.maxhp = random.randint(100, 120)
        self.hp = self.maxhp
        self.attack = random.randint(13, 18)
        self.defense = random.randint(3, 7)
        self.equippedDict = {}
        self.inventoryDict = {}

    def die(self):
        """
        When your hp goes to 0 or below, this method is called and the game ends.
        """
        print(colorama.Style.RESET_ALL + "Oh no, you are dying...")
        print("You have died.")
        print("You can try again, if you want to improve on your FAILUUUURRRREEEE.")

class Monster:
    """
    The Monster class is very similar to the Character class, but with no need to display what items the monster
    has equipped or in its inventory, we put these items in lists instead of dictionaries. This could be changed
    if we want to let monsters equip items.
    """

    def __init__(self, name):
        """
        The if statements concerning names allows us to create different instances of monsters by simply using their
        name as an argument in initialization. Self.setting is used in the setting() function, to display the
        monsters in each room. If functionality is added to allow arguments in the look() function so that players
        can look at Monsters and see a description (as is possible with items), we will want to add a self.description
        variable.
        """
        self.name = name
        self.funcBehave = self.defaultBehavior  # default neutral behavior unless specified otherwise
        self.inventoryList = []  # items a monster is holding are created when the monster is initialized
        self.equippedList = []
        if name == "Ladybug":
            self.hp = 20
            self.attack = 5
            self.defense = 0
            self.setting = "There is a ladybug here."
        if name == "Super Ladybug":
            self.hp = 50
            self.attack = 8
            self.defense = 2
            self.setting = "Whoa, a giant ladybug is here!! How did it get so huge? Why does it have a sword?!?"
            self.createItem("Longsword")
            self.createItem("Polkadot Shirt")
            self.createItem("Polkadot Pants")
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
            self.createItem("Oozy Shirt")
            self.createItem("Oozy Pants")
            self.createItem("Green Sword")
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
            self.attack = 22
            self.defense = 15
            self.setting = "A... a black dragon is here. GULP."
            self.createItem("Charred Leather Vest")
            self.createItem("Charred Leather Pants")
            self.createItem("Blackened Sword")
            self.createItem("Mega Potion")
            self.createItem("Mega Potion")
            self.funcBehave = self.attackBehavior
        if name == "Foppish Palace Guard":
            self.hp = 125
            self.attack = 20
            self.defense = 15
            self.setting = "A foppish palace guard is here, fixing his hair in the mirror."
            self.createItem("Potion")
        if name == "The Corrupt and Nasty King (of destruction-ness and killing)":
            self.hp = 300
            self.attack = 35
            self.defense = 20
            self.setting = "The Corrupt and Nasty King (of destruction-ness and killing) is here, waiting for you to FINISH HIM"
            self.createItem("Shiny New Breastplate")
            self.createItem("Shiny New Legplates")
            self.funcBehave = self.attackBehavior

    def defaultBehavior(self):
        """
        Used in setting(). With lots of monsters we may want to take away the print statement. Probably will still keep
        this variable though, to use as a neutral default behavior, and to allow us to change that neutral behavior
        easily if needed.
        """
        print(self.name + " watches you.")

    def attackBehavior(self):
        """
        For aggro (aggressive) monsters--attack the player immediately upon the player entering the room.
        """
        print(colorama.Fore.RED + self.name + " attacks you!")
        attack()

    def createItem(self, item):
        """
        Creates an item and adds it to the Monster's inventory list.
        """
        new_item = Item(item)
        self.inventoryList.append(new_item)

    def die(self):
        """
        Called when the monster's HP gets to 0 or below. Monster dies, is removed from the room's moblist, and the
        player gets any items the monster was carrying.
        """
        currentroom.mobList.remove(self)
        print(colorama.Style.RESET_ALL + self.name + " has died!")
        for item in self.inventoryList:
            global player
            player.inventoryDict[item.name] = item
            print("You got a " + item.name)


class Item:
    """
    Items have stats just like Monsters and the player's character, but the only time they are used is when the player
    uses an item ( use() ) or equips an item ( equip() ). Currently the only time these are initialized is in the
    Monster init method, and the player gets them when the monster dies. Also, the self.setting variable is currently
    only called from the look() function.
    """
    def __init__(self,name):
        self.name = name
        if self.name == "Balloon Animal Sword":
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
        if self.name == "Polkadot Shirt" or self.name == "Polkadot Pants":
            self.setting = "It's black polkadots on a red background. Well, you got it from a ladybug, right?"
            self.attack = 0
            self.defense = 2
            self.hp = 5
        if self.name == "Oozy Shirt":
            self.setting = "Well, it came from a swamp thingy, right? Still better than your shabby shirt."
            self.attack = 0
            self.defense = 4
            self.hp = 10
        if self.name == "Oozy Pants":
            self.setting = "Well, it came from a swamp thingy, right? Debatably better than your flimsy pants. Kind of gross, really."
            self.attack = 0
            self.defense = 4
            self.hp = 10
        if self.name == "Green Sword":
            self.setting = "There's no reason a green sword should be better than a longsword, but it is."
            self.attack = 8
            self.defense = 0
            self.hp = 5
        if self.name == "Charred Leather Vest":
            self.setting = "A leather vest that looks pretty cooked. Durable though."
            self.attack = 0
            self.defense = 6
            self.hp = 15
        if self.name == "Charred Leather Pants":
            self.setting = "Some leather pants that look pretty cooked. Cuz you're on FIRE!! I mean not for real though, don't worry."
            self.attack = 0
            self.defense = 6
            self.hp = 15
        if self.name == "Blackened Sword":
            self.setting = "This sword used to be shinier, but its previous owner was a 10 packs-a-day smoker."
            self.attack = 11
            self.defense = 0
            self.hp = 0
        if self.name == "Shiny New Breastplate" or self.name == "Shiny New Legplates":
            self.setting = "Some actual armor. Finally!"
            self.attack = 0
            self.defense = 8
            self.hp = 20
        if self.name == "Potion":
            self.setting = "Gotta drink that potion."
            self.attack = 0
            self.defense = 0
            self.hp = 50
        if self.name == "Mega Potion":
            self.setting = "MOAR POTION"
            self.attack = 0
            self.defense = 0
            self.hp = 150

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

# ~~~~~~~~~~~~~~~~~~~~~~~~ Creating functions ~~~~~~~~~~~~~~~~~~~~~~~~

def create_player():
    """
    Initialization of the Character class, using input for the name.
    """
    global player
    player = Character(input("What is your name, Mr/Ms Would-be Hero?: "))
    if player.name == "Mr. Would-be Hero" or player.name == "Ms. Would-be Hero":
        print("Wow, just TOO unoriginal, I'm sorry - try again.")
        player = Character(input("What is your name, Mr/Ms Would-be Hero?: "))
    print("OK " + player.name + "! Let's go on a totally radical adventure!")
    new_item = Item("Balloon Animal Sword")
    player.inventoryDict[new_item.name] = new_item
    equip("Balloon Animal Sword")
    new_item = Item("Shabby Shirt")
    player.inventoryDict[new_item.name] = new_item
    equip("Shabby Shirt")
    new_item = Item("Flimsy Pants")
    player.inventoryDict[new_item.name] = new_item
    equip("Flimsy Pants")

def setting():
    """
    Gets the current room's setting method, plus the currentroom's monster's behavior call.
    """
    print(currentroom.getSetting())
    currentroom.behave()

def prompt():
    """
    This function prints some basic info inbetween <>'s, called at every time you want a player to enter commands.
    The basic info is the current room's name, the player's hp/maxhp, and the exits available from the current room.
    """
    print(colorama.Fore.CYAN + "<" + currentroom.getName() + " : " + str(player.hp) + "/" + str(player.maxhp) + "HP : " + currentroom.getExits() + ">", end="")

def inputcommand():
    """
    The main function call of the game, this loops while the player's hp is above 0. Anything a player types in the
    game is checked against the commands dictionary (commandsDict), with the first word as the command and anything
    after as arguments. Each command function call should protect against argument calls it is not expecting. Anything
    not in the commands dictionary is bad input and the player is prompted to input again.
    """
    while player.hp > 0:
        command = input(" ")
        commandlist = command.split()
        if len(commandlist) == 0:
            prompt()
        elif len(commandlist) > 1 and commandlist[0].upper() in commandsDict:
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
            print(colorama.Style.RESET_ALL + "Um, wait what?", end=" ")
            prompt()

def gonorth(arg=None):  # argument=None passed in to help protect against player typos.
    """
    Changes the currentroom variable to currentroom.north, essentially moving the player north according to the
    room mapping.
    """
    global currentroom
    if arg != None:
        print(colorama.Style.RESET_ALL + "Um, wait what?", end=" ")
    elif currentroom.north == None:
        print(colorama.Style.RESET_ALL + "You can't go that way from here.")
    else:
        currentroom = currentroom.north
        setting()

def gosouth(arg=None):  # argument=None passed in to help protect against player typos.
    """
    Changes the currentroom variable to currentroom.south, essentially moving the player south according to the
    room mapping.
    """
    global currentroom
    if arg != None:
        print(colorama.Style.RESET_ALL + "Um, wait what?", end=" ")
    elif currentroom.south == None:
        print(colorama.Style.RESET_ALL + "You can't go that way from here.")
    else:
        currentroom = currentroom.south
        setting()

def goeast(arg=None):  # argument=None passed in to help protect against player typos.
    """
    Changes the currentroom variable to currentroom.east, essentially moving the player east according to the
    room mapping.
    """
    global currentroom
    if arg != None:
        print(colorama.Style.RESET_ALL + "Um, wait what?", end=" ")
    elif currentroom.east == None:
        print(colorama.Style.RESET_ALL + "You can't go that way from here.")
    else:
        currentroom = currentroom.east
        setting()

def gowest(arg=None):  # argument=None passed in to help protect against player typos.
    """
    Changes the currentroom variable to currentroom.west, essentially moving the player west according to the
    room mapping.
    """
    global currentroom
    if arg != None:
        print(colorama.Style.RESET_ALL + "Um, wait what?", end=" ")
    elif currentroom.west == None:
        print(colorama.Style.RESET_ALL + "You can't go that way from here.")
    else:
        currentroom = currentroom.west
        setting()

def attack(arg=None):
    """
    Attacks the monster in the current room, if there is one. Currently does not take any arguments, and there is
    not any need (strictly speaking) because there is only ever one monster in each room. If argument functionality is
    added, the currentroom.mobList will need to become a dictionary for the same reasons that there are player
    equipped item and inventory item dictionaries (see Character class doc string).
    """
    global player
    if arg != None:
        print("Attack what now? (Hint for the confused: just type attack)")
    elif len(currentroom.mobList) == 0:
        print("You attack the empty air in this empty room...")
        time.sleep(1)
        print("... you win, Mr. Hero!")
    else:
        monster_attacked = currentroom.mobList[0]
        monster_damage = monster_attacked.attack - player.defense
        player_damage = player.attack - monster_attacked.defense
        if monster_damage < 0:
            monster_damage = 0
        if player_damage < 0:
            player_damage = 0
        while player.hp > 0 and monster_attacked.hp > 0:
            player.hp -= monster_damage
            monster_attacked.hp -= player_damage

            if monster_damage > 18: mobattackstring = colorama.Fore.RED + colorama.Style.BRIGHT + "HARD!!"
            elif monster_damage > 14: mobattackstring = "omg so hard"
            elif monster_damage > 12: mobattackstring = "...ouch!"
            elif monster_damage > 10: mobattackstring = "pretty hard."
            elif monster_damage > 7: mobattackstring = "kinda hard."
            elif monster_damage > 5: mobattackstring = "kinda."
            else: mobattackstring = "a little bit."

            if player_damage > 18: playerattackstring = colorama.Fore.RED + colorama.Style.BRIGHT + "HARD!!"
            elif player_damage > 14: playerattackstring = "omg so hard"
            elif player_damage > 12: playerattackstring = "...ouch!"
            elif player_damage > 10: playerattackstring = "pretty hard."
            elif player_damage > 7: playerattackstring = "kinda hard."
            elif player_damage > 5: playerattackstring = "kinda."
            else: playerattackstring = "a little bit."

            print(colorama.Fore.RED + monster_attacked.name + " hits you " + mobattackstring)
            print(colorama.Fore.GREEN + "You hit " + monster_attacked.name + " " + playerattackstring)
            prompt()
            if monster_attacked.hp > 0 and player.hp > 0:
                time.sleep(2)
                print(colorama.Style.RESET_ALL + "\n")
        if monster_attacked.hp <= 0:
            monster_attacked.die()
        if player.hp <= 0:
            player.die()

def look(argument=None):
    """
    Player command. Shortcut: l
    With no arguments, grabs setting(). With arguments, you can look at any of the items you have equipped or in
    your inventory. Could add functionality to look at monsters as well, though this would mean changing
    currentroom.mobList to a dictionary, and adding a Monster.description variable.
    """
    invlist = list(player.inventoryDict.keys())
    eqlist = list(player.equippedDict.keys())
    if argument == None:
        setting()
    elif argument in invlist:
        itemref = player.inventoryDict.get(argument)
        print(colorama.Style.RESET_ALL + itemref.setting)
    elif argument in eqlist:
        itemref = player.equippedDict.get(argument)
        print(colorama.Style.RESET_ALL + itemref.setting)
    else:
        print(colorama.Style.RESET_ALL + "Look at what?")

def inventory(arg=None):
    """
    Player command. Lists item in your inventory.
    arg=None included to avoid errors due to mistypes.
    """
    if len(player.inventoryDict) == 0:
        print(colorama.Style.RESET_ALL + "You are carrying:")
        print("Wait... you aren't carrying anything.")
    else:
        print(colorama.Style.RESET_ALL + "You are carrying:")
        invlist = list(player.inventoryDict.keys())
        for item in invlist:
            print(item)
#        for item in player.inventoryDict:
#            print(item.name)

def equip(item=None):
    """
    Player command.
    With no arguments, shows a list of currently equipped items.
    With an argument, equips an item from your inventory.
    """
    if item == None:
        eqkeylist = list(player.equippedDict.keys())
        print(colorama.Style.RESET_ALL + "You are wearing: ")
        if len(eqkeylist) == 0:
            print("Nothing!")
        else:
            for item in eqkeylist:
                print(item)
    elif item == "Potion" or item == "Mega potion":
        print(colorama.Style.RESET_ALL + "Um, you can't equip a potion, smarty pants.")
    else:
        invkeylist = list(player.inventoryDict.keys())
        if item in invkeylist:
            itemref = player.inventoryDict.get(item) # gets itemref so we can use it to reference the object itself
            player.equippedDict[itemref.name] = itemref # adds the object to the equipped dictionary
            player.maxhp += itemref.hp
            player.attack += itemref.attack
            player.defense += itemref.defense
            print(colorama.Style.RESET_ALL + "You equip your " + itemref.name + ".")
            player.inventoryDict.pop(item) # removes item from inventory
        else:
            print(colorama.Style.RESET_ALL + "You aren't carrying that item.")

def unequip(item=None):
    """
    Player command.
    Unequips an item, by removing it from the equipped dictionary and adding it to the inventory dictionary.
    """
    if item == None:
        print(colorama.Style.RESET_ALL + "Unequip what?")
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
            print(colorama.Style.RESET_ALL + "You unequip your " + itemref.name + ".")
        else:
            print(colorama.Style.RESET_ALL + "You don't have that item equipped.")

def drop(item=None):
    """
    Player command.
    Removes an item from inventory by removing it from the inventory dictionary. An item is not recoverable in game
    after being dropped.
    """
    if item == None:
        print(colorama.Style.RESET_ALL + "Drop what?")
    else:
        keylist = list(player.inventoryDict.keys())
        if item in keylist:
            itemref = player.inventoryDict.get(item)
            player.inventoryDict.pop(item) # remove item from inventory)
            print(colorama.Style.RESET_ALL + "You drop your " + itemref.name + ".")
        else:
            print(colorama.Style.RESET_ALL + "You don't have that item.")

def use(item=None):
    """
    Player command.
    Gets a one-time use out of the item, after which it is removed from the player's inventory. Should add functionality
    to specify items that can be used vs. equipped, but currently any item can be used, and is not recoverable in game
    after doing so.
    """
    if item == None:
        print(colorama.Style.RESET_ALL + "Use what?")
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
        else:
            print(colorama.Style.RESET_ALL + "You don't have that item.")

def stats(arg=None):
    """
    Player command. Prints your stats. arg=None added to keep the game from breaking due to a mistype that would give
    the stats command an argument inadvertently.
    """
    print(colorama.Style.RESET_ALL + "HP: " + str(player.hp) + "/" + str(player.maxhp))
    print(colorama.Style.RESET_ALL + "Attack: " + str(player.attack))
    print(colorama.Style.RESET_ALL + "Defense: " + str(player.defense))

def main():
    """
    Creates the player's character, shows the setting of the first room, and then displays the command prompt and runs
    the inputcommand function.
    """
    create_player()
    setting()
    prompt()
    inputcommand()

# ~~~~~~~~~~~~~~~~~~~~~~~~ Player Commands Dictionary ~~~~~~~~~~~~~~~~~~~~~~~~

commandsDict = {"N": gonorth, #"NORTH": gonorth,
                "S": gosouth, #"SOUTH": gosouth,
                "E": goeast, #EAST": goeast,
                "W": gowest, #"WEST": gowest(),
                "ATTACK": attack,
                "LOOK": look, "L": look,
                "INVENTORY": inventory, "INV": inventory,
                "EQUIP": equip, "EQ": equip,
                "UNEQUIP": unequip, "UNEQ": unequip,
                "STATS": stats,
                "USE": use,
                "DROP": drop}



main()