# Changes the key by a user-specified number of semitones

import librosa
import soundfile


def main():
    input_file = input("Enter the name of the input file: ")
    semitone = input("Enter the number of semitones to transpose: ")
    print(semitone)
    semitone = int(semitone)
    #semitone = -semitone
    print(semitone)
    y, sr = librosa.load(input_file)
    new_y = librosa.effects.pitch_shift(y, sr, semitone)
    soundfile.write("pitchShifted.wav", new_y, sr,)


main()