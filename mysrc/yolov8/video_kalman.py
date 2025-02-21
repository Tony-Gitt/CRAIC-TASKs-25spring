import cv2
import numpy as np
from ultralytics import YOLO
import time
from tqdm import tqdm

# 初始化Kalman滤波器
def init_kalman_filter(measurement):
    kf = cv2.KalmanFilter(4, 2)
    kf.measurementMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0]], np.float32)
    kf.transitionMatrix = np.array([[1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], np.float32)
    kf.processNoiseCov = np.array([[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]], np.float32) * 0.03
    kf.statePost=measurement
    kf.predict()
    return kf

def iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union= box1_area + box2_area - inter
    iou = inter / union
    return iou

def des(box1, box2):
    x1=(box1[0]+box1[2])//2
    y1=(box1[1]+box1[3])//2
    x2=(box2[0]+box2[2])//2
    y2=(box2[1]+box2[3])//2
    des=(x1-x2)**2+(y1-y2)**2
    return des


video_path = "..\src1"  
out_path="..\output"
video_name="\jljt.mp4"
video_input=video_path+video_name
cap = cv2.VideoCapture(video_input)


if not cap.isOpened():
    print("Error: Could not open video.")
    exit()
else:
    starttime=time.time()

model = YOLO('yolov8s-face-lindevs.pt')


output_path = out_path+video_name
fps = cap.get(cv2.CAP_PROP_FPS)
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


with tqdm(total=total_frames, desc="Processing Video") as pbar:
    face_kalman_filters = {}
    filter_count=0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, verbose=False,iou=0.01)
        detected_faces = {}
        delete=[]
        face_id=0
        print(face_kalman_filters)
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                x=(x1+x2)//2
                y=(y1+y2)//2
                detected_faces[face_id]=(x1,y1,x2,y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"({x}, {y},{face_id})", (x,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                face_id+=1
                
        for face_id, kf_list in list(face_kalman_filters.items()):
            kf, prev_box,count,trigger = kf_list["kf"], kf_list["box"], kf_list["count"], kf_list["trigger"]
            matched = False
            for id, box in detected_faces.items():
                if trigger & (iou(prev_box,box)>0 | des(prev_box,box)<20000):
                    del face_kalman_filters[face_id]
                    matched=True
                    break
                if iou(prev_box, box) > 0:
                    # 如果重合率较高，则认为是同一目标
                    matched = True
                    x = (box[0] + box[2]) // 2
                    y = (box[1] + box[3]) // 2
                    measure = np.array([[x], [y]], np.float32)
                    kf.correct(measure)
                    face_kalman_filters[face_id]={"kf": kf, "box": prev_box, "count": count+1, "trigger":0}
                    delete.append(id)  
                    break
                
            if not matched:
                if count >= 12:
                    prediction = kf.predict()
                    cv2.putText(frame, f"prediction:{prediction}", (prev_box[0],prev_box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    x, y = int(prediction[0].item()), int(prediction[1].item())
                    dx=(prev_box[2]-prev_box[0])//2
                    dy=(prev_box[3]-prev_box[1])//2
                    cv2.rectangle(frame, (x-dx, y-dy), (x+dx, y+dy), (0, 0, 255), 2)
                    face_kalman_filters[face_id]={"kf": kf, "box": [x-dx, y-dy, x+dx, y+dy], "count": count, "trigger":1}
                    cv2.putText(frame, f"({x}, {y},{face_id})", (x,y+dy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else:
                    del face_kalman_filters[face_id]
                    
        for id in delete :
            if id not in detected_faces:
                continue
            del detected_faces[id]

        # 初始化新的卡尔曼滤波器
        for face_id, box in detected_faces.items():
            x = (box[0] + box[2]) // 2
            y = (box[1] + box[3]) // 2
            measurement = np.array([[x], [y]], np.float32)
            kf = init_kalman_filter(np.array([[x],[y],[0],[0]],np.float32))
            kf.correct(measurement)
            face_kalman_filters[filter_count] = {"kf": kf, "box": box, "count": 1, "trigger":0}
            filter_count+=1
            
        out.write(frame)  
        pbar.update(1)

endtime=time.time()
cap.release()
out.release()
print('cost ',endtime-starttime,'s')



        
