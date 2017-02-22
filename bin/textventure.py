#!/usr/bin/env python
# textventure.py
#################
## Textventure ##
## ckjbgames ####
## 2017 #########
#################

## Imports
import random  # Map randomization, eventually
import pickle  # For game saving
import sys     # Various uses
import socket  # Eventually for connections
import MySQLdb # For connecting to MySQL
import json    # Decode JSON in MySQL
import os      # Save files, etc.
import tty     # "Press any key to continue..."
## Classes
class gameItem(object):
    """
    An in-game item that can
    be used by the player and will
    be placed randomly in the rooms
    Instances are stored in the Inventory class
    Name is the item's name
    Effect should be an instance of the Effect class
    If Uses is set to true, an item lasts forever
    If Uses is set to one, an item has one use, etc.
    Uses should NOT be set to false!
    Description is self-explainatory
    """
    def __init__(self, name = None, effect = None, uses = None, description = None, movable = True, can_hold = True):
        """
        This is just an initialzer with a docstring
        """
        self.name = name
        self.effect = effect
        self.uses = uses
        self.description = description
        self.movable = movable
        self.can_hold = can_hold
    def __repr__(self):
        """
        Prints out an item's attributes in an actually readable format
        See the main docstring for more info on the main attributes
        """
        uses = self.uses
        if uses == True:
            uses = "*lasts forever*"
        template = "\n%s" +\
        "\nEffect:" +\
        "\n%s" +\
        "\nUses:" +\
        "\n%s" +\
        "\nDescription:" +\
        "\n%s"
        return template%(self.name, self.effect, uses, self.description)
    def itemName(self):
        """
        Used for returning only the item's name (for room descriptions and
        inventory listings)
        """
        return self.name
class Inventory(object):
    """
    The player's inventory
    Contains instances of the gameItem class
    """
    def __init__(self):
        """
        Initialize the inventory to an empty dictionary
        """
        self.player_inventory = {}
    def __repr__(self):
        """
        A separate __repr__ method so that all the
        full attributes of each item are not shown
        in the inventory listing.
        Basically a plain old inventory listing
        """
        if self.player_inventory == {}:
            eggs = "You're not carrying anything."
        else:
            eggs = ''
            for spam in self.player_inventory:
                eggs = eggs + '\n' + spam.itemName()
        return eggs
    def addItem(self, item_to_add):
        """
        Adds an item to the inventory
        item_to_add should be an instance of
        the gameItem class
        """
        self.player_inventory[item_to_add.itemName()] = item_to_add
    def viewItem(self,item_name):
        """
        View an item in the inventory
        Should be the name of an item
        """
        try:
            return self.player_inventory[item_name]
        except (NameError, KeyError):
            return "You don't have that item!"
class Room(object):
    """
    A room with a description, other rooms that it leads to,
    and contents
    name is self-explainatory
    items_room is a dictionary containing instances of the gameItem class that are in a room
    If items_room is set to false, the room contains no items.
    description is also self-explainatory
    in_room is a flag for if you are in the room or not
    """
    def __init__(self, name = None, items_room = False, description = None, in_room = False):
        """
        Initializes attributes described in the main docstring
        """
        self.name = name
        self.items_room = items_room
        self.description = description
        self.in_room = in_room
    def changeFlag(self, val):
        """
        Change in_room flag
        Possible fix for an issue
        """
        self.in_room = val
