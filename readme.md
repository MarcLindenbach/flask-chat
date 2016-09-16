Flask Chat
==========

Chat server/client written in Flask, Flask Socket IO and SOCKET.IO. User names
are stored using the Werkzeug simple cache, worst case - when the cache is
cleared, all users lose their username (but stay connected). 

## How to run
Targets Python3.
- `virtualenv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python server.py`

## How to use
Each browser can have one user (use incognito browsers for multiple users). You
can enter a message to send to the group and change your name. The user count
on the side shows active users and removes them when they leave.

## Future ideas
Color your own messages differently than other users. Global messages when
users enter/leave chatroom. Instead of destroying message elements when they
go past the end of the page, implement scrolling. Keep a chat log. Webcam
support.
