import xml.etree.ElementTree as ET
import numpy as np
import os

if __name__ == '__main__':
    xmlfilepath = r'E:\PycharmProjects\yolov5_7.0_cl\data\Annotations'  # xml文件存放地址
    classes = []
    for i in os.listdir(xmlfilepath):
        in_file = open(xmlfilepath + '/' + i)
        tree = ET.parse(in_file)
        root = tree.getroot()
        for obj in root.iter('object'):
            cls = obj.find('name').text
            classes.append(cls)
    print("总类别数:{}".format(len(np.unique(classes))))
    print(np.unique(classes))
