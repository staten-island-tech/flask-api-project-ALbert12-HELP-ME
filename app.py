from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    joke_url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(joke_url)

    try:
        data = response.json()
    except ValueError:
        return "Error: Could not parse JSON response"

    if data["type"] == "single":
        joke = data["joke"]
        setup = None
        delivery = None
    else:
        joke = None
        setup = data["setup"]
        delivery = data["delivery"]

    return render_template("index.html", joke=joke, setup=setup, delivery=delivery)

if __name__ == '__main__':
    app.run(debug=True)
