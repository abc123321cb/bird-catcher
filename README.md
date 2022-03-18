# Bird Catcher
An arcade game for the 2021-2022 FBLA competition

## About The Project
![](/assets/title_screen.jpg)
I developed Bird Catcher as an arcade game inspired by 1980s-style arcade games, such as Pac Man, Donkey Kong, or Frogger.



## Built With
This game was developed in [Python3](https://www.python.org/) using [PyCharm](https://www.jetbrains.com/pycharm/).



## Getting Started
### Using the Standalone Executable
A standalone exectuable has been created for the Windows environment to be able to run Bird Catcher without installing any of its dependencies: Python3 and PyGame.
##### Prerequisites
None.
##### Installation
Download the file BirdCatcher.bat and the files in the /dist path. Run the BirdCatcher.bat shortcut file by double-clicking it. Alternatively, you can download the files in the /dist path and just double click the BirdCatcher.exe file.

### Building from Scratch
You can run Bird Catcher from the source files.
##### Prerequisites
If you want to run Bird Catcher from source, you will need to have Python3 and Pygame installed. The game is developed to be cross-platform and has been tested on Mac OSX and Linux (Ubuntu).
##### Installation
Download all of the source files into a directory (or simply clone the repo to a local path). Using the terminal or command prompt, navigate to the folder and execute the following command:
>python main.py



## Usage
You can use the WASD keys to move your character ![](/source/turtle.png)
	
> W - up  
A - left   
D - right  

Try to catch the bird ![](/source/NaBlu.png) before it warps to a new location. Make sure to stay away from the cat ![](/source/cat.png) and the ghost ![](/source/ghost.png). Enemies will get harder as you level up. Get a high score to leave your mark on the leaderbaord!



## Roadmap
- [x] Add player ![](/source/turtle.png)
- [x] Add NaBlu ![](/source/NaBlu.png)
- [x] Add first enemy type ![](/source/cat.png)
- [x] Add second enemy type ![](/source/ghost.png)
- [x] Add code to support projectiles
- [x] Update enemy AI
- [x] Add multiple levels
- [x] Add support for arcade buttons and joystick
- [x] Implement leaderboard
- [x] Create standalone executable



## Development Planning

The program was organized using five objects, as shown in the following Unified Modeling Language (UML) diagrams:
![](/assets/UML_diagrams.jpg)

<br />

The game operations were managed by five functions, as shown in the following Input Process Output (IPO) charts:
![](/assets/IPO_charts.jpg)



## License
Distributed under the MIT License. See LICENSE for more information.



## Contact
Steven Pereanu - [pereanusteven@gmail.com](mailto:pereanusteven@gmail)
<br />
Project Link - [https://github.com/abc123321cb/bird-catcher](https://github.com/abc123321cb/bird-catcher)



## Acknowledgments
<ul>
<li>BeepBox - Sound effects and music were created by hand using this free online tool for sketching and sharing instrumental music - [https://www.beepbox.co/](https://www.beepbox.co/)</li>
<li>PhotoPea - Images were saved with transparency as PNGs using this onlinbe photo editor - [https://www.photopea.com/](https://www.photopea.com/)</li>
<li>Piskel - Images were created by hand using this free online sprite editor - [https://www.piskelapp.com/](https://www.piskelapp.com/)</li>
<li>PyCharm - The game was developed using this free Python integrated development environment (IDE) - [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/)</li>
<li>Pygame - Game development was supported by this cross-platform set of Python modules - [https://www.pygame.org/](https://www.pygame.org/)</li>
<li>Python - The game was coded using the Python3 (specifically 3.10.3) programming language - [https://www.python.org/](https://www.python.org/)</li>
</ul>