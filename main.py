import sys

from game24 import Game24Solver

def main():
    game24 = Game24Solver()
    result = game24.solve([5, 8, 11, 13])
    return 0

if __name__ == "__main__":
    sys.exit(main())