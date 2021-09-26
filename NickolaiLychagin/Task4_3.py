# Task 4.3
# Implement The Keyword encoding and decoding for latin alphabet.
# The Keyword Cipher uses a Keyword to rearrange the letters in the
# alphabet. Add the provided keyword at the begining of the alphabet.
# A keyword is used as the key, and it determines the letter matchings
# of the cipher alphabet to the plain alphabet. Repeats of letters in
# the word are removed, then the cipher alphabet is generated with the #
# keyword matching to A, B, C etc. until the keyword is used up,
# whereupon the rest of the ciphertext letters are used in alphabetical
# order, excluding those already used in the key.

from string import ascii_lowercase, ascii_uppercase, printable


class Cipher:
    """
    Cipher class.

    INIT
        keyword - Type string. Only letters of English alphabet are allowed.

    ATTRIBUTES
        __keyword - Type string. Keyword without repeating letters
        __cipher - Type string. __keyword plus other letters of the alphabet

    METHODS
        encode(text) - Encode text and return it.
        decode(text) - Decode text and return it.

    """

    def __init__(self, keyword):
        if not all(letter in ascii_lowercase for letter in keyword.lower()):            
            raise Exception("Keyword must consist only of letters of English alphabet")
        self.__keyword = "".join(dict.fromkeys(keyword.lower()))
        self.__cipher = self.__keyword + "".join(
            [char for char in ascii_lowercase if char not in self.__keyword]
        )

    def encode(self, text):
        if not all(letter in printable for letter in text):            
            raise Exception("Text must consist only of printable characters of English alphabet")
        encoded = ""
        for char in text:
            if char.isupper():
                encoded += self.__cipher[ascii_uppercase.find(char)].upper()
            elif char.islower():
                encoded += self.__cipher[ascii_lowercase.find(char)]
            else:
                encoded += char
        return encoded

    def decode(self, text):
        if not all(letter in printable for letter in text):            
            raise Exception("Text must consist only of printable characters of English alphabet")
        decoded = ""
        for char in text:
            if char.isupper():
                decoded += ascii_uppercase[self.__cipher.upper().find(char)]
            elif char.islower():
                decoded += ascii_lowercase[self.__cipher.find(char)]
            else:
                decoded += char
        return decoded


# =============================================================================
# cipher = Cipher("crypto")
# print(cipher.encode("Hello world"))
# print(cipher.decode("Fjedhc dn atidsn"))
# print(cipher.encode("Привет"))
# cipher = Cipher("crypto26")
# =============================================================================
