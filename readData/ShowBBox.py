from readData.ShowData import ShowData

"""
{'license': 3,
 'file_name': '000000391895.jpg',
 'coco_url': 'http://images.cocodataset.org/train2017/000000391895.jpg',
 'height': 360,
 'width': 640,
 'date_captured': '2013-11-14 11:18:45',
 'flickr_url': 'http://farm9.staticflickr.com/8186/8119368305_4e622c8349_z.jpg',
 'id': 391895}

 {'segmentation':[],
  'area': 2765.1486500000005,
 'iscrowd': 0,
 'image_id': 558840,
 'bbox': [199.84, 200.46, 77.71, 70.88],
 'category_id': 58,
 'id': 156}
"""

"""
这里发现annotation可能存在多对1的关系，这里应当解析出image-annotation
可能有些image不存在annotation的情况，此类一共一共1021个样本
"""

from readData.ReadCoCoData import ReadCoCoData
import cv2 as cv


class ShowBBox(ShowData):
    def __init__(self):
        self.path = "../../data"
        self.train_image_id_map = None
        self.test_image_id_map = None
        self.train_annotation_map = None
        self.test_annotation_map = None
        self.category_map = None
        pass

    def showByAnnotation(self, annotation):
        # 获取图片 id、图片的长宽、图片的文件地址
        # 先从 train 取如果没有再从 test 取
        bbox = annotation['bbox']
        image_id = annotation['image_id']
        # 如果是第一次查找，则将 map 缓存起来供下次使用
        if self.train_image_id_map is None:
            self.build_train_image_id_map()
        image = self.train_image_id_map.get(image_id,None)
        path = self.get_path(image, 'train')

        if image is None:
            if self.test_image_id_map is None:
                self.build_test_image_id_map()
            image = self.test_image_id_map.get(image_id,None)
            path = self.get_path(image, 'test')

        # 绘图
        self.draw(image, annotation, path)

    def showByImage(self, image):
        # 解析图片对应的annotation
        annotations ,path= self.getAnnotationsByImage(image)
        # 推断所有的annotation物体及边缘
        # show
        self.draw(image,annotations,path)


    def getImageByAnnotation(self, annotation):
        pass

    def getAnnotationsByImage(self,image):
        """
        根据image获取所有的annotation
        :param image:
        :return:
        """
        image_id = image['id']
        if self.train_annotation_map is None:
            self.build_train_annotation_map()
        annotations = self.train_annotation_map.get(image_id,None)
        path = self.get_path(image, 'train')

        if annotations is None:
            if self.test_annotation_map is None:
                self.build_test_annotation_map()

            annotations = self.test_annotation_map.get(image_id,None)
            path = self.get_path(image, 'test')
        return annotations,path


    def build_annotation_map(self,type = "train"):
        readData = ReadCoCoData()
        images, annotations, categories = readData.read_data(type)
        d = dict()
        for annotation in annotations:
            l = d.get(annotation['image_id'],[])
            l.append(annotation)
            d[annotation['image_id']] = l

        return d

    def build_train_annotation_map(self):
        self.train_annotation_map = self.build_annotation_map()

    def build_test_annotation_map(self):
        self.test_annotation_map = self.build_annotation_map("test")

    def getAnnotationsByImageId(self, imageId):
        pass

    def getAnnotationsByImageName(self, imageName):
        pass

    def build_test_image_id_map(self):
        """
            创建 test 的 map 关系
        """
        self.test_image_id_map = self.build_map('test')

    def build_train_image_id_map(self):
        """
            创建 train 的 map 关系
        """
        self.train_image_id_map = self.build_map()

    def draw(self, image, annotations, path):
        if type(annotations) == dict:
            annotations = [annotations]

        cateName = ""
        img = cv.imread(path, cv.IMREAD_COLOR)
        for annotation in annotations:
            left_top = (int(annotation['bbox'][0]), int(annotation['bbox'][1]))
            right_bottom = (
            int(annotation['bbox'][0] + annotation['bbox'][2]), int(annotation['bbox'][1] + annotation['bbox'][3]))
            img = cv.rectangle(img, left_top, right_bottom, (0, 255, 0), 2)
            cateName += (self.get_category(annotation) + "-")

        cv.imshow('img' + str(image['id']) + "-" + cateName, img)
        cv.waitKey(10000)
        cv.destroyAllWindows()

    def build_map(self, type="train"):
        """
            :return map
        """
        readData = ReadCoCoData()
        images, annotations, categories = readData.read_data(type)
        d = dict()
        for image in images:
            d[image['id']] = image
        return d

    def get_path(self, image, type='train'):
        # 根据类型获取图片路径
        l = len('000000391895')
        path = self.path + "/" + type + "2017/" + '0' * (l - len(str(image['id']))) + str(image['id']) + ".jpg"
        return path

    def get_category(self, annotation):
        # 获取类目
        category_id = annotation['category_id']
        if self.category_map is None:
            self.build_category_map()
        category_name = self.category_map[category_id]['name']
        return category_name

    def build_category_map(self,type = "train"):
        readData = ReadCoCoData()
        images, annotations, categories = readData.read_data(type)
        d = dict()
        for cate in categories:
            d[cate['id']] = cate

        self.category_map = d
        return d

if __name__ == "__main__":
    annotation =  {'segmentation':[],
                  'area': 2765.1486500000005,
                 'iscrowd': 0,
                 'image_id': 558840,
                 'bbox': [199.84, 200.46, 77.71, 70.88],
                 'category_id': 58,
                 'id': 156}

    image = {'license': 3,
             'file_name': '000000391895.jpg',
             'coco_url': 'http://images.cocodataset.org/train2017/000000391895.jpg',
             'height': 360,
             'width': 640,
             'date_captured': '2013-11-14 11:18:45',
             'flickr_url': 'http://farm9.staticflickr.com/8186/8119368305_4e622c8349_z.jpg',
             'id': 391895}
    show = ShowBBox()
    show.showByAnnotation(annotation)
    show.showByImage(image)