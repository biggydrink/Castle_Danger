__author__ = 'abutz'

import random


class Room:

    def __init__(self,name,exits,setting):
        self.name = name
        self.exits = exits
        self.setting = setting

    def __str__(self):
        return "This room is the " + self.name

    def getSetting(self):
        return self.setting

    def getExits(self):
        exitstring = ""
        for i in range(len(self.exits)):
            exitstring += str(self.exits[i])
        return exitstring


    def getName(self):
        return self.name

class Character:

    def __init__(self,name):
        self.name = name
        self.HP = randint(100,120)
        self.str(13,18)
        self.defense(3,7)

class Monster:

    def __init__(self,name):
        self.name = name
        if self.name == "Ladybug":
            self.HP = 20
            self.str = 5
            self.defense = 0
        if self.name == "Super Ladybug":
            self.HP = 50
            self.str = 7
            self.defense = 2
        if self.name == "":
            return foo

# class Item:

# command class? each command gets a method, then make a dict/list and link the user commands to the methods

def main():
    setting()
    prompt()
    inputcommand(input(" "))

def setting():
    #print(currentroom.setting)
    print(DarkForest1.setting)
    #print("You are in a deep, dark forest. Lucky you have your swiss army knife.")

def prompt():
    # print(currentroom.name,currentroom.exits)
    print("<" + str(DarkForest1.getName()) + " : " +  str(DarkForest1.getExits()) + ">",end="")
    #print("Deep Dark Forest - NSEW>",end=" ")

def inputcommand(command):
    if command in commanddict:
        print(commanddict.get(command))
    else:
        print("Um, wait what?",end=" ")
        prompt()
        inputcommand(input(" "))

commanddict = {}
commanddict["n"] = "You head north" # currentroom.gonorth()
commanddict["s"] = "You head south" # currentroom.gosouth()
commanddict["e"] = "You head east" # currentroom.goeast()
commanddict["w"] = "You head west" # currentroom.gowest()

roomlist = []
DarkForest1 = Room("Deep Dark Forest",["N","S","E","W"],"You are in a deep, dark forest. Lucky you have your \
swiss army knife.")
roomlist.append(DarkForest1)


main()