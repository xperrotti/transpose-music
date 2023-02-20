import os
import sys
import warnings
import music21
from pydub import AudioSegment
import aubio

# Disable warnings for now
warnings.filterwarnings('ignore', message='urllib3')
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Get the input file name
mp3_file = input("Enter the name of the music file: ")

# Get the transpose value from the user
transpose = input("Enter the transpose reference (each number means a half step): ")

# Load the MP3 file with pydub
audio = AudioSegment.from_file(mp3_file, format='mp3')
print(f"Loaded MP3 file: {audio}")

# Export the audio to WAV format
temp_wav = 'temp.wav'
print(f"Exporting the audio to WAV format: {temp_wav}")
audio.export(temp_wav, format='wav')

audio_file = 'temp.wav'

# Load the audio file with aubio
samplerate = 44100
hop_size = 512
s = aubio.source(audio_file, samplerate, hop_size)
samplerate = s.samplerate

# Setup pitch detection
tolerance = 0.8
pitch_o = aubio.pitch("yin", samplerate, hop_size, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

# Container for detected pitches
pitches = []

# Detect pitches
total_frames = 0
while True:
    samples, read = s()
    pitch = pitch_o(samples)[0]
    pitches += [pitch]
    total_frames += read
    if read < hop_size: break

# Convert the pitches to MIDI data
melody = aubio.midi2note(pitches)

# Save the MIDI data to a file
midi_file = 'temp.mid'
with open(midi_file, 'w') as f:
    f.write(melody)
temp_midi = midi_file

# Load the original piece with music21
print(f"Loading MIDI file: {temp_midi}")
try:
    original_piece = music21.converter.parse(temp_midi)
except FileNotFoundError as e:
    print(f"Error loading MIDI file: {e}")
    sys.exit(1)

# Transpose the piece
print(f"Transposing the piece by {transpose} half-steps")
transpose_amount = int(transpose)
transposed_piece = original_piece.transpose(transpose_amount)

# Save the transposed piece as a MIDI file
print("Saving the transposed piece as a MIDI file")
transposed_piece.write('midi', fp='transposed.mid')

# Convert the MIDI file to MP3 with FluidSynth
print("Converting the MIDI file to MP3 with FluidSynth")
fluidsynth_cmd = "fluidsynth -ni /usr/share/sounds/sf2/FluidR3_GM.sf2 transposed.mid -F temp.mp3 -r 44100 -b 16 -T raw"
print(f"Running command: {fluidsynth_cmd}")
os.system(fluidsynth_cmd)

# Get the output file name
filename = os.path.splitext(mp3_file)[0]
output_file = f"{filename}_transposed.mp3"

# Rename the output file
print(f"Renaming the output file to: {output_file}")
os.rename("temp.mp3", output_file)

print("Done!")
