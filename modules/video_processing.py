# Python libraries
import moviepy.editor as mp
import whisper
import os

from os import listdir
from pydub import AudioSegment

# Local imports
from modules.managers.folder_manager import check_folder_existence, delete_file


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

def transcript_video(video_path: str, model_performance: str = 'balanced') -> str:
    # Extract audio from video
    audio_path = extract_audio_from_video(video_path)

    # Ensure the audio file path is correct
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Select the model based on the performance users need
    model_options = {
        'speed': 'tiny',
        'balanced': 'small',
        'accuracy': 'medium'
    }

    # Load whisper model
    model = whisper.load_model(model_options[model_performance]) # VRAM: large 10 GB / medium 5 GB / small 2 GB / base 1 GB / tiny 1 GB (superfast)

    # Transcribe the audio
    result = model.transcribe(
        audio_path, language='pt', temperature=0.0, word_timestamps=True
    )

    delete_file(audio_path)

    return result


if __name__ == '__main__':
    transcript_video()
