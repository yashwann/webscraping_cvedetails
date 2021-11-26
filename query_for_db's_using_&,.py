from flask import Flask, request, jsonify
import json
import sqlite3
import os

app = Flask(__name__)

db_files = os.listdir("/home/authbase/Desktop/webscraping_cvedetails.com/databasefiles")
final_db_files = sorted(db_files)
os.chdir("/home/authbase/Desktop/webscraping_cvedetails.com/databasefiles")
length = len(final_db_files)


@app.route("/cvedata/<one>,<int:two>", methods=["GET"])
@app.route("/cvedata/<one>,<float:two>", methods=["GET"])
@app.route("/cvedata/<one>,<two>", methods=["GET"])
def cvedata(one="", two=""):
    x = 0
    my_list = []
    while x < length:
        for filename in range(length):
            conn = sqlite3.connect(str(final_db_files[x]))
            # query = request.args.get('query')
            oneget = request.args.get('one')
            twoget = request.args.get('two')

            cursor = conn.execute(
                "SELECT * from {} where Description  LIKE '%'||?||'%''%'||?||'%'".format(final_db_files[x]),
                (one, two,))
            cvedata = [dict(Cve_id=row[0], Description=row[1], Publish_Date=row[2], Update_Date=row[3]) for row in
                       cursor.fetchall()]
            my_list.append(cvedata)
            x = x + 1
            if x == length:
                break

        return jsonify(my_list)


@app.route("/cvedata/<one>", methods=["GET"])
@app.route("/cvedata/<one>&<int:two>", methods=["GET"])
@app.route("/cvedata/<one>&<two>", methods=["GET"])
@app.route("/cvedata/<one>&<float:two>", methods=["GET"])
def cvedata1(one="", two=""):
    x = 0
    my_list = []
    while x < length:
        for filename in range(length):
            conn = sqlite3.connect(str(final_db_files[x]))
            # query = request.args.get('query')
            oneget = request.args.get('one')
            twoget = request.args.get('two')

            cursor = conn.execute(
                "SELECT * from {} where Description  LIKE '%'||?||'%''%'||?||'%'".format(final_db_files[x]),
                (one, two,))
            cvedata = [dict(Cve_id=row[0], Description=row[1], Publish_Date=row[2], Update_Date=row[3]) for row in
                       cursor.fetchall()]
            my_list.append(cvedata)
            x = x + 1
            if x == length:
                break

        return jsonify(my_list)


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
