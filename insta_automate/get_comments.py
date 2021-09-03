import itertools
from random import randint
wow_words = ["Great..","Awesome..", "Wow..", "Woo..", "Astonishing..","Nicey..","Good..","Cool..","Incredible.."]
wow_words_long = []
for i in range(0,20):
    for item in wow_words:
        index = randint(0,len(item)) -1
        if index == -1:
            index = 0
        wow_words_long.append(item[:index] + item[index] * randint(2,5)+ item[index:])

# print(len(wow_words_long))
# wow_smileys = [u'\U0001f60d',u'\U0001f600',u'\U0001f603',u'\U0001f604',u'\U0001f642',u'\U0001f60a',u'\U0001f607',u'\U0000263a',u'\U0001f917',u'\U0001f63a',u'\U0001f638',u'\U0001f63b',u'\U0001f497',u'\U00002764',u'\U0001f44c',u'\U0001f44d',u'\U0001f44f']
wow_string = []
for i in range(0,len(wow_words_long)):
    for L in range(0, 3):
        for subset in itertools.combinations(wow_words_long, L):
            wow_string.append(wow_words_long[i] + " ".join(subset))

# print(wow_string[:200])
# print(len(wow_string))