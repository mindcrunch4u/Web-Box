## About

I like [Pastebin.com](https://pastebin.com/), but:
- I don't want to store my text on other people's server.
- I don't want to use clear text.

So I wrote this project. The messages are AES-encrypted on the client (browser), the server only stores encrypted data.

Other than a message box, this project also offers something like [Y2mate.com](https://www.y2mate.com/), the server handles a download request and stores the downloaded files.

### Mode: Message Box

![Message Box Demo](https://github.com/mindcrunch4u/Web-Box/blob/master/about/web-box-demo.gif)

### Mode: Downloader

**Start The Servers**
- One for file access, such as Nginx's `autoindex`.
- Another for handling download requests.

![Starting the servers](https://github.com/mindcrunch4u/Web-Box/blob/master/about/starting-server.gif)

**Using the Downloader**

![Using the downloader](https://github.com/mindcrunch4u/Web-Box/blob/master/about/using-the-downloader.gif)

## Setting up the server

**Clone and Prepare the Environment**
```
cd path/to/project/
python -m venv ./
source bin/activate
pip3 install -r requirements.txt
pip3 install WTForms==2.3.3
pip3 install Werkzeug==2.2.2
pip3 install lxml # for downloader_probe.py
```

**Install Dependencies**

*These are used by the `ytdl.sh` script:*
- ffmpeg (to extract audio from video)
- yt-dlp (to download videos from YouTube)
- 7z (to zip and encrypt downloaded files, in case the download link does not use HTTPS)
- curl # for downloader_probe.py

**Edit configuration.py**

An example (enable downloader mode):
```
default_config.mode = box_mode.downloader
default_config.web_path="test" # the server is available at http://127.0.0.1/test/
default_config.ytdl_script_path = "./ytdl.sh"
default_config.storage_path="./default_storage/"
default_config.ytdl_zip_file = False
```

**Start The Server**

```
python3 capsule.py
```

## Nginx Configuration

### Providing access to Web-Box

**Start the Web-Box (capsule) server**

```
nohup python capsule.py 2>&1 >> capsule_log.txt &
```

**Configure Nginx to pass requests to the server**

Assume you have configured the `default_config.web_path` to `086532dd-a7da-4fdf-9d27-ab31131da975`:

```
location /086532dd-a7da-4fdf-9d27-ab31131da975
{
        proxy_pass http://127.0.0.1:8077/086532dd-a7da-4fdf-9d27-ab31131da975;
}
```

Using the `web_path` option allows you to serve multiple apps under one Nginx server.

### Providing access to Storage

**Start the python http server**

The same can be achived using Nginx's `autoindex`. Assume your `default_config.storage_path` is set to `./default_storage/`:

```
cd ./default_storage
nohup python -m http.server 5005 --bind 127.0.0.1 2>&1 >> fileserver_log.txt &
```

**Configure Nginx to pass requests to the http server**

Assume the path is `c6602910-67cf-43f2-a47b-19e040f20e1e`:

```
location /c6602910-67cf-43f2-a47b-19e040f20e1e/
{
        charset UTF-8;
        proxy_pass http://127.0.0.1:5005/;
}
```
