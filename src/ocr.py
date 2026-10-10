import os
import easyocr

class LocalOCRProcessor:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)

    def extract_and_chunk_multiple(self, image_paths: list[str], chunk_size: int = 250) -> list[str]:
        all_text_fragments = []
        for index, img_path in enumerate(image_paths):
            results = self.reader.readtext(img_path, detail=0)
            page_text = " ".join(results) if results else ""
            all_text_fragments.append(f"[Source Page/Frame {index + 1}] {page_text}")

            print(f"Finished processing {img_path}")
            os.remove(img_path)

            if "temp_page_" in img_path:
                with open(img_path, 'w') as f:
                    f.write("")

        full_unified_text = " ".join(all_text_fragments)
        words = full_unified_text.split()

        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i + chunk_size]
            chunk_string = " ".join(chunk_words)
            chunks.append(chunk_string)

        return chunks
