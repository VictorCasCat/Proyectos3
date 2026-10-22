import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger

class DrawNumber(Node):

    def __init__(self):
        super().__init__('draw_number')

        self.publisher_ = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.timer_callback
        )

        self.paused = False
        self.step = 0

        self.pause_service = self.create_service(
            Trigger,
            '/g02/pause',
            self.pause_callback
        )

        self.resume_service = self.create_service(
            Trigger,
            '/g02/resume',
            self.resume_callback
        )

        self.restart_service = self.create_service(
            Trigger,
            '/g02/restart',
            self.restart_callback
        )
    def pause_callback(self, request, response):
        self.paused = True

        twist = Twist()
        self.publisher_.publish(twist)

        response.success = True
        response.message = 'Movimiento pausado'
        return response

    def resume_callback(self, request, response):
        self.paused = False

        response.success = True
        response.message = 'Movimiento reanudado'
        return response

    def restart_callback(self, request, response):
        self.step = 0
        self.paused = False

        response.success = True
        response.message = 'Dibujo reiniciado'
        return response

    def timer_callback(self):

        if self.paused:
            return

        twist = Twist()

        if self.step < 20:
            twist.linear.x = 0.2
            twist.angular.z = 0.8

        elif self.step < 40:
            twist.linear.x = -0.25
            twist.angular.z = 0.0

        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        self.publisher_.publish(twist)
        self.step += 1

def main(args=None):
    rclpy.init(args=args)

    node = DrawNumber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()