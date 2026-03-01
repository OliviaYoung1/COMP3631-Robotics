import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        #call the superclass initialiser passing in the name of the node
        super().__init__('talker')
        #create a ROS publishier, first arg is message type, second is 
        # a string w/ the name of the topic we want to publish to and 
        # the thrid is the outgoijg message queue size
        self.publisher = self.create_publisher(String, 'chatter', 10)

        timer_in_seconds = 0.5
        self.timer = self.create_timer(timer_in_seconds, self.talker_callback)
        self.counter = 0

    #define talker_callback method
    def talker_callback(self):
        msg = String()
        #populate the message's data property
        msg.data = f'Hello World, {self.counter}'
        #publish the message to the topic
        self.publisher.publish(msg)
        #log a messages- equiv to printing, not actually publishing anything
        self.get_logger().info(f'Publishing: {msg.data}')
        self.counter += 1


def main(args=None):
    #initialise ROS commmunications
    rclpy.init(args=args)

    #create an instance of the class
    talker = Talker()
    #keeps python script running until we kill it
    rclpy.spin(talker)


if __name__ == '__main__':
    main()


