# Du benötigst: pip install google-genai

import mimetypes
import os
import struct
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"Datei gespeichert unter: {file_name}")


def convert_to_wav_header(audio_data: bytes, mime_type: str) -> bytes:
    """Erstellt einen WAV-Header für die Rohdaten (PCM)."""
    # Standardannahmen für PCM aus dem Modell, falls Parsing fehlschlägt
    bits_per_sample = 16
    sample_rate = 24000
    num_channels = 1

    # Simples Parsing des Mime-Types (z.B. "audio/L16;rate=24000")
    if "rate=" in mime_type:
        try:
            sample_rate = int(mime_type.split("rate=")[1].split(";")[0])
        except:
            pass

    data_size = len(audio_data)
    byte_rate = sample_rate * num_channels * (bits_per_sample // 8)
    block_align = num_channels * (bits_per_sample // 8)
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", chunk_size, b"WAVE", b"fmt ", 16, 1, num_channels,
        sample_rate, byte_rate, block_align, bits_per_sample, b"data", data_size
    )
    return header


def generate_audio():
    client = genai.Client(
        api_key=os.environ.get("gen-lang-client-0903430425"),
    )

    text_input = "Brauchwassererwärmung (Warmwasser zum Duschen/Waschen) von der Heizungswärmepumpe hat durchaus Auswirkungen auf die Dimensionierung, allerdings weniger gravierend, als man oft vermutet."

    model = "gemini-2.5-pro-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=text_input)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Zephyr"  # Oder "Puck", "Kore", "Fenrir", "Aoede"
                )
            )
        ),
    )

    print("Generiere text_to_speach_mp3...")

    # Gesamtdaten sammeln
    audio_bytes = b""
    mime_type = ""

    for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
    ):
        if chunk.candidates and chunk.candidates[0].content.parts:
            part = chunk.candidates[0].content.parts[0]
            if part.inline_data:
                audio_bytes += part.inline_data.data
                mime_type = part.inline_data.mime_type

    if audio_bytes:
        # Dateiendung bestimmen
        ext = ".wav"  # Default da Rohdaten oft als WAV verpackt werden müssen
        final_data = audio_bytes

        # Wenn es PCM Rohdaten sind (audio/L16), WAV Header hinzufügen
        if "audio/L16" in mime_type:
            final_data = convert_to_wav_header(audio_bytes, mime_type) + audio_bytes
            ext = ".wav"
        elif "mp3" in mime_type:
            ext = ".mp3"

        save_binary_file(f"Brauchwasserinfo{ext}", final_data)
    else:
        print("Keine Audiodaten empfangen.")


if __name__ == "__main__":
    generate_audio()