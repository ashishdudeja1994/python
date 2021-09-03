import os
from glob import glob
for folder_name in glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final","*")):
        print("'" + folder_name.split("\\")[-1] + "':'',\\")
        for file_name in os.listdir(folder_name):
            original_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",folder_name,file_name)
            if original_name.find(".png") != -1:
                changed_name = original_name.split(".png")[0] + ".jpg"
                print(original_name,changed_name)
                os.rename(original_name,changed_name)
                print(os.path.join(os.path.dirname(os.path.abspath(__file__)),"final",file_name))