from typing import Dict, Any, Optional
from creative_works.services.hf_api_client import HuggingFaceAPIClient
from creative_works.services.exceptions import GenerationError
from creative_works.services.config import get_model_config, OUTPUT_CONFIGS
import base64

class TextToSpeechService:
    def __init__(self, api_client: HuggingFaceAPIClient):
        self.api_client = api_client
        self.config = get_model_config("text_to_speech")
        self.default_model = self.config.get("default_model", "facebook/fastspeech2-en-ljspeech")

    def generate_speech(self, 
                       text: str, 
                       model_id: Optional[str] = None,
                       speaker_id: Optional[int] = None,
                       **kwargs) -> bytes:
        """
        Convert text to speech using the specified model.
        
        Args:
            text: The text to convert to speech
            model_id: Optional model ID to override the default
            speaker_id: Optional speaker ID for multi-speaker models
            **kwargs: Additional parameters for the model
            
        Returns:
            bytes: The generated audio data
        """
        try:
            model = model_id or self.default_model
            payload = {
                "inputs": text,
                "parameters": {
                    "speaker_id": speaker_id or self.config.get("speaker_id", 0),
                    "sample_rate": self.config.get("sample_rate", 22050),
                    **kwargs
                }
            }
            
            result = self.api_client.generate_text(
                model_id=model,
                prompt=text,
                **payload
            )
            
            # Convert base64 audio to bytes if needed
            if isinstance(result, dict) and "audio" in result:
                return base64.b64decode(result["audio"])
            return result
            
        except Exception as e:
            raise GenerationError(f"Error during text-to-speech conversion: {str(e)}", content_type="speech")

    def save_audio(self, audio_data: bytes, filepath: str, format: str = None) -> None:
        """
        Save the generated audio data to a file.
        
        Args:
            audio_data: The audio data in bytes
            filepath: Path where to save the audio file
            format: Audio format (WAV, MP3, etc.)
        """
        try:
            format = format or OUTPUT_CONFIGS["default_audio_format"]
            if format not in OUTPUT_CONFIGS["audio_formats"]:
                raise ValueError(f"Unsupported audio format: {format}")
                
            with open(filepath, 'wb') as f:
                f.write(audio_data)
        except Exception as e:
            raise GenerationError(f"Error saving audio file: {str(e)}", content_type="speech") 