import cv2 as cv
import numpy as np
import sys
from pdf2image import convert_from_path

class IngestionRouter:
    def __init__(self):
        pass

    def capture_from_webcam(self, output_path="captured_document.png") -> list[str]:
        cap = cv.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            gray_preview = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cv.imshow('Press spacebar to scan the document:', gray_preview)

            key = cv.waitKey(1)
            if key == 32:  
                blurred = cv.GaussianBlur(gray_preview, (5, 5), 0)
                adaptive_thresh = cv.adaptiveThreshold(
                    blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2
                )
                cv.imwrite(output_path, adaptive_thresh)
                cap.release()
                cv.destroyAllWindows()
                return [output_path]
            elif key == 27:  
                cap.release()
                cv.destroyAllWindows()
                sys.exit()

    def process_pdf(self, pdf_path: str) -> list[str]:
        pages = convert_from_path(pdf_path, dpi=200)
        saved_page_paths = []
        for idx, page in enumerate(pages):
            page_filename = f"src/temp_page_{idx}.png"
            open_cv_image = np.array(page)
            gray_img = cv.cvtColor(open_cv_image, cv.COLOR_RGB2GRAY)
            cv.imwrite(page_filename, gray_img)
            saved_page_paths.append(page_filename)
        return saved_page_paths

    def get_ingestion_source(self):
        choice = input("Enter choice (Scan document with webcam [1], Upload document file path [2], or Query the LLM [3]):  ")
        if choice == "1":
            return self.capture_from_webcam(), "document"
        elif choice == "2":
            file_path = input("Input the file path of the .pdf: ")
            if file_path.endswith('.pdf'):
                return self.process_pdf(file_path), "document"
            else:
                return [file_path], "document"
        elif choice == "3":
            return [], "direct_chat"
