class MLServiceError(Exception):
    """Base exception class for ML service errors."""
    pass

class APIError(MLServiceError):
    """Exception raised for API-related errors."""
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ModelError(MLServiceError):
    """Exception raised for model-related errors."""
    def __init__(self, message: str, model_id: str = None):
        self.message = message
        self.model_id = model_id
        super().__init__(self.message)

class GenerationError(MLServiceError):
    """Exception raised for content generation errors."""
    def __init__(self, message: str, content_type: str = None):
        self.message = message
        self.content_type = content_type
        super().__init__(self.message)

class ValidationError(MLServiceError):
    """Exception raised for input validation errors."""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

class ResourceError(MLServiceError):
    """Exception raised for resource-related errors."""
    def __init__(self, message: str, resource_type: str = None):
        self.message = message
        self.resource_type = resource_type
        super().__init__(self.message)

class ConfigurationError(MLServiceError):
    """Exception raised for configuration-related errors."""
    def __init__(self, message: str, config_key: str = None):
        self.message = message
        self.config_key = config_key
        super().__init__(self.message) 