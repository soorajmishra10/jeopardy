# jeopardy
## Description
The sole purpose of this project is to design a web application mimicking the famous
“Jeopardy” game. This is a lab project to understand the fundamental concepts of browser
applications running on client-server architecture and design one in a fun way.

Anyone having a browser, an internet connection and desire to have some fun while also
learning something new as well as testing their current knowledge can use our application
and play this game

## Scope
* This application can be used as an actual online quiz game show in which contestants
can participate from all over the country also from all over the world.
* Also, with some modifications and applying certain custom changes this application
can be used as a general awareness screening test for any entrance exam or
competitive exam.
* This application can also be used to collect local as well as global surveys regarding a
particular issue or thing.

## Jeopardy Rules
* The game can be played among 2 to N(here we have taken upto 4 players) players.
* Each player picks a category and an amount value for a clue to be presented turn by
turn.
* The turn starts from the Server Host and after that each player gets his turn one by
one.
* After the clue is presented on screen, all the players need to type their answers in the
answer box and submit it within a time limit(let’s say 20 sec).
* The players need to submit their answers in the form of a question.
* Lastly, the player who gives the correct and fastest answer will be added the
appropriate clue amount to his/her scores and the turn moves to the next player and
the game goes on until all the clues are presented.
* Finally, the player having the highest score will be declared as winner.

## Tools Used
* Programming Languages: HTML, CSS, Bootstrap, JavaScript, Python
* Frameworks / Libraries: Django, Django-Channels, Channel-redis
* Database: SQLite, Redis

## Run Instructions
* Install python
* Clone this repo
* Open terminal at directory level where ```manage.py``` files is present.
* Install requirements.txt using ```pip install requirements.txt```
* Install Redis Server  
* Run command ```python manage.py runserver``` to check whether server is running or not.
* press ```Ctrl+C``` to stop the server.
* Run command ```python manage.py createsuperuser``` to create the admin.
* Enter Username, Email Address & Password according to you and hit ```Enter```
* Run command ```python manage.py makemigrations``` and after that run ```python manage.py migrate``` to register the database models on django admin.
* Run command ```python populate_questions.py``` to populate quiz questions in database.
* Run command ```python manage.py migrate``` to register the database changes.
* Run command ```python manage.py runserver``` to run the development server on localhost.

## Screenshots
 
![Screenshot_01.png](https://github.com/soorajmishra10/jeopardy/blob/master/screenshots/SS_01.png "Home Page")
![Screenshot_02.png](https://github.com/soorajmishra10/jeopardy/blob/master/screenshots/SS_02.png "Login Page")
![Screenshot_03.png](https://github.com/soorajmishra10/jeopardy/blob/master/screenshots/SS_03.png "Signup Page")
![Screenshot_03.png](https://github.com/soorajmishra10/jeopardy/blob/master/screenshots/SS_04.png "Create Game/Join Game Page")
![Screenshot_05.png](https://github.com/soorajmishra10/jeopardy/blob/master/screenshots/SS_05.png "Play Area")

## Bugs
Some known bugs are:
* Due to disconnection of web-sockets(due to slow network or other reasons) web app behaves unusually. 
* When more than one players submit correct answers simultaneously, sometimes server adds the points to all of them. 
