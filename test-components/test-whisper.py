# !pip install git+https://github.com/openai/whisper.git 
import whisper

model = whisper.load_model("base.en")
result = model.transcribe("test1.mp3")
print(result["text"])