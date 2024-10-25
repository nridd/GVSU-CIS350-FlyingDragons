#!pip install mediapipe opencv-python

import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

'''import tkinter as tk
from tkinter import filedialog

def browse_file():
	# Create a root window and hide it
	root = tk.Tk()
	root.withdraw()  # Hide the root window
	
	# Show file dialog and store selected file path
	file_path = filedialog.askopenfilename(title="Select a file", 
											filetypes=[("All Files", "*.*"), ("Video Files", "*.mp4 *.mov *.avi")])
	print(f"Selected file: {file_path}")
	
	# Destroy the root window after use
	root.destroy()
	return file_path

# Call the function
selected_file = browse_file()
print(str(selected_file))'''

import tkinter as tk
from tkinter import filedialog

def browse_file():
	root = tk.Tk()
	root.withdraw()  # Hide the root window
	
	# Make the window appear on top
	root.lift()
	root.call('wm', 'attributes', '.', '-topmost', True)
	
	# Show the file dialog
	file_path = filedialog.askopenfilename(title="Select a file", 
											filetypes=[("All Files", "*.*"), ("Video Files", "*.mp4 *.mov *.avi")])
	print(f"Selected file: {file_path}")
	
	root.destroy()
	return file_path

selected_file = browse_file()










cap = cv2.VideoCapture(selected_file)
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			print("Failed to grab frame or end of video reached.")
			break
		
		# Recolor image to RGB
		image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		image.flags.writeable = False
		
		# Make detection
		results = pose.process(image)
		
		# Recolor back to BGR
		image.flags.writeable = True
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
		
		# Render detections
		mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
								mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
								mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
								)               
		
		cv2.imshow('Mediapipe Feed', image)
		
		if cv2.waitKey(10) & 0xFF == ord('q'):
			break
		
	cap.release()
	cv2.destroyAllWindows()
	