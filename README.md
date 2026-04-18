🏀 TTD: Basketball Shot Tracking & Trajectory Reconstruction

A computer vision system that tracks a basketball in real-time video and reconstructs its flight path using motion modeling and physics-based curve fitting.

The system combines YOLO object detection, temporal tracking, and parabolic trajectory fitting to estimate shot arcs from raw gameplay footage.

*What This Project Does*

This project takes in a basketball video and:

Detects the basketball frame-by-frame using a YOLOv8 model
Tracks the ball’s position over time
Handles missed detections using short-term motion prediction
Reconstructs the shot trajectory
Fits a physics-inspired curve to estimate motion behavior
Outputs a full shot summary + visual trajectory plot

*Why I Built This*

Basketball shot analysis in real environments is messy — the ball gets occluded, motion blur happens, and detections are inconsistent.

I wanted to build a lightweight system that could still reconstruct a meaningful trajectory from imperfect data, similar to what you’d see in real sports analytics pipelines.

*How It Works*
1. Object Detection

Uses a pretrained YOLOv8 model to detect the basketball in each frame.

2. Tracking Logic

A custom tracking system:

locks onto the first strong detection
filters unstable detections using distance constraints
smooths movement using exponential averaging
3. Occlusion Handling

When the ball disappears:

short gaps are filled using velocity-based prediction
tracking resets if confidence is lost for too long
4. Trajectory Reconstruction

Once coordinates are collected:

a quadratic fit is applied to model motion
estimated curve represents shot arc behavior

*Example Output*
RUN BALL STARTED
LOCKED ON BALL
Frame 0: BALL (688, 181)
Frame 1: BALL (701, 161)
Frame 2: BALL (720, 134)
...
Frame 7: PREDICTED (820, 20)
Frame 8: PREDICTED (837, 4)
...
FINAL COORD COUNT: 16

Estimated gravity (relative): 1.56

*Key Features*
Real-time object detection with YOLOv8
Lightweight custom tracking system (no heavy tracking libraries)
Handles occlusion with motion prediction
Physics-based trajectory fitting
Clean modular pipeline (detector → physics → visualization)
Works on real basketball footage (not synthetic data)

*Project Structure*
basketball-shot-tracker/
│
├── main.py               # Entry point (demo launcher)
├── run_ball.py           # Runs full tracking pipeline
├── detector.py           # Core YOLO tracking logic
├── physics.py            # Curve fitting + gravity estimation
├── ttd_utils.py          # Utility functions (court mapping, plotting)
│
├── run_court.py          # Court reference mapping tool
├── run_plot.py           # Court trajectory visualization
│
├── data/
│   ├── test.mp4          # Input basketball footage
│   ├── ball_coords.npy   # Saved tracking data
│   └── court_refs.json   # Court calibration points

*How to Run*
1. Install dependencies
pip install ultralytics opencv-python numpy matplotlib
2. Run full demo
python run_ball.py
3. (Optional) Map court reference points
python run_court.py
4. (Optional) Visualize court trajectory
python run_plot.py

*Requirements*
Python 3.10+
OpenCV
NumPy
Matplotlib
Ultralytics YOLOv8

*What I Learned*
How object detection behaves in noisy real-world environments
Why tracking systems fail (occlusion, duplicate detections, drift)
How to stabilize motion using simple filtering instead of heavy frameworks
How physics-based modeling can still emerge from imperfect data

*Limitations*
Performance depends heavily on video quality
Struggles with heavy occlusion or multiple balls in frame
Assumes relatively stable camera perspective
Prediction is short-term only (not full motion forecasting)

*Future Improvements*
3D trajectory reconstruction (depth estimation)
Multi-angle shot fusion
Real-time overlay visualization on video
Player-aware filtering (remove false positives from hands/body)

*Summary*

This project explores how far you can get with a simple but carefully designed pipeline for sports tracking:

detection → tracking → prediction → physics modeling

Even with imperfect inputs, the system reconstructs meaningful shot trajectories from real gameplay footage.

*Note*

This is an experimental computer vision project built for learning and portfolio purposes. It is actively being improved.
