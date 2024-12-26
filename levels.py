# levels.py
class Level:
    ''' It initialize the level class. 
        It tracks game progress through different levels.
        levels(list): It is a list of dictionaries. it contains what we required for fuel cell,
        number of cars deployed after each level.
        Current_level: it tracks the players current level.
        h2_cars_deployed: it records the total of H2 cars deployed from each level.
        Capacity: The total fuel capacity available for deploymen is set at 100.
        max_levels(int): the maximum number of levels in the game.'''
        
    def __init__(self):

        self.levels = [
            {"fuel_cells": 12, "cost": 5, "h2_cars": 500,"environment": "city"},
            {"fuel_cells": 30, "cost": 20, "h2_cars": 1000,"environment": "Edm-Cal"},
            {"fuel_cells": 50, "cost": 30, "h2_cars": 1500,"environment": "Banff"},
            {"fuel_cells": 90, "cost": 40, "h2_cars": 1000,"environment": "Red deer"},
            {"fuel_cells": 120, "cost":90, "h2_cars": 1000,"environment": "Vancouvar"},
        ]
        self.current_level = 0
        self.h2_cars_deployed = 0
        self.fuel_station_unlocked = False
        self.capacity = 100 
        self.max_levels = len(self.levels)  # Set the maximum number of levels

    def check_level_progression(self, fuel_count):
        # Check if the current fuel count meets the requirement for the current level
        if self.current_level < self.max_levels:
            required_fuel = self.levels[self.current_level]["fuel_cells"]
            if fuel_count >= required_fuel:
                self.unlock_level()
                return True
        return False

    def unlock_level(self):
        # Unlock the current level and increment the H2 cars deployed
        if self.current_level < len(self.levels):
            self.h2_cars_deployed += self.levels[self.current_level]["h2_cars"]
            self.fuel_station_unlocked = True  # Unlock the fuel station
            print(f"Level {self.current_level + 1} complete! Fuel station unlocked.")
            print(f"H2 Cars deployed: {self.h2_cars_deployed}")
            self.current_level += 1
        else:
            print("Congratulations! You've completed all levels!")

    def get_fuel_station_cost(self):
        # Returns the cost of the fuel station for the current level
        if self.current_level < len(self.levels):
            return self.levels[self.current_level]["cost"]
        return None

    def get_h2_cars_deployed(self):
        return self.h2_cars_deployed
    
    def get_current_environment(self):
        # New method to get the current level's environment theme
        if self.current_level < len(self.levels):
            return self.levels[self.current_level]["environment"]
        return None
    