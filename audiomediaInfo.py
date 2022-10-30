from pprint import pprint
from pymediainfo import MediaInfo
import easygui

audio_params_list = ['other_language', 'commercial_name', 'other_bit_rate',
                     'other_sampling_rate', 'other_channel_s']
media = MediaInfo.parse(easygui.fileopenbox(filetypes=["*.*"]))
output_audio = ''
output_list_audio = []
# audio_out_info = ''
for count, audio_type in enumerate(media.audio_tracks):
    audio_string = audio_type.to_data()
    output_list_audio = []
    # print(audio_string)
    if count > 0:
        output_audio += '\n'
    for val in audio_params_list:
        try:
            type(audio_string[val])
            if type(audio_string[val]) == list:
                output_list_audio.append(str(audio_string[val][0]))
            else:
                output_list_audio.append(str(audio_string[val]))
        except KeyError:
            output_list_audio.append(audio_string['other_bit_rate_mode'][0])
    output_audio += 'Audio #' + str(count + 1) + ": " + ', '.join(output_list_audio)

print(output_audio)

# output_audio += f'Audio #{count + 1}: {audio_type.other_language[0]}, {audio_type.commercial_name}, ' \
#                 f'{audio_type.other_nominal_bit_rate[0]}, {audio_type.other_sampling_rate[0]}, ' \
#                 f'{audio_type.channel_s} channel(s)'
