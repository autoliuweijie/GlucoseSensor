from flask import Flask, session, redirect, url_for, request
from mylib.database.datamangers import DevicesTable, UsersTable, RecordsTable
from datetime import datetime


app = Flask(__name__)
app.secret_key = '\xf1\x92Y\xdf\x8ejY\x04\x96\xb4V\x88\xfb\xfc\xb5\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        view = """
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
        """
        return view


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7002)
