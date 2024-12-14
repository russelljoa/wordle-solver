import random
import json
import colorama

with open("data.json", "r") as file:
    data = json.load(file)

class Solver:
    """Class to solve the wordle"""

    def __init__(self, data):
        """Initializes the class and its variables"""
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.data = data

        #format ("letter", position)
        self.green_letters = set()
        #format ("letter", position)
        self.yellow_letters = set()
        #format ("letter", position)
        self.grey_letters = set()

        #format ("letter", position)
        self.unguessed_letters = set()
        for letter in self.alphabet:
            for index in range(5):
                self.unguessed_letters.add((letter, index))

        self.possible_words = set(self.data["words"])

        #format "word": score
        self.weighted_words = {}


        #TODO INTEGRADE WORD COUNT IN TEH CODE
        self.word_count = set()
        
        self.tries = ["first", "second", "third", "fourth", "fifth", "last"]

        self.turn = 0

    
    def get_green_words(self):
        """Returns all the words that contain the green letters"""
        words = set()
        for letter in self.green_letters:
            for word in self.data[f"letter{letter[1]+1}"][letter[0]]:
                if self.is_valid(word):
                    words.add(word)
        return words
    
    def get_yellow_words(self):
        """Returns all the words that contain the yellow letters"""
        words = set()
        for letter in self.yellow_letters:
            for word in self.data["has_letter"][letter[0]]:
                if self.is_valid(word):
                    words.add(word)
        return words
    
    def get_grey_words(self):
        """Returns all the words that don't contain the grey letters"""
        words = set()
        for letter in self.grey_letters:

            for word in self.data["not_letter"][letter[0]]:
                if self.is_valid(word):
                    words.add(word)

        return words

    def get_valid_words(self):
        """Returns all the valid words"""
        words = set()
        words.update(self.get_green_words())
        words.update(self.get_yellow_words())
        words.update(self.get_grey_words())

        print(f"Found {len(words)} valid words")
        return words
    
    def prune_words(self):
        """Prunes the possible words (should be called after every guess)"""
        count = 0
        for word in self.possible_words:
            if not self.is_valid(word):
                count += 1
                self.possible_words.remove(word)

        print(f"Pruned {count} words")

    def is_valid(self, word):
        """Checks if a word is valid based on the current state"""

        for green in self.green_letters:
            letter = green[0]
            position = green[1]
            
            if word[position] != letter:
                #print("false because it doesn't have the green letter in the right spot")
                return False
        for yellow in self.yellow_letters:
            letter = yellow[0]
            position = yellow[1]
            if word[position] == letter or letter not in word:
                return False
        for grey in self.grey_letters:
            letter = grey[0]
            if letter in word:
                #print("false because it has a grey letter")
                return False
        return True
    
    def add_green_letter(self, letter, position):
        """Adds a green letter to the solver"""
        # Adds the letter to the green letters and removes it from the unguessed letters
        self.green_letters.add((letter, position))

        self.unguessed_letters.discard((letter, position))

    def add_yellow_letter(self, letter, position):
        """Adds a yellow letter to the solver"""
        # Adds the letter to the yellow letters and removes it from the unguessed letters
        self.yellow_letters.add((letter, position))
        self.unguessed_letters.discard((letter, position))
    
    def add_grey_letter(self, letter, position):
        """Adds a grey letter to the solver"""
        # Adds the letter to the grey letters and removes it from the unguessed letters
        # doesn't get rid of a letter if it is in green already
        for green in self.green_letters:
            if letter == green[0]:
                self.yellow_letters.add((letter, position))
        add = False
        for yellow in self.yellow_letters:
            if letter == yellow[0]:
                add = True

        if add:
            self.yellow_letters.add((letter, position))
        temp_green = [green[0] for green in self.green_letters]    
        temp_yellow = [yellow[0] for yellow in self.yellow_letters]
        if letter not in temp_green and letter not in temp_yellow:
            self.grey_letters.add((letter, position))

        for x in range(5):
            if (letter, x) in self.unguessed_letters:
                self.unguessed_letters.discard((letter, x))
    
    
    def get_score(self, word):
        """Returns the score of a word"""
        score = 0
        for letter in word:
            #scores if the word contains a green letter and gives more pouints if the letter is in the right spot
            for green in self.green_letters:
                if word[green[1]] == green[0]:
                    score += 10
                elif letter == green[0]:
                    score += 1

            #scores if the word contains a yellow letter and gives no points if the word is in the wrong spot
            for yellow in self.yellow_letters:
                if letter == yellow[0] and word[yellow[1]] != yellow[0]:
                    score += 2
            
            # gives the word a negative score if it contains a grey letter
            if letter in self.grey_letters:
                score = -100
        
        return score

    def weight_words(self):
        """Returns a set of words with their score"""
        # removes all the words that are not possible
        temp = self.weighted_words.copy()
        for word in self.weighted_words:
            if word not in self.possible_words:
                temp.pop(word)
        self.weighted_words = temp
        # adds the score of the word to the weighted words
        for word in self.possible_words:
            score = self.get_score(word)
            if word in self.weighted_words:
                # adds 5 points to the word if it has been in the possible words for longer indicating ahigher chance of it beign the solution
                self.weighted_words[word] += 5
            else:
                self.weighted_words[word] = score
    
    def recommend_word(self):
        """Recommends the best word based on the current state"""
        if not self.weighted_words:
            return None
        return max(self.weighted_words, key=self.weighted_words.get)
    
    def win(self):
        """Returns True if the solver has won"""
        if len(self.green_letters) == 5 or len(self.possible_words) == 1:
            return True
        return False
    
    def input_is_valid(self, word, color):
        # checks if the call is valid
        if len(word) != 5 or len(color) != 5:
            return False
        for letter in word:
            if letter not in self.alphabet:
                return False
        try:
            int(color)
        except:
            return False
        return True
        
            
    
    def handle_word(self, word, color):
        """Handles the word and its color"""
        word = word.lower()
        for x in range(5):
            if color[x] == "2":
                self.add_green_letter(word[x], x)
            elif color[x] == "1":
                self.add_yellow_letter(word[x], x)
            elif color[x] == "0":
                self.add_grey_letter(word[x], x)

    
    def start(self):
        while True:
            print("Starting solver...\n\n")
            while self.turn < 6:
                # gets the reccomended word
                reccomendation = self.recommend_word()
                if reccomendation == None:
                    reccomendation = "Good starting words:\nslate, trace, crane, stale"
                print(f"Reccomended word: {reccomendation}")
                # gets the color of the word
                #input loop to ensure valid input
                while True:
                    word = input(f"Enter the {self.tries[self.turn]} word: ")

                    color = input(f"enter 0 for grey, 1 for yellow, 2 for green for the word\n{word}: \n")
                    # handles the word and its color
                    if self.input_is_valid(word, color):
                        self.handle_word(word, color)
                        break
                    else:
                        print("Invalid input. Please try again\n")
                
                self.possible_words = self.get_valid_words()
                # prunes the possible words
                self.prune_words()
                self.weight_words()
                file = open(f"STUFF{self.turn}.json", "w")
                file.write(json.dumps(list(self.possible_words), indent=4))
                # checks if the solver has won
                
                if self.win():
                    break
                # increments the turn
                
                self.turn += 1

                print(f"There are now {len(self.possible_words)} possible words\n\n")

            if self.win():
                print(f"The word is {self.recommend_word()}")
            else:
                print(f"You lost. There were still {len(self.possible_words)} possible words.")
                test = input("Was your word in the list of possible words? Enter it below:\n")
                if test in self.possible_words:
                    print("I made a mistake. Sorry about that.")
                else:
                    print("I couldn't find your word. Sorry about that.")
            
            # asks the user if they want to play again
            play_again = input("Do you want to play again? (y/n)\n")
            if play_again.lower() == "n":
                break
            else:
                self.__init__(data)
                print("\nStarting new game...\n\n")

solver = Solver(data)
solver.start()