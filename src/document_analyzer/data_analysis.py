import os
from utils.model_loader import ModelLoader
from logger.custom_logger import DualStructLogger as CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentAnalyzer:
    """
    Analyzes documents using a pre-trained model.
    Automatically logs all operations and supports session-based organization.
    """
    def __init__(self):
        pass
    
    def analyze_document(self):
        pass
    