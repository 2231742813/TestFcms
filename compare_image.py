from PIL import Image
from PIL import ImageChops
from Set_log import logger
from datetime import datetime
import shutil


class CompareImage:
    # 对比图片
    @staticmethod
    def compare_image(path_one, path_two, image_id):
        image_one = Image.open(path_one)
        image_two = Image.open(path_two)
        try:
            diff = ImageChops.difference(image_one, image_two)

            if diff.getbbox() is None:
                # 图片间没有任何不同则直接退出
                logger.info('{0} {1}图片对比  成功'.format(image_one, image_two))
                return 1
            else:
                logger.error('{0} {1}图片对比  失败'.format(image_one, image_two))
                imgA = Image.open(path_one)
                imgB = Image.open(path_two)
                width, height = imgA.size
                for x in range(0, width):
                    for y in range(0, height):
                        color1 = imgA.getpixel((x, y))
                        color2 = imgB.getpixel((x, y))
                        if color1 == color2:
                            imgA.putpixel((x, y), (255, 255, 255))
                        else:
                            imgA.putpixel((x, y), (0, 0, 0))

                error_url = ""
                for i in range(min(len(path_one), len(path_two))) :
                    if path_one[i] == path_two[i] :
                        error_url += path_one[i]
                    else :
                        break
                nowtime = datetime.now().strftime("%Y%m%d%H%M%S")
                error_pic_url = error_url + 'Now/different_bak/{0}_{1}.bmp'.format(image_id,nowtime)
                # print(error_pic_url)
                imgA.save(error_pic_url)
                error_picbak_url = error_url + 'Now/different_bak/{0}_{1}_O.bmp'.format(image_id, nowtime)
                # print(path_two)
                # print(error_picbak_url)
                shutil.copy(path_two, error_picbak_url)
                return 0
        except Exception as e:
            logger.error(e)
            logger.error("{0} {1}".format(e, "图片大小和box对应的宽度不一致!"))
            return 0


# if __name__ == "__main__":
#     contrast_result = CompareImage().compare_image('picture/X70/2/512 384/1.bmp','picture/X70/2/512 384/Now/1.bmp',1)
#     if contrast_result:
#         print('图片对比通过')
#     else:
#         print('shibai')