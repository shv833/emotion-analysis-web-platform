from fer import FER
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import imageio
import matplotlib
import time
import mss
import mss.tools


# Set the backend for matplotlib to 'TkAgg' for compatibility with different environments
matplotlib.use("TkAgg")

# Initialize the FER (Face Emotion Recognition) detector using MTCNN
detector = FER(mtcnn=True)

# Set a frame rate for recording the video (adjust based on your capturing capabilities)
frame_rate = 4.3

# Initialize OpenCV's VideoWriter to save the video with the specified frame rate
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("emotion_video.avi", fourcc, frame_rate, (1920, 1080))

# Set up a matplotlib figure for displaying live emotion detection results
plt.ion()  # Turn on interactive mode for live updates
fig, ax = plt.subplots()
emotion_labels = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
bars = ax.bar(emotion_labels, [0] * 7, color="lightblue")  # Initialize bars for each emotion
plt.ylim(0, 1)
plt.ylabel("Confidence")
plt.title("Real-time Emotion Detection")
ax.set_xticklabels(emotion_labels, rotation=45)

# Initialize imageio writer to save live chart updates as a GIF
gif_writer = imageio.get_writer("emotion_chart.gif", mode="I", duration=0.1)

# List to store cumulative emotion statistics for each frame
emotion_statistics = []


# Function to update the live chart
def update_chart(cumulative_emotions, bars, ax, fig):
    # Clear the current axes and set up the bar chart again
    ax.clear()
    ax.bar(emotion_labels, [cumulative_emotions.get(emotion, 0) for emotion in emotion_labels], color="lightblue")
    plt.ylim(0, 1)
    plt.ylabel("Confidence")
    plt.title("Real-time Emotion Detection")
    ax.set_xticklabels(emotion_labels, rotation=45)
    fig.canvas.draw()
    fig.canvas.flush_events()


# Start the timer to measure the active time of the screen capture
screen_capture_start_time = time.time()

# Initialize screen capture using mss
sct = mss.mss()
monitor = sct.monitors[1]  # Capture the first monitor

try:
    while True:
        # Capture the screen
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)

        # Convert the frame from BGRA to BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Detect emotions on the frame
        results = detector.detect_emotions(frame)
        cumulative_emotions = {emotion: 0 for emotion in emotion_labels}

        # Loop through all detected faces
        for face in results:
            box = face["box"]
            current_emotions = face["emotions"]

            # Add current emotions to cumulative emotions
            for emotion, score in current_emotions.items():
                cumulative_emotions[emotion] += score

            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            emotion_type = max(current_emotions, key=current_emotions.get)
            emotion_score = current_emotions[emotion_type]

            emotion_text = f"{emotion_type}: {emotion_score:.2f}"
            cv2.putText(frame, emotion_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Store the emotion data
            emotion_statistics.append(current_emotions)

        update_chart(cumulative_emotions, bars, ax, fig)

        out.write(frame)  # Write the frame to the video file

        # Save the current state of the bar chart as a frame in the GIF
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        gif_writer.append_data(image)

        cv2.imshow("Emotion Detection", frame)  # Display the frame

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    screen_capture_end_time = time.time()  # End timer when screen capture window closes
    print(f"Screen capture active time: {screen_capture_end_time - screen_capture_start_time:.2f} seconds")

    cv2.destroyAllWindows()
    plt.close(fig)

    out.release()
    gif_writer.close()

    emotion_df = pd.DataFrame(emotion_statistics)

    plt.figure(figsize=(10, 10))
    for emotion in emotion_labels:
        plt.plot(emotion_df[emotion].cumsum(), label=emotion)
    plt.title("Cumulative Emotion Statistics Over Time")
    plt.xlabel("Frame")
    plt.ylabel("Cumulative Confidence")
    plt.legend()
    plt.savefig("cumulative_emotions.jpg")
    plt.close()
