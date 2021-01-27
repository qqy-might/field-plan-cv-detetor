import json
import os

from readData.ReadData import ReadData


class ReadCoCoData(ReadData):

    def __init__(self):
        self.path = "../../data"
        self.train_image_path = self.path + "/train2017"
        self.val_image_path = self.path + "/train2017"
        self.test_image_path = self.path + "/train2017"
        self.train_annotation_path = self.path + "/annotations/instances_train2017.json"
        self.val_annotation_path = self.path + "/annotations/instances_val2017.json"

    def read_data(self, type=None):
        """
            读取 cocodata for 图像检测
        :param
        """
        if type is None or type != 'test':
            path = self.train_annotation_path
        else:
            path = self.test_annotation_path
        return self.load_json(path)

    def load_json(self, path):
        """
            解析 train 的 json 文件
            :returns images、annotations、categories
        """
        val_file = os.path.join(path)
        coco_dict = self.read_file_utf8(val_file)
        print('Keys: {}'.format(coco_dict.keys()))

        info = coco_dict['info']
        licenses = coco_dict['licenses']
        images = coco_dict['images']
        annotations = coco_dict['annotations']
        categories = coco_dict['categories']

        print('-' * 50)
        print('[Info] info: {}'.format(info))  # 信息
        print('-' * 50)
        print('[Info] licenses: {}'.format(licenses))  # 8个licenses
        print('-' * 50)
        print('[Info] 图片数: {}'.format(len(images)))  # 图片数
        print('[Info] 图片: {}'.format(images[0]))  # 图片数
        print('-' * 50)
        print('[Info] 标注数: {}'.format(len(annotations)))  # 标注
        print('[Info] 标注: {}'.format(annotations[0]))  # 标注
        print('-' * 50)
        print('[Info] 类别数: {}'.format(len(categories)))  # 类别
        print('[Info] 类别: {}'.format(categories[0]))  # 类别

        return images, annotations, categories

    def read_file_utf8(self, path):
        """:param json 文件地址
            读取 json
        """
        with open(path, 'r') as f:
            text = json.load(f)

        return text


if __name__ == "__main__":
    readData = ReadCoCoData()
    images, annotations, categories = readData.read_data()
    print("len(annotations) = ", len(annotations))
