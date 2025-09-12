import os
import pyperclip
from random import randint

chars = 4  # four chars per word
words = 5  # five words, four separators

word_list = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
word_list_max = len(word_list) - 1  # max index for rng

sep_list = '+-_=.#'
sep_list_max = len(sep_list) - 1  # max index for rng

clip = ''  # blank clipboard string
for n in range(words):
    for w in range(chars):
        clip = clip + word_list[randint(0, word_list_max)]
    clip = clip + sep_list[randint(0, sep_list_max)]

pyperclip.copy(clip[:-1])
print(clip[:-1])

os.system('timeout /t 3')  # wait a few seconds
# os.system('PAUSE')  # wait forever

# EOF
