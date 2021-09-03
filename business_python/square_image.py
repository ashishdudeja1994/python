from PIL import Image
import os,sys

def make_square(im, min_size=256, fill_color=(255, 255, 255, 255)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

if __name__ == '__main__':
    folder_list = []
    for item in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final")):
        # print(item)
        if item.find("jpeg") != -1 or item.find("jpg") != -1:
            get_price = "_".join(item.split("_")[:2])
            # print(get_price)
            if get_price not in folder_list:
                folder_list.append(get_price)
                if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",get_price)):
                    os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",get_price))
            # print(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",item))
            try:
                test_image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",item))
                new_image = make_square(test_image)
                # new_image.show()
                # print(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",get_price))
                # print(item)
                if item.find(".jpg") != -1:
                    item = item[:item.find(".jpg")] + ".png"
                if item.find(".jpeg") != -1:
                    item = item[:item.find(".jpeg")] + ".png"
                print(item)
                if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",get_price,item)):
                    new_image.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",get_price,item))
            except Exception as e:
                print(e)
            # break


