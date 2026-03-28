# Basketball Shot Trajectory Analysis

## Project Overview
This project tracks the vertical motion of a basketball shot from video footage and models its trajectory using basic physics and data analysis techniques. The goal is to demonstrate how **computer vision**, **data tracking**, and **mathematical modeling** can provide insights into basketball shot mechanics.

---

## Features
- Manual/semi-manual ball tracking from video frames  
- Vertical height plotted against frame number to approximate **shot motion over time**  
- Parabolic curve fitted to track the projectile motion of the basketball  
- Highlights challenges of **camera angle distortion** and how to correct for it  

---

## Motivation
Analyzing basketball shots is a key aspect of sports analytics and biomechanics. Understanding the ball's trajectory can help evaluate:

- Release angle and peak height  
- Consistency and accuracy of shots  
- Training interventions for players  

This project is a **first step** toward more advanced AI-driven performance analysis.

---

## Methodology

1. **Video Selection**  
   - Used a screen-recorded video of a player performing a catch-and-shoot jump shot.  
   - Due to limited camera angles, the shot was recorded diagonally behind the player.

2. **Manual Ball Tracking**  
   - Frames were extracted, and the ball’s vertical position was recorded frame by frame.  
   - Initial x-y plots were distorted due to the camera angle (S-shaped curve).

3. **Frame vs Height Plot**  
   - Vertical position plotted against frame number to isolate the vertical motion.  
   - This produced a clean parabola representing the ball’s flight path.

4. **Parabola Fitting**  
   - A quadratic function was fitted to the tracked points using `numpy.polyfit`.  
   - This smooths the curve and models projectile motion under gravity.

---

## Python Libraries Used
- `matplotlib` for plotting  
- `numpy` for curve fitting  
- `opencv` (optional) for video frame extraction  

---

## Example Output

![Ball Height Over Time](./assets/parabola_plot.png)  
*Parabolic trajectory of the basketball shot (vertical height vs frame number)*

---

## Insights / Notes
- **Camera Angle Matters:** Diagonal camera angles distort the raw x-y trajectory. Plotting vertical height against frame number corrects for this.  
- **Physics in Sports:** Even simple frame-based tracking reveals the expected parabolic motion of a basketball shot.  
- **Next Steps:** Automate ball detection with computer vision, extract multiple shots, and analyze release angles and shot consistency.

---

## Skills Demonstrated
- Data collection and manual annotation  
- Python plotting and analysis  
- Quadratic curve fitting  
- Problem-solving around real-world CV limitations  

---

## Next Steps / Roadmap
1. Automate tracking using OpenCV or object detection models  
2. Compare multiple shots for consistency and biomechanics analysis  
3. Expand to full court player and ball tracking for advanced analytics  
4. Create YouTube or GitHub portfolio content explaining the process  

---
