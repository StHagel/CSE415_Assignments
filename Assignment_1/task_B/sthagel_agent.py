import random
import string

memory = []
cycle_counters = [0, 0, 0, 0, 0]


def introduce():
    return "Good morrow, noble squire. My name is Sir Bugsalot.\n" \
           "I was brought down onto this world by Stephan Hagel.\n" \
           "If ye are to bring your word to him, ye shall deliver message to sthagel@uw.edu.\n" \
           "What is your desire?"


def agentName():
    return "Sir Bugsalot"


def respond(the_input):
    exclude = set(string.punctuation)
    input_wo_punctuation = "".join(ch for ch in the_input if ch not in exclude)

    wordlist = input_wo_punctuation.split(" ")
    wordlist[0] = wordlist[0].lower()

    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0] = mapped_wordlist[0].capitalize()

    answer = find_response(wordlist, mapped_wordlist)

    return answer


def you_me(w):
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result


def you_me_map(wordlist):
    return [you_me(w) for w in wordlist]


CASE_MAP = {"i": "you", "I": "you", "me": "you", "you": "me", "my": "your", "your": "my", "are": "am", "yours": "mine",
            "mine": "yours", "am": "are"}


def find_response(wordlist, mapped_wordlist):
    farewells = ["bye", "goodbye", "farewell", "ciao", "faretheewell", "godspeed"]
    question_words = ["when", "why", "where", "how", "what", "which"]
    default_sentences = ["How are you?", "How do you feel today?", "What would you like to talk about today?",
                         "Call your desire!", "How do you like my sword?",
                         "A tale is but half told when only one person tells it."]
    memory_verbs = ["do", "feel", "am", "have", "love", "hate", "like", "know", "wish"]
    verbs = ["do", "are", "am", "have", "go", "try", "eat", "take", "help", "make", "get", "jump", "walk", "write",
             "read", "put", "swing", "think", "drink", "ride", "add", "can", "could"]

    # The first if statement checks, if the input is of some form, that can easily be stored in the bots memory
    if (wordlist[0] == "i" and (wordlist[1] in memory_verbs or wordlist[1:3] == ["dont", "know"])) or \
            wordlist[0:2] == ["my", "favourite"] or wordlist[0:2] == ["my", "favorite"]:
        memory.append(wordlist)

    # The first two rules are some fun responses to certain inputs. They have mainly been used for testing.
    if wordlist[0:4] == ["what", "is", "the", "word"]:
        response = "Bababa Bird, Bird, Bird, Bird is the word!"
        return response
    if wordlist == ["i", "love", "you"]:
        response = "I like you too, but I think we should stay friends."
        return response

    # Next, we check if the input is a farewell. If so, we respond with a farewell as well.
    if wordlist[0] in farewells:
        response = "Fare-thee-well!"
        return response

    # Next, we check for empty inputs. For this case, the cycle feature is used. It takes one of four possible
    # sentences in order.
    if wordlist[0] == "":
        responses_to_silence = ["You don't seem to be very talkative.", "Don't be so shy!",
                                "Is my noble presence intimidating you?", "I am losing my patience..."]
        response = responses_to_silence[cycle_counters[0]]

        cycle_counters[0] += 1
        cycle_counters[0] %= len(responses_to_silence)
        return response

    # This checks for inputs starting with "I am". If the input starts with "I am happy" or "I am glad", a random
    # response out of N different ones is chosen, for any other input starting with "I am", the response cycles through
    # two different possible responses
    if wordlist[0:2] == ["i", "am"] or wordlist[0] == "im":
        if wordlist[2] in ["happy", "glad"] or wordlist[1] in ["happy", "glad"]:
            responses_to_happiness = ["It fills my heart with happiness to hear about your fortune.",
                                      "I am happy to hear that.", "This is some good news."]
            response = random.choice(responses_to_happiness)
            return response

        else:
            responses_to_i_am = ["Why are you " + " ".join(mapped_wordlist[2:]) + "?", "Tell me more."]
            response = responses_to_i_am[cycle_counters[1]]

            cycle_counters[1] += 1
            cycle_counters[1] %= len(responses_to_i_am)
            return response

    # The next rule checks for the input "How are you" and the response is a randomly chosen answer out of three
    # different possibilities
    if wordlist == ["how", "are", "you"]:
        responses_to_how_are_you = ["I feel great today!", "I am good.", "Very well!"]
        response = random.choice(responses_to_how_are_you)
        return response

    # Next we check for a question, which is indicated by one of the words listed in question_words
    if wordlist[0] in question_words:
        response = "I don't know " + wordlist[0] + ". I only know how to use my sword!"
        return response

    # If the input starts with "I feel" or "I felt", the next rule chooses one of two responses randomly
    if wordlist[0:2] == ["i", "feel"] or wordlist[0:2] == ["i", "felt"]:
        responses_to_i_feel = ["I know that feeling.", "Why do you feel " + " ".join(mapped_wordlist[2:]) + "?"]
        response = random.choice(responses_to_i_feel)
        return response

    # The next rule uses the cycle feature to choose a response to sentences starting with "I have" or "I had"
    if wordlist[0:2] == ["i", "have"] or wordlist[0:2] == ["i", "had"]:
        responses_to_i_have = ["How long have you had " + " ".join(mapped_wordlist[2:]) + "?", "I have " +
                               " ".join(wordlist[2:]) + " as well.", "I wish I also had " +
                               " ".join(mapped_wordlist[2:])]

        response = responses_to_i_have[cycle_counters[2]]

        cycle_counters[2] += 1
        cycle_counters[2] %= len(responses_to_i_have)
        return response

    # Next, we check for inputs starting with "I don"t/do not know"
    if wordlist[0:3] == ["i", "dont", "know"] or wordlist[0:4] == ["i", "do", "not", "know"]:
        response = "You do not seem to be a very wise man."
        return response

    # This rule just gives the bot more responses and makes it less likely to hit the default sentences
    if wordlist[0] == "its" or wordlist[0:2] == ["it", "is"]:
        response = "Do you really think " + " ".join(mapped_wordlist) + "?"
        return response

    # Checks for questions starting with "Can/Could you" and gives a random answer.
    if wordlist[0:2] == ["can", "you"] or wordlist[0:2] == ["could", "you"]:
        responses_to_can_you = ["A noble knight like me can do everything!",
                                "Surely I " + wordlist[0] + " ".join(mapped_wordlist[2:]) + ".",
                                "Why do you want to know that?"]
        response = random.choice(responses_to_can_you)
        return response

    # If the input is only one word and has not triggered any rules prior to this, this final one is triggered.
    if len(wordlist) == 1:
        response = "Please be more precise."
        return response

    # A generalization of the previous rule. This rule checks for questions of the form "verb I/you ...?", for example
    # "Do I/do you ...?". The response is again chosen by the cycle feature.
    if (wordlist[1].lower() == "i" or wordlist[1] == "you") and wordlist[0] in verbs:
        responses_to_verb_i = ["Of course " + mapped_wordlist[1] + " " + mapped_wordlist[0] + " " +
                               " ".join(mapped_wordlist[2:]),
                               "I am very positive, that " + mapped_wordlist[1] + mapped_wordlist[0] +
                               " ".join(mapped_wordlist[2:]),
                               "I am not sure, if " + mapped_wordlist[1] + mapped_wordlist[0] +
                               " ".join(mapped_wordlist[2:]), "This is maybe the case."]
        response = responses_to_verb_i[cycle_counters[4]]

        cycle_counters[4] += 1
        cycle_counters[4] %= len(responses_to_verb_i)

        return response

    # This rule checks for inputs starting with "I like/love". The response is chosen randomly
    if wordlist[0:2] == ["i", "like"] or wordlist[0:2] == ["i", "love"]:
        responses_to_love = ["I " + " ".join(mapped_wordlist[2:]) + " as well.",
                             "Why do you " + " ".join(mapped_wordlist[2:]) + "?",
                             "I am glad, that you have something that makes you happy."]
        response = random.choice(responses_to_love)
        return response

    # Checks for inputs of the form "You verb ...". The response is chosen randomly.
    if wordlist[0] == "you" and wordlist[1] in verbs:
        responses_to_you_are = ["You know me well!", "Yes indeed, I " + " ".join(mapped_wordlist[1:])]
        response = random.choice(responses_to_you_are)
        return response

    # This rule just checks for some keywords and gives one of two random responses.
    if "ever" in wordlist or "every" in wordlist or "everyone" in wordlist or "never" in wordlist:
        responses_to_every = ["You like to generalize things, don't you?",
                              "Someone with a good heart does not speak in absolutes!"]
        response = random.choice(responses_to_every)
        return response

    # The next rule is triggered, if the input starts with "no".
    if wordlist[0] == "no":
        response = "Why do you think so negative?"
        return response

    # This rule is similar to the one above, but the response is chosen randomly
    if "yes" in wordlist or "absolutely" in wordlist or "yeah" in wordlist:
        responses_to_yes = ["I like your positive attitude.", "Are you sure about that?", "Can you prove that?"]
        response = random.choice(responses_to_yes)
        return response

    # Another single word check, this time for "because". The response is chosen by the cycle feature
    if "because" in wordlist:
        responses_to_because = ["Do you really think, this is the reason?", "I like your reasoning.",
                                "You seem to know the reason for everything in this world!"]
        response = responses_to_because[cycle_counters[3]]

        cycle_counters[3] += 1
        cycle_counters[3] %= len(responses_to_because)
        return response

    # Another single word rule for "maybe"
    if "maybe" in wordlist:
        response = "Don't be so irresolute!"
        return response

    # Another single word rule for "ok/okay"
    if "ok" in wordlist or "okay" in wordlist:
        response = "Is this really okay for you?"
        return response

    # Another single word rule for "please"
    if "please" in wordlist:
        response = "I like how kind you are."
        return response

    # If the bot has no rule to for a response to the last input, it takes something out of its memory and refers back
    # to it.
    if len(memory) > 0:
        response = " ".join(you_me_map(random.choice(memory))) + ", if I remember correctly. Tell me more about it!"
        return response

    # If no rule was triggered and the bot has nothing stored in its memory yet, it randomly chooses one of the default
    # sentences listed in default_sentences.
    return random.choice(default_sentences)
