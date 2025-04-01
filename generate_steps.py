import json
import uuid
import random
import math

def generate_uuid():
    return str(uuid.uuid4())

def generate_quaternion():
    # Generate random quaternion (normalized)
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    z = random.uniform(-1, 1)
    w = random.uniform(-1, 1)
    magnitude = math.sqrt(x*x + y*y + z*z + w*w)
    return {
        "w": w/magnitude,
        "i": x/magnitude,
        "j": y/magnitude,
        "k": z/magnitude
    }

def generate_joint_angles():
    # Generate random joint angles within safe limits
    return [
        random.uniform(-3.14, 3.14),  # Base
        random.uniform(-3.14, 3.14),  # Shoulder
        random.uniform(-3.14, 3.14),  # Elbow
        random.uniform(-3.14, 3.14),  # Wrist 1
        random.uniform(-3.14, 3.14),  # Wrist 2
        random.uniform(-3.14, 3.14)   # Wrist 3
    ]

def generate_pose():
    quat = generate_quaternion()
    return {
        **quat,
        "x": random.uniform(0, 1),
        "y": random.uniform(0, 1),
        "z": random.uniform(0, 1)
    }

def generate_actuate_gripper_step(step_id, is_primary=True):
    # Generate diameter between 30 and 125
    diameter = random.uniform(30, 125)
    return {
        "id": step_id,
        "stepKind": "ActuateGripper",
        "args": {
            "argumentKind": "ActuateGripper",
            "selectedGripper": "primary" if is_primary else "secondary",
            "diameterMM": round(diameter, 2),
            "forceNewtons": 45,
            "gripKind": "inward",
            "payloadKg": 0,
            "targetDiameterToleranceMeters": 0.01,
            "waitForGripToContinue": False,
            "isFlexGrip": False,
            "forcePercent": 0.5,
            "stopRoutineOnFailure": True
        }
    }

def generate_move_arm_step(step_id):
    return {
        "id": step_id,
        "stepKind": "MoveArmTo",
        "args": {
            "argumentKind": "MoveArmTo",
            "motionKind": "joint",
            "shouldMatchJointAngles": False,
            "tcpOption": "auto",
            "positionListID": None,
            "target": {
                "jointAngles": generate_joint_angles(),
                "pose": generate_pose(),
                "tcpOption": "wrist"
            },
            "targetKind": "singlePosition",
            "isWaypoint": False,
            "isCacheable": False,
            "reduceSmoothing": False,
            "moveDynamicBaseToReachPosition": True
        }
    }

def generate_routine(num_steps):
    steps = []
    step_definitions = {}
    
    for i in range(num_steps):
        # Generate two ActuateGripper steps followed by one MoveArmTo step
        if i % 3 == 0:
            # Primary gripper
            step_id = generate_uuid()
            steps.append({"id": step_id, "stepKind": "ActuateGripper"})
            step_definitions[step_id] = generate_actuate_gripper_step(step_id, True)
        elif i % 3 == 1:
            # Secondary gripper
            step_id = generate_uuid()
            steps.append({"id": step_id, "stepKind": "ActuateGripper"})
            step_definitions[step_id] = generate_actuate_gripper_step(step_id, False)
        else:
            # MoveArmTo
            step_id = generate_uuid()
            steps.append({"id": step_id, "stepKind": "MoveArmTo"})
            step_definitions[step_id] = generate_move_arm_step(step_id)
    
    return {
        "globals": {
            "globalSpace": [],
            "globalVariables": []
        },
        "routine": {
            "motionPlanner": "ROS2",
            "steps": steps,
            "stepDefinitions": step_definitions
        }
    }

def main():
    # Generate 25 steps (8 sets of 3 steps + 1 extra)
    routine = generate_routine(400)
    
    # Write to file
    with open('generated_routine.json', 'w') as f:
        json.dump(routine, f, indent=2)

if __name__ == "__main__":
    main() 