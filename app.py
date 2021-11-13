# Main application code
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

# @app.route("/")
# def base():
#     return render_template("base.html")

@app.route("/")
def login():
    return render_template("auth/login.html")

@app.route("/register")
def register():
    return render_template("auth/register.html")

@app.route("/create")
def create():
    return render_template("grade/create.html")

@app.route("/index")
def index():
    return render_template("grade/index.html")

@app.route("/update")
def update():
    return render_template("grade/update.html")

if __name__ == "__main__":
    app.run()