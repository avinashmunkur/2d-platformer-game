PLATFORM GAMES
Platform games is avideo gamegenre and subgenre ofaction games. Platformers are characterized by their heavy use ofjumpingandclimbingto navigate the player’s environment and reach their goal.
Mechanisms in the game such as jumping,being shot from a cannon are commonly called platforming.
These games typically are either played from the side view using 2D movement or in 3D with the camera either in a first-person or third-person perspective.

INTRODUCTION TO PYGAME
Pygameis across platformset ofPythonmodules designed for writingvideo games. It includescomputer graphicsand soundlibrariesdesigned to be used with the Pythonprogramming language.
Pygame was originally written by Pete Shinners to replace PySDL after its development stalled. It has been acommunityproject since 2000.
Pygame uses theSimple DirectMedia Layer(SDL) library,with the intention of allowingreal-timecomputer gamedevelopment without thelow-levelmechanics of theCprogramminglanguageand its derivatives. This is based on the assumption that the mostexpensivefunctions inside games can be abstracted from the game logic, making it possible to use ahigh-level programming language, such as Python, to structure the game.
Other features that SDL doesn't have include vector math, collision detection, 2d sprite scene graph management,MIDIsupport, camera, pixel-array manipulation, transformations, filtering, advanced freetype font support, and drawing.
Applications using pygame can run on Android phones and tablets with the use of pygame Subset for Android.

TILES OF A MAP
The entire pygame map is composed of rectangular elements, fit together on a grid. We will be calling them “tiles”, because they are arranged like tiles on a kitchen floor. They maybe anything like tiles of actual floor tiles, but also of grass, walls, ground, trees, etc.usually most non-moving things in those games are created using tiles. The graphics for those tiles is usually taken from tilesets. Tilestes are, well sets of tiles, usually in a form of images containing rows of tiles aligned one next to the other, one of each tile type. Our program will slice them into single tiles, and “stamp” those on the screen to create the map.

COLLISIONS DETECTION IN PYGAME
Collision detectionis a very often concept and used in almost all games.The simple and straight forward concept is to match up the coordinates of the two objects and set a condition for the happening of collision.
This is basically done by continuously monitoring the X-axis and Y-axis positions of both the player and the obstacles in the map.
For example-
First, we check if the block passes through the player’s horizontal line. We will set the range such that the block’s base horizontal line should match the player’s horizontal line. In the above image, block 2 and 3 having their baseline out of range of player P’s top and bottom surface line. Hence, they are not in the collision range. Block 1’s baseline is in the range of the player P’s top and bottom. Hence we further see that the block comes in the range of the player’s vertical range or not.
Here, we check the range of player’s left and right side surface dimensions with the blocks left and right surfaces. Here, the blocks 2 and 3 when coming down, will collide the player, and hence the range of 2 and 3 block’s range are between player’s X and player’s Y position.Hence, this concept is to used to detect the collision.

SCROLL
We use a scroll variable with x and y coordinates to indicate the movement of the camera. If the player is still, there is no scroll. The scroll is set to follow the player movement, but in the opposite direction. That is if the player moves to the right the rest of the objects on the screen move to the left and vice-versa.

PARALLAX SCROLLING
In order to achieve smoother graphics, we used Paralax scrolling. This in when objects closer to the camera mover faster with respect to objets that are further away from the camera. We multiply the scroll with a value to scale it up or down. In the game we have used multiple layers.
Tile Layer-This moves with respect to the player.
Layer 1-This layer moves in 50% the speed of the tile layer.
Layer 2-This layer moves in 25% the speed of the tile layer .
Solid Layer-This layer has no scroll, so it does not move These layers are rendered in this order only, which is crucial to achieve the parallax effect.

GRAVITY IN PYGAME
To simulate gravity in pygame while the player is falling, we use variable vertical_momentum and increase it by 0.2 every frame and add it to the total momentum of the player.

