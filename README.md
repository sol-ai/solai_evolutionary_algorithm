# Sol AI Evolutionary Algorithm

Need to set super secret DB password variable in bash enviorment to run with Database.

The evolutionary algorithm component of the Sol AI master project.

![system_overview](https://user-images.githubusercontent.com/20680618/76615414-4dfde600-6522-11ea-99fc-f7793c870fcb.png)

To start ea:

    $ docker-compose build    
    $ docker-compose up    

To test without docker and the database, run:
    
    
    $ pipenv install

to install dependencies, and then
      
    $ python -m solai_evolutionary_algorithm 
