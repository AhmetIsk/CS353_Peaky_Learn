# CS353_Peaky_Learn
 
 Peaky Learn Online Education Platform is a web-based application that allows people to create student accounts and take online educations and also create educator accounts publish their educations while earning money. This project is coded with my teammates Ahmet Kaan Uguralp, Elif Ozer, Pelin Celiksoz an me as a Database Sytem Concepts course project. 

At backend side Python with Django framework, at database SQLite, at frontend side HTML, CSS and Javascript are used. 

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/AhmetIsk/CS353_Peaky_Learn.git
$ cd CS353_Peaky_Learn
```


Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then migrate:

```sh
(env)$ python manage.py migrate
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Then run the project:
```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
