#!/usr/bin/env python3

import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Pose

mp_pose = mp.solutions.pose

# Open the video file
cap = cv2.VideoCapture('/Users/nridd/Downloads/Nate.mov')

# List of joint indexes to keep
required_joints = [7, 8, 11, 12, 13, 14, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

# 3D list to store joint data (frames x joints x coordinates)
joint_data = []

# Process the video
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			break
		
		# Convert the frame to RGB for Mediapipe
		image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		results = pose.process(image)
		
		# Check if pose landmarks are detected
		if results.pose_landmarks:
			# Extract the required joints for this frame
			frame_joint_data = []
			for joint_index in required_joints:
				joint = results.pose_landmarks.landmark[joint_index]
				frame_joint_data.append([joint.x, joint.y, joint.z])  # Store (x, y, z) coordinates
				
			# Append this frame's joint data to the main list
			joint_data.append(frame_joint_data)
			
	cap.release()
	
# Convert joint data to a 3D numpy array
joint_data = np.array(joint_data)  # Shape will be (frames, 16, 3)
print("Joint data shape:", joint_data.shape)

print(joint_data)
print(len(joint_data))

def spcoord(data, x):
	# takes in joint data 3d array and outputs a 2d array with one joint. [frame][joint][x,y,z] -> (same joint)[frame][x,y,z,frame#]
	new_arr = []
	for index, frame in enumerate(data):
		joint_coordinates = frame[x]
		new_arr.append([joint_coordinates[0], joint_coordinates[1], joint_coordinates[2], index])
	return new_arr

new_arr = spcoord(joint_data, 5)

def find_wave_bottoms(data):
	"""
	Finds the indices of the bottom points in a sine-like wave pattern.
	
	Parameters:
		data (list of lists): A 2D array where each element is a list [x, y, z, index] for each frame.
		
	Returns:
		list: A list of indices where the y-coordinate is a local minimum.
	"""
	minima_indices = []
	
	# Loop through each point, starting from the second point and ending at the second-to-last
	for i in range(1, len(data) - 1):
		# Get the y-coordinates of the current, previous, and next points
		y_prev = data[i - 1][1]
		y_curr = data[i][1]
		y_next = data[i + 1][1]
		
		# Check if the current y-coordinate is a local minimum
		if y_curr < y_prev and y_curr < y_next:
			# Append the index of the local minimum
			minima_indices.append(data[i][3])  # Use the frame index from the data
			
	return minima_indices

# Example usage
# Assume `data` is a 2D array where each element is [x, y, z, index] for each frame

bottoms = find_wave_bottoms(new_arr)
print("Indices of wave bottoms:", bottoms)
