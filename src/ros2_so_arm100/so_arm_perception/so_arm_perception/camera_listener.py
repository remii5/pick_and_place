import rclpy
import cv2 as cv

from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self.bridge = CvBridge()
        self.saved = False
        self.colors = {'red': [((0, 50, 50), (20, 255, 255)), ((170, 50, 50), (180, 255, 255)),], 'blue': [((90, 50, 50), (120, 255, 255))], 'green': [((30, 50, 50), (70, 255, 255))]}
        self.subscription = self.create_subscription(Image, '/camera/image', self.listener_callback, 10)
        # prevent unused variable warning
        self.subscription

    def listener_callback(self, msg):
        im = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        
        im_HSV = cv.cvtColor(im, cv.COLOR_BGR2HSV)
        color_masks = {}

        #contours_pos: (key = color cube, value = an array of (x,y) tuples)
        contours_pos = {}
        for key in self.colors:
            if key == 'red':
                mask1 = cv.inRange(im_HSV, self.colors[key][0][0], self.colors[key][0][1])
                mask2 = cv.inRange(im_HSV, self.colors[key][1][0], self.colors[key][1][1])
                final_mask = cv.bitwise_or(mask1, mask2)
                color_masks[key] = final_mask
            else:
                final_mask = cv.inRange(im_HSV, self.colors[key][0][0], self.colors[key][0][1])
                color_masks[key] = final_mask

        #min_area =  (approx)(real_cube_size_m * camera_focal_len_px) / some distance d
        min_area = 500
        for key in color_masks:
            contours, _ = cv.findContours(color_masks[key], cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            for i in range(0, len(contours)):
                cnt = contours[i]
                if cv.contourArea(cnt) > min_area:
                    #only save pos from valid cnt
                    M = cv.moments(cnt)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    cube_pos = (cx, cy)
                    contours_pos.setdefault(key, [])
                    contours_pos[key].append(cube_pos)

        
        if not self.saved:
            cv.imwrite("learning.png", im)
            for key in color_masks:
                cv.imwrite(f"mask_{key}.png", color_masks[key])
            self.saved = True

        
        self.get_logger().info(f'Hearing: height: "{msg.height}",  width: "{msg.width}", type:  "{msg.encoding}"')

        for key in contours_pos:
            for i, (cx, cy) in enumerate(contours_pos[key]):
                self.get_logger().info(f'{key} cube {i}: cx={cx},  cy={cy}')

def main(args=None):
    rclpy.init(args=args)

    camera_subscriber = CameraSubscriber()
    rclpy.spin(camera_subscriber)
    camera_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()