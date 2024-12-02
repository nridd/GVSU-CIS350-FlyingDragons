#!/usr/bin/env python3
'''
0	7	Left Elbow
1	8	Right Elbow
2	11	Left Shoulder
3	12	Right Shoulder
4	13	Left Hip
5	14	Right Hip
6	23	Left Knee
7	24	Right Knee
8	25	Left Ankle
9	26	Right Ankle
10	27	Left Heel
11	28	Right Heel
12	29	Left Foot Index
13	30	Right Foot Index
14	31	Left Big Toe
15	32	Right Big Toe
16  7   Left Ear
17  8   Right Ear
'''
import cv2
import mediapipe as mp
import numpy as np
#'/Users/nridd/Downloads/Nate.mov'
#'/Users/nridd/Downloads/griffin.mov'

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
#get_jd changes a video path to the a 3d array with the relevent joint data. [frame][joint][x,y,z]
def get_jd(path):
	# Open the video file
	cap = cv2.VideoCapture(path)
	# List of joint indexes to keep
	required_joints = [7, 8, 11, 12, 13, 14, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 3, 4]
	
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
	return joint_data

# Example usage
# Replace 'path/to/video.mp4' with the path to your video file
joint_data = get_jd("/Users/nridd/Downloads/Ben.mov")
#print("Shape of joint data:", joint_data)


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



def spcoord(data, x):
	# takes in joint data 3d array and outputs a 2d array with one joint. [frame][joint][x,y,z] -> (same joint)[frame][x,y,z,frame#]
	new_arr = []
	for index, frame in enumerate(data):
		joint_coordinates = frame[x]
		new_arr.append([joint_coordinates[0], joint_coordinates[1], joint_coordinates[2], index])
	return new_arr

new_arr = spcoord(joint_data, 5)
#print(new_arr)


#for i in new_arr:
	#print("(" + str(i[0]) + ", " + str(i[1]) +")")
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

def find_wave_tops(data):
	"""
	Finds the indices of the top points in a sine-like wave pattern.
	
	Parameters:
		data (list of lists): A 2D array where each element is a list [x, y, z, index] for each frame.
		
	Returns:
		list: A list of indices where the y-coordinate is a local maximum.
	"""
	maxima_indices = []
	
	# Loop through each point, starting from the second point and ending at the second-to-last
	for i in range(1, len(data) - 1):
		# Get the y-coordinates of the current, previous, and next points
		y_prev = data[i - 1][1]
		y_curr = data[i][1]
		y_next = data[i + 1][1]
		
		# Check if the current y-coordinate is a local maximum
		if y_curr > y_prev and y_curr > y_next:
			# Append the index of the local maximum
			maxima_indices.append(data[i][3])  # Use the frame index from the data
			
	return maxima_indices

# Example usage
# Assume `data` is a 2D array where each element is [x, y, z, index] for each frame

tops = find_wave_tops(new_arr)
print("Indices of wave tops:", tops)


# Example usage
# Assume `data` is a 2D array where each element is [x, y, z, index] for each frame

bottoms = find_wave_bottoms(new_arr)
print("Indices of wave bottoms:", bottoms)

#5,16,26

print(str(new_arr[5][0]) + ' ' + str(new_arr[5][3]))
print(str(new_arr[16][0]) + ' ' + str(new_arr[16][3]))
print(str(new_arr[26][0]) + ' ' + str(new_arr[26][3]))

def show_frame_from_video(video_path, frame_number):
	"""
	Displays a specified frame from a video in a popup window.
	
	Parameters:
		video_path (str): The path to the video file.
		frame_number (int): The index of the frame to display.
	"""
	# Open the video file
	cap = cv2.VideoCapture(video_path)
	
	# Check if video opened successfully
	if not cap.isOpened():
		print("Error: Could not open video.")
		return
	
	# Set the frame position
	cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
	
	# Read the specified frame
	ret, frame = cap.read()
	
	# Check if the frame was read successfully
	if not ret:
		print(f"Error: Could not read frame {frame_number}.")
		cap.release()
		return
	
	# Display the frame in a popup window
	window_name = f"Frame {frame_number}"
	cv2.imshow(window_name, frame)
	
	# Wait for a key press to close the window
	print("Press any key to close the popup.")
	cv2.waitKey(0)
	
	# Release the video capture and close the window
	cap.release()
	cv2.destroyAllWindows()
	
