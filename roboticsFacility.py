import json
import uuid
import random
from typing import List, Dict, Any

def generate_uuid() -> str:
    """Generate a UUID in the format used in colossus.json"""
    return str(uuid.uuid4()).replace('-', '')

def generate_actuate_gripper_step(step_id: str, diameter_mm: float = 125.0) -> Dict[str, Any]:
    """Generate an ActuateGripper step with the given parameters"""
    return {
        "id": step_id,
        "stepKind": "ActuateGripper",
        "args": {
            "argumentKind": "ActuateGripper",
            "selectedGripper": "primary",
            "diameterMM": diameter_mm,
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

def generate_move_arm_to_step(step_id: str) -> Dict[str, Any]:
    """Generate a MoveArmTo step with the given parameters"""
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
                "jointAngles": [
                    -2.1805537260062495,
                    -2.5829043335048582,
                    3.3608886932056912,
                    -2.4309278912317339,
                    -3.3787062871023856,
                    -2.5858414237113195
                ],
                "pose": {
                    "w": 0.9497853847317869,
                    "i": -0.31284558490773773,
                    "j": -0.0031768834478292946,
                    "k": 0.005026963813846869,
                    "x": 0.24633563732975722,
                    "y": 0.18444669164504088,
                    "z": 1.1899529230881356
                },
                "tcpOption": "wrist"
            }
        }
    }

def generate_steps(n_steps: int) -> Dict[str, Any]:
    """Generate n steps following the pattern in colossus.json"""
    steps = []
    current_diameter = 125.0
    
    for i in range(n_steps):
        step_id = generate_uuid()
        
        # Pattern: Two ActuateGripper steps followed by one MoveArmTo step
        if i % 3 == 0 or i % 3 == 1:
            # Generate ActuateGripper step
            step = generate_actuate_gripper_step(step_id, current_diameter)
            steps.append(step)
            
            # Generate secondary gripper step with same diameter
            secondary_id = generate_uuid()
            secondary_step = generate_actuate_gripper_step(secondary_id, current_diameter)
            secondary_step["args"]["selectedGripper"] = "secondary"
            steps.append(secondary_step)
            
            # Vary diameter between 30 and 125
            current_diameter = random.uniform(30, 125)
        else:
            # Generate MoveArmTo step
            step = generate_move_arm_to_step(step_id)
            steps.append(step)
    
    return {
        "globals": {
            "globalSpace": [],
            "globalVariables": []
        },
        "routine": {
            "motionPlanner": "ROS2",
            "steps": steps
        }
    }

def main():
    # Example usage
    n_steps = 400  # Number of step groups (each group is 2 ActuateGripper + 1 MoveArmTo)
    output = generate_steps(n_steps)
    
    # Write to file
    with open('generated_steps.json', 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main() 