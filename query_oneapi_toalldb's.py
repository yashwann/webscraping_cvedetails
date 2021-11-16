from flask import Flask, request, jsonify
import json
import sqlite3
import os

app = Flask(__name__)
db_files = os.listdir("/home/yashwanth/Desktop/cve/dbfiles2")
final_db_files = sorted(db_files)
os.chdir("/home/yashwanth/Desktop/cve/dbfiles2")
length = len(final_db_files)


@app.route("/cvedata", methods=["GET"])
def cvedata():
    x = 0
    my_list = []
    while x < length:
        for filename in range(length):
            conn = sqlite3.connect(str(final_db_files[x]))
            query = request.args.get('query')
            cursor = conn.execute("SELECT * from {} where Description  LIKE '%'||?||'%'".format(final_db_files[x]),
                                  (query,))
            cvedata = [dict(Cve_id=row[0], Description=row[1], Published_Date=row[2], Modified_Date=row[3]) for row in
                       cursor.fetchall()]
            my_list.append(cvedata)
            x = x + 1
            if x == length:
                break

        return jsonify(my_list)


if __name__ == "__main__":
    app.run(host='1.1.1.1', debug=True)
