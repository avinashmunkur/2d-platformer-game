PLATFORM GAMES:

Platform games is avideo gamegenre and subgenre ofaction games. Platformers are characterized by their heavy use of jumping and climbing to navigate the player’s environment and reach their goal.
Mechanisms in the game such as jumping, and being shot from a cannon are commonly called platforming.
These games are typically played from the side view using 2D movement or in 3D with the camera in a first-person or third-person perspective.

INTRODUCTION TO PYGAME:

Pygameis across platforms of Python modules designed for writing video games. It includes computer graphics and sound libraries designed to be used with the Python programming language.
Pete Shinners originally wrote Pygame to replace PySDL after its development stalled. It has been a community project since 2000.
Pygame uses the Simple DirectMedia Layer(SDL) library, to allow real-time computer game development without the low-level mechanics of the programming language and its derivatives. This is based on the assumption that the most expensive functions inside games can be abstracted from the game logic, making it possible to use a high-level programming language, such as Python, to structure the game.
Other features that SDL doesn't have include vector math, collision detection, 2d sprite scene graph management,MIDI support, camera, pixel-array manipulation, transformations, filtering, advanced freetype font support, and drawing.
Applications using pygame can run on Android phones and tablets with the use of pygame Subset for Android.

TILES OF A MAP:

The entire pygame map is composed of rectangular elements, fit together on a grid. We will be calling them “tiles” because they are arranged like tiles on a kitchen floor. They may be anything like tiles of actual floor tiles, but also of grass, walls, ground, trees, etc. Usually, most non-moving things in those games are created using tiles. The graphics for those tiles are usually taken from tilesets. Tilestes are, well sets of tiles, usually in the form of images containing rows of tiles aligned one next to the other, one of each tile type. The program will slice them into single tiles, and “stamp” those on the screen to create the map.

COLLISION DETECTION IN PYGAME:

Collision detection is a very often concept and is used in almost all games. The simple and straightforward concept is to match up the coordinates of the two objects and set a condition for the happening of collision.
This is done by continuously monitoring the X-axis and Y-axis positions of both the player and the obstacles on the map.
For example-
First, we check if the block passes through the player’s horizontal line. We will set the range such that the block’s base horizontal line should match the player’s horizontal line. In the above image, block 2 and 3 have their baseline out of range of player P’s top and bottom surface line. Hence, they are not in the collision range. Block 1’s baseline is in the range of player P’s top and bottom. Hence we further see whether the block comes in the range of the player’s vertical range or not.
Here, we check the range of the player’s left and right side surface dimensions with the blocks' left and right surfaces. Here, the blocks 2 and 3 when coming down, will collide with the player, and hence the range of 2 and 3 blocks is between the player’s X and the player’s Y positions. Hence, this concept is to be used to detect the collision.

SCROLL:

We use a scroll variable with x and y coordinates to indicate the movement of the camera. If the player is still, there is no scroll. The scroll is set to follow the player's movement but in the opposite direction. That is if the player moves to the right the rest of the objects on the screen move to the left and vice-versa.

PARALLAX SCROLLING:

To achieve smoother graphics, we used Parallax scrolling. This is when objects closer to the camera move faster concerning objects that are further away from the camera. We multiply the scroll with a value to scale it up or down. In the game, we have used multiple layers.
Tile Layer - This moves concerning the player's movements.
Layer 1 - This layer moves at 50% of the speed of the tile layer.
Layer 2 - This layer moves at 25% of the speed of the tile layer.
Solid Layer-This layer has no scroll, so it does not move These layers are rendered in this order only, which is crucial to achieve the parallax effect.

GRAVITY IN PYGAME:

To simulate gravity in pygame while the player is falling, we use the variable vertical_momentum and increase it by 0.2 every frame and add it to the total momentum of the player.
