from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile
from IPython.display import Audio, display 

# --- Section 3: Load the Waray-Waray TTS model and tokenizer ---
model_name = "facebook/mms-tts-war"

try:
    # Load the VITS model. VITS (Variational Inference with adversarial learning for
    # end-to-end Text-to-Speech) is an end-to-end speech synthesis model.
    model = VitsModel.from_pretrained(model_name)
    # Load the tokenizer associated with the model. The tokenizer converts text
    # into numerical inputs that the model can understand.
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("Model and tokenizer loaded successfully!")
except Exception as e:
    print(f"Error loading model or tokenizer: {e}")
    print("Please ensure you have an active internet connection and the model name is correct.")
    # Exit or handle error appropriately if model loading fails

waray_text = "Maupay na adlaw mga real niggas. Pangaon na kamo"