# Day 2
The goal today is to identify development plans for the future:
- Refactor assets (Ship, Asteroids, etc) into separate assets folder
- Add collisions between asteroids (to prevent game-state lock)
	- Technical Explanation: 
		- Asteroids of all sizes should collide with each other;
		- Asteroids of equal size should "bounce" and change trajectory in the opposite direction, relative to the bounce
			- It may be helpful to create a weight value within the asteroid class so you can create more realistic bounce effects with minimal complexity
		- 
