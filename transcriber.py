from dotenv import load_dotenv
import os
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
    AnalyzeOptions,
    TextSource,
)


def transcribe_audio(a_file):
    try:
        load_dotenv()
        audio_file = "C:/Users/MGRyko/Desktop/GP Client Audio/" + a_file

        API_KEY = os.getenv("DG_API_KEY")

        deepgram = DeepgramClient(API_KEY)

        with open(audio_file, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        transcript = response.results.channels[0].alternatives[0].transcript

        transcript_output_file = os.path.splitext(audio_file)[0] + "_transcript.txt"

        with open(transcript_output_file, "w") as text_file:
            text_file.write(transcript)

        return transcript

    except Exception as e:
        print(f"Exception: {e}")
        return None


def summarize_text(t_file):
    try:
        TEXT_FILE = "C:/Users/MGRyko/Desktop/GP Client Audio/" + t_file
        load_dotenv()
        API_KEY = os.getenv("DG_API_KEY")

        deepgram = DeepgramClient(API_KEY)

        with open(TEXT_FILE, "r") as file:
            buffer_data = file.read()

        payload: TextSource = {
            "buffer": buffer_data,
        }

        options = AnalyzeOptions(
            language="en",
            # sentiment=True,
            # intents=True,
            summarize=True,
            # topics=True,
        )

        response = deepgram.read.analyze.v("1").analyze_text(payload, options)
        summary = response.results.summary.text

        summary_output_file = os.path.splitext(TEXT_FILE)[0] + "_summary.txt"
        with open(summary_output_file, "w") as text_file:
            text_file.write(summary)

        return summary

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":

    T = "recording1_transcript.txt"
    result = summarize_text(T)

    if result is not None:
        print(result)
    else:
        print("Transcription failed.")
