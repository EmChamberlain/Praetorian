import requests, json, sys
if sys.version_info < (3,0):
  sys.exit('Python version < 3.0 does not support modern TLS versions. You will have trouble connecting to our API using Python 2.X.')


import itertools
import math

# My implementation of an adapted Five-guess algorithm
# https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm


email = 'mattchamberlain2@gmail.com' # Change this!
r = requests.post('https://mastermind.praetorian.com/api-auth-token/', data={'email':email})
r.json()
# > {'Auth-Token': 'AUTH_TOKEN'}
headers = r.json()
headers['Content-Type'] = 'application/json'


class Level(object):
    data = {}
    guesses_used = 0
    level_num = 0
    response = []
    level_done = False

    numGladiators = 0
    numGuesses = 0
    numRounds = 0
    numWeapons = 0
    def __init__(self, level_num):
        self.level_num = level_num
        r = requests.get('https://mastermind.praetorian.com/level/' + str(self.level_num) + '/', headers=headers)
        self.data = r.json()
        self.update_info()

    def update_info(self):
        self.numGladiators = self.data['numGladiators']
        self.numGuesses = self.data['numGuesses']
        self.numRounds = self.data['numRounds']
        self.numWeapons = self.data['numWeapons']
    # solve switch for handling different possible responses
    def solve(self, guess):
        self.guesses_used += 1
        r = requests.post('https://mastermind.praetorian.com/level/' + str(self.level_num) + '/', data=json.dumps({'guess': guess}),
                          headers=headers)
        read_dict = r.json()
        if 'hash' in read_dict:
            print('We won!')
            print('Hash: ' + str(read_dict['hash']))
            exit(0)
        elif 'message' in read_dict:
            print(read_dict)
            self.level_done = True
            return True
        elif 'response' in read_dict:
            self.response = read_dict['response']
            return False
        elif 'numGladiators' in read_dict:
            self.data = read_dict
            self.update_info()
            self.guesses_used = 0
            return True
        else:
            print('solve switch defaulted')
            print(read_dict)
            exit(1)

# checks if the permutation complies with the guess's chosen weapons
def check_chosen(guess, perm, chosen):
    sum = 0
    for num in guess:
        sum += perm.count(num)
    return sum == chosen

# checks if the permutation complies with the guess's correct weapons
def check_correct(guess, perm, correct):
    sum = 0
    for i in range(len(guess)):
        if guess[i] == perm[i]:
            sum += 1
    return sum == correct

# construct s using a heuristic because high number of weapons creates lists too large to handle
def construct_s(level):
    if level.numWeapons <= 15:
        return list(itertools.permutations(range(level.numWeapons), level.numGladiators))


    # min_guesses we need for this heuristic to work
    min_guesses = level.numGladiators + 1
    # estimate for the num of learning guesses we can make
    num_trash_guesses = level.numGuesses - int(1.5*level.numGladiators)
    # the number of elements in each guess
    num_in_guess = int(level.numWeapons / max(min_guesses, num_trash_guesses))
    guesses = list(range(level.numWeapons))
    guesses = [guesses[i:i + num_in_guess] for i in range(0, len(guesses), num_in_guess)]
    guess_length = len(guesses[0])
    # the numbers we are using as filler numbers
    filler = list(range(level.numGladiators - len(guesses[0])))

    # remove filler numbers from guesses
    for guess in guesses[:]:
        for i in filler:
            if i in guess:
                guesses.remove(guess)
                break

    # add back the filler numbers to make the guess have the correct number of elements
    for guess in guesses:
        guess += filler

    # handle the edge case of the last guess
    curr = 0
    while len(guesses[-1]) != level.numGladiators:
        if curr not in guesses[-1]:
            guesses[-1].append(curr)
        curr += 1
    # print(guesses)

    # gets the responses for each guess as well as keeps track of the minimum number of chosen elements
    # this number is important because it must be the number of chosen elements from the filler elements
    # this is because of a pigeonhole that must be left open due to the min_guesses we declared earlier
    min_chosen = level.numGladiators
    responses = []
    for guess in guesses:
        level.solve(guess)
        responses.append((guess, level.response))
        if level.response[0] < min_chosen:
            min_chosen = level.response[0]
    # print(responses)

    # begin to set up the cartesian product lists
    products = []
    # append filler elements
    for i in range(min_chosen):
        products.append(filler)

    # append other elements
    for res in responses:
        to_append = res[0][:guess_length]
        if 0 in to_append:
            to_append = to_append[:to_append.index(0)]
        for i in range(res[1][0] - min_chosen):
            products.append(to_append)
    # print(products)
    # picks one element from each list in products and creates a new list
    products = list(itertools.product(*products))

    # our products has some lists with duplicate elements in them that need to be removed
    for prod in products[:]:
        if len(set(prod)) != len(prod):
            products.remove(prod)

    # we can finally construct s by permuting the lists in products
    s = []
    for prod in products:
        s += list(itertools.permutations(prod))
    return s

# find the best guess from the set of all possible
def minimax(s):


    guess = s[0]
    # takes too long on large s
    if len(s) > 500:
        return guess

    # we go through the elements in s and compare them to every other element in s
    # we keep track of the number of times that permi has an element in permj in the same place
    # we want the maximum of this number because we want to know how many different elements
    # will be removed from s if we guess permi
    maximin_overall = 0
    for permi in s:
        maximin = 0
        for permj in s:
            for i in range(len(permi)):
                if permi[i] == permj[i]:
                    maximin += 1
        if maximin > maximin_overall:
            guess = permi
            maximin_overall = maximin

    return guess

def solver(level):

    # use heuristic to construct s when numWeapons is large
    s = construct_s(level)
    # print(len(s))
    # get best guess
    guess = minimax(s)
    # keep guessing until we have solved the current round
    while not level.solve(guess):
        print(str(level.guesses_used) + " | " + str(level.numGuesses))
        i = 0
        while i < len(s):
            perm = s[i]
            # Removing any permutations that don't have response[0] of the same weapons in them
            if not check_chosen(guess, perm, level.response[0]):
                del s[i]
                continue
            # Removing any permutations that don't have response[1] of the same weapons in the same location
            if not check_correct(guess, perm, level.response[1]):
                del s[i]
                continue
            i += 1
        # print(s)
        # get the next best guess
        guess = minimax(s)







def reset():
    return requests.post('https://mastermind.praetorian.com/reset/', headers=headers)


reset()


level_num = 1
while True:
    level = Level(level_num)
    print(level.data)
    while not level.level_done:
        solver(level)
    level_num += 1

