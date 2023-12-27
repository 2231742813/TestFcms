from PIL import Image
from PIL import ImageChops
from Set_log import logger


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
                imgA.save('{0}/different-{1}.bmp'.format(path_two,image_id))
                return 0

        except Exception as e:
            logger.error(e)
            logger.error("{0} {1}".format(e, "图片大小和box对应的宽度不一致!"))
            return 0

#

# if __name__ == "__main__":
#     a = CompareImage().compare_image('./picture/test/16.bmp','./picture/2/16.bmp',16)
#     print(a)
