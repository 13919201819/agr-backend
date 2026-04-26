# # active_streams = {}

# import cv2

# active_streams = {}
# camera = None
# camera_running = False

import threading
import cv2

# Shared state
active_streams = {}
latest_frame = None
camera_thread = None
camera_running = False
lock = threading.Lock()