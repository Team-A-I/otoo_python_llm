import cv2
import numpy as np
import re
from models.ocr_processor import MyPaddleOCR

class ImageProcessor:
    def __init__(self):
        self.ocr = MyPaddleOCR()

    def check_guideline(self, point, top_left, bottom_right):
        x, y = point
        x_min, y_min = top_left
        x_max, y_max = bottom_right
        return x_min <= x <= x_max and y_min <= y <= y_max

    def get_bounding_boxes(self, contours, margin=150, direction='left'):
        bounding_boxes = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if direction == 'left':
                x = max(0, x - margin)
            w += margin
            h += 10
            bounding_boxes.append((x, y, x + w, y + h))
        return bounding_boxes

    def extract_text_from_boxes(self, boxes, ocr_results):
        text_list = []
        for box in boxes[::-1]:
            result = []
            for points, text in ocr_results:
                all_inrange = all(self.check_guideline(point, box[1], box[3]) for point in points)
                if all_inrange:
                    result.append(text[0])
            text_list.append(" ".join(result))
        return text_list

    def draw_bounding_boxes(self, image, boxes, color):
        for box in boxes:
            x1, y1, x2, y2 = box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    async def process_image(self, img_bytes):
        try:
            # Use the existing OCR object
            ocr_result = await self.ocr.run_ocr(img_bytes)
            if ocr_result is None:
                raise Exception("Failed to perform OCR")

            # Load and preprocess image
            image = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

            # Convert to HSV and create masks
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            yellow_lower = np.array([25, 150, 150])
            yellow_upper = np.array([30, 255, 255])
            white_lower = np.array([0, 0, 250])
            white_upper = np.array([180, 5, 255])

            mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
            mask_white = cv2.inRange(hsv, white_lower, white_upper)

            # Find contours
            contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_white, _ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if not contours_yellow and not contours_white:
                raise Exception("No yellow or white contours found")

            # Get bounding boxes
            yellow_boxes = self.get_bounding_boxes(contours_yellow, direction='left')
            white_boxes = self.get_bounding_boxes(contours_white, direction='right')

            if not yellow_boxes and not white_boxes:
                raise Exception("No yellow or white bounding boxes found")

            # Draw bounding boxes
            image_with_boxes = image.copy()
            self.draw_bounding_boxes(image_with_boxes, yellow_boxes, (0, 0, 255))
            self.draw_bounding_boxes(image_with_boxes, white_boxes, (100, 36, 100))

            # Extract text from boxes
            yellow_coords = [["yellow", (x1, y1), (x2, y1), (x2, y2), (x1, y2)] for x1, y1, x2, y2 in yellow_boxes]
            white_coords = [["white", (x1, y1), (x2, y1), (x2, y2), (x1, y2)] for x1, y1, x2, y2 in white_boxes]

            yellow_text = self.extract_text_from_boxes(yellow_coords, ocr_result)
            white_text = self.extract_text_from_boxes(white_coords, ocr_result)

            if not yellow_text and not white_text:
                raise Exception("No text found in yellow or white boxes")

            return image_with_boxes, white_text, yellow_text
        except Exception as e:
            print(f"Error processing image: {e}")
            return None, [], []

    async def process_images(self, image_files):
        all_white_text = []
        all_yellow_text = []

        for image_file in image_files:
            img_bytes = await image_file.read()
            image_with_boxes, white_text, yellow_text = await self.process_image(img_bytes)
            
            if image_with_boxes is not None:
                all_white_text.extend(white_text)
                all_yellow_text.extend(yellow_text)
            else:
                raise ValueError("No valid image with boxes found")

        all_white_text = [re.sub(r'크{2,}', 'ㅋㅋ', text) for text in all_white_text if text.strip()]
        all_yellow_text = [re.sub(r'크{2,}', 'ㅋㅋ', text) for text in all_yellow_text if text.strip()]

        return all_white_text, all_yellow_text
