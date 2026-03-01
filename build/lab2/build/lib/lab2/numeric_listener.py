import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int8


class NumericListener(Node):
    def __init__(self):
        super().__init__('numeric_listener')
        self.subscription = self.create_subscription(String, 'chatter', self.listener_callback, 10) #create subscirber to chatter topic

        self.subscription = self.create_subscription(Int8, 'numeric_chatter', self.numeric_callback, 10)
        
    def listener_callback(self, msg): #define a callback for the listener
        self.get_logger().info(f'I heard: {msg.data!r}') #log the message recieved
        
    def numeric_callback(self, msg):
        self.get_logger().info(f'I heard: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    listener = NumericListener()
    rclpy.spin(listener)


if __name__ == '__main__':
    main()
