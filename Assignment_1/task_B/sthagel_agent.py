import random
import string

memory = []
cycle_counters = [0, 0, 0, 0]


def introduce():
    return "Good morrow, noble squire. My name is Sir Bugsalot.\n" \
           "I was brought down onto this world by Stephan Hagel.\n" \
           "If ye are to bring your word to him, ye shall deliver message to sthagel@uw.edu.\n" \
           "What is your desire?"


def agentName():
    return "Sir Bugsalot"


def respond(the_input):
    exclude = set(string.punctuation)
    input_wo_punctuation = ''.join(ch for ch in the_input if ch not in exclude)

    wordlist = input_wo_punctuation.split(' ')
    wordlist[0] = wordlist[0].lower()

    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0] = mapped_wordlist[0].capitalize()

    answer = find_response(the_input, wordlist, mapped_wordlist)

    return answer


def you_me(w):
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result


def you_me_map(wordlist):
    return [you_me(w) for w in wordlist]


CASE_MAP = {'i': 'you', 'I': 'you', 'me': 'you', 'you': 'me',
            'my': 'your', 'your': 'my',
            'yours': 'mine', 'mine': 'yours', 'am': 'are'}


def find_response(the_input, wordlist, mapped_wordlist):
    farewells = ["bye", "goodbye", "farewell", "ciao", "faretheewell", "godspeed"]
    question_words = ['when', 'why', 'where', 'how']
    default_sentences = ["How are you?", "How do you feel today?", "What would you like to talk about today?",
                         "Call your desire!", "How do you like my sword?",
                         "A tale is but half told when only one person tells it."]
    memory_verbs = ["do", "feel", "am", "have", "love", "hate", "like"]
    verbs = ["do", "are", "have", "go", "try", "eat", "take", "help", "make", "get", "jump", "walk", "write", "read",
             "put", "swing", "think", "drink", "ride", "add"]

    if wordlist[0] == "i" and (wordlist[1] in memory_verbs or wordlist[1:3] == ["dont", "know"]):
        memory.append(wordlist)

    if wordlist[0:4] == ["what", "is", "the", "word"]:
        response = "Bababa Bird, Bird, Bird, Bird is the word!"
        return response

    if wordlist == ["i", "love", "you"]:
        response = "I like you too, but I think we should stay friends."
        return response

    if wordlist[0] in farewells:
        response = "Fare-thee-well!"
        return response

    if wordlist[0] == '':
        responses_to_silence = ["You don't seem to be very talkative.", "Don't be so shy!",
                                "Is my noble presence intimidating you?", "I will soon lose my patience..."]
        response = responses_to_silence[cycle_counters[0]]

        cycle_counters[0] += 1
        cycle_counters[0] %= len(responses_to_silence)
        return response

    if wordlist[0:2] == ["i", "am"]:
        if wordlist[2] == "happy" or wordlist[2] == "glad":
            responses_to_happiness = ["It fills my heart with happiness to hear about your fortune.", "To be continued"]
            response = random.choice(responses_to_happiness)
            return response

        else:
            responses_to_i_am = ["Why are you " + ' '.join(mapped_wordlist[2:]) + "?", "Tell me more."]
            response = responses_to_i_am[cycle_counters[1]]

            cycle_counters[1] += 1
            cycle_counters[1] %= len(responses_to_i_am)
            return response

    if wordlist[0:3] == ["how", "are", "you"]:
        responses_to_how_are_you = ["I feel great today!", "I am good.", "Very well!"]
        response = random.choice(responses_to_how_are_you)
        return response

    if wordlist[0] in question_words:
        response = "I don't know " + wordlist[0] + ". I only know how to use my sword!"
        return response

    if wordlist[0:2] == ["i", "feel"]:
        responses_to_i_feel = ["I know that feeling.", "Why do you feel " + ' '.join(mapped_wordlist[2:]) + "?"]
        response = random.choice(responses_to_i_feel)
        return response

    if wordlist[0:2] == ["i", "have"]:
        responses_to_i_have = ["How long have you had " + ' '.join(mapped_wordlist[2:]) + "?", "I have " +
                               ' '.join(wordlist[2:]) + " as well."]

        response = responses_to_i_have[cycle_counters[2]]

        cycle_counters[2] += 1
        cycle_counters[2] %= len(responses_to_i_have)
        return response

    if wordlist[0:3] == ["i", "dont", "know"] or wordlist[0:4] == ["i", "do", "not", "know"]:
        response = "You do not seem to be a very wise man."
        return response

    if "ever" in wordlist or "every" in wordlist or "everyone" in wordlist:
        responses_to_every = ["You like to generalize things, don't you?",
                              "Someone with a good heart does not speak in absolutes!"]
        response = random.choice(responses_to_every)
        return response
    
    if wordlist[0] == "no":
        response = "Why do you think so negative?"
        return response
    
    if "yes" in wordlist:
        responses_to_yes = ["I like your positive attitude.", "Are you sure about that?", "Can you prove that?"]
        response = random.choice(responses_to_yes)
        return response

    if "because" in wordlist:
        responses_to_because = ["Do you really think, this is the reason?", "I like your reasoning.",
                                "You seem to know the reason for everything in this world!"]
        response = responses_to_because[cycle_counters[2]]

        cycle_counters[3] += 1
        cycle_counters[3] %= len(responses_to_because)
        return response

    if "maybe" in wordlist:
        response = "Don't be so irresolute!"
        return response

    if wordlist[0:2] == ["i", "like"] or wordlist[0:2] == ["i", "love"]:
        responses_to_love = ["I " + wordlist[2:] + " as well.", "Why do you " + mapped_wordlist[2:] + "?",
                             "I am glad, that you have something that makes you happy."]
        response = random.choice(responses_to_love)
        return response

    if wordlist[0:2] == ["can", "you"] or wordlist[0:2] == ["could", "you"]:
        responses_to_can_you = ["A noble knight like me can do everything!", "Surely I " + wordlist[0] +
                                ' '.join(mapped_wordlist[2:]) + ".", "Why do you want to know that?"]
        response = random.choice(responses_to_can_you)
        return response

    if wordlist[0] == "you" and wordlist[1] in verbs:
        responses_to_you_are = ["You know me well!", "Yes indeed, I " + ' '.join(mapped_wordlist[1:])]
        response = random.choice(responses_to_you_are)
        return response

    if len(memory) > 0:
        response = ' '.join(you_me_map(random.choice(memory))) + ", if I remember correctly. Tell me more about it!"
        return response

    return random.choice(default_sentences)
