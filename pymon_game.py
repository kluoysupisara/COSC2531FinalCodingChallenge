#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 22:29:55 2024
Pymon skeleton game
Please make modifications to all the classes to match with requirements provided in the assignment spec document
@author: dipto
@student_id : S4071833
@highest_level_attempted (P/C/D/HD): HD

- Reflection:
- Reference:
"""

import random


#you may use, extend and modify the following random generator
def generate_random_number(max_number = 1):
    r = random.randint(0,max_number)
    return r 


class Creature:
    def __init__(self, nickname, description, can_be_pymon=False):
        self.name = nickname
        self.description = description
        self.can_be_pymon = can_be_pymon

    def set_location(self, new_location):
        self.location = new_location

    def get_location(self):
        return self.location
    def get_name(self):
        return self.name

class Pymon(Creature):
    def __init__(self, name = "The player"):
        super().__init__(name, description="", can_be_pymon=True)
        self.current_location = None
        self.energy = 3 # Initail energy 3/3
        self.max_energy = 3 # maximun energy
    
    def move(self, direction = None):
        if self.current_location != None:
            if self.current_location.doors[direction] != None:
                self.current_location.doors[direction].add_creature(self)  
                self.current_location.creatures.remove(self)
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
    
    def chanllenge(self, creature_name, opt):
        # Find a creature with the specified name in the current location
        creature = next(
            (creature for creature in self.current_location.creatures 
            if creature.get_name().lower() == creature_name.lower()), 
            None
        )

        if not creature:
            # No creature with that name in the current location
            print(f"There is no creature named {creature_name} here.")
            return
        elif not isinstance(creature, Pymon):
            # Creature found, but it's not a Pymon, so it can't be challenged
            print(f"{creature_name} cannot be challenged because it is not a Pymon.")
            return
        
        # If the creature is a Pymon, proceed with the challenge
        print(f"{creature.name} gladly accepted your challenge! Ready for battle!")
        print("The first Pymon to win 2 of 3 encounters will win the battle")

        # Start battle
        player_wins = 0
        opponent_wins = 0
        encounter = 1

        while player_wins < 2 and opponent_wins < 2 and self.energy > 0 and encounter <=3:
            print(f"\nEncounter {encounter}!")
            result = self.battle_encounter()

            if result == "win":
                player_wins += 1
                encounter += 1
            elif result == "lose":
                opponent_wins += 1
                self.energy -= 1
                encounter += 1
            else:
                print("This encounter is a draw. Try again.")


        # Determine the battle outcome
        if player_wins >= 2:
            print(f"\nCongrats! You have won the battle and adopted a new Pymon called {creature.name}!")
            opt.pet_list.append(creature)  # Add opponent to pet list
        elif self.energy == 0 or opponent_wins >= 2:
            print(f"\nYou have lost the battle. {self.name} will be released into the wild.")
            self.relinquish(opt)

    def battle_encounter(self):
        shapes = {"r": "rock", "p": "paper", "s": "scissors"}
        player_choice_key = input("Your turn (r)ock, (p)aper, or (s)cissor?: ").lower()

        if player_choice_key not in shapes:
            print("Invalid choice! Please select 'r', 'p', or 's'.")
            return "draw"

        player_choice = shapes[player_choice_key]
        opponent_choice = random.choice(list(shapes.values()))

        print(f"You issued {player_choice}!")
        print(f"Your opponent issued {opponent_choice}!")

        # Determine encounter outcome based on game rules
        if player_choice == opponent_choice:
            print(f"{player_choice} vs {opponent_choice}: Draw, no one wins")
            return "draw"
        elif (player_choice == "rock" and opponent_choice == "scissors") or \
             (player_choice == "paper" and opponent_choice == "rock") or \
             (player_choice == "scissors" and opponent_choice == "paper"):
            print(f"{player_choice} vs {opponent_choice}: {player_choice} wins! You won this encounter.")
            return "win"
        else:
            print(f"{player_choice} vs {opponent_choice}: {opponent_choice} wins! You lost 1 encounter and 1 energy.")
            return "lose"
        
    def relinquish(self, operation):
        # Remove the current Pymon from the player's pet list
        if self in operation.pet_list:
            operation.pet_list.remove(self)
            print(f"{self.name} has been removed from your pet list.")

        # Remove this Pymon from its current location's creature list
        if self.current_location is not None:
            self.current_location.creatures.remove(self)
            print(f"{self.name} has been removed from {self.current_location.name}.")

        # Select a random new location for this Pymon to move to
        new_location = random.choice([loc for loc in operation.locations if loc != self.current_location])
        self.spawn(new_location)  # Use spawn to set the new location and add to the location's creatures
        print(f"{self.name} has been released into the wild at {new_location.name}.")

        # Check if there are any remaining Pymons in the pet list
        if operation.pet_list:
            # Randomly select a new Pymon from the pet list
            new_pymon = random.choice(operation.pet_list)
            operation.current_pymon = new_pymon

            # Randomly select a new location for the new current Pymon
            new_pymon_location = random.choice(operation.locations)
            new_pymon.spawn(new_pymon_location)
            print(f"Your new current Pymon is {new_pymon.name} and has been placed at {new_pymon_location.name}.")
        else:
            # Game over if no Pymons remain
            print("Game Over! You have no remaining Pymons.")
            exit()
         
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
        #please implement this method to by simply appending an item to self.items list.
        if item not in self.items:
            self.items.append(item)
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
        
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    def get_name(self):
        return self.name
    def get_description(self):
        return self.description   
class Record:
    def __init__(self):
        self.locations = []
        self.creatures = []
        #please implement constructor
        self.items = []
       

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
                west = None if west == "None" else west

                north = line_field[3].split(" = ")[1].strip()
                north = None if north == "None" else north

                east = line_field[4].split(" = ")[1].strip()
                east = None if east == "None" else east

                south = line_field[5].split(" = ")[1].strip()
                south = None if south == "None" else south

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
                name = line_field[0].strip()
                description = line_field[1].strip()
                can_be_pymon = line_field[2].strip().lower() == "yes"  # Check if it can be a Pymon
                # Create a Pymon if can_be_pymon is "yes"; otherwise, create a Creature
                if can_be_pymon:
                    new_creature = Pymon(name, description)
                else:
                    new_creature = Creature(name, description, can_be_pymon=False)
                # Add the new creature to the creatures list
                self.creatures.append(new_creature)
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
        #please import data from items.csv
        try:
            filename = 'item.csv'
            file = open(filename,"r")
            line = file.readline()
            while line:
                line_field = line.strip().split(",")
                if len(line_field) == 2:
                    name = line_field[0].strip()
                    description = line_field[1].strip()
                    new_item = Item(name, description)
                    self.items.append(new_item)
                    line = file.readline()
            file.close()
            return True
        except FileNotFoundError:
            return False
    def find_item(self, name):
        for i in range(len(self.items)):
            if name == self.items[i].get_name().lower():
                return self.items[i]
            if i == len(self.items) - 1:
                return None
    
class Operation:
    def __init__(self):
        self.locations = []
        self.current_pymon = Pymon("Kimimon")
        self.pymon_items = []
        self.pet_list = [self.current_pymon]                     
   
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
        #=========== SET UP PASS LEVEL ================
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
        #=========== SET UP CREDIT LEVEL ================
        record.import_items()
        tree = record.find_item("tree")
        potion = record.find_item("potion")
        apple = record.find_item("apple")
        binocular = record.find_item("binocular")
        
        playground.add_item(tree)
        playground.add_item(potion)
        beach.add_item(apple)
        school.add_item(binocular)
        


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
        print("4) Pick an item")
        print("5) View Inventory")
        print("6) Challengr a creature")
        print("0) Exit the program")
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
            self.pick_item()
        elif menu == '5':
            pass
        elif menu == '6':
            self.challenge_creature()
        elif menu == '0':
            exit()
        else:
            print("Invalid menu")
    def inspect_pymon(self):
        print("\nInspect Pymon Menu:")
        print("1) Inspect Current Pymon")
        print("2) List and select a benched Pymon to use")

        choice = input("Choose an option: ").strip()
        if choice == '1':
            print(f"Hi Player, my name is {self.current_pymon.name}, I am white and yellow with a sqare face.")
            print(f"My energy level is {self.current_pymon.energy}/{self.current_pymon.max_energy}. What can I do to help you?")
        elif choice == '2':
            pass
        else:
            print("Invalid Menu. Please try again.")
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
    def pick_item():
        pass
    def challenge_creature(self):
        creature_name = input("Challenge who: ").strip()
        self.current_pymon.challenge(creature_name, self)


if __name__ == '__main__':
    ops = Operation()
    ops.setup()
    #ops.display_setup()
    ops.start_game()