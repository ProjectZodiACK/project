# You can modify your dictionary by adding its path below:
dict_path = "dictionary10000.txt"
# You can add your encrypted text below:
encoded_input = "diqd md dlgc amboq"
# You can add your translation accuracy percentage below:
decryption_accuracy = 100

from itertools import product
import time

content = open(dict_path).read()
def check_if_in_dict(word):
    timelimit = 30
    while timelimit > 0:
        if word in content:
            return True
        else:
            return False
            if remaining <= 0:
                break

def check_if_in_english(text, accuracy):
    text = text.lower()
    text = text.split(" ")
    special_signs = [",", ".", "!", "?", ":", ";", "\"", "\'", "(",")", "$"]
    words_in_dict = 0
    total_words = 0
    for word in text:
        for sign in special_signs:
            if sign in word:
                word = word.replace(sign, "")
        total_words += 1
        if check_if_in_dict(word):
            words_in_dict += 1
    percentage = words_in_dict / total_words * 100
    if percentage >= accuracy:
        return True
    return False

def key_generator(length):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    keywords = [''.join(i) for i in product(alphabet, repeat = length)]
    return keywords

def dec_vigenere(text, key):
    text = text.upper()
    key = key.upper()
    result = ""
    i = 0
    for x in text:
        if i > len(key)-1:
            i = 0
        if ord(x) > 64 and ord(x) < 91:
            if (ord(x) - ord(key[i])) < 0:
                result += chr(ord(x) - ord(key[i]) + 91)
            else:
                result += chr(ord(x) - ord(key[i]) + 65)
        else:
            result += x
            i -= 1
        i += 1
    return result.lower()


def brute_force_decryption_vigenere(text, accuracy):
    y = 0
    while True:
        y += 1
        keys = key_generator(y)
        for key in keys:
            if check_if_in_english(dec_vigenere(text, key), accuracy):
                print(dec_vigenere(text, key))
                return("Vigenere Cipher Results: " + dec_vigenere(text, key))

print(brute_force_decryption_vigenere(encoded_input, decryption_accuracy))