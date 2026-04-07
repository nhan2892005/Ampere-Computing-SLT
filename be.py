from flask import Flask, render_template, request, redirect, url_for
from db import init_db, query_db, get_db, export_db_to_json
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

@app.route("/q2", methods=["GET", "POST"])
def q2():
    error = None
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        if not name or not location:
            error = "Both name and location are required."
        else:
            try:
                with get_db() as conn:
                    conn.execute(
                        "INSERT INTO facility (name, location) VALUES (?, ?)",
                        (name, location),
                    )
                    conn.commit()
                return redirect(url_for("q1"))
            except Exception as e:
                error = str(e)
    return render_template("q2.html", error=error)

@app.route("/q3")
def q3():
    return render_template("q3.html")

@app.route("/q4")
def q4():
    return render_template("q4.html")


@app.route("/q4/export", methods=["POST"])
def q4_export():
    try:
        export_db_to_json("/q4")
        return render_template("q4.html", success=True)
    except Exception as e:
        return render_template("q4.html", success=False, error=str(e))

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)