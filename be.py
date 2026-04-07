from flask import Flask, render_template
from db import init_db, query_db
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/q0")
def q0():
    rows = query_db("SELECT * FROM facility")
    return render_template("q0.html", rows=rows)

@app.route("/q1")
def q1():
    tables = {t: query_db(f"SELECT * FROM {t}")
              for t in ("facility", "supplier", "product", "warehouse", "consumption")}
    return render_template("q1.html", tables=tables)

@app.route("/q3")
def q3():
    return render_template("q3.html")

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)