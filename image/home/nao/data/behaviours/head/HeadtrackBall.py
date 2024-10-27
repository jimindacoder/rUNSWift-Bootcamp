from BehaviourTask import BehaviourTask
from util.actioncommand import head
from math import radians
from util.Global import ballHeading, ballDistance

"""
        Description: Make the robot head follow the ball
        Credit: rUNSWift website and some codes from the website + chatgpt
"""

class HeadtrackBall(BehaviourTask):
    CLOSE_DISTANCE = 600        #in mm
    DEFAULT_PITCH = radians(19)         

    def _reset(self):
        # Initialize pitch angles based on camera parameters for different situations
        camera_pitch = self.world.blackboard.kinematics.parameters.cameraPitchBottom
        self.pitch_behind = self.DEFAULT_PITCH
        self.pitch_close = self.DEFAULT_PITCH + camera_pitch
        self.pitch_far = self.DEFAULT_PITCH + camera_pitch

    def _tick(self):
        yaw = ballHeading()
        # Set pitch based on distance to ball and angle 
        # if ball is within close distance use close pitch 
        if ballDistance() < self.CLOSE_DISTANCE:
            pitch = self.pitch_close
        else:
            pitch = self.pitch_far

        # Command the head to track the ball with controlled movement speed
        self.world.b_request.actions.head = head(yaw, pitch, is_relative=False, yaw_speed=0.50, pitch_speed=0.2)
