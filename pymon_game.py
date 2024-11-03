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
from datetime import datetime
import sys

#you may use, extend and modify the following random generator
def generate_random_number(max_number = 1):
    r = random.randint(0,max_number)
    return r 
class InvalidDirectionException(Exception):
    """Raised when the selected direction does not contain any location."""
    pass
class InvalidInputFileFormat(Exception):
    """Raised when a CSV file has invalid content or incorrect format."""
    pass

class Creature:
    def __init__(self, nickname, description, can_be_pymon=False, current_location=None):
        self.name = nickname
        self.description = description
        self.can_be_pymon = can_be_pymon
        self.current_location= current_location

    def set_location(self, new_location):
        if new_location is not None:
            if self.current_location is not None:
                #old location remove current creature
                self.current_location.remove_creature(self)
            #change current to new location
            self.current_location = new_location
             # Add to new location's creature
            new_location.add_creature(self) 

    def get_location(self):
        return self.current_location
    def get_name(self):
        return self.name
    def get_description(self):
        return self.description

class Pymon(Creature):
    #def __init__(self, name = "The player"):
    def __init__(self, name, description, current_location = None):
        super().__init__(name, description, can_be_pymon=True, current_location=current_location)
        self.energy = 3 # Initail energy 3/3
        self.max_energy = 3 # maximun energy
        self.move_count = 0 # track moove
        self.immunity = False # track magic potion
        self.stat_battle = [] # lsit of store stat battle
    
    def move(self, direction, opt):
        # Check if there is a connected location in the specified direction
        next_location = self.current_location.doors[direction]
        if next_location is not None:
            # Move Pymon to the new location
            self.set_location(next_location)
            #next_location.add_creature(self)  
            #self.current_location.creatures.remove(self)
            #self.current_location = next_location
            self.move_count += 1

            # Decrease energy every 2 moves
            if self.move_count % 2 == 0:
                self.energy -= 1
                print(f"{self.name}'s energy decreased to {self.energy}.")

            # If energy is depleted, Pymon escapes to the wild
            if self.energy <= 0:
                self.relinquish(opt)
        else:
            # No connected location in the specified direction
            print(f"No access to {direction}. Pymon remains at {self.current_location.get_name()}.")
                
    def spawn(self, loc):
        if loc != None:
            loc.add_creature(self)
            self.current_location = loc
            
    def get_location(self):
        return self.current_location
    
    def challenge(self, creature_name, opt):
        # Find a creature with the specified name in the current location
        creature = next(
            (creature for creature in self.current_location.creatures 
            if creature.get_name().lower() == creature_name.lower() and creature.get_name().lower()!= self.name.lower()), 
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

        #record battle of pymon
        wins, draws, losses = 0, 0, 0

        while player_wins < 2 and opponent_wins < 2 and self.energy > 0 and encounter <=3:
            print(f"\nEncounter {encounter}!")
            result = self.battle_encounter()

            if result == "win":
                player_wins += 1
                encounter += 1
                wins += 1
            elif result == "lose":
                if self.immunity:
                    # Prevent energy loss due to potion
                    print(f"{self.name} lost the battle but was protected by the potion. No energy lost.")
                    #reset posion immunity
                    self.immunity = False
                else:
                    print("You lost 1 encounter and 1 energy.")
                    opponent_wins += 1
                    self.energy -= 1
                    encounter += 1
                    losses += 1
            else:
                print("This encounter is a draw. Try again.")
                draws += 1


        # Determine the battle outcome
        self.record_battle(creature_name, wins, draws, losses)
        if player_wins >= 2:
            print(f"\nCongrats! You have won the battle and adopted a new Pymon called {creature.name}!")
            opt.pet_list.append(creature)  # Add opponent to pet list
            # Remove this Creature from its current location's creature list
            self.current_location.creatures.remove(creature)
            creature.set_location(None)
            print(f"{self.name} has been removed from {self.current_location.name}.")
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
            print(f"{player_choice} vs {opponent_choice}: {opponent_choice} wins! ")
            return "lose"
    def record_battle(self, opponent, wins, draws, losses):
        """Record battle results in battle."""
        timestamp = datetime.now().strftime("%d/%m/%Y %I:%M%p")
        battle = {
            "timestamp": timestamp,
            "opponent": opponent,
            "wins": wins,
            "draws": draws,
            "losses": losses
            }
        self.stat_battle.append(battle)

    def display_battle_stats(self):
        """ Display all battle states"""
        if not self.stat_battle:
            print("No battle statistics")
            return
        total_wins, total_draws, total_losses = 0, 0, 0

        print(f"Pymon Nickname: {self.name}")
        for i, battle in enumerate(self.stat_battle, 1):
            print(f"Battle {i}, {battle['timestamp']} Opponent: “{battle['opponent']}”, "
                  f"W: {battle['wins']} D: {battle['draws']} L: {battle['losses']}")
            total_wins += battle['wins']
            total_draws += battle['draws']
            total_losses += battle['losses']

        print(f"Total: W: {total_wins} D: {total_draws} L:{total_losses}")
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
        new_location = random.choice([loc for loc in operation.record.locations if loc != self.current_location])
        self.spawn(new_location)  # Use spawn to set the new location and add to the location's creatures
        print(f"{self.name} has been released into the wild.")

        #reset pymon enerygy
        self.energy = self.max_energy

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
    def use_item(self, item, operation):
        """Uses an item from inventory."""
        if isinstance(item, Item):
            # Edible item like an apple
            if item.name.lower() == "apple" and item.consumable:
                if self.energy < self.max_energy:
                    self.energy += 1
                    operation.inventory.remove(item)
                    print(f"{self.name} ate the {item.name} and gained 1 energy. Current energy: {self.energy}.")
                else:
                    print(f"{self.name}'s energy is already full.")
                    print(f"{self.name} ate the {item.name}")
                    operation.inventory.remove(item)
                    
            # Magic potion
            elif item.name.lower() == "potion" and item.consumable:
                self.immunity = True
                operation.inventory.remove(item)
                print(f"{self.name} used the magic potion and gained temporary immunity.")

            # Binocular
            elif item.name.lower() == "binocular":
                while True:
                    direction = input("Choose direction to view (current, west, north, east, south): ").strip().lower()
                    if direction in ["current", "west", "north", "east", "south"]:
                        self.use_binocular(direction)
                        break
                    else:
                        print("Invalid direction. Please Choose direction to view (current, west, north, east, south)")

    def use_binocular(self, direction):
        """Use binocular to inspect the current location or nearby locations."""
        if direction == "current":
            creatures = [creature.get_name() 
                         if not isinstance(creature, Pymon) 
                            else "another Pymon" 
                            for creature in self.current_location.creatures 
                            if creature != self]
            creatures_str = ", and".join(creatures) if creatures else "no creature"
            # List connected locations in each direction
            connected_directions = []
            for dir_name, loc in self.current_location.doors.items():
                if loc:
                    connected_directions.append(f"in the {dir_name} is {loc.get_name()}")
            
            # Prepare a string description of directions
            directions_description = ", and ".join(connected_directions) if connected_directions else "no connected locations"
            print(f"{creatures_str}, and {directions_description}.")
        elif direction in self.current_location.doors and self.current_location.doors[direction]:
            location = self.current_location.doors[direction]
            item_location = location.items
            creature_location = location.creatures
            another_pymon = [pymon for pymon in creature_location if isinstance(pymon, Pymon)]
            # check if there are another pymon
            if len(another_pymon) > 0:
                print(f"In the {direction}, there is {location.get_name()} with {','.join(item_location.get_name())} and unknown creature nearby.")
            else:
                print(f"In the {direction}, there is {location.get_name()} with {','.join(item_location.get_name())}.")
        else:
            print(f"This direction leads nowhere.")

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
            # add creature to location
            self.creatures.append(creature)
            # add location to creature
            creature.current_location = self
        #please implement this method to by simply appending a creature to self.creatures list.
        
    def remove_creature(self, creature):
        if creature in self.creatures:
            self.creatures.remove(creature)
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
    def get_items(self):
        return self.items
        
class Item:
    def __init__(self, name, description, pickable, consumable):
        self.name = name
        self.description = description
        self.pickable = pickable
        self.consumable = consumable
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


    def load_data(self, location_file, creature_file, item_file):
        """Load data from specified files for locations, creatures, and items."""
        self.import_locations(location_file)
        self.import_creatures(creature_file)
        self.import_items(item_file)

    
    def import_locations(self, filename):
        try:
            # Dictionary to map location names to Location objects
            location_connect = {}
            with open(filename, "r") as file:
                next(file)  # Skip the header row
                line = file.readline()
                while line:  
                    line_field = line.strip().split(",")
                    # Check if the line contains at least 6 elements (name, description, and 4 directions)
                    if len(line_field) != 6:
                        raise InvalidInputFileFormat(f"Invalid format in {filename}. Expected 6 columns.")

                    # Create location object from data
                    location_name = line_field[0].strip()
                    description = line_field[1].strip()

                    west = line_field[2].strip()
                    west = None if west == "None" else west
                    
                    north = line_field[3].strip()
                    north = None if north == "None" else north

                    east = line_field[4].strip()
                    east = None if east == "None" else east

                    south = line_field[5].strip()
                    south = None if south == "None" else south

                    new_location = Location(location_name, description, west, north, east, south)
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
        except InvalidInputFileFormat as e:
            print(f"File format error: {e}")
    def get_locations(self):
        return self.locations
    def find_location(self, name):
        for i in range(len(self.locations)):
            if name.lower() == self.locations[i].get_name().lower():
                return self.locations[i]
            if i == len(self.locations) - 1:
                return None
        
    def import_creatures(self, filename):
        #please import data from creatures.csv
        try:
            with open(filename, "r") as file:
                next(file)  # Skip the header row
                line = file.readline()
                while line:
                    line_field = line.strip().split(",")
                    
                    if len(line_field) != 3:
                        raise InvalidInputFileFormat(f"Invalid format in {filename}. Expected 3 columns.")
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
        except InvalidInputFileFormat as e:
            print(f"File format error: {e}")
    def find_creature(self, name):
        for i in range(len(self.creatures)):
            if name.lower() == self.creatures[i].get_name().lower():
                return self.creatures[i]
            if i == len(self.creatures) - 1:
                return None

    def import_items(self, filename):
        #please import data from items.csv
        try:
            with open(filename, "r") as file:
                next(file)  # Skip the header row
                line = file.readline()

                while line:
                    line_field = line.strip().split(",")
                    if len(line_field) != 4:
                        raise InvalidInputFileFormat(f"Invalid format in {filename}. Expected 4 columns.")
                    name = line_field[0].strip()
                    description = line_field[1].strip()
                    pickable = line_field[2].strip().lower() == "yes"
                    consumable = line_field[3].strip().lower() == "yes"

                    # Create an Item instance and append to items list
                    new_item = Item(name, description, pickable, consumable)
                    self.items.append(new_item)
                    line = file.readline()
                file.close()
                return True
        except InvalidInputFileFormat as e:
            print(f"File format error: {e}")
    def find_item(self, name):
        for i in range(len(self.items)):
            if name.lower() == self.items[i].get_name().lower():
                return self.items[i]
            if i == len(self.items) - 1:
                return None
            
    def add_custom_location(self, filename="locations.csv"):
        """Add a new location and save it to the locations file."""
        print("Enter the location details in the following format:")
        print("Name, Description, West, North, East, South")
        print("Example: School, a secondary school for local creatures with 3 two-story buildings., None, None, Playground, None")
        #add_new_location by admin mode
        while True:
            user_input = input("Enter the new location (eg., name, description, west, north, east, south:")
            new_loc = [new_loc.strip() for new_loc in user_input.split(",")]

            #validate new loc parameter
            if len(new_loc) != 6:
                print("Invalid input formate. Please input 6 column (eg., name, description, west, north, east, south:")
                continue
            name, description, west, north, east, south = new_loc

            #create new location object
            new_location = Location(name, description)
            new_location.doors = {
                "west": west if west.lower() != "none" else None,
                "north": north if north.lower() != "none" else None,
                "east": east if east.lower() != "none" else None,
                "south": south if south.lower() != "none" else None  
            }

            with open(filename, "a") as file:
                file.write(f"{name}, {description}, {west}, {north}, {east}, {south}\n")
            print(f"Custom location '{name}' added and saved to {filename}.")
            break


    def add_custom_creature(self, filename="creatures.csv"):
        """Add a new creature (Pymon or Animal) and save it to the creatures file."""
        while True:
            print("Enter the location details in the following format:")
            print("Name, Description, adoptable(yes/no)")
            user_input = input("Enter the new creature (eg., name, description, adoptable(yes/no):")
            parts = [parts.strip() for parts in user_input.split(",")]

            #validate user_input length must have 3 column
            if len(parts) != 3:
                print("Invalid input format. Please input 3 columns (eg., name, description, adoptable(yes/no).")
                continue
            name, description, adoptable = parts
            if adoptable.lower() == "yes":
                new_creature = Pymon(name, description)
            elif adoptable.lower() == "no":
                new_creature = Creature(name, description)
            else:
                print("Adoptable values must be only 'yes' or 'no'")
                continue

            self.creatures.append(new_creature)
            
            with open(filename, "a") as file:
                file.write(f"{name}, {description}, {adoptable}\n")
            print(f"Custom creature '{name}' added and saved to {filename}.")
            break

    def randomize_locations(self):
        """Randomly assign connections between locations, ignoring existing connections."""
        directions = ["west", "north", "east", "south"]
        opposite_direction = {"west": "east", "north": "south", "east": "west", "south": "north"}

        # Clear current connections
        for location in self.locations:
            location.doors = {dir_name: None for dir_name in directions}
        
        # Randomly connect locations
        for location in self.locations:
            available_directions = random.sample(directions, k=random.randint(1, len(directions)))
            available_locations = [loc for loc in self.locations if loc != location]
            random.shuffle(available_locations)

            for direction in available_directions:
                if available_locations:
                    connected_location = available_locations.pop()

                    # Set the connection in the specified direction
                    location.doors[direction] = connected_location
                    # Set the reciprocal connection in the opposite direction
                    connected_location.doors[opposite_direction[direction]] = location
        print("Locations have been randomly connected.")
    
class Operation:
    def __init__(self):
        self.locations = []
        self.current_pymon = Pymon("Kimimon", "I am white and yellow with a sqare face.")
        self.inventory = []
        self.pet_list = [self.current_pymon]
        self.record = Record()

    def main_menu(self):
        """Display main menu after loading programe to choose mode to begin game"""

        #Read command-line arguments for file names
        args = sys.argv[1:]
        self.location_file = args[0] if len(args) > 0 else "locations.csv"
        self.creature_file = args[1] if len(args) > 1 else "creatures.csv"
        self.item_file = args[2] if len(args) > 2 else "items.csv"

        self.record.load_data(self.location_file, self.creature_file, self.item_file)

        while True:
            print("\nWelcome to Pymon World!")
            print("Please choose an option:")
            print("1) Start New Game")
            print("2) Load Game")
            print("3) Admin Mode")
            print("4) Exit")
            choice = input("Enter your choice: ").strip()
        
            if choice == '1':
                # Start a new game by setting up the game environment
                self.setup()
                self.start_game()
                break
            elif choice == '2':
                # Load a saved game
                if self.load_game():
                    self.start_game()
                break
            elif choice == '3':
                # Enter admin mode
                self.admin_mode()
            elif choice == '4':
                print("Exiting the game. Goodbye!")
                exit()
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")           
   
    def setup(self):
        try:
            # random location pymon born
            a_random_number = generate_random_number(len(self.record.locations)-1)
            spawned_loc = self.record.locations[a_random_number]
            self.current_pymon.spawn(spawned_loc)

            # random item and creatures in locations
            for creature in self.record.creatures:
                random_loc = random.choice(self.record.locations)
                random_loc.add_creature(creature)

            for item in self.record.items:
                random_loc = random.choice(self.record.locations)
                random_loc.add_item(item)
            
            # record.import_location()
            # record.import_creatures()
            # for location in record.get_locations():
            #     self.locations.append(location)

            # a_random_number = generate_random_number(len(self.locations)-1)
            # spawned_loc = self.locations[a_random_number]
            # self.current_pymon.spawn(spawned_loc)

            # Your Pymon will be placed in the playground initially.
            #self.current_pymon.current_location = record.find_location("playground")
            #=========== SET UP PASS LEVEL ================
            # playground = record.find_location("playground")
            # beach = record.find_location("beach")
            # school = record.find_location("school")

            # kitimon = record.find_creature("kitimon")
            # sheep =  record.find_creature("sheep")
            # marimon = record.find_creature("marimon")

            # self.current_pymon.current_location = playground
            # playground.add_creature(self.current_pymon)

            # #set location to creatures
            # kitimon.set_location(playground)
            # sheep.set_location(beach)
            # marimon.set_location(school)
            # #=========== SET UP CREDIT LEVEL ================
            # record.import_items()
            # tree = record.find_item("tree")
            # potion = record.find_item("potion")
            # apple = record.find_item("apple")
            # binocular = record.find_item("binocular")
            
            # playground.add_item(tree)
            # playground.add_item(potion)
            # beach.add_item(apple)
            # school.add_item(binocular)
        except InvalidInputFileFormat as e:
            print(f"File format error: {e}")
            sys.exit(1)
        
    def start_game(self):
        print("\nWelcome to Pymon World\n")
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
        print("6) Challenge a creature")
        print("7) Generate stats")
        print("8) Save game")
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
            self.view_inventory()
        elif menu == '6':
            self.challenge_creature()
        elif menu == '7':
            self.generate_stats()
        elif menu == '8':
            self.save_game()
        elif menu == '0':
            sys.exit(1)
        else:
            print("Invalid menu")
    def inspect_pymon(self):
        print("\nInspect Pymon Menu:")
        print("1) Inspect Current Pymon")
        print("2) List and select a benched Pymon to use")

        choice = input("Choose an option: ").strip()
        if choice == '1':
            print(f"Hi Player, my name is {self.current_pymon.name}, {self.current_pymon.description}")
            print(f"My energy level is {self.current_pymon.energy}/{self.current_pymon.max_energy}. What can I do to help you?")
        elif choice == '2':
            self.swap_creature()
        else:
            print("Invalid Menu. Please try again.")
    def swap_creature(self):
        #benched_pymons = [pymon for pymon in self.pet_list if pymon != self.current_pymon]
        benched_pymons = [pymon for pymon in self.pet_list if pymon != self.current_pymon]

        if not benched_pymons:
            print("There are no Pymons available to swap with.")
            return
        print("\nAvailable Pymons in the bench:")
        for idx, pymon in enumerate(benched_pymons, 1):
            print(f"{idx}) {pymon.name} - {pymon.description} (Energy: {pymon.energy}/{pymon.max_energy})")
        user_input = input("Do you want to swap pymon(y/n)?:")
        if user_input.lower() == 'y' or user_input.lower() == 'yes':
            while True:
                try:
                    choice = int(input("Select a Pymon to swap with the current one: ").strip())
                    if 1 <= choice <= len(benched_pymons):
                        # Swap the selected Pymon with the current one
                        selected_pymon = benched_pymons[choice - 1]
                        parent_location = self.current_pymon.get_location()

                        # Set the selected Pymon as the new current Pymon
                        self.current_pymon = selected_pymon
                        self.current_pymon.current_location = parent_location
                        print(f"You have swapped to {self.current_pymon.name} as your active Pymon.")
                        return
                    else:
                        print("Invalid choice. Please select a valid Pymon number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            return
    def inspect_current_location(self):
        print(f"You are at a {self.current_pymon.get_location().get_name()}, {self.current_pymon.get_location().get_description()}")

        location = self.current_pymon.get_location()

        # Display creatures in the current location, excluding the current Pymon itself
        creatures = [creature for creature in location.creatures if creature != self.current_pymon]
        if creatures:
            print("\nCreatures residing here:")
            for creature in creatures:
                print(f"- {creature.get_name()}: {creature.get_description()}")
        else:
            print("\nNo other creatures reside here.")

        # Display items in the current location
        if location.items:
            print("\nItems available in this location:")
            for item in location.items :
                print(f"- {item.get_name()}")
        else:
            print("\nNo items are available here.")
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
                self.current_pymon.move(direction, self)
                print(f"You traveled {direction} and arrived at {self.current_pymon.get_location().get_name()}.")
        else:
            print("Incorrect direction")
    def pick_item(self):
        item_pick = input("Pinking what:").strip().lower()
        location = self.current_pymon.get_location()

        #find item at crrent location's pymon
        item = next((item for item in location.get_items() if item.name.lower() == item_pick), None)
        if item:
            if item.pickable:
                # Add item to inventory and remove it from the location
                self.inventory.append(item)
                location.items.remove(item)
                print(f"You picked up a {item.name} from the ground.")
            else:
                print(f"The {item.name} cannot be picked up.")
        else:
            print(f"There is no {item_pick} here.")

    def view_inventory(self):
        """Displays items in the Pymon's inventory."""
        if self.inventory:
            print("You are carrying:")
            for item in self.inventory:
                print(f"- {item.name}")
            use = input("Do you want to use an item? (yes/no): ").strip().lower()
            if use == "yes":
                item_used = input("Select item to use:")
                item = next((item for item in self.inventory if item.name.lower() == item_used.lower()), None)
                if item:
                    self.current_pymon.use_item(item, self)
                else:
                    print(f"Invalid items. You don't have {item_used}.")   
        else:
            print("Your inventory is empty.")
    def challenge_creature(self):
        creature_name = input("Challenge who: ").strip()
        self.current_pymon.challenge(creature_name, self)
    def generate_stats(self):
        self.current_pymon.display_battle_stats()

    def save_game(self):
        """ Save the current game"""
        try:
            filename = input("Enter filename to save game (e.g., save2024.csv): ")
            with open(filename, "w") as file:
                # Write a header to clarify sections
                file.write("Type,Name,Description,Location,West,North,East,South,Extra\n")

                # Save locations with connections
                for location in self.record.locations:
                    line = f"Location,{location.name},{location.description},{location.name},"
                    line += f"{location.doors['west'].get_name() if location.doors['west'] else 'None'},"
                    line += f"{location.doors['north'].get_name() if location.doors['north'] else 'None'},"
                    line += f"{location.doors['east'].get_name() if location.doors['east'] else 'None'},"
                    line += f"{location.doors['south'].get_name() if location.doors['south'] else 'None'},None\n"
                    file.write(line)

                # Save creatures and their current location
                for creature in self.record.creatures:
                    creature_type = "Pymon" if isinstance(creature, Pymon) else "Creature"
                    location_name = creature.get_location().name if creature.get_location() else "None"
                    line = f"{creature_type},{creature.name},{creature.description},{location_name},None,None,None,None,{creature.can_be_pymon}\n"
                    file.write(line)

                # Save items and their location (if in the map)
                for location in self.record.locations:
                    for item in location.items:
                        location_name = location.get_name()
                        line = f"Item,{item.name},{item.description},{location_name},None,None,None,None,{item.pickable},{item.consumable}\n"
                        file.write(line)

                
                # Save inventory (items carried by the Pymon)
                for item in self.inventory:
                    line = f"InventoryItem,{item.name},{item.description},Inventory,None,None,None,None,{item.pickable},{item.consumable}\n"
                    file.write(line)

                # Save Pymon's state
                if self.current_pymon:
                    pymon_location = self.current_pymon.get_location().name if self.current_pymon.get_location() else "None"
                    line = f"CurrentPymon,{self.current_pymon.name},{self.current_pymon.description},{pymon_location},None,None,None,None,"
                    line += f"Energy:{self.current_pymon.energy},MaxEnergy:{self.current_pymon.max_energy},Immunity:{self.current_pymon.immunity}\n"
                    file.write(line)

                # Save battle stats for Pymon
                for battle in self.current_pymon.stat_battle:
                    file.write(f"Battle,{battle['opponent']},{battle['timestamp']},None,None,None,None,None,Wins:{battle['wins']},Draws:{battle['draws']},Losses:{battle['losses']}\n")

                # Save captured Pymons in the pet list
                for pet in self.pet_list:
                    pet_location = pet.get_location().name if pet.get_location() else "N/A"
                    file.write(f"Pet,{pet.name},{pet.description},{pet_location},None,None,None,None,Energy:{pet.energy},MaxEnergy:{pet.max_energy},Immunity:{pet.immunity}\n")
            print(f"Game saved successfully to {filename}.")
        except FileNotFoundError:
            print(f"Error: {filename} not found.")

    def load_game(self):
        """Load the game state from a file."""
        filename = input("Enter the filename to load your game (e.g., save2024.csv): ")
        try:
            with open(filename, "r") as file:
                next(file)  # Skip header line
                for line in file:
                    line_field = line.strip().split(",")
                    # Parse each saved element
                    item_type = line_field[0]
                    if item_type == "Location":
                        name, description = line_field[1], line_field[2]
                        west, north, east, south = line_field[4], line_field[5], line_field[6], line_field[7]
                        location = Location(name, description)
                        location.doors = {
                            "west": west if west != "None" else None,
                            "north": north if north != "None" else None,
                            "east": east if east != "None" else None,
                            "south": south if south != "None" else None,
                        }
                        self.record.locations.append(location)
                    
                    elif item_type == "Creature" or item_type == "Pymon":
                        name, description = line_field[1], line_field[2]
                        location_name = line_field[3]
                        can_be_pymon = line_field[8].lower() == "yes"
                        creature = Pymon(name, description) if can_be_pymon else Creature(name, description)
                        if location_name != "None":
                            location = self.record.find_location(location_name)
                            if location:
                                creature.set_location(location)
                        self.record.creatures.append(creature)

                    elif item_type == "Item":
                        name, description = line_field[1], line_field[2]
                        location_name = line_field[3]
                        pickable = line_field[8].lower() == "yes"
                        consumable = line_field[9].lower() == "yes"
                        item = Item(name, description, pickable, consumable)
                        if location_name != "Inventory":
                            location = self.record.find_location(location_name)
                            if location:
                                location.items.append(item)
                        else:
                            self.inventory.append(item)
                        self.record.items.append(item)

                    elif item_type == "InventoryItem":
                        name, description = line_field[1], line_field[2]
                        pickable = line_field[8].lower() == "yes"
                        consumable = line_field[9].lower() == "yes"
                        item = Item(name, description, pickable, consumable)
                        self.inventory.append(item)

                    elif item_type == "CurrentPymon":
                        name, description = line_field[1], line_field[2]
                        location_name = line_field[3]
                        energy = int(line_field[8].split(":")[1])
                        max_energy = int(line_field[9].split(":")[1])
                        immunity = line_field[10].split(":")[1].lower() == "true"
                        
                        self.current_pymon = Pymon(name, description)
                        self.current_pymon.energy = energy
                        self.current_pymon.max_energy = max_energy
                        self.current_pymon.immunity = immunity

                        print("Check location pymon item_type = Pymon:", location_name )

                        if location_name != "None":
                            location = self.record.find_location(location_name)
                            print("Check location pymon:", location.get_name())
                            self.current_pymon.set_location(location)
                        
                        self.pet_list.append(self.current_pymon)

                    elif item_type == "Battle":
                        opponent = line_field[1]
                        timestamp = line_field[2]
                        wins = int(line_field[8].split(":")[1])
                        draws = int(line_field[9].split(":")[1])
                        losses = int(line_field[10].split(":")[1])
                        self.current_pymon.stat_battle.append({"opponent": opponent, "timestamp": timestamp, "wins": wins, "draws": draws, "losses": losses})

                    elif item_type == "Pet":
                        name, description = line_field[1], line_field[2]
                        location_name = line_field[3]
                        energy = int(line_field[8].split(":")[1])
                        max_energy = int(line_field[9].split(":")[1])
                        immunity = line_field[10].split(":")[1].lower() == "true"
                        
                        pet = Pymon(name, description)
                        pet.energy = energy
                        pet.max_energy = max_energy
                        pet.immunity = immunity

                        if location_name != "N/A":
                            location = next((loc for loc in self.record.locations if loc.name == location_name), None)
                            if location:
                                pet.set_location(location)

                        self.pet_list.append(pet)
                print(f"Game loaded successfully from {filename}.")
                return True
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return False



    def admin_mode(self):
        """Provides options for admin functions."""
        while True:
            print("\nAdmin Mode:")
            print("1) Add Custom Location")
            print("2) Add Custom Creature")
            print("3) Randomize Location Connections")
            print("4) Return to Main Menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                # Add a custom location
                self.record.add_custom_location(self.location_file)
            elif choice == '2':
                # Add a custom creature
                self.record.add_custom_creature(self.creature_file)
            elif choice == '3':
                # Randomize location connections
                self.record.randomize_locations()
                print("Location connections randomized.")
                # current pymon use bew map
                #self.current_pymon.current_location = self.record.find_location(self.current_pymon.current_location.get_name())
            elif choice == '4':
                # Return to main menu
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")
                
if __name__ == '__main__':
    ops = Operation()
    # ops.setup()
    # ops.display_setup()
    # ops.start_game()
    ops.main_menu()