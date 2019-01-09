import random
import string

memory = []
cycle_counters = [0, 0]


def introduce():
    return "Good morrow, noble squire. My name is Sir Bugsalot.\n" \
           "I was brought down onto this world by Stephan Hagel.\n" \
           "If ye are to bring your word to him, ye shall deliver message to sthagel@uw.edu.\n" \
           "What is your desire?"


def agentName():
    return "Sir Bugsalot"


def respond(the_input):
    questionmark = (the_input[-1] == '?')

    exclude = set(string.punctuation)
    input_wo_punctuation = ''.join(ch for ch in the_input if ch not in exclude)

    wordlist = input_wo_punctuation.split(' ')
    wordlist[0] = wordlist[0].lower()

    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0] = mapped_wordlist[0].capitalize()

    answer = find_response(the_input, wordlist, mapped_wordlist, questionmark)

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


def find_response(the_input, wordlist, mapped_wordlist, questionmark):
    if wordlist[0:3] == ["what", "is", "the", "word"]:
        response = "Bababa Bird, Bird, Bird, Bird is the word!"
        return response

    if wordlist[0] == '':
        responses_to_silence = ["You don't seem to be very talkative.", "Don't be so shy!",
                                "Is my noble presence intimidating you?", "I will soon lose my patience..."]
        response = responses_to_silence[cycle_counters[0]]

        cycle_counters[0] += 1
        cycle_counters[0] %= len(responses_to_silence)
        return response

    if wordlist[0:1] == ["i", "am"]:
        memory.append(wordlist)
        if wordlist[2] == "sad":
            return "Don't be sad, because sad backwards is 'das'. Und das ist nicht gut!"

        if wordlist[2] == "happy" or wordlist[2] == "glad":
            responses_to_happiness = ["It fills my heart with happiness to hear about your fortune.", "To be continued"]
            return random.choice(responses_to_happiness)

        else:
            responses_to_i_am = ["Why are you " + ' '.join(mapped_wordlist[2:]) + ".", "Tell me more."]
            response = responses_to_i_am[cycle_counters[1]]

            cycle_counters[1] += 1
            cycle_counters[1] %= len(responses_to_i_am)
            return response


    return "Hello World!"
