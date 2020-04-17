from solai_evolutionary_algorithm import main
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if 'run_with_database' in sys.argv:
            main.dummy_simulation_with_database()
    else:
        main.dummy_simulation_without_database()
