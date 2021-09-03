import requests, sys, os, re, shutil
from bs4 import BeautifulSoup

BASE_URL = "http://www.wholesalemantra.com"
def get_all_catalog(url):
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"cache.html")):
        page = requests.get(url)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"cache.html"), "w") as f:
            f.write(page.text)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"cache.html")) as f:
        soup = BeautifulSoup(f, "html.parser")
    cataloglist = soup.find_all("div",{"class","product-img"})
    return cataloglist
def get_each_catalog(all_catalog_links):
    for each_catalog in all_catalog_links:
        print(each_catalog)
        page = requests.get(each_catalog)
        soup = BeautifulSoup(page.content, "html.parser")
        each_catalog = soup.find_all("div", {"class","col-xs-5 control-label"})
        original_price = each_catalog[0].find_next_sibling().text[each_catalog[0].find_next_sibling().text.find("Rs.")+4:]
        if original_price.find(".") != -1:
            original_price = int(original_price.split(".")[0])
            price = (original_price//10 + 1) * 10
        else:
            original_price = int(original_price)
            price = (original_price//10 + 1) * 10
        print(original_price)
        print(price)

        all_suits = soup.find_all("button", {"class=","btn btn-view-catalogs cloudzoom-gallery"})
        for suit in all_suits:
            if suit.get("data-cloudzoom") is not None:
                image_url = suit.get("data-cloudzoom")[suit.get("data-cloudzoom").find("image:") + 7:-2]
                image_file_name = str(original_price) + "_" + str(price) + "_" + image_url.split("/")[-1]
                # print(url)
                if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),image_file_name)):
                    url = BASE_URL + image_url
                    response = requests.get(url, stream=True)
                    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),image_file_name), 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    del response


# print(productlist_img[0])
# print(productlist_pieces[0])

if __name__ == '__main__':
    url = "https://wholesalemantra.com/salwar-kameez"
    all_catalog = get_all_catalog(url)
    all_catalog_links = [BASE_URL + x.find("a").get("href") for x in all_catalog]
    print(all_catalog_links)
    
    # print([x for x in each_catalog if x.text.find("Average") != -1][0])
    # all_catalog = [x for x in all_catalog if  len(x.findChildren()) >= 1]
    # all_catalog = [x for x in all_catalog if  x.findChildren()[0].name == "img"]
    # print(all_catalog[4].fetchNextSiblings()[0].fetchNextSiblings())
    # all_catalog_links = ["http://www.wholesalemantra.com/salwar-kameez" + x.get("href") for x in all_catalog if len(x.get("href")) > 10 and x.get("href").find("wholesalemantra.com")==-1]
    # for item in all_catalog:
        
    #     if len(item.findChildren()) >= 1:
    #         if item.findChildren()[0].name == "img":
    #             # print("here")
    #             print(item)
            # print(item.findall("img",{"class","lazy img-full"}))
            # print(item.nextSibling.name)
    # print(all_catalog[0].)
    # page = requests.get(all_catalog_links[0])
    # soup = BeautifulSoup(page.content, "html.parser")
    # cataloglist = soup.find_all("a",href=True)
    each_catalog = get_each_catalog(all_catalog_links)