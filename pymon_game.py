#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 22:29:55 2024
Pymon skeleton game
Please make modifications to all the classes to match with requirements provided in the assignment spec document
@author: dipto
@student_id : S4071833
@highest_level_attempted (P/C/D/HD):

- Reflection:
- Reference:
"""

import random


#you may use, extend and modify the following random generator
def generate_random_number(max_number = 1):
    r = random.randint(0,max_number)
    return r 


class Pymon:
    def __init__(self, name = "The player"):
        self.name = name
        self.current_location = None
        self.energy = 3 # Initail energy 3/3
        self.max_energy = 3 # maximun energy
    
    def move(self, direction = None):
        if self.current_location != None:
            if self.current_location.doors[direction] != None:
                #self.current_location.doors[direction].add_creature(self)  
                #self.current_location.creatures.remove(self)
                next_location = self.current_location.doors[direction]
                self.current_location = next_location

            else:
                print("no access to " + direction)
                
    def spawn(self, loc):
        if loc != None:
            loc.add_creature(self)
            self.current_location = loc
            
    def get_location(self):
        return self.current_location
            
class Location:
    def __init__(self, name = "New room",description = "", w = None, n = None , e = None, s = None):
        self.name = name
        self.description = description
        self.doors = {}
        self.doors["west"] = w
        self.doors["north"] = n
        self.doors["east"] = e
        self.doors["south"] = s
        self.creatures = []
        self.items = []
        
    def add_creature(self, creature):
        if creature not in self.creatures:
            self.creatures.append(creature)
        #please implement this method to by simply appending a creature to self.creatures list.
        
    def add_item(self, item):
        pass
        #please implement this method to by simply appending an item to self.items list.
        
    def connect_east(self, another_room):
        self.doors["east"] = another_room 
        another_room.doors["west"]  = self
        
    def connect_west(self, another_room):
        self.doors["west"] = another_room 
        another_room.doors["east"]  = self
    
    def connect_north(self, another_room):
        self.doors["north"] = another_room 
        another_room.doors["south"]  = self
        
    def connect_south(self, another_room):
        self.doors["south"] = another_room 
        another_room.doors["north"]  = self
        
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
        
class Creature:
    def __init__(self, nickname, description, location=None):
        self.nickname = nickname
        self.description = description
        self.location = location

    def set_location(self, new_location):
        self.location = new_location

    def get_location(self):
        return self.location
    def get_name(self):
        return self.nickname
class Record:
    def __init__(self):
        self.locations = []
        self.creatures = []
        #please implement constructor
       

    def import_location(self):
        try:
            # Dictionary to map location names to Location objects
            location_connect = {}
            #please import data from locations.csv
            filename = "locations.csv"
            file = open(filename,"r")
            line = file.readline()
            while line:
                
                line_field = line.strip().split(",")
                # Check if the line contains at least 6 elements (name, description, and 4 directions)
                if len(line_field) < 6:
                    print(f"Skipping line due to missing data: {line}")
                    line = file.readline()
                    continue

                # Create location object from data
                location_name = line_field[0].strip()
                description = line_field[1].strip()
                print(line_field[2])
                west = line_field[2].split(" = ")[1].strip() 
                north = line_field[3].split(" = ")[1].strip()
                east = line_field[4].split(" = ")[1].strip()
                south = line_field[5].split(" = ")[1].strip()
                new_location = Location(location_name,  description, west, north, east, south)
                self.locations.append(new_location)
                location_connect[location_name] = new_location
                line = file.readline()
            file.close()

            # Connect direction with Dictionary
            for location_name, location in location_connect.items():
                # Playground, an ., west = School, north = Beach, east = None,  south = None
                # Get connected locations' names from the doors
                west = location.doors["west"]
                north = location.doors["north"]
                east = location.doors["east"]
                south = location.doors["south"]
                # Connect locations if they exist in the dictionary
                if west in location_connect:
                    location.connect_west(location_connect[west])
                if north in location_connect:
                    location.connect_north(location_connect[north])
                if east in location_connect:
                    location.connect_east(location_connect[east])
                if south in location_connect:
                    location.connect_south(location_connect[south])
        except FileNotFoundError:
            return False
    def get_locations(self):
        return self.locations
    def find_location(self, name):
        for i in range(len(self.locations)):
            if name == self.locations[i].get_name().lower():
                return self.locations[i]
            if i == len(self.locations) - 1:
                return None
        
    def import_creatures(self):
        #please import data from creatures.csv
        try:
            filename = 'creatures.csv'
            file = open(filename,"r")
            line = file.readline()
            while line:
                line_field = line.strip().split(",")
                nickname = line_field[0].strip()
                description = line_field[1].strip()
                location = line_field[2].strip()
                new_creatures = Creature(nickname, description, location)
                self.creatures.append(new_creatures)
                line = file.readline()
            file.close()
            return True
        except FileNotFoundError:
            return False
    def find_creature(self, name):
        for i in range(len(self.creatures)):
            if name == self.creatures[i].get_name().lower():
                return self.creatures[i]
            if i == len(self.creatures) - 1:
                return None
        
    def import_items(self):
        pass #please import data from items.csv
    
class Operation:
    def __init__(self):
        self.locations = []
        self.current_pymon = Pymon("Kimimon")
   
    def setup(self):
        record = Record()
        record.import_location()
        record.import_creatures()
        for location in record.get_locations():
            self.locations.append(location)

        # a_random_number = generate_random_number(len(self.locations)-1)
        # spawned_loc = self.locations[a_random_number]
        # self.current_pymon.spawn(spawned_loc)

        # Your Pymon will be placed in the playground initially.
        #self.current_pymon.current_location = record.find_location("playground")
        playground = record.find_location("playground")
        beach = record.find_location("beach")
        school = record.find_location("school")

        kitimon = record.find_creature("kitimon")
        sheep =  record.find_creature("sheep")
        marimon = record.find_creature("marimon")

        self.current_pymon.current_location = playground
        playground.add_creature(kitimon)
        beach.add_creature(sheep)
        school.add_creature(marimon)


    def display_setup(self):
        for location in self.locations:
            print(location.name + " has the following creatures:")
            for creature in location.creatures:
                print(creature.name)

    #you may use this test run to help test methods during development
    def test_run(self):
        print(self.current_pymon.get_location().get_name())
        self.current_pymon.move("west")
        print(self.current_pymon.get_location().get_name())
        
    def start_game(self):
        print("Welcome to Pymon World\n")
        print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n")
        print("You started at ",self.current_pymon.get_location().get_name())
        while True:
            self.handle_menu()

    def handle_menu(self):
        print("\nPlease issue a command to your Pymon:")
        print("1) Inspect Pymon")
        print("2) Inspect current location")
        print("3) Move")
        print("4) Exit the program")
        menu = input("Your command: ")
        self.select_menu(menu)

    def select_menu(self, menu):
        if menu == '1':
            self.inspect_pymon()
        elif menu == '2':
            self.inspect_current_location()
        elif menu == '3':
            self.move()
        elif menu == '4':
            exit()
        else:
            print("Invalid menu")
    def inspect_pymon(self):
        print(f"Hi Player, my name is {self.current_pymon.name}, I am white and yellow with a sqare face.")
        print(f"My energy level is {self.current_pymon.energy}/{self.current_pymon.max_energy}. What can I do to help you?")
    def inspect_current_location(self):
        print(f"You are at a {self.current_pymon.get_location().get_name()}, {self.current_pymon.get_location().get_description()}")

    def move(self):
        direction = input("Moving to which directions?:").lower()
        if (direction in ('west','north','east','south')):
            current_location = self.current_pymon.get_location()
            next_location = current_location.doors[direction]
            if next_location is None:
                # No door in the specified direction
                print(f"There is no door to the {direction}. Pymon remains at {current_location.get_name()}.")
            else:
                # Move the Pymon to the new location
                self.current_pymon.move(direction)
                print(f"You traveled {direction} and arrived at {self.current_pymon.get_location().get_name()}.")
        else:
            print("Incorrect direction")

if __name__ == '__main__':
    ops = Operation()
    ops.setup()
    #ops.display_setup()
    ops.start_game()