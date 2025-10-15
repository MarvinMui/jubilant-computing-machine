import duckdb
import pandas as pd
import os
from flask import Flask, jsonify, request
import db
# from db_utils import init_db, load_sample_data
# from models import db, Device

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


# --- example route: ingest raw file ---
@app.route("/ingest", methods=["POST"])
def ingest_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    # You can call your data parsing or AI enrichment here
    return jsonify({"message": "File uploaded", "path": filepath})


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)
    # main()