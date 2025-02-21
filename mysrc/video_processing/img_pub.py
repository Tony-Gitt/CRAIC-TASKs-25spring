import rospy
import cv2
import time
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def image_pub():
    rospy.init_node('view_publisher', anonymous=True)
    
    pub = rospy.Publisher("processed_view", Image, queue_size=10)
    bridge = CvBridge()
        
    # cv2读取信息
    cap = cv2.VideoCapture(0,cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    #uvc摄像头需要设置格式
    
    starttime=time.time()
    
    if not cap.isOpened():
        rospy.logerr("无法打开摄像头")
        return
    
    rate = rospy.Rate(30)  # 30 Hz
    i=0
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            rospy.logerr("无法读取摄像头图像")
            rospy.logerr("{},{}".format(ret,frame))
            break
         
        # 处理图像
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_red1 = np.array([0, 120, 70])  
        upper_red1 = np.array([10, 255, 255])  
        lower_red2 = np.array([170, 120, 70])  
        upper_red2 = np.array([180, 255, 255])  

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contour_areas = [(cv2.contourArea(contour), contour) for contour in contours]
        contour_areas.sort(key=lambda x: x[0], reverse=True)
        largest_contour = contour_areas[0][1]

        x, y, w, h = cv2.boundingRect(largest_contour)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"({x}, {y})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        
        # 将处理后的 OpenCV 图像转换为 ROS 图像消息
        try:
            ros_image = bridge.cv2_to_imgmsg(frame, "bgr8")
        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))
            return
        
        # 发布处理后的图像
        i+=1
        pub.publish(ros_image)
        finishtime=time.time()
        rospy.loginfo("图像已发布 目前第 {} 帧 用时 {} s".format(i,finishtime-starttime))
        rate.sleep()
        
    cap.release()


if __name__ == '__main__':
    try:
        image_pub()
    except rospy.ROSInterruptException:
        rospy.logerr("error when publish")
