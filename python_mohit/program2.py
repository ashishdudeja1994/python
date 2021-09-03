from typing import final
from PIL import Image, ImageDraw, ImageFont
import os,sys,glob
# import win32com.client as win32  
# mail = win32.Dispatch('outlook.application').CreateItem(0)
# mail.To = 'sample@sample.com'
# mail.Subject = 'test'
from io import StringIO

import pandas as pd
pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>

def create_final_html(final_df_list,image_html_string):
    abs_path_html = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_files','myhtml.html')
    abs_path_css = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_files','df_style.css')
    # print(df.to_html())
    # create css File
    with open(abs_path_css, 'w') as f:
        f.write("""/* includes alternating gray and white with on-hover color */
                    .mystyle {
                        border: 1px solid #B0CBEF;
                        border-width: 1px 0px 0px 1px;
                        font-size: 10pt;
                        font-family: Arial;
                        font-weight: 100;
                        border-spacing: 0px;
                    }

                    .mystyle TH {
                        background-image: url(excel-2007-header-bg.gif);
                        background-repeat: repeat-x; 
                        font-weight: normal;
                        font-size: 14px;
                        border: 1px solid #9EB6CE;
                        border-width: 0px 1px 1px 0px;
                        height: 17px;
                    }

                    .mystyle TD {
                        border: 0px;
                        background-color: white;
                        padding: 0px 4px 0px 2px;
                        border: 1px solid #D0D7E5;
                        border-width: 0px 1px 1px 0px;
                    }

                    .mystyle TD B {
                        border: 0px;
                        background-color: white;
                        font-weight: bold;
                    }

                    .mystyle TD.heading {
                        background-color: #E4ECF7;
                        text-align: center;
                        border: 1px solid #9EB6CE;
                        border-width: 0px 1px 1px 0px;
                    }

                    .mystyle TH.heading {
                        background-image: url(excel-2007-header-left.gif);
                        background-repeat: none;
                    }
                    """)
    # print(len(final_df_list))
    df_html = ""
    for df in final_df_list:
        object_counter_columns = ['pmNoSystemRabReleasePacket','pmNoSystemRabReleaseSpeech',\
            'pmTotNoRrcConnectReqCs','pmTotNoRrcConnectReqCsSucc','pmTotNoRrcConnectReqPs','pmTotNoRrcConnectReqPsSucc']
        if df.columns.tolist()[:2] == ['Object','Counter']:
            df = df.loc[df['Counter'].isin(object_counter_columns)]
        df_html += df.to_html(classes='mystyle', index=False)
        df_html += "<br>"
    # print(df_html)
    html_string = '''
    <html>
    <head><title>HTML Pandas Dataframe with CSS</title></head>
    <link rel="stylesheet" type="text/css" href="df_style.css"/>
    <body>
        {df_html}
        {image_html_string}
    </body>
    </html>.
    '''
    # OUTPUT AN HTML FILE
    with open(abs_path_html, 'w') as f:
        html_string_each_file = html_string.format(df_html = df_html,\
            image_html_string=image_html_string)
        f.write(html_string_each_file)
    return html_string_each_file
def create_df(all_lines_list):
    print("Getting DataFrames")
    # print([x for x in all_lines_list if x[:6].find('Date:')!=-1])
    prompt_list = [x[:x.find(">")] for x in all_lines_list if x.find('st cell') != -1]
    prompt = prompt_list[0]
    print(prompt)
    start_line = None
    end_line = None
    df_index = []
    for line_index in range(0,len(all_lines_list)):
        if all_lines_list[line_index][:6].find('Date:') != -1:
            start_line =line_index + 1
        elif all_lines_list[line_index].find(">") != -1 and start_line is not None:
            end_line = line_index
            df_index.append([start_line,end_line])
            start_line = None
        if all_lines_list[line_index][:16].find('CELL RESOURCES') != -1:
            start_line =line_index + 1
        elif all_lines_list[line_index].find("<") != -1 and start_line is not None:
            end_line = line_index - 1
            df_index.append([start_line,end_line])
            start_line = None
    print(df_index)
    # print(start_line,end_line)
    df_list = []
    for item in df_index:
        all_lines_list_final = [x[:-1].strip() for x in all_lines_list[item[0]:item[1]-1] if x[:-1].strip() != '']
        TESTDATA = StringIO("\n".join(all_lines_list_final))
        df = pd.read_fwf(TESTDATA, dtype=str, keep_default_na=False)
        if df.columns.tolist()[0] == 'CELL':
            # print(prompt[2:-1])
            df = df.loc[df['CELL'].str.contains(prompt[2:-1])]
        df_list.append(df)
    final_df_list = []
    df_dict = {}
    for index in range(0,len(df_list)):
        if "".join(df_list[index].columns.tolist()[:2]) in df_dict.keys():
            df_dict["".join(df_list[index].columns.tolist()[:2])].append(df_list[index])
        else:
            df_dict["".join(df_list[index].columns.tolist()[:2])] = [df_list[index]]
    for k,v in df_dict.items():
        final_df_list.append(pd.concat(v, axis=0))
    return final_df_list

        
    

