import sys
from pathlib import Path
import fitz
from logger.custom_logger import DualStructLogger as CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    def __init__(self):
        self.log = CustomLogger().get_logger()

    def delete_existing_files(self):
        """
        Deletes existing files at the specified paths.
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error occurred while deleting existing files:", error=str(e))
            raise DocumentPortalException("Error occurred while deleting existing files.", sys)

     
    def save_uploaded_files(self):
        """
        Saves uploaded files to a specific directory.
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error occurred while saving uploaded files:", error=str(e))
            raise DocumentPortalException("Error occurred while saving uploaded files.", sys)

    def read_pdf(self):
        """
        Reads a PDF file and extracts text from each page.
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error occurred while reading PDF:", error=str(e))
            raise DocumentPortalException("Error occurred while reading PDF.", sys)
