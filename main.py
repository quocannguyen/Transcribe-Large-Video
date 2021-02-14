# Install packages: pydub, SpeechRecognition
# Download ffmpeg.exe into project folder

# Importing libraries
import speech_recognition
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


# Splits the audio file into list of segments
def get_segment_list_from_audio(wav_path):
    sound = AudioSegment.from_wav(wav_path)     # Open the audio file using pydub.AudioSegment
    print('Splitting audio into segments...')

    # split audio sound where silence is 700 milliseconds or more and get chunks
    # experiment with this value for your target audio file
    segments = split_on_silence(sound, min_silence_len=500, silence_thresh=sound.dBFS - 14, keep_silence=500)

    print('Number of segments:', len(segments))
    return segments


# Splits the audio file into segments and applies speech recognition
def get_large_audio_transcription(wav_path):
    segments = get_segment_list_from_audio(wav_path)    # Splits the audio file into list of segments

    folder_name = 'audio-segments'      # Create a directory to store the audio segments
    if not os.path.isdir(folder_name):  #
        os.mkdir(folder_name)           #

    # Process each segment
    print('Processing the segments...')
    audio_text = ''
    for i, segment in enumerate(segments, start=1):     # Iterate through the segment list
        # Export audio segment and save it in {folder_name}.
        segment_path = os.path.join(folder_name, f'segment-{i}.wav')
        segment.export(segment_path, format='wav')

        # Speech-recognize the segment
        with speech_recognition.AudioFile(segment_path) as source:
            recognizer = speech_recognition.Recognizer()    # Create a speech recognition object

            audio_recorded = recognizer.record(source)

            # Try converting it to text
            try:
                segment_text = recognizer.recognize_google(audio_recorded)
            except speech_recognition.UnknownValueError as error:
                print('speech_recognition.UnknownValueError:', str(error), 'Processing...')
            else:
                segment_text = f'{segment_text.capitalize()}.'
                # print(segment_path, ':', text)
                audio_text += segment_text + '\n'

        os.remove(segment_path)     # Remove audio segments to save memory

    return audio_text


def write_to_file(name, text):
    output_file = open(name, 'w')
    output_file.write(text)
    output_file.close()


if __name__ == '__main__':
    video_name = 'video.mp4'    #
    text_name = 'text.txt'      #
    wav_name = 'audio.wav'

    os.system(f'ffmpeg -i {video_name} {wav_name}')     # Convert .mp4 into .wav
    transcript = get_large_audio_transcription(wav_name)
    write_to_file(text_name, transcript)

    print('\nFull text:', transcript)
