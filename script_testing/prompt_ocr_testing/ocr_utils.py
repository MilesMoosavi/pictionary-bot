import cv2
import numpy as np
import pytesseract
import os

def detect_underscores_and_letters(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not open or find the image: {image_path}")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    # Dilate to combine close contours
    kernel = np.ones((2,2), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    
    # Save the preprocessed image
<<<<<<< Updated upstream
    preprocessed_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'preprocessed.png')
=======
    preprocessed_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'preprocessed.png')
>>>>>>> Stashed changes
    cv2.imwrite(preprocessed_image_path, binary)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_elements = []
    recognized_text = ""
    
    # Iterate over contours to detect underscores and letters
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        
        if aspect_ratio > 3 and h < 20:  # Improved underscore detection
            detected_elements.append((x, y, w, h, '_', 100))  # Assume 100% confidence for underscores
            recognized_text += "_"
        else:
            # Combine close vertical contours
            close_contours = [contour]
            for other_contour in contours:
                if other_contour is not contour:
                    ox, oy, ow, oh = cv2.boundingRect(other_contour)
                    if abs(ox - x) < w and abs(oy - (y + h)) < 20:  # Adjust the vertical threshold as needed
                        close_contours.append(other_contour)

            # Create a combined bounding box for close contours
            combined_x, combined_y, combined_w, combined_h = cv2.boundingRect(np.vstack(close_contours))
            padding = 10
            combined_x, combined_y, combined_w, combined_h = max(0, combined_x-padding), max(0, combined_y-padding), combined_w+2*padding, combined_h+2*padding
            roi = gray[combined_y:combined_y+combined_h, combined_x:combined_x+combined_w]

            # Additional preprocessing on ROI
            roi = cv2.GaussianBlur(roi, (3, 3), 0)
            _, roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Use image_to_data to get detailed OCR results including confidence
            config = '--psm 8'  # Single word mode for better character recognition
            data = pytesseract.image_to_data(roi, config=config, output_type=pytesseract.Output.DICT)
            text = ""
            confidence = 0
            n_boxes = len(data['text'])
            for i in range(n_boxes):
                if int(data['conf'][i]) > 0:  # Filter out negative confidences
                    text += data['text'][i]
                    confidence += int(data['conf'][i])

            if text.strip() and confidence / len(text) > 50:  # Only keep text with average confidence above 50
                avg_conf = confidence / len(text)
                detected_elements.append((combined_x, combined_y, combined_w, combined_h, text.strip(), avg_conf))
                recognized_text += text.strip()
    
    # Sort detected elements by x-coordinate
    detected_elements.sort(key=lambda elem: elem[0])

    # Filter out false positives for 'I'
    filtered_elements = []
    for elem in detected_elements:
        if elem[4] == 'I' and elem[3] > elem[2]:  # Remove if height is greater than width (likely a false I)
            continue
        filtered_elements.append(elem)

    # Construct the recognized text in order
    recognized_text = "".join([elem[4] for elem in filtered_elements])
    
    # Draw detected elements on the image
    for (x, y, w, h, elem, conf) in filtered_elements:
        if elem != 'I' and elem != '.':  # Avoid drawing uppercase I or period if it overlaps with lowercase i
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, elem, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    # Save the result image to be displayed in the GUI
    result_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'result_with_confidence.png')
    cv2.imwrite(result_image_path, image)

    return filtered_elements, recognized_text, result_image_path, preprocessed_image_path, image_path
