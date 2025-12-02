#!/usr/bin/env python3
"""
DarkVoice - Audio Steganography Decryptor
"""

import wave
import argparse
import hashlib
import sys

GOLD = "\033[38;5;220m"
RESET = "\033[0m"

BANNER = GOLD + r"""
██████╗  █████╗ ██████╗ ██╗  ██╗██╗   ██╗ ██████╗ ██╗ ██████╗ ███████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██║   ██║██╔═══██╗██║██╔════╝ ██╔════╝
██   ██╔███████║██████╔╝█████╔╝ ██║   ██║██║   ██║██║██║  ███╗█████╗  
██╔══██╗██╔══██║██╔══██╗██╔═██╗ ██║   ██║██║   ██║██║██║   ██║██╔══╝  
██████╔╝██║  ██║██║  ██║██║  ██╗╚██████╔╝╚██████╔╝██║╚██████╔╝███████╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝

                   DarkVoice Decryptor - By HasnainDarkNet
""" + RESET


HELP = """
Usage:
  python3 decrypt.py -i encoded.wav
  python3 decrypt.py -i encoded.wav --key "1234"

Notes:
  • Works with both locked (encrypted) and normal messages
  • If key is wrong → output will be garbage
"""


def decrypt_message(encrypted_bytes, key):
    """Decrypt using same XOR-hash encryption"""
    hashed = hashlib.sha256(key.encode()).digest()
    decrypted = []

    for i, byte in enumerate(encrypted_bytes):
        decrypted.append(byte ^ hashed[i % len(hashed)])

    try:
        return bytes(decrypted).decode()
    except:
        return "[!] Wrong key or corrupted message"


def decode_audio(input_file, key=None):

    with wave.open(input_file, 'rb') as audio:
        frames = bytearray(list(audio.readframes(audio.getnframes())))

    # Extract bits until EOF marker
    bits = ""
    for byte in frames:
        bits += str(byte & 1)

        if bits.endswith("1111111111111110"):
            bits = bits[:-16]
            break

    if len(bits) % 8 != 0:
        print("[!] Error: Invalid or corrupted audio")
        sys.exit(1)

    # Convert binary → bytes
    extracted_bytes = []
    for i in range(0, len(bits), 8):
        extracted_bytes.append(int(bits[i:i+8], 2))

    extracted_bytes = bytes(extracted_bytes)

    # If key provided (locked message)
    if key:
        print("[+] Key mode enabled → decrypting…")
        return decrypt_message(extracted_bytes, key)

    # Without key (normal text)
    try:
        return extracted_bytes.decode()
    except:
        return "[!] Message appears encrypted. Use correct key."


if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-i', '--input')
    parser.add_argument('--key', required=False)
    parser.add_argument('--help', action='store_true')

    args = parser.parse_args()

    if args.help or not args.input:
        print(HELP)
        sys.exit(0)

    message = decode_audio(args.input, args.key)

    print("\n==========================")
    print(" Extracted Message:")
    print("==========================")
    print(message)
    print("==========================\n")
