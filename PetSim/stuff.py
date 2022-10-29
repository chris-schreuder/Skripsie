    #  <!-- <script>
    #     window.addEventListener('DOMContentLoaded', (event) => {
    #         setInterval(Update, 1000);
    #     });

    #     function Update() {
    #         fetch("{{ url_for('update_img') }}")
    #             .then((response) => {
    #             return response.json();
    #             })
    #             .then((dict) => {
    #             if(${dict["pet_img"]} == 'skip'){
    #                 document.getElementById("pet_img").src=${dict["pet_img"]};
    #             });
    #     }
    #  </script> -->

    # Loading the Libraries
from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Read the Audiofile
samplerate, data = read('eat_64bit.wav')
# Frame rate for the Audio
print(samplerate)

# Duration of the audio in Seconds
duration = len(data)/samplerate
print("Duration of Audio in Seconds", duration)
print("Duration of Audio in Minutes", duration/60)

time = np.arange(0,duration,1/samplerate)

# Plotting the Graph using Matplotlib
plt.plot(time,data)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('6TU5302374.wav')
plt.show()

file_name='silence_removed.wav'

# Reading and splitting the audio file into chunks
sound = AudioSegment.from_wav("eat_64bit.wav") 
print(type(sound))
audio_chunks = split_on_silence(sound
                            ,min_silence_len = 100
                            ,silence_thresh = -45
                            ,keep_silence = 50
                        )

# Putting the file back together
combined = AudioSegment.empty()
for chunk in audio_chunks:
    combined += chunk
combined.export(file_name, format = 'wav')