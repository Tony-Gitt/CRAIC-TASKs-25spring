import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def image_callback(msg):

    bridge = CvBridge()
    
    try:
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
        rospy.logerr("CvBridge Error: {0}".format(e))
        return
    
    # 显示图像
    # cv2.imshow("Processed Image", cv_image)
    # cv2.waitKey(33)

def image_sub():
    rospy.init_node('view_subscriber', anonymous=True)
    rospy.Subscriber("processed_view", Image, image_callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        image_sub()
    except rospy.ROSInterruptException:
        rospy.logerr("error when subscribe")