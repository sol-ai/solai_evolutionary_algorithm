from solai_evolutionary_algorithm import main
import sys

if __name__ == '__main__':
    if sys.argv[1] == 'run_with_database':
        main.dummy_simulation_with_database()
    else:
        main.dummy_simulation_without_database()
