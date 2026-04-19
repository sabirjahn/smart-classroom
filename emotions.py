import cv2
from deepface import DeepFace
import numpy as np
import os
from datetime import datetime

def detect_emotion(frame):
    """
    Detect the dominant emotion from a provided image frame.

    Args:
        frame: numpy array (BGR image)

    Returns:
        str: The dominant emotion detected, or None if no faces/emotions were detected
    """
    try:
        if frame is None:
            print("Error: No frame provided")
            return None

        # Analyze emotions using DeepFace
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # Count emotions across all detected faces
        emotion_counts = {}

        # Handle both single face and multiple faces
        if isinstance(result, list):
            faces = result
        else:
            faces = [result]

        for face in faces:
            dominant_emotion = face['dominant_emotion']
            emotion_counts[dominant_emotion] = emotion_counts.get(dominant_emotion, 0) + 1

        # Determine the dominant emotion overall
        if emotion_counts:
            dominant_emotion = max(emotion_counts, key=emotion_counts.get)
            print(f"Dominant emotion detected: {dominant_emotion}")
            return dominant_emotion
        else:
            print("No emotions detected")
            return None

    except Exception as e:
        print(f"Error in emotion detection: {str(e)}")
        return None

def detect_emotion_detailed(frame):
    """
    Detect emotions with detailed information from a provided image frame.

    Args:
        frame: numpy array (BGR image)

    Returns:
        dict: Detailed emotion data including confidence, face count, and image path
    """
    try:
        if frame is None:
            print("Could not capture frame from any source")
            return None

        # Save captured image
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_filename = f"capture_{timestamp}.jpg"
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        os.makedirs(static_dir, exist_ok=True)
        image_path = os.path.join(static_dir, image_filename)
        
        # Save the original frame
        cv2.imwrite(image_path, frame)

        # Analyze emotions using DeepFace
        try:
            # enforce_detection=True qilinadi, shunda odam bo'lmasa xato (exception) beradi
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=True)
        except ValueError:
            # Agar yuz topilmasa DeepFace ValueError beradi, shuni ushlaymiz
            print("Human not available")
            return {
                'emotion': 'Human not available',
                'confidence': 0.0,
                'face_count': 0,
                'image_path': image_filename
            }

        # Process results
        emotion_counts = {}
        total_confidence = 0
        face_count = 0

        # Handle both single face and multiple faces
        if isinstance(result, list):
            faces = result
        else:
            faces = [result]

        face_count = len([face for face in faces if 'emotion' in face])

        for face in faces:
            if 'emotion' in face:
                dominant_emotion = face['dominant_emotion']
                emotion_counts[dominant_emotion] = emotion_counts.get(dominant_emotion, 0) + 1

                # Get confidence for the dominant emotion
                if dominant_emotion in face['emotion']:
                    total_confidence += face['emotion'][dominant_emotion]

        # Determine the dominant emotion overall
        if emotion_counts:
            dominant_emotion = max(emotion_counts, key=emotion_counts.get)
            avg_confidence = total_confidence / len([f for f in faces if 'emotion' in f]) if faces else 0

            print(
                f"Dominant emotion detected: {dominant_emotion} (Confidence: {avg_confidence:.1f}%, Faces: {face_count})")

            return {
                'emotion': dominant_emotion,
                'confidence': float(avg_confidence),  # Convert numpy float to Python float
                'face_count': int(face_count),  # Convert to Python int
                'image_path': image_filename  # Return relative path for static serving
            }
        else:
            print("Human not available")
            return {
                'emotion': 'Human not available',
                'confidence': 0.0,
                'face_count': 0,
                'image_path': image_filename
            }

    except Exception as e:
        print(f"Error in detailed emotion detection: {str(e)}")
        return None

def get_emotion_color(emotion):
    """
    Returns a color (BGR format) associated with each emotion for visualization
    
    Args:
        emotion (str): Detected emotion
        
    Returns:
        tuple: BGR color values
    """
    emotion_colors = {
        'happy': (0, 255, 255),    # Yellow
        'sad': (255, 0, 0),        # Blue
        'angry': (0, 0, 255),      # Red
        'fear': (255, 0, 255),     # Magenta
        'surprise': (0, 255, 0),   # Green
        'neutral': (255, 255, 255), # White
        'disgust': (0, 165, 255),   # Orange
        'Human not available': (128, 128, 128),  # Gray for no human
        'human not available': (128, 128, 128)  # Gray (lowercase fallback)
    }
    
    return emotion_colors.get(emotion, (200, 200, 200))  # Default gray