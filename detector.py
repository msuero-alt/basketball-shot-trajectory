import cv2
import numpy as np


def distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


def detect_ball(
    video_path,
    model,
    conf_threshold=0.25,
    max_jump=200,
    smooth_factor=0.6,
    max_predict_frames=10
):

    cap = cv2.VideoCapture(video_path)

    coords = []
    last_pos = None
    velocity = np.array([0.0, 0.0])
    locked = False
    missed_frames = 0

    frame_idx = 0

    print("RUN BALL STARTED")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)[0]

        detections = []

        # ----------------------------
        # DETECT BALL (class 32)
        # ----------------------------
        if results.boxes is not None:
            boxes = results.boxes.xyxy.cpu().numpy()
            confs = results.boxes.conf.cpu().numpy()
            classes = results.boxes.cls.cpu().numpy()

            for i in range(len(boxes)):
                cls = int(classes[i])
                conf = float(confs[i])

                # FIX #1: strict ball filtering
                if cls == 32 and conf >= conf_threshold:
                    x1, y1, x2, y2 = boxes[i]
                    cx = (x1 + x2) / 2
                    cy = (y1 + y2) / 2
                    detections.append((cx, cy, conf))

        # FIX #2: sort detections so best confidence wins first
        detections = sorted(detections, key=lambda x: x[2], reverse=True)

        chosen = None

        # ----------------------------
        # SELECT BEST DETECTION
        # ----------------------------
        if detections:

            # FIX #3: safer initial lock
            if not locked and len(detections) > 0:
                chosen = detections[0]
                locked = True
                print("LOCKED ON BALL")

            else:
                best_score = -999

                for d in detections:
                    pos = np.array([d[0], d[1]])
                    conf = d[2]

                    dist = distance(pos, last_pos)

                    if dist > max_jump:
                        continue

                    score = conf - (dist * 0.01)

                    if score > best_score:
                        best_score = score
                        chosen = d

        # ----------------------------
        # TRACKING / SMOOTHING
        # ----------------------------
        if chosen is not None:

            missed_frames = 0

            pos = np.array([chosen[0], chosen[1]])

            if last_pos is not None:
                pos = smooth_factor * pos + (1 - smooth_factor) * last_pos
                velocity = pos - last_pos

            last_pos = pos
            coords.append((float(pos[0]), float(pos[1])))

            print(f"Frame {frame_idx}: BALL {coords[-1]}")

        # ----------------------------
        # PREDICTION (ONLY SHORT GAPS)
        # ----------------------------
        else:
            missed_frames += 1

            if last_pos is not None and missed_frames < max_predict_frames:

                # FIX #4: velocity decay (stability fix)
                velocity = 0.9 * velocity
                predicted = last_pos + velocity

                last_pos = predicted
                coords.append((float(predicted[0]), float(predicted[1])))

                print(f"Frame {frame_idx}: PREDICTED {coords[-1]}")

            else:
                print(f"Frame {frame_idx}: no ball")
                last_pos = None
                locked = False

        frame_idx += 1

    cap.release()

    print("FINAL COORD COUNT:", len(coords))
    return coords
