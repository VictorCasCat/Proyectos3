import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy


class ObstacleController(Node):

    def __init__(self):
        super().__init__('obstacle_controller')

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            qos
        )

        self.distancia_seguridad = 0.5
        self.velocidad = 0.2
        self.obstaculo_detectado = False

        self.get_logger().info('Controlador de obstáculos iniciado')

    def lidar_callback(self, msg):

        distancia_minima = float('inf')

        for i, distancia in enumerate(msg.ranges):

            if not math.isfinite(distancia):
                continue

            angulo = msg.angle_min + i * msg.angle_increment

            if -math.radians(15) <= angulo <= math.radians(15):

                if distancia < distancia_minima:
                    distancia_minima = distancia

        obstaculo = distancia_minima < self.distancia_seguridad

        movimiento = Twist()

        if obstaculo:
            movimiento.linear.x = 0.0
            movimiento.angular.z = 0.0

            if not self.obstaculo_detectado:
                self.get_logger().info('Obstáculo detectado - PARANDO')
                self.obstaculo_detectado = True

        else:
            movimiento.linear.x = self.velocidad
            movimiento.angular.z = 0.0

            if self.obstaculo_detectado:
                self.get_logger().info('Obstáculo retirado - REANUDANDO')
                self.obstaculo_detectado = False

        self.publisher.publish(movimiento)


def main(args=None):

    rclpy.init(args=args)

    node = ObstacleController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        movimiento = Twist()
        node.publisher.publish(movimiento)

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
