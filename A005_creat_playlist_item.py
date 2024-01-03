import random
import time

#
# # 生成10条数据
# for i in range(20):
#     item_no = i
#     item_data = f"{random.randint(900, 3000)},1,1,\\fs6464 {i+1} "
#     print(f"item{item_no} = {item_data}")


# timelist = []
# for i in range(6):
#     a = random.randint(8, 16)
#     timelist.append(a)
# print(timelist)

# timelist = [15, 13, 16, 9, 16, 8]
# for i in timelist:
#     time.sleep(i)
#     print('打印')


# import time
# from datetime import datetime
#
# def main():
#     res = datetime.now().strftime("%M:%S")
#     print(res)
# res = datetime.now().strftime("%M:%S")
# print(res)
# timelist = [15, 10, 7, 8]
# time.sleep(3)
# res = datetime.now().strftime("%M:%S")
# for i in range(len(timelist)):
#     main()
#     time.sleep(timelist[i])

# timelist = [5, 6, 10, 5]
# [3,8,14,24]



# timelist = ['5', '6', '10', '5']
# timelist = [int(x) for x in timelist]
# jiange = 3
# num = 0
# newlist = [jiange]
# for i in range(len(timelist)-1) :
#     num = newlist[i] + timelist[i]
#     print(num)
#     newlist.append(num)
# print(newlist)

timelist = ['2300', '1700', '1300', '2900','1100']
timelist = [int(x) for x in timelist]
timelist = [x // 100 for x in timelist]
jiange_time = 7
num = 0
newlist = [jiange_time]
for i in range(len(timelist)-1) :
    num = newlist[i] + timelist[i]
    print(num)
    newlist.append(num)
print(newlist)
for i in range(len(newlist)) :
    if i == 0:
        waittime = newlist[i]
    else:
        waittime = newlist[i] - newlist[i-1] - jiange_time
    print(waittime)
    time.sleep(waittime)
    print('取当前显示画面')



# timelist = [5, 6, 10, 5]
# cumulative_times = [sum(timelist[:i+1]) for i in range(len(timelist))]
# print(cumulative_times)




# import time
# # 定义时间表（单位为毫秒）
# time_table = ['2330', '1751', '1322', '2912', '1197', '2412', '1151', '2203', '2040', '1651', '998', '1905', '2363', '1741', '1349', '2644', '2786', '2442', '2251', '1449']
# # 计算每个时间点的累积时间
# cumulative_times = [int(time_table[0])]
# for i in range(1, len(time_table)):
#     cumulative_times.append(cumulative_times[i-1] + int(time_table[i]))
# # 获取当前时间
# start_time = time.time() * 1000  # 将当前时间转换为毫秒
# # 循环执行
# for i in range(len(cumulative_times)):
#     current_time = time.time() * 1000  # 获取当前时间
#     elapsed_time = current_time - start_time  # 计算已经过去的时间
#     if elapsed_time < cumulative_times[i]:  # 判断是否到达指定的时间点
#         time_to_sleep = (cumulative_times[i] - elapsed_time) / 1000  # 计算需要睡眠的时间（转换为秒）
#         time.sleep(time_to_sleep)  # 等待到达指定的时间点
#     print(f"在第{i+1}秒取值")  # 执行相应的操作
