########     ###    ######### ######### ##        #########     ######## ##     ## ######### ########    ########  ##       ##
##    ###   ## ##      ###       ###    ##        ##           ###       ##     ##    ###    ##     ##   ##     ## ###     ###
########   ##   ##     ###       ###    ##        ######         #####   #########    ###    ########    ########    #######
##    ### #########    ###       ###    ##        ##                 ### ##     ##    ###    ##          ##            ###
########  ##     ##    ###       ###    ######### #########     #######  ##     ## ######### ##        # ##            ###
# Made by Jacob Sieber | Version 1.0 | Made : 9/28/2025 - 10/1/2025

import random
import os

from helper import * 

class Ship:
    def __init__(self, length):
        self.length = length
        self.health = self.length

    def hit(self):
        self.health -= 1
        if self.health == 0:
            return True
        else:
            return False

class Board:
    def __init__(self, r, c):
        self.rows = r
        self.columns = c

        self.ships = [Ship(i) for i in range(5,1,-1)]
        self.needed_postions = 0
        for ship in self.ships:
            self.needed_postions += ship.length

        self.player_map = self.blank_board()
        self.enemy_map = None

        # I fix the error when placing mines by making sure the value is never None
        while self.enemy_map == None:
            self.enemy_map = self.place_ships()
        self.enemy_map = self.place_mines(7, self.enemy_map)
    
    def blank_board(self):
        b = []
        for i in range(self.rows):
            b.append([' ' for _ in range(self.columns)])
        return b

    def place_ships(self):
        """This function is a pain in my a... Also don't name your variable l they all look like fucking 1's"""
        b = self.blank_board()
        for r in range(self.rows):
            for c in range(self.columns):
                b[r][c] = 'o'

        ships_to_place = self.ships[:]
        attempt = len(ships_to_place)
        positions = []

        while attempt > 0:
            for ship in ships_to_place:
                horizontal = random.choice([True, False])

                test_r = random.randint(0, self.rows-1)
                test_c = random.randint(0, self.columns-1)

                f_blocked = False
                b_blocked = False
                valid_points = []

                if (test_r, test_c, ship) not in positions:
                    if horizontal:
                        output = self.find_horizontal_positions(test_r, test_c, valid_points, f_blocked, b_blocked, ship)
                        if output:
                            positions.append(output)
                            attempt -= 1
                        else:
                            break
                    else:
                        output = self.find_vertical_postions(test_r, test_c, valid_points, f_blocked, b_blocked, ship)
                        if output:
                            positions.append(output)
                            attempt -= 1
                        else:
                            break
                else:
                    break
        
        # Check to make sure we have the right number of points
        # This gets checked again because it sometimes returns 'None'
        if len(positions) == len(self.ships):
            for pos in positions:
                for point in pos:
                    b[point[0]][point[1]] = point[2]
            
            return b
        else:
            return None
            
    # I think that a lot of these functions take in too many arguments
    # A position class that the board makes would fix this(hopefully), but I didn't want to break my code 
    def next_horizontal_position(self, pos_r, pos_c, i, points, f_block, b_block, ship):
        if pos_c + i <= self.columns-1 and not f_block:
            if (pos_r, pos_c+i, ship) not in points:
                return [pos_r, pos_c+i, ship]
            else:
                return "Forward Blocked"
        if pos_c - (i - len(points)) >= 0 and not b_block: 
            if (pos_r, pos_c - (i - len(points)), ship) not in points:
                return [pos_r, pos_c - (i - len(points)), ship]
            else:
                return "Backward Blocked"
        return False
    
    def next_vertical_position(self, pos_r, pos_c, i, points, f_block, b_block, ship):
        if pos_r + i <= self.rows-1 and not f_block:
            if (pos_r+i, pos_c, ship) not in points:
                return [pos_r+i, pos_c, ship]
            else:
                return "Forward Blocked"
        if pos_r - (i - len(points)) >= 0 and not b_block: 
            if (pos_r - (i - len(points)), pos_c, ship) not in points:
                return [pos_r - (i - len(points)), pos_c, ship]
            else:
                return "Backward Blocked"
        return False
    
    def find_horizontal_positions(self, pos_r, pos_c, points, f_block, b_block, ship):
        f_b = f_block
        b_b = b_block
        valid_points = []
        for l in range(ship.length):
            output = self.next_horizontal_position(pos_r, pos_c, l, valid_points, f_b, b_b, ship)
            if output == "Forward Blocked":
                f_b = True
            elif output == "Backward Blocked":
                b_b = True
            elif output != False:
                valid_points.append(output)

        if len(valid_points) == ship.length:
            m = []
            for point in valid_points:
                oh_shit = valid_points.count(point)
                if oh_shit > 1:
                    m.append(False)
            if any(x == False for x in m):
                valid_points[:] = []
                return False
            return valid_points[:]
        else:
            points[:] = []
            return False
    
    def find_vertical_postions(self, pos_r, pos_c, points, f_block, b_block, ship):
        f_b = f_block
        b_b = b_block
        valid_points = []
        for l in range(ship.length):
            output = self.next_vertical_position(pos_r, pos_c, l, valid_points, f_b, b_b, ship)
            if output == "Forward Blocked":
                f_b = True
            elif output == "Backward Blocked":
                b_b = True
            elif output != False:
                valid_points.append(output)

        if len(valid_points) == ship.length:
            m = []
            for point in valid_points:
                oh_shit = valid_points.count(point)
                if oh_shit > 1:
                    m.append(False)
            if any(x == False for x in m):
                points[:] = []
                return False
            return valid_points[:]
        else:
            points[:] = []
            return False
    
    def place_mines(self, number, map):
        b = map[:] # error was the map object was not iterable meaning somehting before this messed up a lot.
        for i in range(number):
            test_r = random.randint(0, self.rows-1)
            test_c = random.randint(0, self.columns-1)
            if b[test_r][test_c] == 'o':
                b[test_r][test_c] = '*'
            else:
                i -=1
        return b