# Example usage
# Replace 'path/to/video.mp4' with the path to your video file and specify the frame number
frames_list = [8, 20, 29]
#for i in frames_list:
	#show_frame_from_video('/Users/nridd/Downloads/Ben.mov', i)

def most_front(jd, frames, j1, j2):
	"""
	Finds the frame in which two specified joints are closest to each other on the xy-plane.
	
	Parameters:
		jd (np.ndarray): 3D array of joint data with shape (frames, joints, 3).
		frames (list of int): List of frame indices to check.
		j1 (int): Index of the first joint to compare (default is 0).
		j2 (int): Index of the second joint to compare (default is 1).
		
	Returns:
		int: The frame index from the list `frames` where the two joints are closest.
	"""
	min_distance = float('inf')  # Initialize with a large value
	min_frame = None  # To store the frame with the smallest distance
	
	# Iterate over each specified frame
	for frame in frames:
		# Get the xy-coordinates of both joints in the current frame
		joint1_xy = jd[frame, j1, :2]  # (x, y) coordinates of the first joint
		joint2_xy = jd[frame, j2, :2]  # (x, y) coordinates of the second joint
		
		# Calculate the Euclidean distance between the two joints on the xy-plane
		distance = np.linalg.norm(joint1_xy - joint2_xy)
		print(distance)
		
		# Update the minimum distance and corresponding frame if this distance is smaller
		if distance < min_distance:
			min_distance = distance
			min_frame = frame
			
	return min_frame

# Example usage
# Assuming `joint_data` is your 3D array of joint data and `frames_to_check` is a list of frames



def get_slope(data):
	"""
	Calculates the slope of the ground by finding the angle of the best-fit line
	through the data points over time. The data points should follow a sine wave pattern.

	Parameters:
		data (list of lists): A 2D array where each element is a list [x, y, z, index].
								The 'y' values represent the vertical position over time.

	Returns:
		float: The angle in degrees indicating how much the ground is sloped
				relative to the camera's framing. Positive indicates upward slope.
	"""
	# Extract the time (index) and y-coordinate values
	indices = [point[3] for point in data]  # Time or frame indices
	y_values = [point[1] for point in data]  # Y-coordinates
	
	# Perform a linear regression (line of best fit)
	slope, intercept = np.polyfit(indices, y_values, 1)  # Degree 1 polynomial (linear fit)
	
	# Calculate the angle of the slope in degrees
	angle = np.arctan(slope) * (180 / np.pi)
	
	return angle

# Example usage
# Assume `data` is a 2D array where each element is [x, y, z, index]

slope_angle = get_slope(new_arr)
print("The ground is sloped by {:.2f} degrees.".format(slope_angle))
print(new_arr)




def analyze(path):
	jd = get_jd(path)
	hipr=  spcoord(jd, 5)
	framenum = most_front(jd,find_wave_bottoms(hipr),4,5)
	framedata = jd[framenum]
	slope = get_slope(hipr)
	q1 = a1(slope, framedata)
	#show_frame_from_video(path, framenum)

def anal_image(path):
	framedata = get_jdimage(path)
	q1 = a1(0, framedata)
	



