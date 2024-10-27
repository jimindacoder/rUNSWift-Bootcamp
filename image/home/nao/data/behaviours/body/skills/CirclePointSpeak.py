from BehaviourTask import BehaviourTask
from body.skills.CircleToPose import CircleToPose
from body.skills.ApproachBall import ApproachBall  
from util.Global import ballWorldPos, ballDistance, myPos
from util.MathUtil import normalisedTheta
from util.Timer import Timer
from util.actioncommand import raiseArm
from math import pi
import robot

"""
    Description:
    Walk up to the ball, circle around it, point at it, and say "I found the ball!"
    Credit: RunSwift website and debugging support from GPT.

"""
class RaiseArm(BehaviourTask):
    def _tick(self):
        self.world.b_request.actions.body = raiseArm()

class ApproachAndReportBall(BehaviourTask):
    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "ApproachBall": ApproachBall(self),  
            "CircleAroundBall": CircleToPose(self),
            "PointAtBall": RaiseArm(self),
        }

    def _reset(self):
        # Initialize variables and timers
        self._current_sub_task = "ApproachBall"  
        self._start_angle = None
        self._angle_covered = 0   
        # 5 seconds for pointing 
        self._pointTimer = Timer(timeTarget = 5000000)
        # 7 seconds to announce i found the ball
        self._announceTimer = Timer(timeTarget=7000000)
        self.is_finished = False

    def _transition(self):
        # Transition to circling around the ball once ApproachBall is done
        if self._current_sub_task == "ApproachBall" and ballDistance() < 500:
            self._current_sub_task = "CircleAroundBall"
            self._start_angle = normalisedTheta(ballWorldPos().heading() - myPos().heading())

        # After circling, switch to pointing at the ball
        elif self._current_sub_task == "CircleAroundBall" and self._angle_covered >= 2 * pi:
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
        if self._current_sub_task == "ApproachBall":
            # Use ApproachBall's sophisticated approach mechanics
            self._tick_sub_task()
        
        elif self._current_sub_task == "CircleAroundBall":
            ball_position = ballWorldPos()
            current_angle = normalisedTheta(ball_position.heading() - myPos().heading())
            
            # Update angle covered for one complete circle around the ball
            if self._start_angle is not None:
                angle_diff = abs(current_angle - self._start_angle)
                self._angle_covered += angle_diff
                self._start_angle = current_angle  # Reset start angle for next tick

            # Circle around the ball with ball as the center
            self._tick_sub_task(final_position=ball_position, circle_centre=ball_position, speed=0.5)

        elif self._current_sub_task == "PointAtBall":

            self._tick_sub_task()


