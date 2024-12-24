# ExDark数据集转化为YOLO格式
import os, sys
from PIL import Image
import argparse
import shutil
import utils.util as utils

labels = ['Bicycle', 'Boat', 'Bottle', 'Bus', 'Car', 'Cat', 'Chair', 'Cup', 'Dog', 'Motorbike', 'People', 'Table']


def ExDark2Yolo(txts_dir: str, imgs_dir: str, ratio: str, version: int, output_dir: str):
    ratios = ratio.split(':')
    ratio_train, ratio_test, ratio_val = int(ratios[0]), int(ratios[1]), int(ratios[2])
    ratio_sum = ratio_train + ratio_test + ratio_val
    dataset_perc = {'train': ratio_train / ratio_sum, 'test': ratio_test / ratio_sum, 'val': ratio_val / ratio_sum}

    for t in dataset_perc:
        os.makedirs('/'.join([output_dir, 'images', t]))
        os.makedirs('/'.join([output_dir, 'labels', t]))

    for label in labels:
        print('Processing {}...'.format(label))
        filenames = os.listdir('/'.join([txts_dir, label]))
        cur_idx = 0
        files_num = len(filenames)

        for filename in filenames:
            cur_idx += 1
            filename_no_ext = '.'.join(filename.split('.')[:-2])
            if cur_idx < dataset_perc.get('train') * files_num:
                set_type = 'train'
            elif cur_idx < (dataset_perc.get('train') + dataset_perc.get('test')) * files_num:
                set_type = 'test'
            else:
                set_type = 'val'
            output_label_path = '/'.join([output_dir, 'labels', set_type, filename_no_ext + '.txt'])
            yolo_output_file = open(output_label_path, 'a')

            name_split = filename.split('.')
            img_path = '/'.join([imgs_dir, label, '.'.join(filename.split('.')[:-1])])
            try:
                img = Image.open(img_path)
            except FileNotFoundError:
                img_path = '/'.join([imgs_dir, label, ''.join(name_split[:-2]) + '.' + name_split[-2].upper()])
                img = Image.open(img_path)

            output_img_path = '/'.join([output_dir, 'images', set_type])
            shutil.copy(img_path, output_img_path)

            width, height = img.size
            txt = open('/'.join([txts_dir, label, filename]), 'r')
            txt.readline()  # ignore first line
            line = txt.readline()

            while line != '':
                datas = line.strip().split()
                class_idx = labels.index(datas[0])
                x0, y0, w0, h0 = int(datas[1]), int(datas[2]), int(datas[3]), int(datas[4])
                if version >= 5:
                    x = (x0 + w0/2) / width
                    y = (y0 + h0/2) / height
                elif version == 3:
                    x = x0 / width
                    y = y0 / height
                else:
                    print("Version of YOLO error.")
                    return
                w = w0 / width
                h = h0 / height

                yolo_output_file.write(' '.join([str(class_idx),
                                                 format(x, '.6f'),
                                                 format(y, '.6f'),
                                                 format(w, '.6f'),
                                                 format(h, '.6f'),
                                                 ]) + '\n')
                line = txt.readline()

            yolo_output_file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@', conflict_handler='resolve')
    parser.convert_arg_line_to_args = utils.convert_arg_line_to_args

    parser.add_argument('--anndir', type=str, default='/home/fyh/data/ExDark/Annnotations', help="ExDark annotations directory.")         #ExDark的标注目录
    parser.add_argument('--imgdir', type=str, default='/home/fyh/data/ExDark/Images', help="ExDark images directory.")                   #ExDark的图像目录
    parser.add_argument('--ratio', type=str, default='8:1:1', help="Ratio between train/test/val, default 8:1:1.")     #train/test/val之间的比例，默认为8:1:1
    parser.add_argument('--version', type=int, default=11, help="Version of YOLO")
    parser.add_argument('--output_dir', type=str, default="output", help="Images and converted YOLO annotations output directory.")#图像和转换后的yolo标注的输出目录
    
    if sys.argv.__len__() == 2:
        arg_filename_with_prefix = '@' + sys.argv[1]
        args = parser.parse_args([arg_filename_with_prefix])
    else:
        args = parser.parse_args()

    ExDark2Yolo(args.anndir, args.imgdir, args.ratio, args.version, args.output_dir)

    # anndir = "/home/fyh/data/ExDark/Annnotations"
    # imgdir = "/home/fyh/data/ExDark/Images"
    # ratio = "8:1:1"
    # output_dir = "./"
    # version = 5
    # ExDark2Yolo(anndir, imgdir, ratio, version, output_dir)

