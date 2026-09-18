import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, Empty


class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')

        self.pub = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.estado = 0
        self.tiempo = 0.0
        self.pausado = False

        self.timer = self.create_timer(
            0.1,
            self.mover
        )

        self.clear_client = self.create_client(
            Empty,
            '/clear'
        )

        self.reset_client = self.create_client(
            Empty,
            '/reset'
        )

        self.srv_detener = self.create_service(
            Trigger,
            'detener',
            self.detener
        )

        self.srv_reanudar = self.create_service(
            Trigger,
            'reanudar',
            self.reanudar
        )

        self.srv_reiniciar = self.create_service(
            Trigger,
            'reiniciar',
            self.reiniciar
        )

        self.get_logger().info(
            "Controlador iniciado"
        )


    def detener(self, request, response):

        self.pausado = True

        response.success = True
        response.message = "Tortuga detenida"

        return response



    def reanudar(self, request, response):

        self.pausado = False

        response.success = True
        response.message = "Dibujo reanudado"

        return response



    def reiniciar(self, request, response):

        self.pausado = True

        self.estado = 0
        self.tiempo = 0.0

        if self.clear_client.wait_for_service(timeout_sec=1):

            self.clear_client.call_async(
                Empty.Request()
            )

        if self.reset_client.wait_for_service(timeout_sec=1):

            self.reset_client.call_async(
                Empty.Request()
            )

        self.pausado = False

        response.success = True
        response.message = "Dibujo reiniciado"

        return response



    def mover(self):

        msg = Twist()

        if self.pausado:

            self.pub.publish(msg)

            return


        self.tiempo += 0.1


        if self.estado == 0:

            msg.linear.x = 1.5
            msg.angular.z = -1.0

            if self.tiempo >= 3.14:

                self.estado = 1
                self.tiempo = 0



        elif self.estado == 1:

            msg.linear.x = -2.0
            msg.angular.z = 0.0

            if self.tiempo >= 2.0:

                self.estado = 2
                self.tiempo = 0



        else:

            msg.linear.x = 0.0
            msg.angular.z = 0.0


        self.pub.publish(msg)



def main(args=None):

    rclpy.init(args=args)

    node = TurtleController()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()



if __name__ == '__main__':

    main()
