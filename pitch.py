# Changes the key by a user-specified number of semitones

import librosa
import soundfile


def main():
    input_file = input("Insira o nome da música de origem: ")
    #generates the output file based on the input_file name + _transposed.wav
    
    semitone = input("Insira o numero de semitons (números positivos sobem o tom, números negativos descem o tom): ")
    output_file = input_file[:-4] + "_" + semitone + "-semitons_transposed.wav"
    semitone = int(semitone)
    y, sr = librosa.load(input_file, sr=44100)
    #new_y = librosa.effects.pitch_shift(y, sr, semitone, n_fft=16384)
    new_y = librosa.effects.pitch_shift(y, sr, semitone)
    soundfile.write(output_file, new_y, sr,)


main()