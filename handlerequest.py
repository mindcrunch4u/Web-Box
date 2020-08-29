from flask import render_template, escape
from datetime import datetime
import os
def Post_Id_Valid( post_id ):
    if len(str(post_id)) < 1:
        return False
    return True
#    if post_id == "testid" :
#        return True
#    else:
#        return False

def Append_To_Post( post_id, append_string ):
    #append_string = str(datetime.now()) + "\n>-------------\n" + append_string  +  "\n-------------<\n"
    MAIN_DIR=str(os.getcwd()) + "/" + "Posts"
    POST_DIR=MAIN_DIR+"/"+ post_id
    POST_FILE_PATH = POST_DIR+"/"+ "post_log"
    if not os.path.isdir(MAIN_DIR):
        print("[Urteil] Creating Posts Main Storage.")
        os.makedirs(MAIN_DIR)
    if not os.path.isdir(POST_DIR):
        print("[Urteil] Creating Storage for Post: ", post_id)
        try:
            os.makedirs(POST_DIR)
        except:
            return False
    if os.path.isdir(POST_DIR) and os.path.isdir(MAIN_DIR):
        post = open(POST_FILE_PATH,'a')
        post.write("\n\n\n")
        post.write( append_string )
        post.close()
    return True


def Fetch_Post( post_id ):
    MAIN_DIR=str(os.getcwd()) + "/" + "Posts"
    POST_DIR=MAIN_DIR+"/"+post_id
    POST_FILE_PATH = POST_DIR+"/"+"post_log"
    if os.path.isfile(POST_FILE_PATH):
        post = open(POST_FILE_PATH,'r')
        post_data = post.read()
        return post_data
    return None

def Urteil(content, post_id):
    if not Post_Id_Valid( post_id ):
        print("[Urteil] Invalid Post Id.")
        return render_template('invalid_id.html', title="Nope.")

    if len(content) == 0:
        print("[Urteil] Received Empty Content.")
        print("[Urteil] Providing Post to user.")
        return render_template('display_msg.html', title="Log", incoming_massage=Fetch_Post(post_id))
    else:
        print("[Urteil] Content Provided.")
        print("[Urteil] Check Post Dir: " + str(os.getcwd()))
        print("[Urteil] Updating Post, ID:" + str(post_id))
        if Append_To_Post( post_id, content ):
            return render_template('posted.html', title="Posted")
        else:
            return render_template('posted_fail.html', title="Can\'t Post")
