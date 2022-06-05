# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, callback,callback_context
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
from dash.exceptions import PreventUpdate
import dash
from flask_caching import Cache
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash
#from helpers import apology, login_required
from layouts import graph_layout, index_string_login, index_string_logout,sidebar,content,sidebar_right,modal_error
import callbacks
from callbacks import con
import sqlite3
from flask_share import Share
import psycopg2
#from tkinter import *
#from tkinter import messagebox
#import tkinter as tk

import ctypes  # An included library with Python install.
import pymsgbox
from pymsgbox import *
#import pymsgbox.native as pymsgbox
app = Dash(__name__ , title='Mini Technical Analytics and Strategy',suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.COSMO])
#app = dash.Dash(__name__)
server = app.server
share = Share(app.server)

# Ensure templates are auto-reloaded
server.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
server.config["SESSION_PERMANENT"] = False
server.config["SESSION_TYPE"] = "filesystem"
Session(server)


@server.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

cache = Cache(app.server, config={
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'NullCache',
    #'CACHE_REDIS_URL': os.environ.get('REDIS_URL', '')
})
cache.clear()


url_bar_and_content_div = dbc.Container([
                # dbc.Row(navbar),
                #navbar,
                #dcc.Location(id='url', refresh=False),
                dcc.Location(id='url', refresh=True),
                html.Div(id='page-content-main')]
                ,fluid=True)

app.layout = url_bar_and_content_div

app.validation_layout = html.Div([
    url_bar_and_content_div,
    #graph_layout,
])

app.index_string=index_string_login

# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content')
# ])

