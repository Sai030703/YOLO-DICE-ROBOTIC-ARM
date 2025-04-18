# robot_controller.py
import socket
import threading
import time

class RobotController:
    def __init__(self, host="127.0.0.1", port=3920):
        self.pos_joint_current = {"ax1": 0.0, "ax2": 0.0, "ax3": 0.0, "ax4": 0.0, "ax5": 0.0, "ax6": 0.0}
        self.pos_joint_target = self.pos_joint_current.copy()

        self.CRI_ALIVEJOG = "CRISTART 1000 ALIVEJOG 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 CRIEND"
        self.CRI_PROGRAM_LOAD = "CRISTART 1004 CMD LoadProgram [ProgName] CRIEND"
        self.CRI_PROGRAM_START = "CRISTART 1005 CMD StartProgram CRIEND"

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((host, port))
        print("✅ Connected to robotic arm")

        threading.Thread(target=self.read_msg, daemon=True).start()
        threading.Thread(target=self.keep_alive, daemon=True).start()

    def read_msg(self):
        while True:
            try:
                response = self.sock.recv(1024).decode("utf-8")
                self.update_current_joint_position(response)
            except Exception as e:
                print("Error reading:", e)

    def send_msg(self, msg, interval=0.1, console=False):
        if console:
            print(f"SENT: {msg}")
        self.sock.sendall(bytearray(msg.encode("utf-8")))
        time.sleep(interval)

    def keep_alive(self):
        while True:
            self.send_msg(self.CRI_ALIVEJOG)
            time.sleep(0.5)

    def cmd_move_joint(self, ax1=0, ax2=0, ax3=0, ax4=0, ax5=0, ax6=0, speed=40.0):
        return f"CRISTART 2000 CMD Move Joint {ax1} {ax2} {ax3} {ax4} {ax5} {ax6} 0.0 0.0 0.0 {speed} CRIEND"

    def update_current_joint_position(self, msg):
        data = msg.split()
        if "POSJOINTCURRENT" in data:
            idx = data.index("POSJOINTCURRENT")
            for i, key in enumerate(["ax1", "ax2", "ax3", "ax4", "ax5", "ax6"], 1):
                try:
                    self.pos_joint_current[key] = float(data[idx + i])
                except:
                    pass

    def equals(self, target):
        return all(abs(self.pos_joint_current[k] - v) < 0.1 for k, v in target.items())

    def move_to_position(self, joint_dict):
        self.pos_joint_target = joint_dict
        self.send_msg(self.cmd_move_joint(**joint_dict), console=True)
        while not self.equals(joint_dict):
            time.sleep(0.1)

    def run_gripper_program(self, prog_name):
        self.send_msg(self.CRI_PROGRAM_LOAD.replace("[ProgName]", prog_name), console=True)
        self.send_msg(self.CRI_PROGRAM_START, console=True)
        time.sleep(1)

    # ------------------ Task Definitions ------------------
    def run_task_1(self):
        print("▶️ Running Task 1")
        self.run_gripper_program("GripperOpen.xml")
        self.move_to_position({"ax1": -90, "ax2": -10.2, "ax3": 99.5, "ax4": 0, "ax5": 90.7, "ax6": 0})
        self.move_to_position({"ax1": -90, "ax2": -0.3, "ax3": 120.7, "ax4": 0, "ax5": 59.7, "ax6": 0})
        self.run_gripper_program("GripperClose.xml")
        self.move_to_position({"ax1": -90, "ax2": -9.3, "ax3": 108.5, "ax4": 0, "ax5": 80.7, "ax6": 0})
        self.move_to_position({"ax1": 90, "ax2": -9.2, "ax3": 108.5, "ax4": 0, "ax5": 80.7, "ax6": 0})
        self.move_to_position({"ax1": 90, "ax2": -1.0, "ax3": 120.5, "ax4": 0, "ax5": 60.7, "ax6": 0})
        self.run_gripper_program("GripperOpen.xml")
        self.move_to_position({"ax1": 0, "ax2": 0, "ax3": 90, "ax4": 0, "ax5": 90, "ax6": 0})

    def run_task_2(self):
        print("▶️ Running Task 2")
        self.run_gripper_program("GripperOpen.xml")
        self.move_to_position({"ax1": -56.6, "ax2": 6.5, "ax3": 99.5, "ax4": 0, "ax5": 75.7, "ax6": 1.5})
        self.move_to_position({"ax1": -56.6, "ax2": 12.6, "ax3": 106.0, "ax4": 0, "ax5": 62.3, "ax6": 1.5})
        self.run_gripper_program("GripperClose.xml")
        self.move_to_position({"ax1": -56.6, "ax2": 4.7, "ax3": 94.5, "ax4": 0, "ax5": 81.8, "ax6": 1.5})
        self.move_to_position({"ax1": 54.3, "ax2": 0.3, "ax3": 99.0, "ax4": 0, "ax5": 80.4, "ax6": 112.3})
        self.move_to_position({"ax1": 54.3, "ax2": 7.3, "ax3": 109.9, "ax4": 0, "ax5": 62.4, "ax6": 112.3})
        self.run_gripper_program("GripperOpen.xml")
        self.move_to_position({"ax1": 0, "ax2": 0, "ax3": 90, "ax4": 0, "ax5": 90, "ax6": 0})
   
