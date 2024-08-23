
from flask import render_template, url_for, flash, redirect, request, session
from chatapp.forms import registrationForm, loginForm
from chatapp.models import User
from chatapp import app, db, bcrypt, socketIO
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import join_room, leave_room, send
import random
from string import ascii_uppercase




# Route for user registration
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            avatar=form.avatar.data
        )
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Username already exists. Please use a different Username.', 'error')
            return redirect(url_for('register'))
        if existing_email:
            flash('Email address already exists. Please use a different email.', 'error')
            return redirect(url_for('register'))
        db.session.add(user)
        db.session.commit()
        flash(f'Account succesfully created for {form.username.data}, now you can log in!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


# Route for user login
@app.route("/login",  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Loggged in succesfully' , 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Log in attempt Unsuccesfully' , 'error')
            return redirect(url_for('login'))
    return render_template("login.html", form=form)


# Route for user logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))



rooms = {}

def generate_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break
    return code


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or room not in rooms:
        return redirect(url_for("join"))
    messages=rooms[room]["messages"]
    return render_template("room.html", room=room, messages=messages)



@socketIO.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    user = User.query.filter_by(username=current_user.username).first()
    content = {
        "name": user.username,
        "avatar": user.avatar,
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketIO.on("connect")
def connect(auth):
    user = User.query.filter_by(username=current_user.username).first()
    room = session.get("room")
    name = user.username
    avatar = user.avatar

    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"avatar":avatar, "name":name, "message": " has entered the room!"}, to=room)
    rooms[room]["members"]+=1
    print(f"{name} joined room {room}")

@socketIO.on("disconnect")
def disconnect():
    user = User.query.filter_by(username=current_user.username).first()
    room = session.get("room")
    name = user.username
    avatar = user.avatar
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"avatar":avatar, "name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")




# Route for the home page
@app.route("/", methods=["POST", "GET"])
def index():
    name = None
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        name = user.username

        if request.method == "POST":
            code = request.form.get("code")
            join = request.form.get("join", False)
            create = request.form.get("create", False)

            if not name:
                return render_template("home.html", error="Please enter a name", code=code, name=name)
            if join != False and not code:
                return render_template("home.html", error="Please enter a room code", code=code, name=name)

            room = code
            if create != False:
                room = generate_code(9)
                rooms[room] = {"members": 0, "messages": []}
            elif code not in rooms:
                return render_template("home.html", error="The room does not exist", code=code, name=name)

            session["name"] = name
            session["room"] = room

            return redirect(url_for("room", name=name))
    return render_template("home.html" , name=name)

