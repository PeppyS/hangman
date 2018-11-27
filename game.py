import os
import random

class GameState:
    Pending = 1
    Won = 2
    Lost = 3

class BadGuessError(Exception):
    pass

class Letter:
    def __init__(self, letter):
        self.letter = letter
        self.guessed = False

    def guess(self, letter):
        if self.letter == letter:
            self.guessed = True
        
        return self.guessed
    
    def get_display_value(self):
        if self.guessed:
            return self.letter
        else:
            return '_'

class Hangman:
    def __init__(self, word = random.choice(['winter', 'love', 'teppy', 'eggs']), num_tries = 10):
        self.word = word
        self.num_tries = num_tries
        self.letters = map(lambda x: Letter(x), word)
        self.incorrect_guesses = []
        self.game_state = GameState.Pending
    
    def start(self):
        self.show()

        while self.game_state == GameState.Pending:
            letter = raw_input('\nGuess a letter: ')

            try:
                self.guess(letter)
                self.show('You guessed {letter}'.format(letter=letter))
            except BadGuessError, e:
                self.show(e.message)
        
        self.show_results()

    def guess(self, guessed_letter):
        guessed_letters = map(lambda x: x.letter, filter(lambda x: x.guessed == True, self.letters))

        if guessed_letter.isalpha() == False or len(guessed_letter) != 1:
            raise BadGuessError('Please enter a valid letter')
        elif guessed_letter in guessed_letters:
            raise BadGuessError('You already guessed {letter} correctly'.format(letter=guessed_letter))
        elif guessed_letter in self.incorrect_guesses:
            raise BadGuessError('You already guessed {letter} incorrectly'.format(letter=guessed_letter))
        
        guessed_correctly = reduce(lambda x,y: (y.guessed == False and y.guess(guessed_letter)) or x, self.letters, False)
 
        if guessed_correctly == False:
            self.incorrect_guesses.append(guessed_letter)

            if len(self.incorrect_guesses) >= self.num_tries:
                self.game_state = GameState.Lost
        else:
            all_letters_guessed = reduce(lambda x,y: y.guessed and x, self.letters, True)
            if all_letters_guessed:
                self.game_state = GameState.Won

    def show(self, prompt = ''):
        # Clear screen
        os.system('clear')

        print('=================================')
        print('=======Welcome To Hangman========')
        print('=================================')
        print('\nTries left: {}'.format(self.num_tries - len(self.incorrect_guesses)))
        print('\nBad guesses: {}'.format(', '.join(self.incorrect_guesses)))
        display_values = map(lambda l: l.get_display_value(), self.letters)

        print('\n\nWord: ' + ' '.join(display_values))
        print(prompt)
        print("""
   ____
  |    |
  |    o
  |   /|\\
  |    |
  |   / \\
 _|_
|   |______
|          |
|__________|
        """)

    def show_results(self):
        if self.game_state == GameState.Lost:
            print('OHHH NOOO!!!!')
            print('\nSorry you lost :(')
            print('\nThe word was {word}'.format(word=self.word))
        elif self.game_state == GameState.Won:
            print('Congratulations!!!!!!!!')
            print('\nYou guessed {word} correctly!!!'.format(word=self.word))

        print('\nThanks for playing hangman!')
