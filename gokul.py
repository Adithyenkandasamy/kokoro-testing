from IPython.display import Audio
from kokoro import KPipeline
import soundfile as sf
import numpy as np



def text_to_speech(text, lang_code='a', voice='af_heart', speed=1, output_file='output.wav'):
    """
    Converts text to speech and plays the generated audio.

    :param text: Input text to be converted to speech.
    :param lang_code: Language code for the TTS pipeline.
    :param voice: Voice model to use.
    :param speed: Speech speed.
    :param output_file: Output WAV file.
    :return: None
    """
    pipeline = KPipeline(lang_code=lang_code)
    generator = pipeline(text, voice=voice, speed=speed, split_pattern=r'\n\n\n\n\+')

    # Collect all audio data
    all_audio = []

    for _, _, audio in generator:
        all_audio.append(audio)

    # Concatenate all audio segments
    combined_audio = np.concatenate(all_audio)

    # Write to a single WAV file
    sf.write(output_file, combined_audio, 24000)

    # Play the audio
    file_path = f'{output_prefix}_{i}.wav'
    display(Audio(combined_audio, rate=24000))

text_to_speech("The Territorial Force was a part-time volunteer auxiliary created in 1908. It was designed to reinforce the British Army overseas during war without resorting to conscription, but for political reasons it was constituted as a home defence force in which foreign service was voluntary. It was not well regarded by the military authorities. On the outbreak of the First World War, the regular army was expanded by raising the New Army from scratch rather than relying on the Territorial Force. Territorials volunteered for foreign service in large numbers, and territorial divisions filled the gap between the near destruction of the regular army during the German offensive of 1914 and the arrival of the New Army in 1915. The force also provided the bulk of the British contingent in the Sinai and Palestine campaign. The territorial identity was eroded by the introduction of conscription in 1916, and by the war's end there was little to distinguish between regular, territorial and New Army formations.")

