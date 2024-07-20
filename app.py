from flask import Flask, render_template, jsonify
from src.main import main as main_function

app = Flask(__name__)
bot_running = False

@app.route("/")
def index():
    return render_template('index.html', title='Home')

@app.route("/run-main", methods=["POST"])
def run_main():
    global bot_running
    if not bot_running:
        # Start the bot (This should be your logic to start the bot)
        main_function()
        bot_running = True
        return jsonify({"message": "Bot is running"})
    else:
        return jsonify({"message": "Bot is already running"})

@app.route("/stop-main", methods=["POST"])
def stop_main():
    global bot_running
    if bot_running:
        # Implement your logic to stop the bot
        bot_running = False
        return jsonify({"message": "Bot has been stopped"})
    else:
        return jsonify({"message": "Bot is not running"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
