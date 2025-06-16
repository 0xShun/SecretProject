from celery import shared_task
from typing import Dict, Any
from creative_works.services.summary_service import SummaryService
from creative_works.services.text_to_speech_service import TextToSpeechService
from creative_works.services.cover_photo_generator_service import CoverPhotoGeneratorService
from creative_works.services.hf_api_client import HuggingFaceAPIClient
from creative_works.services.exceptions import GenerationError

# Initialize services
api_client = HuggingFaceAPIClient()
summary_service = SummaryService(api_client)
tts_service = TextToSpeechService(api_client)
cover_photo_service = CoverPhotoGeneratorService(api_client)

@shared_task
def generate_summary(text: str, max_length: int = 130) -> Dict[str, Any]:
    """Celery task for generating text summary."""
    try:
        return summary_service.summarize_text(text, max_length=max_length)
    except Exception as e:
        return {"error": str(e)}

@shared_task
def generate_speech(text: str, output_path: str, format: str = None) -> Dict[str, Any]:
    """Celery task for text-to-speech conversion."""
    try:
        audio_data = tts_service.generate_speech(text)
        tts_service.save_audio(audio_data, output_path, format=format)
        return {"status": "success", "output_path": output_path}
    except Exception as e:
        return {"error": str(e)}

@shared_task
def generate_cover_photo(prompt: str, output_path: str, style: str = "professional", format: str = None) -> Dict[str, Any]:
    """Celery task for cover photo generation."""
    try:
        image = cover_photo_service.generate_cover_photo(prompt, style=style)
        cover_photo_service.save_image(image, output_path, format=format)
        return {"status": "success", "output_path": output_path}
    except Exception as e:
        return {"error": str(e)}

@shared_task
def process_content_batch(content_list: list) -> Dict[str, Any]:
    """
    Celery task for batch processing multiple content items.
    
    Args:
        content_list: List of dictionaries containing content and processing options
        
    Returns:
        Dict containing results for each processed item
    """
    results = []
    for item in content_list:
        try:
            if item.get("type") == "summary":
                result = generate_summary.delay(item["text"], item.get("max_length", 130))
            elif item.get("type") == "speech":
                result = generate_speech.delay(
                    item["text"],
                    item["output_path"],
                    item.get("format")
                )
            elif item.get("type") == "cover_photo":
                result = generate_cover_photo.delay(
                    item["prompt"],
                    item["output_path"],
                    item.get("style", "professional"),
                    item.get("format")
                )
            results.append({"id": item.get("id"), "task_id": result.id})
        except Exception as e:
            results.append({"id": item.get("id"), "error": str(e)})
    
    return {"results": results} 