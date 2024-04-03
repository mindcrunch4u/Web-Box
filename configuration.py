
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
default_config.mode = box_mode.message_box
default_config.web_path="" # /another-name/
default_config.ytdl_script_path = "./ytdl.sh"
default_config.storage_path="./default_storage/"
default_config.ytdl_zip_file = False
