import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int8


class NumericTalker(Node): # define Talker- inherits from node
    def __init__(self): #intialiser
        super().__init__('numeric_talker') #call superclass
        self.publisher = self.create_publisher(String, 'chatter', 10) #create ROS publisher
        self.numeric_publisher = self.create_publisher(Int8, 'numeric_chatter', 10)

        timer_in_seconds = 0.5
        self.timer = self.create_timer(timer_in_seconds, self.talker_callback) #args: frequency we want the method to be called, method of the clss we want called
        self.counter = 0

    def talker_callback(self):
        msg = String() #create ROS String object
        msg.data = f'Hello World, {self.counter}' # populate data property
        self.publisher.publish(msg) # publish the message to the topic
        self.get_logger().info(f'Publishing: {msg.data}') #log a message (equiv to printing)
        
        numeric_msg = Int8()
        numeric_msg.data = self.counter
        self.numeric_publisher.publish(numeric_msg)
        
        self.get_logger().info(f'Publishing: "{msg.data}" and numeric value {numeric_msg.data}')
        
        self.counter += 1
        if self.counter > 127:
            self.counter = 0


def main(args=None):
    rclpy.init(args=args) #initialise ROS communications

    numericTalker = NumericTalker() # create an instance of class
    rclpy.spin(numericTalker) # spin keeps the python script running until we kill it


if __name__ == '__main__':
    main()
