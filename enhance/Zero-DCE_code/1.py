import cv2
import numpy as np


# 加载YOLO模型
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]


def preprocess_image(image):
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    return blob


def detect_objects(net, blob, image):
    net.setInput(blob)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(output_layers)
    return outputs


def parse_detections(outputs, image, confidence_threshold=0.5, nms_threshold=0.4):
    height, width, channels = image.shape
    class_ids = []
    confidences = []
    boxes = []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)
    return boxes, confidences, class_ids, indices


def draw_detections(image, boxes, confidences, class_ids, indices, classes):
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    for i in indices:
        i = i[0]
        box = boxes[i]
        x, y, w, h = box
        label = str(classes[class_ids[i]])
        confidence = confidences[i]
        color = colors[class_ids[i]]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(image, f"{label}: {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return image


def main():
    image = cv2.imread("your_image.jpg")
    blob = preprocess_image(image)
    outputs = detect_objects(net, blob, image)
    boxes, confidences, class_ids, indices = parse_detections(outputs, image)
    result_image = draw_detections(image, boxes, confidences, class_ids, indices, classes)
    cv2.imshow("YOLO Detection", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()