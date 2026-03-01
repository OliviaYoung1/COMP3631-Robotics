import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        #create a subscriber to the chatter topic
        #string- type of messages we expect from that topic
        #chatter is the name of the topic we want to subscribe to
        #self.Listener_Callbakc a method to process messages recieved from the topic
        #10 - the queue size
        self.subscription = self.create_subscription(String, 'chatter', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning

    #define a callback listener, msg is the message incoming from the topic
    def listener_callback(self, msg):
        #log the message recieved
        self.get_logger().info(f'I heard: {msg.data!r}')


def main(args=None):
    rclpy.init(args=args)
    listener = Listener()
    rclpy.spin(listener)


if __name__ == '__main__':
    main()
