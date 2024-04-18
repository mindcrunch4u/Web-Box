from configuration import default_config, box_mode
from flask import Flask, render_template, url_for, redirect, request
from forms import MsgForm
from handlerequest import handle_post
import os
import secrets
import string

app = Flask(__name__) 
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = os.urandom(24)

def generate_password(password_length):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(password_length))
    return password

password_length = 50
amount_of_passwords = 5
list_of_passwords = []
for i in range(amount_of_passwords):
    tmp_password = generate_password(password_length)
    list_of_passwords.append(tmp_password)
    print("[{}] Password: {}".format(i, tmp_password))

@app.route("/" + default_config.web_path, methods=('GET','POST')) 
def home(): 
    form = MsgForm()
    if request.method == "POST":
        form = request.form
        content = form['content']
        post_id = form['post_id']
        print(form)
        if default_config.require_password and "password" in form:
            password = form['password']
            if password not in list_of_passwords:
                return render_template('access_denied.html', title="Invalid Password")
        return handle_post(content, post_id)
    
    is_message_box = False
    if default_config.mode == box_mode.message_box:
        is_message_box = True

    return render_template(
            'home.html',
            title="Home", 
            form=form, 
            require_password=default_config.require_password, 
            html_web_path=default_config.web_path, 
            mode_message_box=is_message_box)

if __name__ == '__main__':
    app.run(debug=True, port=8077)
