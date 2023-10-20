import time
import retrying
import pandas as pd
from upload_00playlst import Upload

# 读取Excel文件
df = pd.read_excel('./data/test.xlsx')

# while True:
for index, row in df.iterrows() :
    playlst = row[0]
    Upload(ip = '192.168.210.88', port = 5009).upload(document_url = playlst, document_name = 'play00.lst')
    time.sleep(5)
df.close()



# 福建匝道生成循环文件
# df = pd.read_excel('./data/V01.xlsx')
# while True:
# for index, row in df.iterrows() :
#     num = row[0]
#     num_100 = int(num) + 100
#     miaoshu = row[1]
#     shijian = row[2]
#     playlst = row[3]
#     plsthex = Upload(ip = '192.168.210.88', port = 5009).upload(document_url = playlst, document_name = 'play00.lst')
#     time.sleep(4)
#     print(num)
#     with open('a.txt', 'a') as f :
#         f.write('N{0}={1},{2},{3}\nN{1}=H,{4}\n\n'.format(num_100,num,miaoshu,shijian,plsthex))

