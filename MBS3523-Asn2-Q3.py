import cv2
import numpy as np

confThreshold = 0.8

fruit_prices = {
    'apple': 1.00,
    'banana': 0.50,
    'orange': 2.00
}

img = cv2.imread('testabo10.jpg')


height, width, _ = img.shape

classesFile = 'coco80.names'
classes = []
with open(classesFile, 'r') as f:
    classes = f.read().splitlines()

net = cv2.dnn.readNetFromDarknet('yolov3-608.cfg', 'yolov3-608.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

blob = cv2.dnn.blobFromImage(img, 1/255, (320, 320), (0, 0, 0), swapRB=True, crop=False)
net.setInput(blob)
output_layers_names = net.getUnconnectedOutLayersNames()
LayerOutputs = net.forward(output_layers_names)

bboxes = []
confidences = []
class_ids = []

for output in LayerOutputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > confThreshold and classes[class_id] in fruit_prices:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w/2)
            y = int(center_y - h/2)

            bboxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

indexes = cv2.dnn.NMSBoxes(bboxes, confidences, confThreshold, 0.4)

font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(len(bboxes), 3))

fruit_counts = {fruit: 0 for fruit in fruit_prices}
total_price = 0.0

if len(indexes) > 0:
    for i in indexes.flatten():
        x, y, w, h = bboxes[i]
        label = classes[class_ids[i]]

        if label in fruit_prices:
            confidence = str(round(confidences[i], 2))
            color = colors[i]

            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, f"{label} {confidence}", (x, y + 20), font, 1, (255, 0, 0), 2)

            fruit_counts[label] += 1
            total_price += fruit_prices[label]

total_fruits = sum(fruit_counts.values())
price_text = f"Total: {total_fruits} fruits, ${total_price:.2f}"
cv2.putText(img, price_text, (width - 400, 30), font, 1.5, (0, 255, 0), 2)

y_offset = 60
for fruit, count in fruit_counts.items():
    if count > 0:
        cv2.putText(img, f"{fruit}: {count}", (width - 400, y_offset), font, 1, (0, 255, 0), 2)
        y_offset += 30

output_path = 'detected_fruits.jpg'
cv2.imwrite(output_path, img)
print(f"Result saved to {output_path}")

cv2.imshow('Fruit Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()