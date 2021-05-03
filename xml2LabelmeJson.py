### xml to csv
import cv2
import os
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import json
import base64

def xml2csv(xml_path):
   
    print("xml to csv {}".format(xml_path))
    xml_list = []
    xml_df=pd.DataFrame()
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
            column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
            xml_df = pd.DataFrame(xml_list, columns=column_name)
    except Exception as e:
        print('xml conversion failed:{}'.format(e))
        return pd.DataFrame(columns=['filename,width,height','class','xmin','ymin','xmax','ymax'])
    return xml_df



def xml2Labelme(xml_path):
    xml_csv=xml2csv(xml_path)
    xml_csv['min']= xml_csv[['xmin','ymin']].values.tolist()
    xml_csv['max']= xml_csv[['xmax','ymax']].values.tolist()
    xml_csv['points']= xml_csv[['min','max']].values.tolist()
    xml_csv['shape_type']='rectangle'
    xml_csv['group_id']=None
    xml_csv.rename(columns = {'class':'label','filename':'imagePath','height':'imageHeight','width':'imageWidth'},inplace=True)


    version = '4.5.7'
    shapes = xml_csv[['label','points','group_id','shape_type']].to_dict('records')
    flags = {}
    imagePath = xml_csv['imagePath'][0]
    imageHeight = xml_csv['imageHeight'][0]
    imageWidth = xml_csv['imageWidth'][0]
    encoded = base64.b64encode(open(xml_csv['imagePath'][0], "rb").read())
    imageData = str(encoded)[1:]

    data = dict(
            version=version,
            flags=flags,
            shapes=shapes,
            imagePath=imagePath,
            imageData=imageData,
            imageHeight=int(imageHeight),
            imageWidth=int(imageWidth),
           )
    filename = xml_path[:-3]+'json'
    try:
        with open('./json/'+filename, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print('xml to json {}'.format(filename))
    except Exception as e:
        raise print(e)

        
        
        
xml_list = []

try:
    os.mkdir('./json')
except:
    pass


for i in os.listdir():
    if i[-3:] == 'xml':
        xml_list.append(i)
        
for i in xml_list:
    xml2Labelme(i)