# Concept
A game of classic asteroids where the different asteroids have letters embedded in them. Blowing up asteroids functionaly plays a game of hangman. 

## Prompt Instructions
- The game will be built in python using the pygame module. Please create a list of pip install commands for any library dependencies needed for testing. 
- The game will begin revealing how many letters are in the word "ASTEROID" with blank lines or underscore characters.
- The ship will have all of the same capabilities of the ship in the arcade game asteroids. The ship will have 10 lives and will lose a life whenever it collides with an object or collects the incorrect letter. The initial key mapping should be arrow keys for movement and spacebar for firing.
- The asteroids will also behave similarly to the original arcade game. In addition, each asteroid will contain a single letter. When destroyed the letter will be collected for the hangman style game at searching for the word "ASTEROID".
- Please take the list of letters below and create a frequency list where each letter appears in the list a number of times equal to it's value score:
7 value: A, E, I, O, U, L, N, S, T, R
6 value: D, G
5 value: B, C, M, P
4 value: F, H, V, W, Y
3 value: K
2 value: J, X
1 value: Q, Z
- When the user discovers the word correctly or runs out of lives the game is over. Please create a dynamic end of game screen that pops up and doesn't cover the whole screen.

## Additional Instructions
I do not currently have any assets created. Please create basic assets that you can use for creating the pygame. 
