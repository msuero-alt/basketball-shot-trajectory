import cv2
import matplotlib.pyplot as plt

coords = []             

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        coords.append((x, y))
        print(f"Clicked: {x}, {y}")

cap = cv2.VideoCapture("WembyShot.mp4")

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_event)

frame_num = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(0) 
    if key == 27: 
        break

    frame_num += 1

cap.release()
cv2.destroyAllWindows()

y_vals = [c[1] for c in coords]
frames = list(range(len(y_vals)))

import numpy as np

coeffs = np.polyfit(frames, y_vals, 2)
curve = np.poly1d(coeffs)

# Plot data + fitted curve
plt.plot(frames, y_vals, 'o', label='Data')
plt.plot(frames, curve(frames), '-', label='Fitted Parabola')
plt.gca().invert_yaxis()
plt.legend()
plt.title("Ball Height Over Time (Fitted Parabola)")
plt.xlabel("Frame")
plt.ylabel("Height (pixel)")
plt.show()

plt.plot(frames, y_vals, marker='o')
plt.gca().invert_yaxis()  # because image y increases downward
plt.title("Ball Height Over Time")
plt.xlabel("Frame")
plt.ylabel("Height (pixel)")
plt.show()

# Click and then press any key in order to proceed to next frame
# Press any key when you're done plotting the trajectory
