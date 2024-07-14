from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "RADNOM"
socketIO = SocketIO(app)

rooms = {}

def generate_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break
    return code



@app.route("/rooms", methods=["POST", "GET"])
def join():
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("rooms.html", error="Please enter a name", code=code, name=name)
        if join != False and not code:
            return render_template("rooms.html", error="Please enter a room code", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("rooms.html", error="The room does not exist", code=code, name=name)
        
        session["name"] = name
        session["room"] = room

        return redirect(url_for("room"))

    return render_template("rooms.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("join"))

    return render_template("room.html")



if __name__ == "__main__":
    socketIO.run(app, debug=True)