# Day 2
The goal today is to identify development plans for the future:

# Technical Feedback: 
- Refactor assets (Ship, Asteroids, etc) into separate assets folder. Update game.py to summon assets with imports and function calls.
- Add collisions between asteroids (to prevent game-state lock)
- Asteroids of all sizes should collide with each other;
	- If helpful, separate the collision system into it's own class/model (whatever is most appropriate)
- Asteroids of equal size should "bounce" and change trajectory in the opposite direction, relative to the bounce
	- It may be helpful to create a weight value within the asteroid class so you can create more realistic bounce effects with minimal complexity
- Asteroids should have a new value called hit points that scales based on size (4,3,2,1)
	- Asteroids should have a color applied to them based on their starting hit points. Choose a distinct color for each size asteroid that will contrast with the background and brighten up the game a little. 
- New Collision Damage Amounts:
	- A normal bullet does 2 damage to any target (asteroids or the ship hitting itself)
	- An asteroid hitting the same the same size object or the ship deals 1 damage
	- An asteroid hitting an asteroid 1 size smaller deals 2 damage
	- An asteroid hitting an asteroid 2 sizes small deals 4 damage
	- When asteroids destroy asteroids the letters are not collected. 
	- When the smallest size of asteroid is destroyed (condition: No hit points remaining) a new asteroid of random size is created
- Letter Frequency table:
	- The letter frequency table should only display asteroids with unique letters (across all asteroids currently on the field);
	- No letter that has been guessed previously should be allowed to spawn
- Hit Point Dislay and Hangman
	- The blank lines / underscores are a perfect display for the v1 of the game
	- Please remove the Hangman display as it is not needed. Replace this graphic with a series of Hearts to represent the ships current Hit Points
		- Whenever a hit point is lost due to collision, remove a heart. 
		- When the player has 0 hearts display the game over screen
			- Improvement: 
				- Make the Game over screen persist. 
				- Create an OK or X on the Game over screen to dismiss it.
- Ship Improvements
	- Make the ship an acute isocles triangle. The current shape is too equilateral and hard to tell which point is forward. 
	- The forward key does an excellent job with the acceleration of the ship
	- Please make the backward key decelerate the ship. If the backward key is held for 0.3 seconds when the ship has no acceleration that changes the gear to reverse and makes the ship travel backward
		- create new ship variables and values as needed to mock-up this feature.   
