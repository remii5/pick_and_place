import os

import rclpy
import cv2 as cv
from message_filters import Subscriber, ApproximateTimeSynchronizer

from rclpy.node import Node
import rclpy.time
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, PointCloud2
from sensor_msgs_py import point_cloud2

import tf2_geometry_msgs
from geometry_msgs.msg import PointStamped
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from tf2_ros import LookupException, ExtrapolationException

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self.bridge = CvBridge()

        self.colors = {'red': [((0, 50, 50), (20, 255, 255)), ((170, 50, 50), (180, 255, 255)),], 'blue': [((90, 50, 50), (120, 255, 255))], 'green': [((30, 50, 50), (70, 255, 255))]}
        self.saved = False

        self.output_dir = os.path.expanduser("~/Projects/so-arm/vision_results")

        self.im_sub = Subscriber(self, Image, 'camera/image')
        self.pt_sub = Subscriber(self, PointCloud2, 'camera/points')

        self.sync = ApproximateTimeSynchronizer([self.im_sub, self.pt_sub], queue_size = 10, slop = 0.1)
        self.sync.registerCallback(self.sync_callback)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def sync_callback(self, im_msg, pc_msg):
        im = self.bridge.imgmsg_to_cv2(im_msg, desired_encoding="bgr8")
        
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
        min_area = 300
        #dict list of 2d points for all cubes keyed by color
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
            cv.imwrite(os.path.join(self.output_dir, "learning.png"), im)
            for key in color_masks:
                cv.imwrite(os.path.join(self.output_dir, f"mask_{key}.png"), color_masks[key])
            self.saved = True
            self.get_logger().info(f'Hearing: height: "{im_msg.height}",  width: "{im_msg.width}", type:  "{im_msg.encoding}"')

        #dict list of 3d coordinates, keyed by color
        pc_pos = {}

        #transform pc_pos into base_link
        base_frame_pos = {}

        uv_list = []
        lookup = []

        for key in contours_pos:
            for i, (cx, cy) in enumerate(contours_pos[key]):
                self.get_logger().info(f'{key} cube {i}: cx={cx},  cy={cy}')
                uv_list.append(cy * pc_msg.width + cx)
                lookup.append((key, i))
                
        points = list(point_cloud2.read_points(pc_msg, field_names=("x", "y", "z"), skip_nans=True, uvs=uv_list))

        #once per frame, lookup transform
        target_frame = 'base_link'
        source_frame = pc_msg.header.frame_id

        try:
            #get the latest available transform
            now = rclpy.time.Time()
            transform = self.tf_buffer.lookup_transform(target_frame = target_frame, source_frame = source_frame, time = now)
        except LookupException as le:
            self.get_logger().info(f'Lookup Failed! Target: {target_frame}, Source: {source_frame}, {le}', throttle_duration_sec = 2.0)
            return
        except ExtrapolationException as ee:
            self.get_logger().info(f'No data at this time: {ee}', throttle_duration_sec = 2.0)
            return

        for (key, i), pt in zip(lookup, points):
            #skip if lookup points to NaN
            if any(v != v for v in (pt['x'], pt['y'], pt['z'])):
                continue
            pc_pos.setdefault(key, [])
            pc_pos[key].append((pt['x'], pt['y'], pt['z']))

            self.get_logger().info(f'{key} cube {i}: pt.x={pt["x"]}, pt.y={pt["y"]}, pt.z={pt["z"]}', throttle_duration_sec = 2.0)

            pt_stamp = PointStamped()
            pt_stamp.header.stamp = now.to_msg()
            pt_stamp.header.frame_id = source_frame
            pt_stamp.point.x = pt["x"]
            pt_stamp.point.y = pt["y"]
            pt_stamp.point.z = pt["z"]

            transformed_point = tf2_geometry_msgs.do_transform_point(pt_stamp, transform)
            base_frame_pos.setdefault(key, [])
            base_frame_pos[key].append((transformed_point.point.x, transformed_point.point.y, transformed_point.point.z))
            self.get_logger().info(f'{key} cube {i} in base_link: x={transformed_point.point.x:.3f}, y={transformed_point.point.y:.3f}, z={transformed_point.point.z:.3f}', throttle_duration_sec = 2.0)
        
        self.get_logger().info(f'Hearing from PointCloud2: height: "{pc_msg.height}",  width: "{pc_msg.width}"', throttle_duration_sec = 2.0)

        


def main(args=None):
    rclpy.init(args=args)

    camera_subscriber = CameraSubscriber()
    rclpy.spin(camera_subscriber)
    camera_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()