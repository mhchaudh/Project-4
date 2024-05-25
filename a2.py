from collections.abc import MutableSet
from random import choice

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class TooShortError(Exception): pass
class TooLongError(Exception): pass
class NotLettersError(Exception): pass

class WordleWords(MutableSet):
    def __init__(self, letters):
        '''Creates a WordleWords instance, letters specifies the characters length'''
        # Initialize _words to an empty set
        self._words = set()
        # Initialize _letters field that will hold characters length
        self._letters = letters
    
    def __contains__(self, word):
        '''Checks if word is in the set _words'''
        return word in self._words

    def __iter__(self):
        '''Returns an iterator over all the words'''
        return iter(self._words)

    def __len__(self):
        '''Return the number of words in the dictionary'''
        return len(self._words)

    def add(self, word):
        '''Add word to the dictionary'''
        # Checking if the word is valid
        if self.check_word(word):
            self._words.add(word.upper())

    def discard(self, word):
        '''Remove word from the dictionary'''
        # Checking if the word exists in the dictionary 
        if self.check_word(word) and word in self._words:
            self._words.discard(word)
        else:
            pass

    def load_file(self, filename):
        '''Add words from filename list to the set'''
        # Reading file in read mode and splitting lines by '\n'
        with open(filename, 'r') as file:
            lines = file.read().splitlines()

        # For each line in the file
        for line in lines:
            # The add method automatically checks the word's validity
            try:
                self.add(line.upper())
            # Skipping errors
            except TooShortError:
                pass
            except TooLongError:
                pass
            except NotLettersError:
                pass



    
    def check_word(self, word):
        '''Checks if word is valid'''
        if len(word) > self._letters:
            raise TooLongError()
        elif len(word) < self._letters:
            raise TooShortError()
        else:
            # Checking alphabets
            for character in word:
                if character.upper() not in ALPHABET:
                    raise NotLettersError()
        return True    

    def letters(self):
        '''Returns the number of letters in every word'''
        return self._letters 
    
    def copy(self):
        '''Returns a copy which contains the same words'''
        newInstance = WordleWords(self._letters)
        for word in self:
            newInstance.add(word)
        return newInstance
    

class Guess:
    def __init__(self, guess, answer):
        '''Constructs a new Guess instance'''
        self._guess = guess
        self._answer = answer
                
    def guess(self):
        '''Returns the guess that the player made'''
        return self._guess
    
    def correct(self):
        '''Returns a string that is the same length of the answer'''
        result = ''
        for i in range(len(self._answer)):
            # If it's the same character
            if self._answer[i] == self._guess[i]:
                result += self._guess[i]
            # Else
            else:
                result += '_'
        return result

    def misplaced(self):
        '''Returns a sorted string that contains every letter which the player guessed that is also in the answer but not at the same position'''
        result = []
        correct = self.correct()

        for i in range(len(self._guess)):
            # If the character is different that his answer 
            if correct[i] == '_' and self._answer[i] in self._guess:
                result.append(self._answer[i])
        return ''.join(sorted(result))


    def wrong(self):
        '''Returns a sorted string that contains every letter which the player guessed that was not in the answer'''
        result = []
        correct = self.correct()
        misplaced = self.misplaced()

        for i in range(len(self._guess)):
            # If the a character is different that his answer 
            if correct[i] == '_' and self._guess[i] not in misplaced:
                result.append(self._guess[i])
        return ''.join(sorted(result))

    def is_win(self):
        '''Returns True if the guess was the same as the answer'''
        return self._answer == self._guess


class Wordle:
    def __init__(self, words):
        '''Creates a WorldeWords instance object. It should choose a random word for the game.'''
        self._word = choice(list(words._words))
        self._guesses = 0

    def guesses(self):
        '''Returns the number of guesses the player has made so far.'''
        return self._guesses

    def guess(self, guessed):
        '''Take a string guessed and return a Guess instance object that represents the results of the guess'''
        self._guesses += 1
        return Guess(guessed, self._word)