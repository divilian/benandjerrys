
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
    if 'flavor' not in request.args:
        return redirect(url_for("chooseflavor"))
    the_flavor_they_apparently_like = request.args['flavor']
    conn = sqlite3.connect(os.path.join(current_app.root_path,"bj.sqlite"))
    recipes = conn.cursor().execute("""
        select name from recipe
        where flavorName=?
    """, (the_flavor_they_apparently_like,)).fetchall()

    return render_template("browserecipes.html",
        flavor=the_flavor_they_apparently_like, recipes=recipes)

@bj.route("/viewrecipe", methods=['GET','POST'])
def viewrecipe():
    if request.method=='GET' and 'recipe' not in request.args:
        return redirect(url_for("chooseflavor"))
    elif 'numCartons' not in request.form:
        conn = sqlite3.connect(os.path.join(current_app.root_path,"bj.sqlite"))
        ingredients = conn.cursor().execute("""
            select mixin_name, costPerOz
            from mixin join ingredients on mixin.name=ingredients.mixin_name
            where recipe_name=?
        """, (request.args['recipe'],)).fetchall()
        baseFlavor = conn.cursor().execute("""
            select flavorName from recipe
            where name=?
        """, (request.args['recipe'],)).fetchone()
        cartonsOrdered = conn.cursor().execute("""
            select cartonsOrdered from recipe
            where name=?
        """, (request.args['recipe'],)).fetchone()
        
        return render_template("viewrecipe.html", recipe=request.args['recipe'],
            ingredients=ingredients, baseFlavor=baseFlavor[0],
            cartonsOrdered=cartonsOrdered[0])
    else:
        conn = sqlite3.connect(os.path.join(current_app.root_path,"bj.sqlite"))
        conn.cursor().execute("""
            update recipe set cartonsOrdered=cartonsOrdered+?
            where name=?
        """, (request.form['numCartons'],request.form['recipe']))
        conn.commit()
        newCartonsOrdered = conn.cursor().execute("""
            select cartonsOrdered from recipe where name=?
        """, (request.form['recipe'],)).fetchone()
        return render_template("confirmorder.html",
            recipe=request.form['recipe'],
            newCartonsOrdered=newCartonsOrdered)

    