class allRooms(object):
    """
    A map-type arrangement of all rooms as a 2-dimensional list/array
    More effective than having a really, really complicated
    initializer method for the Room class
    The player will never actually view this unless they have a map
    There is a __repr__ method in case they do
    """
    def __init__(self, rooms = [],coords = (0,0)):
        """
        Initializer method
        rooms should be a list containing other lists, which
        should be a combination of instances of Room and
        the False value
        See the main docstring for more info
        """
        self.rooms = rooms
        self.coords = coords
    def __repr__(self):
        """
        Kind of displays a map
        # - A room, but you are not in it
        Space - There is no room here
        @ - You are here
        """
        map_of = ''
        for row in self.rooms:
            for room in row:
                if room == False:
                    map_of += ' '
                elif room.in_room == True:
                    map_of += '@'
                else:
                    map_of += '#'
            map_of += '\r\n'
        return map_of
    def move(self, direction = 8):
        """
        A method for moving to another room
        Uses a try-except block for determining
        if there is a room that can be entered from
        the specified direction
        These directions are based on the number pad
        So:
        7   8   9
          \ | /
        4 - 5 - 6
          / | \ 
        1   2   3
        In other words:
        8 - North
        2 - South
        4 - West
        6 - East
        A map of the game kind of looks like
        corridors in Nethack :)
        """
        if direction == 8:
            try:
                if isinstance(self.rooms[self.coords[0] - 1][self.coords[1]],Room):
                    self.rooms[self.coords[0]][self.coords[1]].changeFlag(False)
                    self.rooms[self.coords[0] - 1][self.coords[1]].changeFlag(True)
                    self.coords =(self.coords[0] - 1,self.coords[1])
                else:
                    raise NoRoom
            except (IndexError,NoRoom,AttributeError):
                return "There is no room to enter in this direction!"
        elif direction == 2:
            try:
                if isinstance(self.rooms[self.coords[0] + 1][self.coords[1]],Room):
                    self.rooms[self.coords[0]][self.coords[1]].changeFlag(False)
                    self.rooms[self.coords[0] + 1][self.coords[1]].changeFlag(True)
                    self.coords = (self.coords[0] + 1,self.coords[1]) 
                else:
                    raise NoRoom
            except (IndexError,NoRoom,AttributeError):
                return "There is no room to enter in this direction!"
        elif direction == 4:
            try:
                if isinstance(self.rooms[self.coords[0]][self.coords[1] - 1],Room):
                    self.rooms[self.coords[0]][self.coords[1]].changeFlag(False)
                    self.rooms[self.coords[0]][self.coords[1] - 1].changeFlag(True)
                    self.coords = (self.coords[0],self.coords[1] - 1)
                else:
                    raise NoRoom
            except (IndexError,NoRoom,AttributeError):
                return "There is no room to enter in this direction!"
        elif direction == 6:
            try:
                if isinstance(self.rooms[self.coords[0]][self.coords[1] + 1],Room):
                    self.rooms[self.coords[0]][self.coords[1]].changeFlag(False)
                    self.rooms[self.coords[0]][self.coords[1] + 1].changeFlag(True)
                    self.coords =(self.coords[0], self.coords[1] + 1)
                else:
                    raise NoRoom
            except (IndexError,NoRoom,AttributeError):
                return "There is no room to enter in this direction!"
        else:
            return "Sorry, that's not a valid direction."
    def randomgen(self):
        """
        For random generation of a map
        Will eventually use MySQL to find item templates
        """
        possible = [False, Room(in_room = False)]            # Possibilities for a room ; will be updated soon 
        size = (random.randint(10,25),random.randint(10,25)) # Make the map size anywhere from 10x10 to 25x25
        new_rooms = []                                       # An empty list that new rooms that will be created
        for x in range(size[0]):                             # Start a for loop
            row = []                                         # Make an empty list that will be appended to
            for y in range(size[1]):                         # Start another for loop
                row.append(random.choice(possible))          # Append another room or empty space to the current row
            new_rooms.append(row)                            # Append the row to new_rooms
        self.rooms = new_rooms                               # Assign new_rooms to the attribute rooms
class NoRoom(Exception):
    """
    An exception for the absence of a room to enter
    """
    pass
class Controller(object):
    """
    Purposes:
     1. Loads and saves games using pickle
    Store save files by default in
    /var/games/textventure/saves
    See "Installation" in the Wiki for more
     2. Performs some functions having to do with
    interactions between the player and the environment
     3. Executes textventure commands the player inputs
    """
    def __init__(self,inventory = None,allrooms = None):
        self.game = [inventory,allrooms]
    def loadgame(self,username = None):
        """
        Loads a game with pickle.load
        A save file should be in the /var/games/textventure/saves directory
        The extension doesn't matter, but I have decided to use *.pickle
        """
        print 'Loading game...'
        try:
            with open('/var/games/textventure/saves/%s.pickle'%(username),'r') as f:
                self.game = pickle.load(f)
        except EnvironmentError:
            print 'The game could not be loaded. Sorry about that.'
            pressanykey()
            sys.exit()
        else:
            print 'Success!'
            return self.game
    def savegame(self,username = None):
        """
        Save a game with pickle.dump
        Save file path is mentioned in the docs of loadgame()
        """
        print 'Saving game...'
        try:
            with open('/var/games/textventure/saves/%s.pickle'%(username),'w') as f:
                pickle.dump(self.game,f)
        except EnvironmentError:
            print 'The game could not be loaded. Sorry about that.'
            pressanykey()
            sys.exit()
        else:
            print 'Success!'
## Functions
def pressanykey():
    print 'Press any key to continue...'
    tty.setraw(1)
    sys.stdin.read(1)
## Main Program
if __name__ == '__main__':
    control=Controller('','')
    username=sys.argv[1]
    savepath="/var/games/textventure/saves/%s.pickle"%(username)
    if os.path.exists(savepath):
        inv,allrooms=control.loadgame(username)
    else:
        open(savepath,'a').close() # .close() could be omitted, but only in CPython.
                                   # It was kept so it will work in other implementations.
    
