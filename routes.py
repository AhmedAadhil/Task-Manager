from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

routes = Blueprint("routes", __name__)

@routes.route("/register")
def register():
    return render_template("register.html")

@routes.route("/")
def login():
    return render_template("login.html")

@routes.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