@callback(Output('page-content-main', 'children'),
              Output('url', 'pathname'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/graph':
        #app.index_string=index_string_login
        #print(callback_context.triggered)
        if session.get("user_id") is None:
            app.index_string = index_string_logout
            print("none userid")
            return [dash.no_update,"/login" ]
        app.index_string = index_string_login
        return [graph_layout, "/graph"]
    elif pathname == '/login' or pathname == '/':
        if session.get("user_id") is None:
            app.index_string = index_string_logout
            print("none userid")
            return [dash.no_update,"/login" ]
        else:
            app.index_string = index_string_login
            return [graph_layout, dash.no_update]
    return '404'

def message(title,msg):
    root = Tk()
    root.geometry("300x200")
    w = Label(root, text ='GeeksForGeeks', font = "50")
    w.pack()
    messagebox.showwarning(title, msg)
    root.mainloop()

#top = Tk()
#def hello():
#    messageBox.showinfo("Say Hello", "Hello World")

# B1 = Label(top, text ='GeeksForGeeks', font = "50")
# B1.pack()


@server.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    print("login")
    # #tkinter._test()
    # window = tk.Tk()
    # window.geometry("700x250")
    # greeting = tk.Label(text="Hello, Tkinter")
    # greeting.pack()
    # window.mainloop()
    # Forget any user_id
    print("tk")
    session.clear()
    if session.get("user_id") is None:
        app.index_string = index_string_logout
    else:
        app.index_string = index_string_login
    #User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        print("post")
        # Ensure username was submitted
        #pymsgbox.alert('This is an alert!', 'Title')
        #message("warning","must provide username")
        #B1 = Tkinter.Button(top, text = "Say Hello", command = hello)
        #B1.pack()
        #alert(text='', title='', button='OK')
        if not request.form.get("username"):
            #pymsgbox.alert('This is an alert!', 'Title')
            #alert(text='', title='', button='OK')
            #response = pymsgbox.prompt('What is your name?')
            #ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)
            #message("warning","must provide username")
            return render_template("warning.html", msg="YOU MUST PROVIDE USERNAME.",login="/login")
            return apology("You must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            #pymsgbox.alert('This is an alert!', 'Title1')
            #message("warning","must provide passoword")
            return render_template("warning.html", msg="YOU MUST PROVIDE PASSWORD.",login="/login")
            return apology("must provide password", 403)
        #con = sqlite3.connect("./chart.db", check_same_thread=False)
        con = psycopg2.connect(database="db1sc0b7bf1f8d", user='vgqtsparahzsjh', password='61473f3d10715838adce26169ab55863a3fb33bb9edaaea104c6ff89c7eea766', host='ec2-52-203-118-49.compute-1.amazonaws.com', port= '5432')

        #con.row_factory = sqlite3.Row
        db = con.cursor()
        #db = con.cursor()
        rows=[]
        for row in db.execute("SELECT * FROM users WHERE username = (?)",(request.form.get("username"),)):
            rows.append(row)
        print(rows)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("warning.html", msg="INVALID USERNAME AND/OR PASSWORD.",login="/login")
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        # Redirect user to home page
        app.index_string=index_string_login
        return redirect("/graph")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        print("get")
        return render_template("login.html")
        #return redirect("/login")

@server.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    render_template("register.html")
    if request.method == "POST":
        # CHECK THE PASSWORD IS ALL NUMBER OR NOT AND AT LEAST ONE CHARACTER
        if request.form.get("password").isdigit():
            pass
            return render_template("warning.html", msg="PASSWORD AND CONFIRMED PASSWORD NEEDED AT LEAST ONE CHARACTER.",login="/register")
            #return apology("password and confirmed passoword needed the at least one character", 400)
        else:
            #CHECK CONFIRMATION PASSWORD AND NEW PASSWORD MATCHED
            if not request.form.get("username"):
                return render_template("warning.html", msg="MUST PROVIDE USERNAME.",login="/register")
                return apology("must provide username", 400)
            elif not request.form.get("password"):
                return render_template("warning.html", msg="MUST PROVIDE PASSWORD.",login="/register")
                return apology("must provide password", 400)
            elif not request.form.get("confirmation"):
                return render_template("warning.html", msg="MUST PROVIDE CONFIRMED PASSWORD.",login="/register")
                return apology("must provide confirmed password", 400)
            if request.form.get("password") != request.form.get("confirmation"):
                return render_template("warning.html", msg="PASSWORD AND CONFIRMED PASSWORD NEEDED THE SAME.",login="/register")
                return apology("password and confirmed passoword needed the same", 400)
            #print(type(request.form.get("password")))

            # Query database for username
            con = psycopg2.connect(database="db1sc0b7bf1f8d", user='vgqtsparahzsjh', password='61473f3d10715838adce26169ab55863a3fb33bb9edaaea104c6ff89c7eea766', host='ec2-52-203-118-49.compute-1.amazonaws.com', port= '5432')
            db = con.cursor()
            rows=[]
            for row in db.execute("SELECT * FROM users WHERE username = (?)",(request.form.get("username"),)):
                rows.append(row)
            print(type(rows))
            if len(rows) == 0:
                name = request.form.get("username")
    # GENERATE A HASH
                passwordhash = generate_password_hash(
                    request.form.get("password"))
                con = psycopg2.connect(database="db1sc0b7bf1f8d", user='vgqtsparahzsjh', password='61473f3d10715838adce26169ab55863a3fb33bb9edaaea104c6ff89c7eea766', host='ec2-52-203-118-49.compute-1.amazonaws.com', port= '5432')
                db = con.cursor()
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                           (name, passwordhash))
                con.commit()
                rows=[]
                for row in db.execute("SELECT * FROM users WHERE username = (?)",
                                  (request.form.get("username"),)):
                    rows.append(row)
                print(rows)
                #session["user_id"] = rows[0]["id"]
                session["user_id"] = rows[0][0]
                session["username"] = rows[0][1]
                flash('You were successfully registered')
                app.index_string = index_string_login
                return redirect("/graph")
            else:
                #pass
                return render_template("warning.html", msg="THIS USERNAME ALREADY REGISTERED, PLEASE USE ANOTHER ONE.",login="/register")
                return apology("this username already registered, please use another username", 400)
    else:
        return render_template("register.html")

@server.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

if __name__ == '__main__':
    app.run_server(debug=True)
    #app = dash.Dash(__name__, debug=True,title='Weekly Analytics')