import json

class Solver:


from word_dict import words

# dictionary with words and data attached to them
data = {

    "first_letter": {

    },
    "second_letter": {

    },
    "third_letter": {

    },
    "fourth_letter": {

    },
    "fifth_letter": {

    },
    "has_letter": {

    },
    "not_letter": {
    },

    "double_letter": {
    },

    "words": {
    }

}

for word in words:
    data["words"][word] = {}

    if word[0] not in data["first_letter"]:
        data["first_letter"][word[0]] = [word]
    else:
        data["first_letter"][word[0]].append(word)

    if word[1] not in data["second_letter"]:
        data["second_letter"][word[1]] = [word]
    else:
        data["second_letter"][word[1]].append(word)

    if word[2] not in data["third_letter"]:
        data["third_letter"][word[2]] = [word]
    else:
        data["third_letter"][word[2]].append(word)
    
    if word[3] not in data["fourth_letter"]:
        data["fourth_letter"][word[3]] = [word]
    else:
        data["fourth_letter"][word[3]].append(word)
    
    if word[4] not in data["fifth_letter"]:
        data["fifth_letter"][word[4]] = [word]
    else:
        data["fifth_letter"][word[4]].append(word)
    
    

