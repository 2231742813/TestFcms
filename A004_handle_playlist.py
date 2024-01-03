import re
import time


def handle_playlist(playlist):
    if playlist:
        pattern = r'item\d+\s*=\s*(\d+)'
        matches = re.findall(pattern, playlist)
        return matches
    else:
        print('播放表正则表达式匹配异常')
        return [1]

# if __name__ == '__main__':
#     # res = handle_playlist(playlist = testlist)
#     # 读播放表 是个列表
#     from read_yaml import Read_CSV
#     playlists = Read_CSV().Playlist_csv('x91_fcms - 副本.csv')
#     for i in playlists:
#         print(i[4])
#         res = handle_playlist(playlist = i[4])
#         print(res)
#         print(len(res))

