import time
import sys
from controller import Robot

TIME_STEP = 32

class State:
    WAIT = 0
    PICK = 1
    ROTATING = 2
    DROP = 3
    ROTATING_BACK = 4

def main():
    robot = Robot()
    counter = 0
    i = 0
    state = State.WAIT
    target_positions = [-1.88, -2.14, -2.38, -1.51]
    speed = 1.0

    if len(sys.argv) == 2:
        speed = float(sys.argv[1])

    hand_motors = [robot.getDevice("finger_1_joint_1"),
                   robot.getDevice("finger_2_joint_1"),
                   robot.getDevice("finger_middle_joint_1")]
    ur_motors = [robot.getDevice("shoulder_lift_joint"),
                 robot.getDevice("elbow_joint"),
                 robot.getDevice("wrist_1_joint"),
                 robot.getDevice("wrist_2_joint")]

    for motor in ur_motors:
        motor.setVelocity(speed)

    distance_sensor = robot.getDevice("distance sensor")
    distance_sensor.enable(TIME_STEP)

    position_sensor = robot.getDevice("wrist_1_joint_sensor")
    position_sensor.enable(TIME_STEP)

    while robot.step(TIME_STEP) != -1:
        if counter <= 0:
            if state == State.WAIT:
                if distance_sensor.getValue() < 500:
                    state = State.PICK
                    counter = 8
                    print("Pick")
                    for motor in hand_motors:
                        motor.setPosition(0.85)
            elif state == State.PICK:
                for i in range(4):
                    ur_motors[i].setPosition(target_positions[i])
                print("Arm Rotating")
                state = State.ROTATING
            elif state == State.ROTATING:
                if position_sensor.getValue() < -2.3:
                    counter = 8
                    print("Drop")
                    state = State.DROP
                    for motor in hand_motors:
                        motor.setPosition(motor.getMinPosition())
            elif state == State.DROP:
                for motor in ur_motors:
                    motor.setPosition(0.0)
                print("Arm Rotating back")
                state = State.ROTATING_BACK
            elif state == State.ROTATING_BACK:
                if position_sensor.getValue() > -0.1:
                    state = State.WAIT
                    print("Waiting for object")
        counter -= 1

    robot.cleanup()

if __name__ == "__main__":
    main()
