import random
from string import ascii_lowercase

def game():
    print("H A N G M A N")
    keywords = ['python', 'java', 'kotlin', 'javascript']
    keyword = list(random.choice(keywords))
    answer = list(len(keyword) * '-')
    letters = []
    i = 0
    while i < 8:
        i += 1
        print()
        print("".join(answer))
        letter = input("Input a letter: ")
        if letter in letters:
            print("You already typed this letter")
            i -= 1
        elif len(letter) != 1:
            print("You should input a single letter")
            i -= 1
        elif letter not in ascii_lowercase:
            print("It is not an ASCII lowercase letter")
            i -= 1
        elif letter in keyword:
            i -= 1
            letters.append(letter)
            while letter in keyword:
                answer[keyword.index(letter)] = letter
                keyword[keyword.index(letter)] = '-'
        else:
            letters.append(letter)
            print('No such letter in the word')
        if ''.join(answer) in keywords:
            print('You guessed the word! ' + ''.join(answer) + '\nYou survived!')
            break
    else:
        print("You are hanged!")


while True:
    message = input('Type "play" to play the game, "exit" to quit: ')
    if message == "play":
        game()
    elif message == "exit":
        break
