#!/usr/bin/env python

import sys
import time
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
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.robot_name = robot_name
        time.sleep(.5)
        if robot_name == 'ur5':
            group_name = "manipulator"
        elif robot_name == 'panda':
            group_name = 'panda_arm'
        # else:
        #     print(robot_name + ' not regocnized')
        self.group = moveit_commander.MoveGroupCommander(group_name)
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                       moveit_msgs.msg.DisplayTrajectory,
                                                       queue_size=20)
        # PRODUCT PARAMETERS----------
        ## All the inner lists must have 7 elements
        self.product_app_loc = [
                            [.3678, .5182, .3, 3.14, 1.57, 0],
                            [.5743, .2982, .0153, 3.14, 0, 1.57],
                            [],
        ]
        self.product_locations = [
                            [.3678, .5182, .2, 3.14, 1.57, 0], 
                            [.5743, .3982, .0153, 3.14, 0, 1.57],
                            [.5402, .4, .14],
                        ]
        self.place_locations = [
                            [.66, 0.0, .08],
                            [.66, 0.0, .08],
                            [.66, 0.0, .08],
                        ]
        assert len(self.place_locations) == len(self.product_locations)
        self.productcount = len(self.product_locations)

    def go_to_pose_goal(self, x, y, z, rx=pi, ry=0, rz=0, w=None):
        group = self.group

        coords = [x, y, z, rx, ry, rz]
        if w != None:
            coords.append(w)
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

        if self.robot_name == 'ur5':
            pass
            ## todo dit nog werkend krijgen - lijkt erop alsof de box niet goed toegevoegd is
            # p = moveit_commander.PoseStamped()
            # p.header.frame_id = self.robot.get_planning_frame()
            # p.pose.position.x = 0
            # p.pose.position.y = 0
            # p.pose.position.z = 1
            # self.scene.add_box('Ground', p, (2,2,.15))
            # print('Box added')

        joint_goal = self.group.get_current_joint_values()
        joint_goal[0] = .63
        joint_goal[2] = .609
        self.group.go(joint_goal, wait=True)

        # joint_goal = self.group.get_current_joint_values()
        # joint_goal[3] = 5.07
        # joint_goal[4] = 4.712
        # joint_goal[5] = -2.511
        # self.group.go(joint_goal, wait=True)

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