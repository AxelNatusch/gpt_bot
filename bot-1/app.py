from flask import Flask, render_template, request, jsonify, session
from chatbot_assistant import ChatbotAssistant, ChatMessage
import chatbot_scenarios
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
messages = []


def get_system_prompt(scenario):
    if scenario == "1":
        return chatbot_scenarios.email_rewriting_german
    elif scenario == "2":
        return chatbot_scenarios.python_code_assistant
    elif scenario == "3":
        return chatbot_scenarios.sql_code_assistant
    elif scenario == "4":
        return chatbot_scenarios.data_engineer_assistant
    elif scenario == "5":
        return chatbot_scenarios.markdown_beautifier
    elif scenario == "6":
        return "placeholder"


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/scenarios")
def scenario():
    return render_template("gpt_home.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    scenario = request.args.get("scenario")
    message = ""
    if request.method == "POST":
        message = request.form.get("user_message")
    return render_template("chat.html", scenario=scenario, message=message)


@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_input = data.get("user_input")
    scenario = data.get("scenario")

    system_prompt = get_system_prompt(scenario)
    if "system_prompt_added" not in session:
        messages.append(ChatMessage(role="system", content=system_prompt))
        session["system_prompt_added"] = True

    chatbot = ChatbotAssistant(system_prompt=system_prompt)

    messages.append(ChatMessage(role="user", content=user_input))
    assistant_response = chatbot.get_chatbot_response(messages)
    messages.append(ChatMessage(role="assistant", content=assistant_response))

    return jsonify({"assistant_response": assistant_response})


@app.route("/new_session", methods=["POST"])
def new_session():
    session.pop("system_prompt_added", None)
    global messages
    messages = []
    return "ok", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
