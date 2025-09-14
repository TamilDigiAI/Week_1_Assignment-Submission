from flask import Flask   # <-- use Flask, not flash

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello My dear Friends"

if __name__ == "__main__":
    app.run(debug=True)
