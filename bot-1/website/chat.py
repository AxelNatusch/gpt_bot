from flask import Blueprint, render_template, request

chat = Blueprint("chat", __name__)


@chat.route("/chat", methods=["GET", "POST"])
def chat_home():
    scenario = request.args.get("scenario")
    message = ""
    if request.method == "POST":
        message = request.form.get("user_message")
    return render_template("chat.html", scenario=scenario, message=message)
