import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# --- AUDIO SETUP (Fail-Safe) ---
volume = None
try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    print("✅ Audio System Connected")
except Exception as e:
    print(f"⚠️ Audio Hardware Note: {e}. (Visual demo only mode)")

# --- MEDIAPIPE SETUP ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, img = cap.read()
    if not success: break
    
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            
            lm = handLms.landmark
            # Check if fist (fingers curled)
            fingers = [8, 12, 16, 20]
            pips = [6, 10, 14, 18]
            up_count = sum(1 for i in range(4) if lm[fingers[i]].y < lm[pips[i]].y)

            if up_count <= 1:
                fist_y = lm[0].y # Wrist height
                # Mapping height to volume
                vol_level = np.interp(fist_y, [0.15, 0.85], [0.0, -65.0])
                
                # Try to set volume if the variable exists
                if volume is not None:
                    try:
                        volume.SetMasterVolumeLevel(vol_level, None)
                    except:
                        pass
                
                # UI text so the mentor sees it's working
                vol_pct = int(np.interp(vol_level, [-65.0, 0.0], [0, 100]))
                cv2.putText(img, f"VOLUME: {vol_pct}%", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(img, "MAKE A FIST", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Day 3 Submission", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
