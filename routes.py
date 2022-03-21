
from flask import redirect, render_template, request, url_for, current_app
from sanity import bj
import os
import sqlite3

@bj.route("/")
@bj.route("/chooseflavor")
def chooseflavor():
    if 'flavor' not in request.args:
        conn = sqlite3.connect(os.path.join(current_app.root_path,"bj.sqlite"))
        flavors = conn.cursor().execute("""
            select name from flavor
        """).fetchall()
        return render_template("chooseflavor.html", flavors=flavors)
    else:
        return redirect(url_for("browserecipes",flavor=request.args['flavor']))

@bj.route("/browserecipes")
def browserecipes():
    return f"<html><body>The flavor is: {request.args['flavor']}</body></html>"
