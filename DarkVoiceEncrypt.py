#!/usr/bin/env python3
"""
DarkVoice - Audio Steganography Encryptor (with Key Mode)
"""

import wave
import argparse
import sys
import os
import hashlib

# Golden Color
GOLD = "\033[38;5;220m"
RESET = "\033[0m"

BANNER = GOLD + r"""
██████╗  █████╗ ██████╗ ██╗  ██╗██╗   ██╗ ██████╗ ██╗ ██████╗ ███████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██║   ██║██╔═══██╗██║██╔════╝ ██╔════╝
██   ██╔███████║██████╔╝█████╔╝ ██║   ██║██║   ██║██║██║  ███╗█████╗  
██╔══██╗██╔══██║██╔══██╗██╔═██╗ ██║   ██║██║   ██║██║██║   ██║██╔══╝  
██████╔╝██║  ██║██║  ██║██║  ██╗╚██████╔╝╚██████╔╝██║╚██████╔╝███████╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝

          DarkVoice Encryptor - Hide Secret Text Inside Audio
""" + RESET


HELP_TEXT = """
Usage:
  python3 run.py -i input.wav -o output.wav -m "Your secret" --key "1234"

Modes:
  • Without key  -> Normal hide
  • With key     -> Message is encrypted with password

Info:
  • Input must be WAV format
  • Output is new WAV containing hidden message
"""


def encrypt_message(message, key):
    """Encrypt message with key using simple XOR hash"""
    hashed = hashlib.sha256(key.encode()).digest()
    encrypted = []

    for i, ch in enumerate(message.encode()):
        encrypted.append(ch ^ hashed[i % len(hashed)])

    return bytes(encrypted)


def encode_audio(input_file, output_file, secret_msg, key=None):

    # If key provided → encrypt message first
    if key:
        print("[+] Key Mode Enabled")
        encrypted = encrypt_message(secret_msg, key)
        # Convert to binary
        binary = ''.join(format(b, '08b') for b in encrypted)
        binary += "1111111111111110"
    else:
        print("[+] Normal Mode Enabled")
        binary = ''.join(format(ord(i), '08b') for i in secret_msg)
        binary += "1111111111111110"

    with wave.open(input_file, 'rb') as audio:
        frames = bytearray(list(audio.readframes(audio.getnframes())))

    if len(binary) > len(frames):
        print("[!] Error: Audio too small for message")
        sys.exit(1)

    # Hide message in audio
    for i in range(len(binary)):
        frames[i] = (frames[i] & 254) | int(binary[i])

    # Save output
    with wave.open(output_file, 'wb') as out:
        with wave.open(input_file, 'rb') as original:
            out.setparams(original.getparams())
        out.writeframes(bytes(frames))

    print(f"[✓] Message hidden successfully! Saved as: {output_file}")


if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-m', '--message')
    parser.add_argument('--key', required=False)
    parser.add_argument('--help', action='store_true')
    args = parser.parse_args()

    if args.help or not (args.input and args.output and args.message):
        print(HELP_TEXT)
        sys.exit(0)

    if not os.path.exists(args.input):
        print("[!] Input audio not found")
        sys.exit(1)

    encode_audio(args.input, args.output, args.message, args.key)
