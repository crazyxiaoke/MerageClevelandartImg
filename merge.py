#!/usr/bin/python3
# -*-coding:utf-8-*-

import os
from PIL import Image


# 横向合并
def mergei(files, output_file):
    img = Image.open(files[0])
    h = img.size[1]
    totalSize = get_total_row_size(files)
    merge_img = Image.new('RGB', (totalSize, h), 0xffffff)
    x = 0
    for f in files:
        img = Image.open(f)
        merge_img.paste(img, (x, 0))
        x += img.size[0]
    merge_img.save(output_file)
    return output_file


# 纵向合并
def mergej(files, output_file):
    img = Image.open(files[0])
    w = img.size[0]
    totalSize = get_total_cos_size(files)
    merge_img = Image.new('RGB', (w, totalSize), 0xffffff)
    y = 0
    for f in files:
        img = Image.open(f)
        merge_img.paste(img, (0, y))
        y += img.size[1]
    merge_img.save(output_file)
    return output_file


# 获取横向总的宽度
def get_total_row_size(files):
    w = 0
    for f in files:
        img = Image.open(f)
        w += img.size[0]
    return w


# 获取纵向总的高度
def get_total_cos_size(files):
    h = 0
    for f in files:
        img = Image.open(f)
        h += img.size[1]
    return h


# 获取目录下所有文件
def get_total_file(dir):
    list_name = []
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if '-' in file_path:
            list_name.append(file_path)
    return list_name


# 排序文件目录
def sort_files(list_file):
    list_name = sorted(list_file, key=lambda s: (int(s.replace('.jpg', '').split('-')[1]), int(s.replace('.jpg', '').split('-')[2])))
    list_parent = []
    list_child = []
    i = 0
    for file_path in list_name:
        if int(file_path.replace('.jpg', '').split('-')[1]) != i:
            i = int(file_path.replace('.jpg', '').split('-')[1])
            list_parent.append(list_child)
            list_child = []
            list_child.append(file_path)
        else:
            list_child.append(file_path)
    list_parent.append(list_child)
    return list_parent


# 删除临时文件
def del_temp(list_file):
    for filepath in list_file:
        os.remove(filepath)


# 删除下载文件
def del_download_temp(list_file):
    for files in list_file:
        for file in files:
            os.remove(file)


def merge(dir_path, output_file, callback):
    list_name = get_total_file(dir_path)
    list_name = sort_files(list_name)
    # 纵向合并后文件集
    x_outputs = []
    i = 0
    # 先纵向合并，然后再把合并好的图片做横向合并
    for xnames in list_name:
        x_outputs.append(mergej(xnames, dir_path + "/temp{0}.jpg".format(i)))
        i += 1
    # 横向合并
    mergei(x_outputs, "{0}/{1}".format(dir_path, output_file))
    # 合并完成后删除临时文件
    del_download_temp(list_name)
    del_temp(x_outputs)
    if callback:
        callback(1, '删除临时文件')
        callback(1, '合并完成')
        callback(1, '完成')
        callback(0, '')


if __name__ == '__main__':
    merge('10', '完整版.jpg', None)
