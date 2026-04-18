import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import json


# -----------------------------
# BALL TRACKING
# -----------------------------
def track_ball(video_path, save_path="data/ball_coords.npy"):

    if os.path.exists(save_path):
        print(f"Loading saved ball coordinates from {save_path}")
        coords = np.load(save_path, allow_pickle=True).tolist()
        return coords

    coords = []

    def ball_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            coords.append((x, y))
            print(f"Ball clicked at: {x}, {y}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    cv2.namedWindow("BallClick")
    cv2.setMouseCallback("BallClick", ball_click)

    print("Click the ball in each frame. Press SPACE to advance, ESC to finish early.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display_frame = cv2.resize(frame, (960, 540))
        frame_displayed = True

        while frame_displayed:
            cv2.imshow("BallClick", display_frame)
            key = cv2.waitKey(1) & 0xFF

            if key == 32:
                frame_displayed = False
            elif key == 27:
                frame_displayed = False
                cap.release()
                cv2.destroyAllWindows()
                print("Stopped early by user")

    cap.release()
    cv2.destroyAllWindows()

    print(f"Total frames clicked: {len(coords)}")

    if coords:
        np.save(save_path, coords)

    return coords


# -----------------------------
# PARABOLA FIT (FRAME-BASED)
# -----------------------------
def fit_parabola(coords):

    coords = [c for c in coords if isinstance(c, (list, tuple)) and len(c) == 2]

    if len(coords) < 3:
        print("No coordinates to fit parabola.")
        return None, None

    y_vals = [c[1] for c in coords]
    frames = list(range(len(y_vals)))

    coeffs = np.polyfit(frames, y_vals, 2)
    curve = np.poly1d(coeffs)

    return frames, curve


def plot_ball_trajectory(coords, curve=None):

    coords = [c for c in coords if isinstance(c, (list, tuple)) and len(c) == 2]

    if not coords:
        print("No ball coords to plot.")
        return

    y_vals = [c[1] for c in coords]
    frames = list(range(len(y_vals)))

    plt.figure()
    plt.plot(frames, y_vals, 'o', label='Ball Pixels')

    if curve is not None:
        plt.plot(frames, curve(frames), '-', label='Fitted Parabola')

    plt.gca().invert_yaxis()
    plt.xlabel("Frame")
    plt.ylabel("Y pixel")
    plt.legend()
    plt.title("Ball Height Over Time (Pixel Coordinates)")
    plt.show()


# -----------------------------
# COURT MAPPING
# -----------------------------
def map_court(video_path, save_path="data/court_refs.json"):

    if os.path.exists(save_path):
        print(f"Loading saved court references from {save_path}")
        with open(save_path, 'r') as f:
            return json.load(f)

    court_refs = {}
    ref_points = ["hoop", "free_throw_line", "baseline"]

    def court_click(event, x, y, flags, param):
        _, name = param
        if event == cv2.EVENT_LBUTTONDOWN and name not in court_refs:
            court_refs[name] = (x, y)
            print(f"{name} clicked at: {x}, {y}")

    cap = cv2.VideoCapture(video_path)
    ret, first_frame = cap.read()
    cap.release()

    if not ret:
        raise ValueError("Could not read video")

    display_frame = cv2.resize(first_frame, (960, 540))
    cv2.namedWindow("CourtClick")

    for name in ref_points:
        cv2.setMouseCallback("CourtClick", court_click, (None, name))

        while name not in court_refs:
            cv2.imshow("CourtClick", display_frame)
            cv2.waitKey(1)

    cv2.destroyAllWindows()

    with open(save_path, 'w') as f:
        json.dump(court_refs, f)

    return court_refs


# -----------------------------
# COORD CONVERSION (SAFE)
# -----------------------------
def convert_to_court_coords(coords, court_refs):

    coords = [c for c in coords if isinstance(c, (list, tuple)) and len(c) == 2]

    if not coords:
        return []

    x_scale = 94 / abs(court_refs["baseline"][0] - court_refs["hoop"][0])
    y_scale = 50 / abs(court_refs["baseline"][1] - court_refs["hoop"][1])

    return [((x - court_refs["hoop"][0]) * x_scale,
             (y - court_refs["hoop"][1]) * y_scale)
            for x, y in coords]


def plot_court_trajectory(ball_court_coords):

    if not ball_court_coords:
        print("No court coords to plot.")
        return

    court_x_vals = [c[0] for c in ball_court_coords]
    court_y_vals = [c[1] for c in ball_court_coords]

    plt.figure(figsize=(10, 5))
    plt.plot(court_x_vals, court_y_vals, marker='o')
    plt.xlabel("Court X (ft)")
    plt.ylabel("Court Y (ft)")
    plt.title("Ball Trajectory in Court Coordinates (Feet)")
    plt.show()


# -----------------------------
# PHYSICS FIT (FIXED, SAFE)
# -----------------------------
def fit_physics(coords, fps=30):

    coords = [c for c in coords if isinstance(c, (list, tuple)) and len(c) == 2]

    if len(coords) < 3:
        print("Not enough data for physics fit.")
        return None, None, None

    t = np.array([i / fps for i in range(len(coords))])
    y = np.array([c[1] for c in coords])

    coeffs = np.polyfit(t, y, 2)
    curve = np.poly1d(coeffs)

    return t, curve, coeffs


def plot_physics(t, coords, curve=None):

    coords = [c for c in coords if isinstance(c, (list, tuple)) and len(c) == 2]

    if not coords:
        print("No data to plot.")
        return

    y = [c[1] for c in coords]

    plt.figure()
    plt.plot(t, y, 'o', label="Ball")

    if curve is not None:
        plt.plot(t, curve(t), '-', label="Fit")

    plt.gca().invert_yaxis()
    plt.legend()
    plt.title("Ball Trajectory with Physics Model")
    plt.show()
