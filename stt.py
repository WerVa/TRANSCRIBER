# importing libraries
import speech_recognition as sr
import os
import shutil
from pydub import AudioSegment
from pydub.silence import split_on_silence
# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition


def get_large_audio_transcription(path, msl, st, ks, lang):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_mp3(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=msl,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS+st,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=ks,
                              )
    folder_name = "audio-chunks"

    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    global errorcount
    errorcount = 0
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language=lang)
            except sr.UnknownValueError as e:
                errorcount += 1
            else:
                text = f"{text.capitalize()}. "
                whole_text += text
    # return the text for all chunks detected
    shutil.rmtree(folder_name)
    return whole_text
