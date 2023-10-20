# with open('./123.txt','r',encoding = 'gbk') as f:
#     a = f.readlines()
#     print(a)
# -*- coding: 编码 -*-
import re


# 打开原始文件和新文件
with open('123.txt', 'r',encoding = 'utf-8') as file:
    with open('output.txt', 'w') as new_file:
        # 逐行读取原始文件内容
        for line in file:
            print(line.title())
            new_file.write(line)

# 关闭文件
file.close()
new_file.close()
