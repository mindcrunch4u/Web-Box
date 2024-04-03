from flask import render_template, escape
from datetime import datetime
import subprocess
from subprocess import Popen, PIPE, STDOUT
import os
from threading import Thread
from configuration import default_config, box_mode

def is_post_id_valid( post_id ):
    if len(str(post_id)) < 1:
        return False
    return True


def append_to_post( post_id, append_string):
    if default_config.mode == box_mode.message_box:
        #append_string = str(datetime.now()) + "\n>-------------\n" + append_string  +  "\n-------------<\n"
        parent_dir=default_config.storage_path + "/" + "Posts"
        post_dir=parent_dir+"/"+ post_id
        post_file_path = post_dir+"/"+ "post_log"
        if not os.path.isdir(parent_dir):
            print("[Urteil] Creating Posts Main Storage.")
            os.makedirs(parent_dir)
        if not os.path.isdir(post_dir):
            print("[Urteil] Creating Storage for Post: ", post_id)
            try:
                os.makedirs(post_dir)
            except:
                return False
        if os.path.isdir(post_dir) and os.path.isdir(parent_dir):
            post = open(post_file_path,'a')
            post.write("\n\n\n")
            post.write( append_string )
            post.close()
        return True

    else:
        parent_dir=default_config.storage_path
        post_dir=parent_dir+"/"+ post_id
        temp_file_name="datablock"
        post_temp_dir = post_dir+"/"+ temp_file_name
        if not os.path.isdir(parent_dir):
            print("[*] Creating Posts Main Storage.")
            try:
                os.makedirs(parent_dir)
            except:
                return False;
        if os.path.isdir(post_dir):
            print("[-] Post exists")
            return False;
        if not os.path.isdir(post_dir):
            print("[*] Creating Storage for Post: ", post_id)
            try:
                os.makedirs(post_dir)
            except:
                return False
        if os.path.isdir(post_dir) and os.path.isdir(parent_dir) and not os.path.isdir(post_temp_dir):
            try:
                os.makedirs(post_temp_dir)
            except:
                return False

        use_zip_file = "use_zip_file"
        if not default_config.ytdl_zip_file:
            use_zip_file = ""

        print("[*] Executing Script: {}, Args: {}".format(default_config.ytdl_script_path, [append_string, post_temp_dir, use_zip_file]))
        thread = Thread(target = execute_script, args = (append_string, post_temp_dir, use_zip_file))
        thread.start()
        return True


def execute_script( content, destination, use_zip_file ):
    script_path = default_config.ytdl_script_path
    content = ' '.join(content.strip().splitlines())
    process = Popen(["/usr/bin/bash", script_path, content, destination, use_zip_file] , stdout=PIPE, stderr=STDOUT)
    logfile_location = destination + "/../" + "log.txt"
    with process.stdout:
        log_subprocess_output(process.stdout, logfile_location)
    exitcode = process.wait()


def log_subprocess_output(pipe, logfile_location):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        try:
            decoded_line = line.decode()
        except:
            decoded_line = str(line)
        post = open(logfile_location, 'a+')
        post.write( decoded_line )
        post.close()


def fetch_post( post_id ):
    if default_config.mode == box_mode.message_box:
        parent_dir=default_config.storage_path + "/" + "Posts"
        post_dir=parent_dir+"/"+post_id
        post_file_path = post_dir+"/"+"post_log"
        if os.path.isfile(post_file_path):
            post = open(post_file_path,'r')
            post_data = post.read()
            return post_data
        return None
    else:
        return "Visit The Download Folder on the Server."


def handle_post(content, post_id):
    if not is_post_id_valid( post_id ):
        print("[!] Invalid Post Id.")
        return render_template('invalid_id.html', title="Invalid ID")

    if len(content) == 0:
        # empty message gox means get content by ID
        print("[*] Received Empty Content, Providing Post to User.")
        return render_template('display_msg.html', title="Log", incoming_massage=fetch_post(post_id))
    else:
        # when both ID and content are provided, append to the original post
        print("[*] Content Provided.")
        print("[*] Updating Post, ID:" + str(post_id))
        if append_to_post( post_id, content ):
            return render_template('posted.html', title="Posted.")
        else:
            return render_template('posted_failed.html', title="Post Denied.")