class BattleShip:
    def __init__(self):
        self.board = Board(10, 10)
        self.current_message = ""
        self.remaining_ships = len(self.board.ships)
        self.health = 3
        
    def start(self):
        self.game()

        again = (input("Would you like to play again: ")).lower()
        if again == "yes" or again == 'y':
            self.__init__()
            self.start()
    
    def game(self):
        while True:
            letter,number = self.safe_guess()
            enemy_position = self.board.enemy_map[letter][number]

            if enemy_position in self.board.ships:
                self.board.player_map[letter][number] = "\033[31mx\033[0m"
                if enemy_position.hit():
                    self.current_message = "\nYou sunk my battle ship"
                    self.remaining_ships -= 1
                    if self.remaining_ships == 0:
                        self.current_message = "\nYou Win!"
                        self.print_screen()
                        break
                else:
                    self.current_message = "\nYou hit something"
            elif enemy_position == '*':
                self.board.player_map[letter][number] = "\033[33m*\033[0m"
                self.current_message = "\nYou hit a bomb."
                self.health -= 1
                if self.health == 0:
                    self.current_message = "\nYou Lose!"
                    self.print_screen()
                    break
            else:
                self.board.player_map[letter][number] = "o"
                self.current_message = "\nYou missed"
    
    def print_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear') # stack overflow my goat

        print_large("battle_ship!")

        print("\n-- enter 'exit' or 'quit' to close the program --")

        # Board Numbers
        print("\n  ", end="")
        for c in range(self.board.columns):
            print(f"\033[4m {c+1} \033[0m", end="")

        # Board letters and Spaces
        for r in range(self.board.rows):
            print(f"\n{chr(65+r)}|", end="")
            for c in range(self.board.columns):
                print(f"[{self.board.player_map[r][c]}]", end="")
        
        print(self.current_message)
    
    def safe_guess(self):
        """Returns the letter and number of target"""
        while True:
            self.print_screen()
            l,n = '', 0
            g = (input("\nWhat square would you like to fire at: ")).upper()
            g = g.replace(" ", "")
            if len(g) <= 3 and g.isalnum():
                if g[1:].isdigit():
                    l = g[0]
                    n = int(g[1:])
                    if n > self.board.columns or ord(l) > 65 + self.board.columns-1:
                        self.current_message = "\nInvaild square outside map. Please try again."
                    else:
                        if self.board.player_map[ord(l) - 65][n-1] == ' ':
                            return ord(l) - 65, n-1 # when n is zero it returns -1 the valid last pos of the list
                        else:
                            self.current_message = "\nYou already guessed that square."
                else:
                    self.current_message = "\nSquare must be in format A2"
            elif g == "EXIT" or g == "QUIT":
                exit()
            else:
                self.current_message = "\nSquare must a letter and a number with no special characters."

        
if __name__=='__main__':
    game = BattleShip()
    game.start()