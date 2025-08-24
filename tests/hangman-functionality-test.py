from main import Hangman
h = Hangman("ASTEROID", 10)
print(h.guess('A'))  # True
print(h.guess('X'))  # False
print(h.is_solved())  # False
for c in "STEROID":
    h.guess(c)
print(h.is_solved())  # True