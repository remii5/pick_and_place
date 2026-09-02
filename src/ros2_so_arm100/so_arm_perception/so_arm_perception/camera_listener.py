import rclpy
import cv2 as cv

from rclpy.node import Node
from cv_bridge import CvBridge
from std_msgs.msg import Header
from sensor_msgs.msg import Image

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self.bridge = CvBridge()
        self.saved = False
        self.subscription = self.create_subscription(Image, '/camera/image', self.listener_callback, 10)
        # prevent unused variable warning
        self.subscription

    def listener_callback(self, msg):
        im = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        
        im_HSV = cv.cvtColor(im, cv.COLOR_BGR2HSV)
        im_thresh = cv.inRange(im_HSV, (0, 0, 0), (20, 255, 255))
        im_thresh = cv.bitwise_and(im_HSV, im_HSV, mask=im_thresh)

        if not self.saved:
            cv.imwrite("learning.png", im)
            cv.imwrite("threshold.png", im_thresh)
            self.saved = True

        self.get_logger().info(f'Hearing: height: "{msg.height}",  width: "{msg.width}", type:  "{msg.encoding}"')

def main(args=None):
    rclpy.init(args=args)

    camera_subscriber = CameraSubscriber()
    rclpy.spin(camera_subscriber)
    camera_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()