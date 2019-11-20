#!/usr/bin/env python

'''
NOTES! 
Voor dit bestand uitgevoerd kan worden moet er eest in een ander terminal hetvolgende uitgevoerd worden:
roslaunch ur5_moveit_config demo.launch
    Dit bestand is opgeslagen in 
    /opt/ros/kinetic/share



/ur5_moveit_config/config/ur5.srdf



Om ur5 te openen in gazebo gooi deze commands in 2 terminals (en open vervolgens dit script in een 3e): 
roslaunch ur_gazebo ur5.launch
roslaunch ur5_moveit_config ur5_moveit_planning_execution.launch sim:=true limited:=true



'''
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi



class MoveGroupPythonInteface(object):
    def __init__(self, robot_name):
        super(MoveGroupPythonInteface, self).__init__()
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('move_group_python_interface_tutorial',
                        anonymous=True)
        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()
        rospy.sleep(.5)
        if robot_name == 'ur5':
            group_name = "manipulator"
        elif robot_name == 'panda':
            group_name = 'panda_arm'
        group = moveit_commander.MoveGroupCommander(group_name)
        display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                       moveit_msgs.msg.DisplayTrajectory,
                                                       queue_size=20)
        self.box_name = ''
        self.robot = robot
        self.scene = scene
        self.group = group
        self.display_trajectory_publisher = display_trajectory_publisher

        # PRODUCT PARAMETERS----------
        self.product_locations = [
                            [-.4, .4, 0.1], 
                            [-.5, .3, 0.1], 
                            [-.57, .17, 0.1],
                        ]
        self.place_locations = [
                            [.2, .6, 0.1],
                            [.2, .6, 0.15],
                            [.2, .6, 0.2],
                        ]
        assert len(self.place_locations) == len(self.product_locations)
        self.productcount = len(self.product_locations)

    def add_objects(self):
        p = moveit_commander.PoseStamped()
        p.header.frame_id = self.robot.get_planning_frame()
        p.pose.position.x = 0.
        p.pose.position.y = 0.
        p.pose.position.z = 0.
        self.scene.add_box("table", p, (0.5, 1.5, 0.6))

    def go_to_pose_goal(self, x, y, z, rx=pi, ry=0, rz=0):
        group = self.group

        coords = [x, y, z, rx, ry, rz]
        group.set_pose_target(coords)

        ## Now, we call the planner to compute the plan and execute it.
        plan = group.go(wait=True)
        # Calling stop() ensures that there is no residual movement
        group.stop()
        group.clear_pose_targets()

        # # Kunnen weg?
        current_pose = self.group.get_current_pose().pose
        # return all_close(pose_goal, current_pose, 0.01)

    def get_pose():
        return self.group.get_current_pose().pose

    def go_to_joint_state(self):
        joint_goal = self.group.get_current_joint_values()
        joint_goal[1] = -.977
        self.group.go(joint_goal, wait=True)

        joint_goal = self.group.get_current_joint_values()
        joint_goal[0] = .63
        joint_goal[2] = .609
        joint_goal[3] = 5.07
        joint_goal[4] = 4.712
        joint_goal[5] = -2.511
        self.group.go(joint_goal, wait=True)

        self.group.stop()


def temp():
    robot = MoveGroupPythonInteface()
    while True:
        try:
            x = float(raw_input('x: '))
            y = float(raw_input('y: '))
            z = float(raw_input('z: '))
            robot.go_to_pose_goal(x, y, z)
        except Exception:
            print('ongeldige input, probeer opnieuw')


def main():
    robot = MoveGroupPythonInteface()
    robot.go_to_pose_goal(.5, .5, .5)

if __name__ == '__main__':
    temp()