import sys
import time
import requests
import subprocess
from subprocess import Popen, PIPE, STDOUT
from lxml import etree
from io import StringIO

# cd default_storage
# python -m http.server 5000
parser = etree.HTMLParser()

def get_link_from_result(result):
    html = result.content.decode("utf-8")
    tree = etree.parse(StringIO(html), parser=parser)
    refs = tree.xpath("//a")
    links = [link.get('href', '') for link in refs]
    return links[0]


def return_if_found(request_endpoint, is_debug=False):
    probe_delay = 5
    while True:
        try:
            result = requests.get(request_endpoint, verify=(not is_debug))
            if result.status_code == 200:
                return result
            else:
                print("Probing for path: {}...".format(request_endpoint))
        except Exception as e:
            print(e)
            return None
        time.sleep(probe_delay)


def probe_id(storage_endpoint, post_id, is_debug):
    # probe folder
    print("Looking into folder...")
    post_endpoint = "{}/{}".format(storage_endpoint, post_id)
    result = return_if_found(post_endpoint, is_debug)

    # probe confirmation
    print("Looking for confirmation...")
    post_endpoint = "{}/{}/{}".format(storage_endpoint, post_id, "confirmation")
    result = return_if_found(post_endpoint, is_debug)
    confirmation_code = int(result.content.decode().strip())

    if confirmation_code == 1:
        print("Looking for download link...")
        post_endpoint = "{}/{}/{}".format(storage_endpoint, post_id, "datablock")
        result = return_if_found(post_endpoint, is_debug)
        link = get_link_from_result(result)
        link = "{}/{}/{}/{}".format(storage_endpoint, post_id, "datablock", link)
        return link
    else:
        return None


def download_and_save(from_link, to_folder="./"):
    process = Popen(["/usr/bin/curl", "-s", "-O", from_link])
    exitcode = process.wait()
    if exitcode != 0:
        return -1

    process = Popen(["/usr/bin/mkdir", "-p", to_folder])
    exitcode = process.wait()
    if exitcode != 0:
        return -1

    file_name = from_link.split("/")[-1]
    process = Popen(["/usr/bin/mv", file_name, to_folder], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    exitcode = process.wait()

    return "{}/{}".format(to_folder, file_name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <ID>")
        sys.exit(1)

    is_debug = True
    storage_endpoint="http://127.0.0.1:5000"
    link = probe_id(storage_endpoint, sys.argv[1], is_debug)
    outfile = download_and_save(link)
    print(outfile)
