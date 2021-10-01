from ai_garden import AIGarden
from flask import Flask, Response, render_template

# App Globals
app = Flask(__name__)

# Init AI garden
ai_garden = AIGarden()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video_feed():
    return Response(
        ai_garden.scanPlants, mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/sensors")
def video_feed():
    return ai_garden.readSensors


if __name__ == "__main__":
    print("AIGarden 🚰🌱🥕🍅")
    print("Bc. Martin Kubovčík")
    print("https://github.com/markub3327/AIGarden")
    print()

    # Main process
    app.run(host="0.0.0.0", debug=False)
