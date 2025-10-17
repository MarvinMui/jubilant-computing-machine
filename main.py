import duckdb
import pandas as pd
import os
from flask import Flask, jsonify, request
import db
import json
from db import DB_PATH
import ingest

# Import and ingest data
# exctract and normalize the data
# store in a database
# use ai for data cleaning and enrinching
# temporarily put aside problem of making "dirty data"
# or add option to disable
# parsing and structuring might be better with the defualt...
# enrich missing or inconsistant fields
# inconsistent being out of bound, incorrect data type, data format
# have an api that that has a limited query bound
# basically just make it recieve commands in natrual language that converts them to apis

UPLOAD_FOLDER = './data/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# --- example route: health check ---
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI CMDB backend running."})


# --- ingest raw file ---
@app.route("/ingest", methods=["POST"])
def ingest_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    # You can call your data parsing or AI enrichment here

    with open(filepath, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    print(df.to_string())

    normalized_df = ingest.normalize(df)

    device_df = normalized_df[df.columns[[0, 1, 4, 3, 2, 6, 8]]]
    # user_df = normalized_df[df.columns[[0, 1, 4, 3, 2, 6, 8]]]
    # app_df = normalized_df[df.columns[[0, 1, 4, 3, 2, 6, 8]]]

    # Insert into DuckDB
    with duckdb.connect(DB_PATH) as con:
        con.execute("INSERT INTO devices SELECT * FROM device_df")

    return jsonify({"message": "Data ingested successfully", "records": len(df)}), 200


@app.route("/data", methods=["GET"])
def show_all_data():
    table = request.args.get("table", "devices")  # default
    with duckdb.connect(DB_PATH) as con:
        df = con.execute(f"SELECT * FROM {table}").df()

    return df.to_dict(orient="records")


@app.route("/reset", methods=["POST"])
def reset_db():
    try:
        with duckdb.connect(DB_PATH) as con:
            con.execute("DELETE FROM user_device;")
            con.execute("DELETE FROM user_app;")
            con.execute("DELETE FROM devices;")
            con.execute("DELETE FROM users;")
            con.execute("DELETE FROM apps;")


        return {"message": "Database tables dropped successfully."}, 200
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)
    # main()
