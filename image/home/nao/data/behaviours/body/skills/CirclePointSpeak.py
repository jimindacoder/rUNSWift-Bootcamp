from BehaviourTask import BehaviourTask
from body.skills.WalkStraightToPose import WalkStraightToPose
from body.skills.CircleToPose import CircleToPose
from util.Global import ballWorldPos, ballDistance, myPos
from util.actioncommand import raiseArm
from util.Vector2D import Vector2D
from util.MathUtil import normalisedTheta 
from util.Timer import Timer
from math import pi 
import robot

"""
        Description:
        walk up to ball do a circle and then say i found the ball
        credit
        runswift website :) 
        and some debugging from gpt
"""
class ApproachAndReportBall(BehaviourTask):

    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "WalkToBall": WalkStraightToPose(self),
            "CircleAroundBall": CircleToPose(self),
            "PointAtBall": RaiseArm(self),
        }

    def _reset(self):
        self._current_sub_task = "WalkToBall"
        self._start_angle = None
        self._angle_covered = 0   
        # 3 seconds to point 
        self._pointTimer = Timer(timeTarget=3000000)  
        # 2 seconds to say i found the ball
        self._announceTimer = Timer(timeTarget=200000) # Time for announcement
        self.is_finished = False

    def _transition(self):
        # Transition to circling around the ball once close enough
        if self._current_sub_task == "WalkToBall" and ballDistance() < 500:
            self._current_sub_task = "CircleAroundBall"
            ball_position = ballWorldPos()
            self._start_angle = normalisedTheta(ball_position.heading() - myPos().heading())  # Record initial angle

        # After circling, switch to pointing at the ball
        elif self._current_sub_task == "CircleAroundBall" and self._angle_covered >= 2 * pi:  # Complete one circle
            self._current_sub_task = "PointAtBall"
            self._pointTimer.start()

        # After pointing, start the announcement timer
        elif self._current_sub_task == "PointAtBall" and self._pointTimer.finished():
            robot.say("I found ze ball!")
            self._announceTimer.start()
            self._current_sub_task = "Announce"

        # Set task as finished after announcement
        elif self._current_sub_task == "Announce" and self._announceTimer.finished():
            self.is_finished = True

    def _tick(self):
        if self._current_sub_task == "WalkToBall":
            ball_position = ballWorldPos()
            self._tick_sub_task(ball_position, speed=1.0)
        
        elif self._current_sub_task == "CircleAroundBall":
            ball_position = ballWorldPos()
            current_angle = normalisedTheta(ball_position.heading() - myPos().heading())
            
            if self._start_angle is not None:
                # Update the angle covered since starting the circle
                angle_diff = abs(current_angle - self._start_angle)
                self._angle_covered += angle_diff
                self._start_angle = current_angle  # Reset start angle for next tick

            self._tick_sub_task(final_position=ball_position, circle_centre=ball_position, speed=0.5)
        
        elif self._current_sub_task == "PointAtBall":
            self._tick_sub_task()

class RaiseArm(BehaviourTask):
     def _tick(self):
        self.world.b_request.actions.body = raiseArm()