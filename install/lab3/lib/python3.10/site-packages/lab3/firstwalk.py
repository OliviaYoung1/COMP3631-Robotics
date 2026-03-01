import threading
import rclpy
from rclpy.node import Node
#since we need to publish to cmd_vel which expects a twist message
from geometry_msgs.msg import Twist
#need to catch exeptions incase program unexpectedly terminates
from rclpy.exceptions import ROSInterruptException
import signal


class FirstWalker(Node):
    def __init__(self):
        super().__init__('firstwalker')
        #create a publisher to publish velocities to /cmd_vel- note new type twist
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        #we create a rate ibject at 10Hz to help us send velocities at the specified frequency
        self.rate = self.create_rate(10)  # 10 Hz

    def walk_forward(self):
        #create a twist object- represents twist messages, which define velocites
        #initalised w/ empty velocities- meaning both linear and angular velocities are set to 0
        desired_velocity = Twist()
        desired_velocity.linear.x = 0.2  # Forward with 0.2 m/s

        for _ in range(30):  # Stop for a brief moment
            #publish the Twist message and then sleep using the rate object
            #the rate object maintains a constant loop rate of 10Hz
            #w/ 30 iterations, the loop will execute and publish velocites to the robot for 3 seconds
            self.publisher.publish(desired_velocity)
            self.rate.sleep()

    ##same as walk_forward but with -0.2 linear x velocity instead
    def walk_backward(self):
        desired_velocity = Twist()
        desired_velocity.linear.x = -0.2  # Backward with 0.2 m/s
        for _ in range(30):  # Stop for a brief moment
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
        first_walker.stop()
        rclpy.shutdown()

    rclpy.init(args=None)
    first_walker = FirstWalker()

    signal.signal(signal.SIGINT, signal_handler)
    #starts the rclpy.spin(first_walker) in a seperate thread
    #allows ROS to start communications while enabling us to execute other commands concurrently
    #running as thread => runs asynchronously, preventing blocage of main program flow
    thread = threading.Thread(target=rclpy.spin, args=(first_walker,), daemon=True)
    thread.start()

    #CORRECT APPROACH OF RUNNING INFINTE LOOPS IN ROS
    #rclpy.ok() to check if ROS is activley running before executing ros commands
    try:
        while rclpy.ok():
            first_walker.walk_forward()
            first_walker.walk_backward()
    except ROSInterruptException:
        pass


if __name__ == "__main__":
    main()


