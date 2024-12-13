import json

from word_dict import words

alphabet = "abcdefghijklmnopqrstuvwxyz"
# dictionary with words and data attached to them
data = {

    "letter1": {

    },
    "letter2": {

    },
    "letter3": {

    },
    "letter4": {

    },
    "letter5": {

    },
    "has_letter": {

    },
    "not_letter": {
    },

    "double_letter": {
    },

    "words": []

}


# populate data dictionary
for word in words:
    print(f"Handling {word}...")
    data["words"].append(word)

    # populate not letter dictionary
    for letter in alphabet:
        if letter not in word:
            if letter not in data["not_letter"]:
                data["not_letter"][letter] = [word]
            else:
                data["not_letter"][letter].append(word)

    # populate letter dictionaries

    added_to_letter = set()
    for i in range(5):
        if word[i] not in added_to_letter:
            if word[i] not in data["has_letter"]:
                data["has_letter"][word[i]] = [word]
            else:
                data["has_letter"][word[i]].append(word)
            added_to_letter.add(word[i])

        if word[i] not in data[f"letter{i+1}"]:
            data[f"letter{i+1}"][word[i]] = [word]
        else:
            data[f"letter{i+1}"][word[i]].append(word)
    
    # Check for double letters
    added_to_double_letter = set()
    for letter in set(word):
        if word.count(letter) > 1 and word not in added_to_double_letter:
            if letter not in data["double_letter"]:
                data["double_letter"][letter] = [word]
            else:
                data["double_letter"][letter].append(word)
            added_to_double_letter.add(word)
    


    if len(data["words"]) > 100:
        break

print(data)

file = open("data.json", "w")
file.write(json.dumps(data, indent=4))

