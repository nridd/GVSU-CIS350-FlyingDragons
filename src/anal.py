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

print(joint_data[1])
print(len(joint_data))

def is_running(joint_data):
	# Indices for left and right ankles in the filtered joint data
	LEFT_ANKLE = 8
	RIGHT_ANKLE = 9
	
	# Variables to track the last ankle with the higher x value and expected alternation
	last_higher_x = None
	last_higher_ankle = None  # Expect None initially, then "left" or "right"
	
	# Loop through each frame to analyze the ankle positions
	for frame in joint_data:
		left_ankle_x = frame[LEFT_ANKLE][0]
		right_ankle_x = frame[RIGHT_ANKLE][0]
		left_ankle_y = frame[LEFT_ANKLE][1]
		right_ankle_y = frame[RIGHT_ANKLE][1]
		
		# Determine which ankle has the higher x-coordinate
		if left_ankle_x > right_ankle_x:
			current_higher_x = "left"
		elif right_ankle_x > left_ankle_x:
			current_higher_x = "right"
		else:
			# If the x-coordinates are the same, it does not meet the criteria
			current_higher_x = "good enough"
		
		# Check if the ankle with the higher x has changed
			#if last_higher_x and current_higher_x != last_higher_x:
		if current_higher_x != last_higher_x:
			#if forward leg has switched:
			if left_ankle_y > right_ankle_y:
				current_higher_ankle = "right"
			elif right_ankle_y > left_ankle_y:
				current_higher_ankle = "left"
			else:
				# If the x-coordinates are the same, it does not meet the criteria
				current_higher_ankle = "good enough"
		
		
		
		if current_higher_ankle == last_higher_ankle:
			last_higher_ankle = current_higher_ankle
			last_higher_x = current_higher_x
			return False
		else:
			last_higher_ankle = current_higher_ankle
			last_higher_x = current_higher_x
			return True

		#print(is_running(joint_data))

def iss_running(joint_data):
	# Indices for left and right ankles in the filtered joint data
	LEFT_ANKLE = 8
	RIGHT_ANKLE = 9
	
	# Track the last forward ankle (based on x-coordinate) and the ankle with the lower y value
	last_higher_x_ankle = None
	last_lower_y_ankle = None  # None initially, then "left" or "right"
	
	# Loop through each frame to analyze the ankle positions
	for frame in joint_data:
		# Get x and y coordinates for left and right ankles
		left_ankle_x = frame[LEFT_ANKLE][0]
		right_ankle_x = frame[RIGHT_ANKLE][0]
		left_ankle_y = frame[LEFT_ANKLE][1]
		right_ankle_y = frame[RIGHT_ANKLE][1]
		
		# Determine which ankle has the higher x-coordinate (forward)
		if left_ankle_x > right_ankle_x:
			current_higher_x_ankle = "left"
		elif right_ankle_x > left_ankle_x:
			current_higher_x_ankle = "right"
		else:
			# If the x-coordinates are the same, this does not meet the criteria
			return False
		
		# Check if the forward ankle has changed (based on x-coordinate)
		if current_higher_x_ankle != last_higher_x_ankle:
			# Determine which ankle has the lower y-coordinate
			if left_ankle_y < right_ankle_y:
				current_lower_y_ankle = "left"
			elif right_ankle_y < left_ankle_y:
				current_lower_y_ankle = "right"
			else:
				# If the y-coordinates are the same, this does not meet the criteria
				return False
			
			# Ensure that the ankle with the lower y-coordinate alternates
			if last_lower_y_ankle and current_lower_y_ankle == last_lower_y_ankle:
				return False  # The lower y ankle didn't alternate as expected
			
			# Update last known states for the next iteration
			last_higher_x_ankle = current_higher_x_ankle
			last_lower_y_ankle = current_lower_y_ankle
			
	# If the function completes without returning False, return True
	return True
print(iss_running(joint_data))

import numpy as np

def all_joints_tracked(joint_data):
	"""
	Checks if all required joints are tracked in every frame.
	
	Parameters:
		joint_data (np.ndarray): 3D array of shape (frames, joints, coordinates).
		
	Returns:
		bool: True if all required joints are tracked in every frame, False otherwise.
	"""
	# Define the adjusted indices for the required joints in the filtered data
	required_joints = list(range(16))  # Joints 0 through 15 in the filtered joint_data
	
	for frame in joint_data:
		for joint_index in required_joints:
			joint_coordinates = frame[joint_index]
			
			# Check if joint is untracked (coordinates are all zeros)
			if np.allclose(joint_coordinates, [0, 0, 0]):
				return False  # Return False if any required joint is untracked
			
	# If all frames and joints pass the check, return True
	return True
#print(all_joints_tracked(joint_data))
#numpy functions
#amazon s3 buckets

import numpy as np



def spcoord(data, x):
	# Initialize a new list to store the results
	new_arr = []
	
	# Loop through each frame in the data
	for index, frame in enumerate(data):
		# Get the (x, y, z) coordinates of the specified joint
		joint_coordinates = frame[x]
		
		# Append the coordinates along with the frame index as an integer
		new_arr.append([joint_coordinates[0], joint_coordinates[1], joint_coordinates[2], index])
		
	return new_arr

# Example usage
# Assume joint_data is your 3D array (frames, joints, coordinates)
new_arr = spcoord(joint_data, 5)
print(new_arr)


for i in new_arr:
	print("(" + str(i[0]) + ", " + str(i[1]) +")")
	#print(len(joint_data[0]))

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

5,16,26

print(str(new_arr[5][0]) + ' ' + str(new_arr[5][3]))
print(str(new_arr[16][0]) + ' ' + str(new_arr[16][3]))
print(str(new_arr[26][0]) + ' ' + str(new_arr[26][3]))