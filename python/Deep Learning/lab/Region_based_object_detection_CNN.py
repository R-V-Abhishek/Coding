import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import cv2
tf.get_logger().setLevel('ERROR')

MODEL_URL = "https://tfhub.dev/tensorflow/efficientdet/d0/1"
detector = hub.load(MODEL_URL)

def detect_objects(image_path, detector):
    # Load and preprocess image
    image = cv2.imread(image_path)
    orig_image = image.copy()
    input_tensor = tf.convert_to_tensor(image)
    input_tensor = input_tensor[tf.newaxis, ...]

    # Run object detection
    detections = detector(input_tensor)

    # Extract detection results
    num_detections = int(detections["num_detections"])
    detection_boxes = detections["detection_boxes"].numpy()[0]
    detection_classes = detections["detection_classes"].numpy()[0].astype(np.int32)
    detection_scores = detections["detection_scores"].numpy()[0]

    confidence_threshold = 0.5
    for i in range(num_detections):
        score = detection_scores[i]
        if score > confidence_threshold:
            box = detection_boxes[i]

            # Convert box coordinates to pixel values
            h, w, _ = orig_image.shape
            y_min, x_min, y_max, x_max = box
            x_min, x_max = int(x_min * w), int(x_max * w)
            y_min, y_max = int(y_min * h), int(y_max * h)

            label = f"Object {detection_classes[i]}: {score:.2f}"
            cv2.rectangle(orig_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(orig_image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

       
    return orig_image

image_path = "Deep Learning/parcel-box-multiple-delivery-boxes-placed-in-a-3d-illustration-on-white-background_9849571.webp"  # Replace with your image path
result_image = detect_objects(image_path, detector)

cv2.imshow('Detected Objects', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()