#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q2_source
if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    import game
    game.Game().run()