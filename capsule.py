from configuration import default_config, box_mode
from flask import Flask, render_template, url_for, redirect, request
from forms import MsgForm
from handlerequest import handle_post
import os
app = Flask(__name__) 
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route("/" + default_config.web_path, methods=('GET','POST')) 
def home(): 
    form = MsgForm()
    if request.method == "POST":
        form = request.form
        content = form['content']
        post_id = form['post_id']
        return handle_post(content, post_id)
    
    is_message_box = False
    if default_config.mode == box_mode.message_box:
        is_message_box = True

    return render_template(
            'home.html',
            title="Home", 
            form=form, 
            html_web_path=default_config.web_path, 
            mode_message_box=is_message_box)

if __name__ == '__main__':
    app.run(debug=True, port=8077)
