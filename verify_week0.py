import torch
print("torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A"
print("GPU:", gpu_name)

from transformers import pipeline
device = 0 if torch.cuda.is_available() else -1
print(f"Running pipeline on device={device} ...")
generator = pipeline("text-generation", model="gpt2", device=device)
out = generator("The future of AI is", max_new_tokens=20)
print("GENERATED:", out[0]["generated_text"])
print("PIPELINE_OK")
