import random
import string


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
    if wordlist[0:3] == ["what", "is", "the", "word"] and questionmark:
        return "Bababa Bird, Bird, Bird, Bird is the word!"

    return "Hello World!"
