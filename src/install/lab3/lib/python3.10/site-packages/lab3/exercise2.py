import threading
import rclpy
from rclpy.node import Node
#since we need to publish to cmd_vel which expects a twist message
from geometry_msgs.msg import Twist
#need to catch exeptions incase program unexpectedly terminates
from rclpy.exceptions import ROSInterruptException
import signal
import math


class Exercise2(Node):
    def __init__(self):
        super().__init__('excercise2')
        #create a publisher to publish velocities to /cmd_vel- note new type twist
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        #we create a rate ibject at 10Hz to help us send velocities at the specified frequency
        self.rate = self.create_rate(10)  # 10 Hz

    def trace_square(self):
        #create a twist object- represents twist messages, which define velocites
        #initalised w/ empty velocities- meaning both linear and angular velocities are set to 0
        desired_velocity = Twist()

        for i in range(4):
            desired_velocity.linear.x = 0.2  # Forward with 0.2 m/s
            desired_velocity.angular.z = 0.0 #no rotation- straight
        
            for _ in range(30):  # 4 for sides of a square
                self.publisher.publish(desired_velocity)
                self.rate.sleep()
            
            desired_velocity.linear.x = 0.0 #stop forward movement
            # pi/2 is 90 degree in radians
            # /5 makes the turn slower and more controlled- rotates in 5 increments
            desired_velocity.angular.z = (math.pi / 2) / 5
        
            for _ in range(50):
                self.publisher.publish(desired_velocity)
                self.rate.sleep()

    def stop(self):
        desired_velocity = Twist()
        desired_velocity.linear.x = 0.0  # Send zero velocity to stop the robot
        self.publisher.publish(desired_velocity)

def main():
    #defining a function when the user presses CTRL+C, signalling interrupt
    #ensures robot will stop moving after code is terminated
    def signal_handler(sig, frame):
        square_walker.stop()
        rclpy.shutdown()

    rclpy.init(args=None)
    square_walker = Exercise2()

    signal.signal(signal.SIGINT, signal_handler)
    #starts the rclpy.spin(first_walker) in a seperate thread
    #allows ROS to start communications while enabling us to execute other commands concurrently
    #running as thread => runs asynchronously, preventing blocage of main program flow
    thread = threading.Thread(target=rclpy.spin, args=(square_walker,), daemon=True)
    thread.start()

    #CORRECT APPROACH OF RUNNING INFINTE LOOPS IN ROS
    #rclpy.ok() to check if ROS is activley running before executing ros commands
    try:
        while rclpy.ok():
            square_walker.trace_square()
    except ROSInterruptException:
        pass


if __name__ == "__main__":
    main()