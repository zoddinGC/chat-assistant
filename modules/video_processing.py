# Python libraries
import moviepy.editor as mp
import whisper
import os

from os import listdir
from pydub import AudioSegment

# Local imports
from modules.managers.folder_manager import check_folder_existence, delete_file


def extract_audio_from_video(video_path: str) -> str:
    """
        This function will load a saved video and extract the audio in 16kHz framerate
        and then save it in a .wav format in a temporary folder.

        :param video_path: A string representing where the saved video is located
    """
    # Check how many temporary audios are within the temp/ folder
    check_folder_existence('temp/')
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

def transcript_video(video_path: str, model_performance: str = 'balanced') -> dict:
    """
        This function receives a saved video and then process it based on the Whisper
        OpenAI object and transcript the audio to a text format. Based on the model
        performance, the function will load a tiny, small or medium version of Whisper 
        and being necessary 1, 2 or 5 GB of VRAM consecutively.

        :param video_path: A string representing the path to a local video
        :param model_performance: A string representing the Whisper model selection
        :return: A dictionary containing the transcription of the video, segments of text 
        and their time and other important metadata
    """
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

    # Add type key
    result['type'] = 'video'

    delete_file(audio_path)

    segments = [
        [x['text'] for x in result['segments']],
        [[x['start'], x['end']] for x in result['segments']]
    ]

    return result['text'], segments


if __name__ == '__main__':
    transcript_video()
