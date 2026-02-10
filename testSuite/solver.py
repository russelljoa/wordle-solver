import random
import json
import colorama


# Version of solver made to run without user input for testing purposes.

def compute_feedback(guess, secret):
    """
    Computes Wordle feedback for a guess:
    - '2' means the letter is in the correct spot (green),
    - '1' means the letter is in the word but in a different spot (yellow),
    - '0' means the letter is not in the word (grey).
    """
    result = [None] * 5
    secret_remaining = list(secret)
    # First pass: mark greens.
    for i in range(5):
        if guess[i] == secret[i]:
            result[i] = '2' # type: ignore
            secret_remaining[i] = None  # Mark this letter as used.
    # Second pass: mark yellows and greys.
    for i in range(5):
        if result[i] is None:
            if guess[i] in secret_remaining:
                result[i] = '1' # type: ignore
                # Remove the first occurrence so that repeated letters are handled correctly.
                secret_remaining[secret_remaining.index(guess[i])] = None
            else:
                result[i] = '0' # type: ignore
    return ''.join(result) # type: ignore

class Solver:
    """Class to solve the Wordle puzzle."""
    def __init__(self, data):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.data = data

        # Stores letters that have been marked as green/yellow/grey.
        self.green_letters = set()    # Each element is (letter, position)
        self.yellow_letters = set()   # Each element is (letter, position)
        self.grey_letters = set()     # Each element is (letter, position)

        # All letter/position pairs that haven’t been guessed yet.
        self.unguessed_letters = set()
        for letter in self.alphabet:
            for index in range(5):
                self.unguessed_letters.add((letter, index))

        # The set of possible words is taken from the data.
        self.possible_words = set(self.data["words"])

        # A dictionary of words to scores.
        self.weighted_words = {}

        self.turn = 0

    def get_green_words(self):
        words = set()
        for letter in self.green_letters:
            for word in self.data[f"letter{letter[1]+1}"][letter[0]]:
                if self.is_valid(word):
                    words.add(word)
        return words

    def get_yellow_words(self):
        words = set()
        for letter in self.yellow_letters:
            for word in self.data["has_letter"][letter[0]]:
                if self.is_valid(word):
                    words.add(word)
        return words

    def get_grey_words(self):
        words = set()
        for letter in self.grey_letters:
            for word in self.data["not_letter"][letter[0]]:
                if self.is_valid(word):
                    words.add(word)
        return words

    def test_prune_letters(self):
    
        if self.turn == 6 or len(self.possible_words) <= 10:
            return False
        if len(self.remaining_letters()) < (5 - self.turn) * 5 and self.turn <= 2:
            return True
        return False

    def remaining_letters(self):
        letters = set()
        green = [g[0] for g in self.green_letters]
        yellow = [y[0] for y in self.yellow_letters]
        for word in self.possible_words:
            for letter in word:
                if (letter not in green and letter not in yellow) or (letter in "aeiou"):
                    letters.add(letter)
        return letters

    def get_valid_words(self):
        words = set()
        words.update(self.get_green_words())
        words.update(self.get_yellow_words())
        words.update(self.get_grey_words())
        return words

    def prune_words(self):
        # Remove words that do not match the current clues.
        for word in list(self.possible_words):
            if not self.is_valid(word):
                self.possible_words.remove(word)

    def is_valid(self, word):
        # Check that the word has the required green letters.
        for green in self.green_letters:
            letter, pos = green
            if word[pos] != letter:
                return False
        # Check yellow letters: they must be in the word but not in the given position.
        for yellow in self.yellow_letters:
            letter, pos = yellow
            if word[pos] == letter or letter not in word:
                return False
        # Exclude words containing grey letters.
        for grey in self.grey_letters:
            letter, _ = grey
            if letter in word:
                return False
        return True

    def add_green_letter(self, letter, position):
        self.green_letters.add((letter, position))
        self.unguessed_letters.discard((letter, position))

    def add_yellow_letter(self, letter, position):
        self.yellow_letters.add((letter, position))
        self.unguessed_letters.discard((letter, position))

    def add_grey_letter(self, letter, position):
        for green in self.green_letters:
            if letter == green[0]:
                self.yellow_letters.add((letter, position))
        add = False
        for yellow in self.yellow_letters:
            if letter == yellow[0]:
                add = True
        if add:
            self.yellow_letters.add((letter, position))
        temp_green = [g[0] for g in self.green_letters]
        temp_yellow = [y[0] for y in self.yellow_letters]
        if letter not in temp_green and letter not in temp_yellow:
            self.grey_letters.add((letter, position))
        for x in range(5):
            if (letter, x) in self.unguessed_letters:
                self.unguessed_letters.discard((letter, x))

    def get_score(self, word):
        score = 0
        for letter in word:
            for green in self.green_letters:
                if word[green[1]] == green[0]:
                    score += 10
                elif letter == green[0]:
                    score += 1
            for yellow in self.yellow_letters:
                if letter == yellow[0] and word[yellow[1]] != yellow[0]:
                    score += 2
            if letter in self.grey_letters:
                score = -100
        return score

    def old_weight_words(self):
        temp = self.weighted_words.copy()
        for word in self.weighted_words:
            if word not in self.possible_words:
                temp.pop(word)
        self.weighted_words = temp
        for word in self.possible_words:
            score = self.get_score(word)
            if word in self.weighted_words:
                self.weighted_words[word] += 5
            else:
                self.weighted_words[word] = score
                
    def weight_words(self):
        # Calculate letter frequencies across all possible words
        letter_frequencies = self.calculate_letter_frequencies()
        positional_frequencies = self.calculate_positional_frequencies()

        temp = self.weighted_words.copy()
        for word in self.weighted_words:
            if word not in self.possible_words:
                temp.pop(word)
        self.weighted_words = temp

        for word in self.possible_words:
            # Base score from the current scoring system
            score = self.get_score(word)

            # Add score based on letter frequencies
            score += sum(letter_frequencies.get(letter, 0) for letter in set(word))

            # Add score based on positional frequencies
            score += sum(positional_frequencies[i].get(word[i], 0) for i in range(5))

            # Add a penalty for repeated letters to encourage diversity
            if len(set(word)) < len(word):
                score -= 5

            # Update the weighted words dictionary
            if word in self.weighted_words:
                self.weighted_words[word] += score
            else:
                self.weighted_words[word] = score

    def calculate_letter_frequencies(self):
        """Calculate the frequency of each letter in the remaining possible words."""
        frequencies = {}
        for word in self.possible_words:
            for letter in set(word):  # Use set to avoid double-counting letters in the same word
                frequencies[letter] = frequencies.get(letter, 0) + 1
        return frequencies

    def calculate_positional_frequencies(self):
        """Calculate the frequency of each letter in each position across the remaining possible words."""
        positional_frequencies = [{} for _ in range(5)]
        for word in self.possible_words:
            for i, letter in enumerate(word):
                positional_frequencies[i][letter] = positional_frequencies[i].get(letter, 0) + 1
        return positional_frequencies

    def recommend_word(self):
        if not self.weighted_words:
            return None
        #if self.test_prune_letters():
            words = set()
            remaining_letters = self.remaining_letters()
            for word in self.possible_words:
                count = 0
                for letter in word:
                    if letter in remaining_letters:
                        count += 1
                if count >= 3:
                    words.add(word)
            if len(words) == 0:
                return max(self.weighted_words, key=self.weighted_words.get) # type: ignore
            else:
                return random.choice(list(words))
        else:
            return max(self.weighted_words, key=self.weighted_words.get) # type: ignore

    def handle_word(self, word, color):
        """
        Updates the solver's state with the guessed word and its feedback.
        The input `color` should be a 5-digit string where each digit is:
          0: grey, 1: yellow, 2: green.
        """
        word = word.lower()
        # Create a list of [feedback, letter, position] and sort so that greens are processed first.
        word_list = [[int(color[x]), word[x], x] for x in range(len(word))]
        word_list.sort(reverse=True)
        for item in word_list:
            if item[0] == 2:
                self.add_green_letter(item[1], item[2])
            elif item[0] == 1:
                self.add_yellow_letter(item[1], item[2])
            elif item[0] == 0:
                self.add_grey_letter(item[1], item[2])

    def run_game(self, secret_word):
        """
        Runs a simulated game using the solver logic for a given secret word.
        Returns a tuple:
            (number_of_guesses, solved_boolean, secret_word)
        The number of guesses is 6 if the solver fails to guess the word.
        """
        # Reset solver state for a new game.
        self.turn = 0
        self.green_letters = set()
        self.yellow_letters = set()
        self.grey_letters = set()
        self.unguessed_letters = set()
        for letter in self.alphabet:
            for index in range(5):
                self.unguessed_letters.add((letter, index))
        self.possible_words = set(self.data["words"])
        self.weighted_words = {}

        # Use "trace" as the first guess.
        first_guess = "stale"
        feedback = compute_feedback(first_guess, secret_word)
        self.handle_word(first_guess, feedback)
        self.prune_words()
        self.weight_words()
        if first_guess == secret_word:
            return self.turn + 1, True, secret_word
        self.turn += 1

        while self.turn < 6:
            self.prune_words()
            self.weight_words()
            recommendation = self.recommend_word()
            if recommendation is None:
                recommendation = random.choice(list(self.possible_words))
            # Compute feedback automatically.
            feedback = compute_feedback(recommendation, secret_word)
            self.handle_word(recommendation, feedback)
            
            if recommendation == secret_word:
                return self.turn + 1, True, secret_word
            self.turn += 1
        return -1, False, secret_word

def run_solver(secret_word, data):
    """
    Convenience function to create a new Solver instance and run a game.
    Returns a tuple (number_of_guesses, solved_boolean, secret_word).
    """
    solver = Solver(data)
    return solver.run_game(secret_word)

if __name__ == "__main__":
    # For interactive testing if desired.
    with open("data.json", "r") as file:
        data = json.load(file)
    solver = Solver(data)
    secret_word = input("Enter the secret word for testing: ").strip().lower()
    guesses, solved, word = solver.run_game(secret_word)
    print(json.dumps({"guesses": guesses, "solved": solved, "word": word}))
