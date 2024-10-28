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
    
    def _reset(self):
        # Set default pitch angles based on camera parameters
        camera_pitch = self.world.blackboard.kinematics.parameters.cameraPitchBottom
        self.PITCH_BEHIND = radians(19)  # Fixed pitch when ball is behind
        self.PITCH = radians(19 + camera_pitch) 
    
    def _tick(self):
        # Determine yaw (horizontal angle to ball)
        yaw = ballHeading()
        pitch = self.PITCH if ballDistance() < 800 else self.PITCH
        pitch = self.PITCH_BEHIND if abs(yaw) > radians(60) else self.PITCH

        # Send head command with calculated yaw and pitch
        self.world.b_request.actions.head = head(yaw, pitch, False, 0.50, 0.2)