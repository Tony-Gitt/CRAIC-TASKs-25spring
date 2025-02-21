import cv2
from ultralytics import YOLO

model = YOLO('yolov8s-face-lindevs.pt')

image_path = "..\src\image.png"
image = cv2.imread(image_path)

if image is None:
    print("Error: Could not load image.")


results = model(image)

for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0]) 
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

output_path = "..\src\out.jpg"
cv2.imwrite(output_path, image)
#cv2.imshow("Face Detection", image) 

cv2.waitKey(0)
cv2.destroyAllWindows()