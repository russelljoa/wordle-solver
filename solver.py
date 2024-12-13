import random
import json
with open("data.json", "r") as file:
        data = json.load(file)

class Solver:
    def __init__(self, data):
        #TODO change colored letters to a dictionary
        # Green should be a dictionary with a value as the index of the letter position
        # Yellow should be a dictionary with a value as the index of the letter position
        self.data = data
        self.possible_words = []
        self.green_letters = []
        self.yellow_letters = []
        self.disallowed_letters = []
        self.invalid_words = []
        self.tries = ["first", "second", "third", "fourth", "fifth", "last"]
        self.weighted_letters = []
        self.turn = 0
        self.possible_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        
    def start(self):
        print("Starting solver...\n\n")
        while True:
            #TODO handle possible words being 0 and it being 1
            reccomendation = ""
            if len(self.possible_words) > 0:
                reccomendation = "(reccomended word:" + self.get_random_word() + ")"
            while True:
                word = input(f"Enter {self.tries[self.turn]} word {reccomendation}: ")
                if "0" in word:
                    print("Please enter a valid word")
                else:
                    break

            if word == "exit":
                break
            colors = input(f"enter 0 for grey, 1 for yellow, 2 for green for the word\n{word}: \n")
            self.handle_result(word, colors)
                
            self.turn += 1
    
    def handle_result(self, word, colors):
        # TODO handle if word is not in possible words before doing stuff
        # make it so invalid letters can only appear once in the list

        last_list = []
        for x in range(len(colors)):
            print(f"Handling {word[x]}...")
            turn_valid_words = []
            invalid_words = []
            letter_index = self.possible_letters.index(word[x])
            if colors[x] == "0":
                self.disallowed_letters.append(word[x])
                
            elif colors[x] == "1":
                self.yellow_letters.append([word[x], x])

            elif colors[x] == "2":

                self.green_letters.append([word[x], x])

        print(f"Possible words before: {len(self.possible_words)}")
        #adds words to invalid words list that can not be the solution
        self.filter_invalid_words()

        print(f"Possible words after: {len(self.possible_words)}")
            
            
    def get_mutuals(self, list1, list2):
        for word in list1:
            if word not in list2:
                list2.append(word)
        return list2
        
    def filter_invalid_words(self):
        count = 0


        for letter in self.green_letters:
            for word in self.data[f"letter{letter[1]+1}"][letter[0]]:
                if word not in self.possible_words:
                    self.possible_words.append(word)
                if word not in self.invalid_words:
                    self.invalid_words += self.data["not_letter"][letter[0]]
        
        for letter in self.yellow_letters:
            for word in self.data[f"letter{letter[1] + 1}"][letter[0]]:
                if word not in self.invalid_words:
                    self.invalid_words.append(word)
            self.possible_words += self.data["has_letter"][letter[0]]

        for letter in self.disallowed_letters:
            for word in self.possible_words:
                if letter in word and word in self.possible_words:
                    self.possible_words.remove(word)
                    count += 1
        
        for word in self.possible_words:
            if word in self.invalid_words:
                self.possible_words.remove(word)

        file = open("STUFFFILTERINVALED.json", "w")
        file.write(json.dumps(self.possible_words, indent=4))

    def return_valid(self, list1):
        count = 0
        for letter in self.disallowed_letters:
            for word in list1:
                if letter in word and word in list1:
                    list1.remove(word)
                    count += 1
        return list1

            
        file = open("STUFF.json", "w")
        file.write(json.dumps(data, indent=4))

            

        print(f"Removed {count} words")

    def get_random_word(self):
        print(self.disallowed_letters)
        if len(self.green_letters) > 0:
            possible = self.return_valid(self.data[f"letter{self.green_letters[0][1]+1}"][self.green_letters[0][0]])
            return random.choice(possible)
        elif len(self.yellow_letters) > 0:
            possible = self.return_valid(self.data["has_letter"][self.yellow_letters[0][0]])
            return random.choice(possible)
        else:
            possible = self.return_valid(self.possible_words)
            return random.choice(possible)


solver = Solver(data)
solver.start()    