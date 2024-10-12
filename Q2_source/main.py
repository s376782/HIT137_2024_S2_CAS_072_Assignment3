import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import game
game.Game().run()