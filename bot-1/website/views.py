from flask import Blueprint, render_template, request

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/scenarios")
def scenario():
    return render_template("gpt_home.html")
