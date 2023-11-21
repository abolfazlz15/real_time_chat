# real time chat
This project is powered by Django and provides real-time group chat.

- use channels library for websocket protocol.
- use redis as channel layer.

## run project 

- in terminal `git clone https://github.com/abolfazlz15/real_time_chat.git`
- `cd /real_time_chat` , Where the requirements.txt is
- In terminal: `python -m venv venv`
- activate your venv: in windows `cd venv\scripts\activate` in linux: `source venv/bin/activate`
- Run `pip install -r requirements.txt`
- `cd src/` Where the manage.py is
- Run `python manage.py runserver`