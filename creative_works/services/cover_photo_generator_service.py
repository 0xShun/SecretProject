from typing import Dict, Any, Optional
from creative_works.services.hf_api_client import HuggingFaceAPIClient
from creative_works.services.exceptions import GenerationError
from creative_works.services.config import get_model_config, get_style_config, OUTPUT_CONFIGS
import io
from PIL import Image

class CoverPhotoGeneratorService:
    def __init__(self, api_client: HuggingFaceAPIClient):
        self.api_client = api_client
        self.config = get_model_config("image_generation")
        self.default_model = self.config.get("default_model", "stabilityai/stable-diffusion-2-1")

    def generate_cover_photo(self,
                           prompt: str,
                           model_id: Optional[str] = None,
                           width: int = None,
                           height: int = None,
                           style: str = "professional",
                           **kwargs) -> Image.Image:
        """
        Generate a cover photo based on the given prompt.
        
        Args:
            prompt: The text prompt describing the desired image
            model_id: Optional model ID to override the default
            width: Width of the generated image
            height: Height of the generated image
            style: Style of the image (professional, artistic, minimal)
            **kwargs: Additional parameters for the model
            
        Returns:
            PIL.Image.Image: The generated image
        """
        try:
            model = model_id or self.default_model
            style_config = get_style_config(style)
            
            # Enhance prompt with style-specific additions
            enhanced_prompt = f"{prompt}, {style_config['prompt_suffix']}"
            
            # Set default dimensions from config if not provided
            width = width or self.config.get("width", 1024)
            height = height or self.config.get("height", 768)
            
            payload = {
                "inputs": enhanced_prompt,
                "parameters": {
                    "width": width,
                    "height": height,
                    "negative_prompt": style_config["negative_prompt"],
                    "num_inference_steps": self.config.get("num_inference_steps", 50),
                    "guidance_scale": self.config.get("guidance_scale", 7.5),
                    **kwargs
                }
            }
            
            image_data = self.api_client.generate_image(
                model_id=model,
                prompt=enhanced_prompt,
                **payload
            )
            
            return Image.open(io.BytesIO(image_data))
            
        except Exception as e:
            raise GenerationError(f"Error generating cover photo: {str(e)}", content_type="image")

    def save_image(self, image: Image.Image, filepath: str, format: str = None) -> None:
        """
        Save the generated image to a file.
        
        Args:
            image: The PIL Image object to save
            filepath: Path where to save the image
            format: Image format (PNG, JPEG, etc.)
        """
        try:
            format = format or OUTPUT_CONFIGS["default_image_format"]
            if format not in OUTPUT_CONFIGS["image_formats"]:
                raise ValueError(f"Unsupported image format: {format}")
                
            image.save(filepath, format=format)
        except Exception as e:
            raise GenerationError(f"Error saving image: {str(e)}", content_type="image")

    def enhance_prompt(self, base_prompt: str, style: str = "professional") -> str:
        """
        Enhance the base prompt with style-specific additions.
        
        Args:
            base_prompt: The original prompt
            style: The desired style (professional, artistic, minimal, etc.)
            
        Returns:
            str: Enhanced prompt
        """
        style_prompts = {
            "professional": "professional photography, high quality, detailed, 4k, sharp focus",
            "artistic": "artistic style, creative composition, vibrant colors, painterly",
            "minimal": "minimalist design, clean lines, simple composition, white space"
        }
        
        style_addition = style_prompts.get(style.lower(), style_prompts["professional"])
        return f"{base_prompt}, {style_addition}" 