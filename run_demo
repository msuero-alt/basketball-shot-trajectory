from ultralytics import YOLO
from detector import detect_ball
from physics import fit_projectile, estimate_gravity
import numpy as np
import matplotlib.pyplot as plt

VIDEO_PATH = "data/WembyFreethrow.mp4"

print("\n=== TTD DEMO START ===")

# 1. LOAD MODEL
model = YOLO("yolov8n.pt")

# 2. TRACK BALL
coords = detect_ball(VIDEO_PATH, model)

coords = np.array(coords)

print(f"\nTotal tracked points: {len(coords)}")

if len(coords) < 5:
    print("Not enough data for shot reconstruction.")
    exit()

# 3. PHYSICS FIT
t, x_curve, y_curve = fit_projectile(coords)

g_est = estimate_gravity(y_curve)

print("\n=== SHOT SUMMARY ===")
print(f"Frames tracked: {len(coords)}")
print(f"Estimated gravity (relative): {g_est:.4f}")

# 4. VISUALIZE TRAJECTORY
x = coords[:, 0]
y = coords[:, 1]

t_plot = np.arange(len(coords))

plt.figure()
plt.plot(x, y, 'o', label="Ball Path")
plt.plot(x_curve(t_plot), y_curve(t_plot), '-', label="Physics Fit")

plt.gca().invert_yaxis()
plt.legend()
plt.title("TTD Ball Trajectory Reconstruction")
plt.show()

print("\n=== TTD DEMO END ===")
