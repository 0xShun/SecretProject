import os
from typing import Dict, Any

# API Configuration
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
API_TIMEOUT = 30  # seconds
MAX_RETRIES = 3

# Model Configurations
MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
    # Text Generation Models
    "text_generation": {
        "default_model": "gpt2",
        "max_length": 100,
        "temperature": 0.7,
        "top_p": 0.9,
    },
    
    # Summarization Models
    "summarization": {
        "default_model": "facebook/bart-large-cnn",
        "max_length": 130,
        "min_length": 30,
        "do_sample": False,
    },
    
    # Text-to-Speech Models
    "text_to_speech": {
        "default_model": "facebook/fastspeech2-en-ljspeech",
        "sample_rate": 22050,
        "speaker_id": 0,
    },
    
    # Image Generation Models
    "image_generation": {
        "default_model": "stabilityai/stable-diffusion-2-1",
        "width": 1024,
        "height": 768,
        "num_inference_steps": 50,
        "guidance_scale": 7.5,
    }
}

# Style Configurations
STYLE_CONFIGS: Dict[str, Dict[str, str]] = {
    "professional": {
        "prompt_suffix": "professional photography, high quality, detailed, 4k, sharp focus",
        "negative_prompt": "blurry, low quality, distorted, amateur",
    },
    "artistic": {
        "prompt_suffix": "artistic style, creative composition, vibrant colors, painterly",
        "negative_prompt": "photorealistic, plain, boring, simple",
    },
    "minimal": {
        "prompt_suffix": "minimalist design, clean lines, simple composition, white space",
        "negative_prompt": "busy, cluttered, complex, detailed",
    }
}

# Output Configurations
OUTPUT_CONFIGS = {
    "image_formats": ["PNG", "JPEG", "WEBP"],
    "audio_formats": ["WAV", "MP3"],
    "default_image_format": "PNG",
    "default_audio_format": "WAV",
    "max_file_size": 10 * 1024 * 1024,  # 10MB
}

# Cache Configuration
CACHE_CONFIG = {
    "enabled": True,
    "ttl": 3600,  # 1 hour
    "max_size": 1000,  # Maximum number of cached items
}

# Rate Limiting
RATE_LIMIT_CONFIG = {
    "requests_per_minute": 60,
    "burst_limit": 10,
}

def get_model_config(model_type: str) -> Dict[str, Any]:
    """Get configuration for a specific model type."""
    return MODEL_CONFIGS.get(model_type, {})

def get_style_config(style: str) -> Dict[str, str]:
    """Get configuration for a specific style."""
    return STYLE_CONFIGS.get(style, STYLE_CONFIGS["professional"]) 