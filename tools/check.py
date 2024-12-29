import cv2
import json
import os

dir = "./mk2"        # jpg和json位置文件夹
bbox_color = (255, 0, 255)

def draw_label_type(draw_img, bbox, label, label_color, thickness):
    labelSize = cv2.getTextSize(label + '0', cv2.FONT_HERSHEY_SIMPLEX, 1.5, 10)[0]
    if bbox[1] - labelSize[1] - 11 < 0:
        cv2.rectangle(draw_img,
                      (bbox[0], bbox[1] + 2),
                      (bbox[0] + labelSize[0], bbox[1] + labelSize[1] + 3),
                      color=label_color,
                      thickness=-1
                      )
        cv2.putText(draw_img, label,
                    (bbox[0], bbox[1] + labelSize[1] + 3),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (255, 255, 255),
                    thickness=2
                    )
    else:
        cv2.rectangle(draw_img,
                      (bbox[0], bbox[1] - labelSize[1] - 3),
                      (bbox[0] + labelSize[0], bbox[1] - 3),
                      color=label_color,
                      thickness=-1
                      )
        cv2.putText(draw_img, label,
                    (bbox[0], bbox[1] - 3),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (255, 255, 255),
                    thickness=2
                    )

img_files = sorted([file for file in os.listdir(dir) if file.endswith((".jpg", ".JPG", ".png"))])

cv2.namedWindow("img", cv2.WINDOW_NORMAL)

for i, img_name in enumerate(img_files):
    print(f"{i} / {len(img_files)}")
    print(img_name)

    js_name = img_name.split('.')[0] + '.json'
    img = cv2.imread(os.path.join(dir, img_name))
    with open(os.path.join(dir, js_name), 'r') as f_json:
        js_file = json.load(f_json)
    line_thickness = js_file['imageHeight'] // 250
    print(len(js_file['shapes']))

    for shape in js_file['shapes']:
        label = shape['label']
        tl, rb = tuple(map(int, shape['points'][0])), tuple(map(int, shape['points'][2]))
        cv2.rectangle(img, tl, rb, color=bbox_color, thickness=line_thickness)
        draw_label_type(img, tl, label, bbox_color, thickness=line_thickness)
    
    cv2.imshow("img", img)

    key = cv2.waitKey()
    if key == ord('f'):  # 按 'f' 键标记为不合格
        cv2.imwrite(f"./pass/{img_name}", img)
        print(f"pass {img_name}")
            

