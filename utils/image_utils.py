import re
import base64
import requests


def get_jpg_url(google_img_url):
    file_id_regex = re.compile("file/d/(.*)/view")
    file_id = file_id_regex.search(google_img_url).group(1)
    binary_img_response = requests.get(
        f"https://drive.google.com/uc?id={file_id}&export=download")
    img_base64_string = base64.b64encode(binary_img_response.content).decode("utf-8")
    request_data = {"key": "6d207e02198a847aa98d0a2a901485a5",
                    "source": img_base64_string,
                    "format": "json"}
    img_host_response = requests.post("https://freeimage.host/api/1/upload",
                                      data=request_data)
    response_json = img_host_response.json()
    if response_json["status_code"] != 200:
        return None
    # if necessary, contains thumb and medium sizes
    jpg_url = img_host_response.json()["image"]["image"]["url"]
    return jpg_url
