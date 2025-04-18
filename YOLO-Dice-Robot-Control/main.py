import cv2
from ultralytics import YOLO
import time
from robot_controller import RobotController

# Load YOLOv11 model (make sure best.pt is in your folder)
print("📦 Loading YOLOv11 model...")
model = YOLO("my_model.pt") 

# Get class labels from the model
labels = model.names

# Connect to robotic arm
robot = RobotController()

def trigger_robot_task(detected_class):
    try:
        dice_number = int(detected_class)
        task_map = {
            1: robot.run_task_1,
            2: robot.run_task_1,
            3: robot.run_task_1,
            4: robot.run_task_2,
            5: robot.run_task_2,
            6: robot.run_task_2,
        }
        task = task_map.get(dice_number)
        if task:
            print(f"🎯 Dice value: {dice_number} → Running Task {dice_number}")
            task()
        else:
            print(f"⚠️ No task defined for detected number: {dice_number}")
    except ValueError:
        print(f"Invalid class label '{detected_class}' – expected numeric class names like '1', '2', ...")

# --- MAIN WEBCAM LOOP ---
cap = cv2.VideoCapture(0)

last_triggered = None
cooldown_seconds = 3
last_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    # YOLO inference (Ultralytics)
    results = model(frame, verbose=False)
    frame = results[0].plot()
    detections = results[0].boxes

    object_count = 0
    dice_value = None

    for i in range(len(detections)):
        # Get box and class info
        xyxy = detections[i].xyxy.cpu().numpy().squeeze().astype(int)
        classidx = int(detections[i].cls.item())
        classname = labels[classidx]
        conf = detections[i].conf.item()

        # Draw only if above threshold
        if conf > 0.5:
            object_count += 1
            color = (0,255,0)
            xmin, ymin, xmax, ymax = xyxy
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
            label = f'{classname}: {int(conf*100)}%'
            cv2.putText(frame, label, (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # Only process the first dice found (or adjust as needed)
            if dice_value is None:
                dice_value = classname

    # Trigger robot task for detected value, with cooldown to avoid spam
    if dice_value is not None:
        cv2.putText(frame, f'Detected: {dice_value}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        if (dice_value != last_triggered or time.time() - last_time > cooldown_seconds):
            trigger_robot_task(dice_value)
            last_triggered = dice_value
            last_time = time.time()

    # Draw object count
    cv2.putText(frame, f'Number of objects: {object_count}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,255,255), 2)

    # Show webcam window
    cv2.imshow('YOLO Dice Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