def generate_images_output_files(all_lines_list):
    print("Getting Images")
    commands = ['st cell', 'alt', 'hget retsubunit operationalState|userlabel|electricalant|maxtilt|mintilt|iuantbasestationid|iuantsectorid', \
        'mfitr','hget UtranCell']
    images_string = ""
    for command_index in range(0,len(commands)):
            # print(commands[command_index])
            prompt_list = [x[:x.find(">")] for x in all_lines_list if x.find(commands[command_index]) != -1]
            if len(prompt_list) == 0:
                continue
            else:
                prompt = prompt_list[0]
            print(prompt)
            start_line = None
            end_line = None
            for line_index in range(0,len(all_lines_list)):
                if all_lines_list[line_index].find(commands[command_index]) != -1:
                    start_line = line_index
                elif all_lines_list[line_index].find(prompt) != -1 and start_line is not None:
                    if commands[command_index] == 'hget retsubunit operationalState|userlabel|electricalant|maxtilt|mintilt|iuantbasestationid|iuantsectorid':
                        end_line = line_index - 2
                    elif commands[command_index] == 'hget UtranCell':
                        end_line = line_index - 2
                    else:
                        end_line = line_index
                    break
            print(start_line,end_line)
            if start_line is None or end_line is None:
                continue
            number_of_lines = len(all_lines_list[start_line:end_line-1])
            
            # print(all_lines_list[start_line:end_line-1])
            all_lines_list_final = [x[:-1].strip() for x in all_lines_list[start_line:end_line-1] if x[:-1].strip() != '']
            max_column = [max([len(x) for x in all_lines_list_final])][0]
            fnt = ImageFont.truetype("./COUR.TTF", 17)
            img = Image.new('RGB', (max_column * 10 + 20, number_of_lines*19), color = (0, 0, 0))
            d = ImageDraw.Draw(img)
            d.text((12,12), "\n".join(all_lines_list_final), font=fnt, fill=(255,255,255))
            image_abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_files',prompt + "_" + commands[command_index].replace("|","_") + '.png' )
            # print(image_abs_path)
            img.save(image_abs_path)
            images_string += '<p><img src="' + image_abs_path + '"></p>'
    return images_string
def generate_images_rlstp(all_lines_list):
    print("Generating RLSTP Images")
    count = 0
    start_line = None
    end_line = None
    for line_index in range(0,len(all_lines_list)):
        # print(all_lines_list[line_index][:-1].strip())
        if all_lines_list[line_index].find('<RLSTP') != -1:
            if count == 0:
                start_line = line_index
            count += 1
        elif all_lines_list[line_index][:-1].strip().find('END') != -1 and \
            all_lines_list[line_index+2][:-1].strip().find('<') != -1 and start_line is not None and count == 3:
            end_line = line_index + 2
    if start_line is None or end_line is None:
        return ""
    print(start_line,end_line)
    number_of_lines = len(all_lines_list[start_line:end_line-1])
    all_lines_list_final = [x[:-1].strip() for x in all_lines_list[start_line:end_line] if x[:-1].strip() != '']
    max_column = [max([len(x) for x in all_lines_list_final])][0]
    fnt = ImageFont.truetype("./ARIAL.TTF", 15)
    img = Image.new('RGB', (max_column * 10, number_of_lines*16), color = (0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((12,12), "\n".join(all_lines_list_final), font=fnt, fill=(255,255,255))
    image_abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_files',  'RLSTP.png' )
    # print(image_abs_path)
    img.save(image_abs_path)
    images_string = '<p><img src="' + image_abs_path + '"></p>'
    return images_string
    # print(count)
    # print(all_lines_list[start_line:])
    # print([x[:-1].strip() for x in all_lines_list[start_line:] if x[:-1].strip() != ''])
image_html_final_string = ""
final_df_list = []
for file1 in glob.glob("./input_files/*.txt"):
    with open(file1,'r') as f:
        print(file1)
        # all_data = f.read()
        all_lines_list = f.readlines()
        images_list = []
        image_html_string = generate_images_output_files(all_lines_list)
        image_html_final_string += image_html_string
        image_html_string1 = generate_images_rlstp(all_lines_list)
        image_html_final_string += image_html_string1
        final_df_list_each_file = create_df(all_lines_list)
        final_df_list.extend(final_df_list_each_file)
# print(final_df_list)
final_html = create_final_html(final_df_list,image_html_final_string)
# print(final_html)

# mail.HTMLBody = '<html><body><br><br>' + \
# images_string + \
# '</body></html>'
# mail.Display(True)