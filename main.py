# 🌑 🌒 🌓 🌔 🌕 🌖 🌗 🌘
import cv2
import numpy as np

video_path = 'badApple_h264.mp4'
cellX = 3  # Width of each segment
cellY = 12   # Height of each segment

def getRegionCode(RegionX, RegionY, frame):
    output = ""
    for i in range(0, cellX*4, cellX):  # Combine 4 segments (total width = cellX*4)
        output += getSegmentCode(RegionX, RegionY, i, frame)
    return output

def getSegmentCode(RegionX, RegionY, Segment, frame):
    # Clamp ROI to stay within frame bounds
    roi = frame[
        max(0, RegionY) : min(RegionY + cellY, frame.shape[0]),  # Y bounds
        max(0, RegionX + Segment) : min(RegionX + Segment + cellX, frame.shape[1])  # X bounds
    ]
    white_pixels = np.all(roi > [240, 240, 240], axis=2)  # Detect white pixels (BGR > 240)
    return str(int(np.sum(white_pixels) > 3))  # Threshold: 5+ white pixels = "1"

def mapToEmojiMoon(segmentString):
    # Map 4-segment codes to moon emojis
    if segmentString == "0000":    return "🌑"
    if segmentString == "1000":    return "🌘"
    if segmentString == "1100":    return "🌗"
    if segmentString == "1110":    return "🌖"
    if segmentString == "1111":    return "🌕"
    if segmentString == "0111":    return "🌔"
    if segmentString == "0011":    return "🌓"
    if segmentString == "0001":    return "🌒"
    if segmentString == "1101":    return "🌗"  # Edge cases
    if segmentString == "1011":    return "🌓"
    if segmentString in ["1010", "0101"]: return "🌑"
    return "🌕"  # Fallback for unhandled patterns

# Initialize video capture
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Video resolution: {width}x{height}")

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    display = ""
    # Process frame in cellY x (cellX*4) blocks
    for j in range(0, height - cellY + 1, cellY):  # Rows (Y-axis)
        for i in range(0, width - cellX*4 + 1, cellX*4):  # Columns (X-axis, 4 segments per emoji)
            display += mapToEmojiMoon(getRegionCode(i, j, frame))
        display += "\n"  # Newline after each row
    
    # Optional: Print frame number and sample emoji
    print(f"Frame {frame_count}: {mapToEmojiMoon(getRegionCode(0, 0, frame))}")
    print(display)

    # Display video (optional)
    #cv2.imshow('Frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()
