from posixpath import dirname
from PIL import Image
import os,sys,shutil
from glob import glob

if __name__ == '__main__':
    folder_list = []
    for folder_name in glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final","*")):
        # print("'" + folder_name.split("\\")[-1] + "':'',\\")
        for file_name in os.listdir(folder_name):
            print(folder_name)
            print(file_name)
            original_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",folder_name,file_name)
            if original_name.find(".jpg") != -1 or original_name.find(".jpeg") != -1:
                changed_name = original_name.split(".")[0] + ".png"
                # print(original_name,changed_name)
                dest = os.path.join(os.path.dirname(os.path.dirname(changed_name)),os.path.basename(changed_name))
                # os.rename(original_name,changed_name)
                print(original_name, dest)
                shutil.move(original_name, dest)

    # for item in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final")):
    #     # print(item)
    #     if item.find("jpeg") != -1 or item.find("jpg") != -1:
    #         get_price = "_".join(item.split("_")[:2])
    #         # print(get_price)
    #         if get_price not in folder_list:
    #             folder_list.append(get_price)
    #             if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",get_price)):
    #                 os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",get_price))
    #         # print(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",item))
    #         try:
    #             test_image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",item))
    #             new_image = make_square(test_image)
    #             # new_image.show()
    #             # print(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",get_price))
    #             # print(item)
    #             if item.find(".jpg") != -1:
    #                 item = item[:item.find(".jpg")] + ".png"
    #             if item.find(".jpeg") != -1:
    #                 item = item[:item.find(".jpeg")] + ".png"
    #             print(item)
    #             if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",get_price,item)):
    #                 new_image.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",get_price,item))
    #         except Exception as e:
    #             print(e)
    #         # break


