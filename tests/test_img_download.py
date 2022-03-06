from utils.image_utils import get_jpg_url

google_urls = [
    "https://drive.google.com/file/d/1qFdhOP6aXYrAlsAjGjfF0EDsT6hvu3Dq/view?usp=sharing",
    "https://drive.google.com/file/d/1Ndp75tH15M9FCIiVGJw031MnQ1fkANac/view?usp=sharing"]

for url in google_urls:
    print(get_jpg_url(
        url))