def a1(slope, frame_data):
		"""
		Analyzes posture based on the angle between the shoulder and hip minus the ground slope.

		Parameters:
				slope (float): The slope of the ground in degrees.
				frame_data (2D list): A 2D array representing a selected frame's joint data.
															Should contain [x, y, z] for each joint, with:
															- Left Shoulder at index 2
															- Left Hip at index 4

		Prints:
				The posture analysis and exercise suggestions if needed.
		"""
		# Extract coordinates for the left shoulder and left hip
		left_shoulder = frame_data[3][:2]  # [x, y]
		left_hip = frame_data[5][:2]       # [x, y]
		
		
		relative_angle = calculate_angle(left_shoulder, left_hip, slope)
		# Calculate the angle between shoulder and hip
		#delta_x = left_hip[0] - left_shoulder[0]
		#delta_y = left_hip[1] - left_shoulder[1]
		#angle_shoulder_hip = np.degrees(np.arctan2(delta_y, delta_x))
	
		# Adjust the angle by subtracting the ground slope
		#relative_angle = 220 - angle_shoulder_hip - slope 
	
		# Define the acceptable range
		min_angle = 85
		max_angle = 88
		#97.2-111.6
		#good =   134.34
		#forward = 131.89
		# back  108.63
		# Analyze posture
		print(f"Ground slope: {slope:.2f} degrees")
		print(f"Angle between shoulder and hip (relative to ground): {relative_angle:.2f} degrees")
	
		if relative_angle < min_angle:
				print("Posture analysis: Leaning too far forward.")
				print("Recommendations: Focus on strengthening glutes and back muscles with exercises like:")
				print("- Supermans")
				print("- Glute bridges")
		elif relative_angle > max_angle:
				print("Posture analysis: Leaning too far backward.")
				print("Recommendations: Work on hip flexor strength and mobility exercises like:")
				print("- Hip flexor stretches")
				print("- Dynamic lunges")
		else:
				print("Posture analysis: Good posture!")
			

			#slope = 10  # Example ground slope in degrees
#a1(slope, frame_data)


def get_jdimage(image_path):
	"""
	Extracts joint data from a single image and returns a 2D array of selected joint coordinates.
	
	Parameters:
		image_path (str): Path to the image file.
		
	Returns:
		list: A 2D list where each element is [x, y, z] for each selected joint.
	"""
	# Initialize Mediapipe Pose
	mp_pose = mp.solutions.pose
	
	# List of joint indexes to extract
	required_joints = [7, 8, 11, 12, 13, 14, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 3, 4]
	
	# Read the image
	image = cv2.imread(image_path)
	if image is None:
		print("Error: Could not load image.")
		return None
	
	# Convert the image to RGB
	image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	
	# Initialize Mediapipe Pose
	with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
		# Process the image to detect landmarks
		results = pose.process(image_rgb)
		
		# Check if pose landmarks are detected
		if results.pose_landmarks:
			# Extract the required joints
			joint_data = []
			for joint_index in required_joints:
				joint = results.pose_landmarks.landmark[joint_index]
				joint_data.append([joint.x, joint.y, joint.z])  # Store (x, y, z) coordinates
				
			return joint_data
		else:
			print("Error: No pose landmarks detected in the image.")
			return None
		

def calculate_angle(shoulder, hip, ground_slope=0):
	"""
	Calculates the angle between the shoulder-hip vector and the ground.

	Parameters:
		shoulder (list): [x, y] coordinates of the shoulder.
		hip (list): [x, y] coordinates of the hip.
		ground_slope (float): Slope of the ground in degrees.

	Returns:
		float: Angle in degrees.
	"""
	# Vector from hip to shoulder
	vector1 = [shoulder[0] - hip[0], shoulder[1] - hip[1]]
	
	# Horizontal ground vector (adjusted for slope)
	vector2 = [1, np.tan(np.radians(ground_slope))]  # Unit vector
	
	# Calculate the dot product and magnitudes
	dot_product = np.dot(vector1, vector2)
	magnitude1 = np.linalg.norm(vector1)
	magnitude2 = np.linalg.norm(vector2)
	
	# Calculate the angle (in radians)
	angle_radians = np.arccos(dot_product / (magnitude1 * magnitude2))
	
	# Convert to degrees
	return np.degrees(angle_radians)






















print('reset')
print('reset')
print('reset')
print('reset')
print('reset')
print('Natey')
analyze('/Users/nridd/Downloads/Nate.mov')
print('reset')
print('reset')
print('G Dawg')
analyze('/Users/nridd/Downloads/ogriff.mov')
print('reset')
print('reset')
print('Benny boy')
analyze('/Users/nridd/Downloads/Ben.mov')
print('reset')
print('reset')

