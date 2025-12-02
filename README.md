# 🔥 DarkVoice – Advanced Audio Steganography Tool  
#### Created by: **HasnainDarkNet**
<img width="610" height="148" alt="Capture" src="https://github.com/user-attachments/assets/8fd4588e-f260-43f1-ae2c-4a56c8c72421" />

DarkVoice is a professional audio-steganography tool designed to hide secret text messages inside WAV audio files using LSB (Least Significant Bit) encoding.
----
### Convert Any Audio to Proper WAV (PCM 16-bit)
```
 ffmpeg -i YOUR_AUDIO.wav -acodec pcm_s16le -ar 44100 fixed.wav
 ```
---

✔ Supports **two modes**:  
1️⃣ **Normal Mode** – hide message without any key.  
2️⃣ **Encrypted Mode** – hide message using strong SHA-256 key-based encryption  

Perfect for cybersecurity researchers, steganography learners, and privacy enthusiasts.

---

## ✨ Features

- 🎧 Hide secret text inside WAV audio  
- 🔐 Optional encryption using custom key  
- 🔓 Decrypt with or without key  
- ⚡ Ultra-fast LSB processing  
- 💡 Fully open-source  
- 🖥 Clean Golden Terminal Banner (DarkVoice Branding)

---


## 📌 Requirements

- Python 3.8+
- Standard library (no extra installation)


---

## 🧪 How It Works

DarkVoice uses the **LSB Method**, where the least significant bit of audio frames is replaced with secret text bits.

If lock mode is used:
- Message text is encrypted using **XOR + SHA-256 hashed key**
- Extraction requires the same key to produce real text

---

## 🎥 Official Channel  
### **YouTube:** HasnainDarkNet  
Cyber Security ⚡ Steganography ⚡ Ethical Hacking Tools ⚡

---




