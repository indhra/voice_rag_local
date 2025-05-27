import os 
import whisper 
import chromadb
from sentence_transformers import SentenceTransformer
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter


AUDIO_FILE = "user_input.wav"
RESPONSE_AUDIO_FILE = "response.wav"
PDF_FILE = "Insurance_Handbook_20103.pdf"
SAMPLE_RATE = 16000
WAKE_WORD = "Hi"
SIMILARITY_THRESHOLD = 0.4
MAX_ATTEMPTS = 5
