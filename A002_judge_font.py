from PIL import ImageFont

# 要判断的文字
character_to_check = "as"

# 加载字体文件
font_path = "./font/HWYGWDE.TTF"  # 替换为实际的字体文件路径
font_size = 64  # 字体大小
font = ImageFont.truetype(font_path, font_size)

# 判断文字是否存在
if font.getbbox(character_to_check):
    print(f"字符 '{character_to_check}' 在字体库")
else:
    print(f"字符 '{character_to_check}' 不在字体库")

print(character_to_check.encode('utf-8'))
print(character_to_check.encode('gbk'))
print(character_to_check.encode('ascii'))

print(character_to_check.encode('utf-8').hex())
print(character_to_check.encode('gbk').hex())
print(character_to_check.encode('ascii').hex())
