import json
import random
import time
from solver import run_solver

# Load the word data.
with open("data.json", "r") as file:
    data = json.load(file)

# Load or initialize the fails.json file.
try:
    with open("testSuite/fails.json", "r") as file:
        fails_data = json.load(file)
except FileNotFoundError:
    fails_data = {"fails": []}  # Initialize with an empty "fails" list if the file doesn't exist.

# Set the number of test runs.

words = data["words"]
#words = fails_data["fails"]
num_tests = len(words)

# Select a random sample of secret words.
test_words = random.sample(words, num_tests)

results = []
success_count = 0
guess_list = []
count = 1
for secret in test_words:
    print(f'Attempt {count} of {num_tests} | Success Rate: {int((success_count/count) * 10000)/100}%', end='\r')
    count += 1
    guesses, solved, word = run_solver(secret, data)
    results.append((secret, guesses, solved))
    
    # Track success and failure.
    if solved:
        success_count += 1
        guess_list.append(guesses)
    else:
        # Add failed word to the "fails" list in fails_data.
        if secret not in fails_data["fails"]:
            fails_data["fails"].append(secret)

# Save the updated fails.json data.
with open("testSuite/fails.json", "w") as file:
    json.dump(fails_data, file, indent=2)

# Calculate and display the success rate.
average_guesses = sum(guess_list) / len(guess_list) if guess_list else 0
r = False
if r:
    for secret, guesses, solved in results:
        print(f"Secret: {secret}, Guesses: {guesses}, Solved: {solved}")

print(f"Success rate: {success_count} out of {num_tests} ({(success_count/num_tests)*100:.2f}%) in an average of {average_guesses:.2f} guesses.")