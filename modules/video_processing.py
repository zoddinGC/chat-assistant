# Python libraries
import moviepy.editor as mp
import speech_recognition as sr

from os import listdir
from pydub import AudioSegment

# Local imports
from modules.managers.folder_manager import check_folder_existence


def extract_audio_from_video(video_path: str) -> str:
    # Check how many temporary audios are within the temp/ folder
    amount_files = len(listdir('temp/'))

    # Create a temporary audio path
    audio_path = f'temp/temp_audio_{amount_files}.wav'

    # Check if the audio folder exists
    check_folder_existence(audio_path[:audio_path.rfind('/')])

    # Load the video file
    video = mp.VideoFileClip(video_path, verbose=False)

    # Extract audio from the video
    audio = video.audio
    audio.write_audiofile(audio_path, codec='pcm_s16le')

    # Load the audio file with pydub
    audio_segment = AudioSegment.from_file(audio_path, format='wav')

    # Setting audio to mono, 16kHz, and 16-bit
    audio = audio_segment.set_channels(1).set_frame_rate(16_000).set_sample_width(2)

    # Save the audio again
    audio.export(audio_path, format='wav')

    return audio_path

def transcript_video(video_path: str) -> str:
    # Extract audio from video
    audio_path = extract_audio_from_video(video_path)

    # Initialize recognizer class (for transcript audio)
    r = sr.Recognizer()

    # Open audio file
    with sr.AudioFile(audio_path) as source:
        audio_text = r.record(source)

    text = r.recognize_google(audio_text, language='pt-BR')

    return text


if __name__ == '__main__':
    transcript_video()
