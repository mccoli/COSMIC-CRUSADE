COSMIC CRUSADE
1. make sure you have python installed
2. make sure you have pygame installed using the terminal command 'pip install pygame'
3. cd to the space shooter directory
4. type 'python main.py' to run the program

CONTROLS:
player 1 - UP: up arrow
	 DOWN: down arrow
	 LEFT: down arrow
	 RIGHT: down arrow
	 SHOOT: right ctrl 
	 MISSILES: right shift
player 2 - UP: w
	 DOWN: s
	 LEFT: a
	 RIGHT: d
	 SHOOT: capslock
	 MISSILES: x

ABOUT
This program was inspired by the retro classic Space Invaders. It is a 2 player arcade-style shooter, where the goal is to survive longer than your opponent. Enemy drones attack in waves and you must dodge and fire back in order to raise your score. Once the game ends you can see wether you won, lost, or tied.

TECHNICAL
I decided to use pygame because of the many built in features it has that make game development more simple. There are also many resources online to help with pygame specific development.
At first I used parent and child classes to keep my code organised and easy to read. But as my project grew I found this to be unsustainable. Separating the code into modules taught me a lot about concepts such as scope, inheritance, object methods and properties, and general good practice for trying to keep a project legible.
I decided to implement a state machine into my program. I found the increasingly large number of classes and loops starting to become overwhelming, especially when I started working on different screens I wanted to use. Despite not being able to use all of those screens at this stage of the project, I am still happy with the state machine I have at the moment and am sure I can add to it with more knowledge and time. 

CHALLENGES/FUTURE
One of the things I initially struggled with was sprite groups and collisions. Being a beginner to pygame I had learnt about groups hoping for better organisation of my code and implemented them without understanding them fully. I learnt an important lesson about getting ahead of my own knowledge. Another big challenge was creating the state machine. I did a lot of research and preparation because I was already converting a program that was about 800 lines long. I did so because I was determined to implement my idea of the user being able to select a character. Unfortunately I couldn't figure out the logic in time but I hope to work on this project more in the future.
I would love to add sound, animations, and a background, as well as more states that could include levels, a pause screen etc.

CREDITS
everyone the python-forum.io threads
Witty Wong for the designs of the spaceships
CodingWithRuss for the youtube tutorials