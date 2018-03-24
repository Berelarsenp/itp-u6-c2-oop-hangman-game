from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self, character, hit=None, miss=None):
        if hit and miss:
            raise InvalidGuessAttempt("Can't be both")
        self.character = character
        self.hit = hit
        self.miss = miss
    
    def is_hit(self):
        return bool(self.hit)
    
    def is_miss(self):
        return bool(self.miss)


class GuessWord(object):
    def __init__(self, word):
        if not word:
            raise InvalidWordException
        self.answer = word.lower()
        self.masked = self._mask_word(self.answer)
    
    def perform_attempt(self, character):
        if len(character) > 1:
            raise InvalidGuessedLetterException()
        if character.lower() not in self.answer:
            return GuessAttempt(character, miss=True)
        
        new_word = ''
        for answer_char, masked_char in zip(self.answer, self.masked):
            if character.lower() == answer_char:
                new_word += answer_char
            else:
                new_word += masked_char
        self.masked = new_word
        return GuessAttempt(character, hit=True)
    
    @classmethod
    def _mask_word(cls, word):
        return '*' * (len(word))


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(word_list))
    
    def is_won(self):
        return self.word.masked == self.word.answer
    def is_lost(self):
        return self.remaining_misses == 0
    def is_finished(self):
        return self.is_won() or self.is_lost()
    
    def guess(self, character):
        char = character.lower()
        if char in self.previous_guesses:
            raise InvalidGuessedLetterException
        
        if self.is_finished():
            raise GameFinishedException
        
        self.previous_guesses.append(char)
        attempt = self.word.perform_attempt(char)
        if attempt.is_miss():
            self.remaining_misses -= 1
        
        if self.is_won():
            raise GameWonException
        if self.is_lost():
            raise GameLostException
        
        return attempt
    
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)