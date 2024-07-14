from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, join_room, leave_room, send
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "RADNOM"
socketIO = SocketIO(app)


@app.route("/rooms", methods=["POST", "GET"])
def rooms():
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("rooms.html", error="Please enter a name")
        if join != False and not code:
            return render_template("rooms.html", error="Please enter a room code")


    return render_template("rooms.html")






if __name__ == "__main__":
    socketIO.run(app, debug=True)