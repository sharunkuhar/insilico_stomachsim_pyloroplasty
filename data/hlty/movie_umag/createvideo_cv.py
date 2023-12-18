import cv2
import glob

png_files = sorted(glob.glob('*.png')) # gets a list of all PNG files in the current directory and sorts them
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # sets the codec for the output video
frame = cv2.imread(png_files[0]) # reads the first frame to get the dimensions
height, width, channels = frame.shape
video = cv2.VideoWriter('movie.mp4', fourcc, 10, (width, height)) # creates a VideoWriter object with the specified codec, frame rate, and dimensions

for png_file in png_files:
    frame = cv2.imread(png_file) # reads the current frame
    video.write(frame) # writes the current frame to the video

video.release() # releases the VideoWriter object
