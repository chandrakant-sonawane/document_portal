import os
import sys
from typing import Any
from dotenv import load_dotenv
from utils.config_loader import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from logger.custom_logger import DualStructLogger as CustomLogger
from exception.custom_exception import DocumentPortalException

log = CustomLogger().get_logger()

class ModelLoader:
    """
    A utility class for loading and managing language models.

    This class handles the loading of:
    1. Embedding models (for converting text to vectors)
    2. Language Models (LLMs) for text generation

    Attributes:
        config (dict): Configuration settings loaded from config file
        api_keys (dict): Dictionary containing API keys for different services
    """
    
    def __init__(self):
        """
        Initialize the ModelLoader with necessary configurations and API keys.
        Raises:
            DocumentPortalException: If required environment variables are missing
        """
        load_dotenv()
        self._validate_env()
        self.config = load_config()
        log.info("Configuration loaded successfully", config_keys=list(self.config.keys()))
        
    def _validate_env(self):
        """
        Validate necessary environment variables.
        Ensure API keys exist.
        """
        required_vars=["GOOGLE_API_KEY","GROQ_API_KEY"]
        self.api_keys={key:os.getenv(key) for key in required_vars}
        missing = [k for k, v in self.api_keys.items() if not v]
        if missing:
            log.error("Missing environment variables", missing_vars=missing)
            raise DocumentPortalException("Missing environment variables", sys)
        log.info("Environment variables validated", available_keys=[k for k in self.api_keys if self.api_keys[k]])

    def load_embeddings(self) -> Any:
        """Load embeddings."""

        try:
            log.info("Loading embedding model...")
            embedding_model = self.config.get("embedding_model").get("model_name")
            return GoogleGenerativeAIEmbeddings(model=embedding_model)

        except Exception as e:
            log.error(f"Error loading embedding model for {embedding_model}: {str(e)}")
            raise DocumentPortalException(f"Failed to load embedding model for {embedding_model}: {str(e)}", sys) from e

    def load_llm(self):
        """
        Load and initialize the Language Model based on configuration.

        Supported providers:
        - google: Uses Google's generative AI models
        - groq: Uses Groq's language models

        Returns:
            Union[ChatGoogleGenerativeAI, ChatGroq]: Initialized language model

        Raises:
            ValueError: If specified provider is not supported or configuration is invalid
        """
        llm_block = self.config["llm"]
        provider_key = os.getenv("LLM_PROVIDER", "groq")

        if provider_key not in llm_block:
            log.error("LLM provider not found in config", provider_key=provider_key)
            raise ValueError(f"Provider '{provider_key}' not found in config")

        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        max_tokens = llm_config.get("max_output_tokens", 2048)
        
        log.info("Loading LLM", provider=provider, model=model_name, 
                temperature=temperature, max_tokens=max_tokens)

        if provider == "google":
            return ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        elif provider == "groq":
            return ChatGroq(
                model=model_name,
                api_key=self.api_keys["GROQ_API_KEY"],
                temperature=temperature,
            )
        else:
            log.error("Unsupported LLM provider", provider=provider)
            raise ValueError(f"Unsupported LLM provider: {provider}")

    
if __name__ == "__main__":
    loader = ModelLoader()
    
    # Test embedding model loading
    embeddings = loader.load_embeddings()
    print(f"Embedding Model Loaded: {embeddings}")
    
    # Test the ModelLoader
    result=embeddings.embed_query("Hello, how are you?")
    print(f"Embedding Result: {result}")
    
    # Test LLM loading based on YAML config
    llm = loader.load_llm()
    print(f"LLM Loaded: {llm}")
    
    # Test the ModelLoader
    result=llm.invoke("Hello, how are you?")
    print(f"LLM Result: {result.content}")