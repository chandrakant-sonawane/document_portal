import os
import sys
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import DualStructLogger as CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    """
    Handles document saving and retrieval operations.
    Automatically logs all operations and supports session-based organization.
    """
    def __init__(self, data_dir=None, session_id=None):
        try:
            self.log=CustomLogger().get_logger()
            self.data_dir = data_dir or os.getenv("DATA_STORAGE_PATH", os.path.join(os.getcwd(), "data", "document_analysis"))
            self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            
            # create base session directory
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)
            self.log.info("DocumentHandler initialized", session_id=self.session_id, session_path=self.session_path)
        except Exception as e:
            self.log.error("Error initializing DocumentHandler", error=str(e))
            raise DocumentPortalException("Failed to initialize DocumentHandler", sys)

    def save_pdf(self, uploaded_file):
        try:
            filename = os.path.basename(uploaded_file.name)
            if not filename.lower().endswith('.pdf'):
                raise DocumentPortalException("Uploaded file is not a PDF", sys)
            save_path = os.path.join(self.session_path, filename)
            with open(save_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            self.log.info("PDF saved successfully", file_name=filename, save_path=save_path)
            return save_path
        except Exception as e:
            self.log.error("Error saving PDF", error=str(e))
            raise DocumentPortalException("Failed to save PDF", sys)

    def read_pdf(self, pdf_path: str) -> str:
        try:
            text_chunks = []
            with fitz.open(pdf_path) as doc:
                for page_num, page in enumerate(doc):
                    text = page.get_text()
                    text_chunks.append(f"\n--- Page {page_num + 1} ---\n{text}")
            text = "\n".join(text_chunks)
            self.log.info("PDF read successfully", pdf_path=pdf_path, session_id=self.session_id)
            return text
        except Exception as e:
            self.log.error("Error reading PDF", error=str(e))
            raise DocumentPortalException("Failed to read PDF", sys)

if __name__ == "__main__":
    handler = DocumentHandler()
    print(f"session_id: {handler.session_id}")
    print(f"session_path: {handler.session_path}")
    