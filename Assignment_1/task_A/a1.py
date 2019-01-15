def five_x_cubed_plus_1(x):
    return 5 * x ** 3 + 1


def pair_off(initial_list):
    final_list = []
    for index in range(0, len(initial_list), 2):
        if (index + 1) < len(initial_list):
            new_pair = [initial_list[index], initial_list[index + 1]]
        else:
            new_pair = [initial_list[index]]

        final_list.append(new_pair)

    return final_list


def mystery_code(plaintext):
    import string
    ciphertext = ""
    for char in plaintext:
        if not char.isalpha():
            ciphertext += char

        elif char.islower():
            old_index = string.ascii_lowercase.index(char)
            new_index = (old_index + 19) % 26
            ciphertext += string.ascii_uppercase[new_index]

        elif char.isupper():
            old_index = string.ascii_uppercase.index(char)
            new_index = (old_index + 19) % 26
            ciphertext += string.ascii_lowercase[new_index]

        else:
            raise ValueError("Unexpected character given to mystery_code function.")

    return ciphertext


def past_tense(initial_list):
    irregulars = ["have", "has", "be", "am", "is", "are", "eat", "eats", "go", "goes"]
    vowels = ['a', 'e', 'i', 'o', 'u']
    final_list = []
    for verb in initial_list:
        verb = verb.lower()
        if verb in irregulars:
            if verb == "have" or verb == "has":
                past_verb = "had"

            elif verb == "be" or verb == "am" or verb == "is":
                past_verb = "was"

            elif verb == "are":
                past_verb = "were"

            elif verb == "eat" or verb == "eats":
                past_verb = "ate"

            elif verb == "go" or verb == "goes":
                past_verb = "went"

            else:
                raise ValueError("Unknown irregular verb given to past_tense function.")

        elif verb[-1] == 'e':
            past_verb = verb + 'd'

        elif verb[-1] == 'y' and (verb[-2] not in vowels):
            past_verb = verb
            past_verb[-1] = 'i'
            past_verb += "ed"

        elif (verb[-2] in vowels) and (not verb[-3] in vowels) and (not verb[-1] in vowels) and (not verb[-1] == 'y') \
                and (not verb[-1] == 'w'):
            past_verb = verb
            past_verb += past_verb[-1]
            past_verb += "ed"

        else:
            past_verb = verb + "ed"

        final_list.append(past_verb)

    return final_list
