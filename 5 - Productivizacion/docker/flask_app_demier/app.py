from flask import Flask

app = Flask(__name__) 

@app.route("/", methods=["GET"])
def hola():
    return "<h1>Hola dockerfile</h1>"


app.run(host="0.0.0.0", port=5001)
