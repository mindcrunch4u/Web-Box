#!/usr/bin/python3.5
from flask import Flask, render_template, url_for, redirect, request
from forms import MsgForm
from handlerequest import Urteil
import os
app = Flask(__name__) 
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route("/", methods=('GET','POST')) 
def home(): 
    form = MsgForm()
    if request.method == "POST":
        form = request.form
        content = form['content']
        post_id = form['post_id']
        return Urteil( content, post_id )

    return render_template('home.html',title="Home", form=form)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=False, port=9900)
