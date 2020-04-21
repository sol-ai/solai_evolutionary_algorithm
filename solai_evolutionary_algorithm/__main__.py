from solai_evolutionary_algorithm import main
import sys
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    environment = str(config['APP']['ENVIRONMENT']).upper()
    print(dict(config))
    endpoints = dict(config[environment + "_ENDPOINTS"])

    with_database = False
    if environment == 'PROUDCTION':
        with_database = True

    main.dummy_simulation(with_database=with_database, endpoints=endpoints)
