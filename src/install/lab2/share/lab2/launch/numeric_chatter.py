from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
            #1st node going to be launched
            Node(
                package='lab2', #package it lives in
                executable='numeric_talker', #the file name
                name='my_numeric_talker' #the name we give to the node when we run it
            ),
            #2nd node going to be launched
            Node(
                package='lab2',
                executable='numeric_listener',
                name='my_numeric_listener'
            ),
        ])
