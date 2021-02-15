import requests_html
import requests
import re


link = "https://www.spriters-resource.com/pc_computer/heroes3/"

url_main = "https://www.spriters-resource.com"

session = requests_html.HTMLSession()

re_sheet = re.compile("pc_computer/heroes3/sheet")

response = session.get(link)

links = [x for x in response.html.links if re.search(re_sheet, x) and
         x not in response.html.absolute_links and "login" not in x]

import os
os.mkdir("heroes/")
os.chdir("heroes/")

for link in sorted(links):
    number = link.split("/")[4]
    print(number)
    url = url_main + "/download/" + number + "/"
    image = requests.get(url)

    with open(str(number) + ".png", "wb") as fi:
        fi.write(image.content)
