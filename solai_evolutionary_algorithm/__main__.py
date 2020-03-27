from solai_evolutionary_algorithm import main
import sys

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'run_with_database':
            # main.main()
            main.dummy_simulation_with_database()
    except:
        main.dummy_simulation_without_database()
