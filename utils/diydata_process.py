import leancloud
import os
from bs4 import BeautifulSoup

leanId = os.environ["leanId"]
leanKey = os.environ["leanKey"]
leancloud.init(leanId, leanKey)

def process_item():
    Content = leancloud.Object.extend("Diy")
    query = Content.query
    try:
        # item = query.first()
        not_parsed_items = query.not_equal_to("parsed", True).limit(1000).find()
        # item = query.get('5b5861c2128fe1002f78bed8')
        # item = query.get('5b5861c2ee920a003ca9c842')
        # item = query.get('5b5861c2808ca4006fafd60c')
        # item = query.get('5b5861c2128fe1002f78bee0')
        for item in not_parsed_items:
            print(item.get("objectId"))
            content = item.get("article")
            # print(content)
            # print("\r\n")
            if content:
                result = parseItem(content)
                print(result)
                if result:
                    item.set("content", result)
                    item.set("parsed", True)
                    item.save()
    except leancloud.errors.LeanCloudError as e:
      print(e)
        # content = Content()
        # content.set("category", item["category"])
        # content.set("url", item["url"])
        # content.set("backgroundImg", item["backgroundImg"])
        # content.set("title", item["title"])
        # content.set("desc", item["desc"])
        # content.set("article", item["article"])
        # content.save()

    # return item

def parseItem(content):
    soup = BeautifulSoup(content, "lxml")
    for a in soup.findAll('a'):
      a.replaceWithChildren()
    # print("\r\n")
    div = soup.div

    result = []
    for child in div.children: 
        # print(child)

        if child.name == "img":
          src = getImg(child)
          # print(src)
          if src:
            result.append(src)
        string = child.string
        if not string:
          string = ""
          for strTmp in child.strings:
            string = string + strTmp
        # if not string:
        try:
            imgs = child.findAll('img')
            for img in imgs:
              src = getImg(img)
              # print(src)
              if src:
                result.append(src)
        except AttributeError:
            pass

        # else:
          # print("\r\n")
          # print(string)
        if string:
          result.append(string)
    return result

def getImg(img):
    # print(img)
    src = ""
    try:
      src = img["src"]
      if src and src.startswith("//"):
        src = "https:"+src
    except KeyError:
      pass
    return src

process_item()