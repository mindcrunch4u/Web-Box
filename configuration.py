
class Modes:
    def __init__(self):
        self.message_box = "message_box"
        self.downloader = "downloader"

box_mode = Modes()

class DefaultConfig:
    def __init__(self):
        self.mode = "message_box"
        #self.mode = "ytdl"
        self.web_path=""
        self.storage_path="./"
        self.ytdl_script_path = "./ytdl.sh"
        self.ytdl_zip_file = False

default_config = DefaultConfig()
default_config.mode = box_mode.downloader
default_config.web_path="" # /another-name/
default_config.ytdl_script_path = "./ytdl.sh"
# NOTE: provide user with some sort of access to storage_path, such as NginX autoindex.
default_config.storage_path="./default_storage/"
default_config.ytdl_zip_file = False
