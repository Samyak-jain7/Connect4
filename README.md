# Connect4
My sister was bored on a plane, so I made a quick Connect4 game. Then my sister kept beating me, so I implemented the MiniMax AI algorithm - it now beats her (and my girlfriend!). The AI uses MiniMax, Alpha-Beta Pruning, and Iterative Deepening. To value a state, I use a heuristic that depends on the number of "threats," which I define as a group of 4 colinear, consecutive slots with 3 of one player's tile and 1 empty. The value of a state is the number of AI threats minus the number of human threats, discounted exponentially by the depth of the search.

`python multiplayer.py` to play with 2 humans.

`python singleplayer.py` to play with 1 human and 1 MiniMax AI.
