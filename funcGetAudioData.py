from pymediainfo import MediaInfo


def get_audio_data(path, audio_params_output):
    file = MediaInfo.parse(path)
    extracted_audio_data = ''
    for count, audio_type in enumerate(file.audio_tracks):
        audio_data_list = []
        # строка с параметрами audio_params_out
        if count > 0:
            extracted_audio_data += '\n'
        for param in audio_params_output:
            try:
                type(audio_type.to_data()[param])
                if type(audio_type.to_data()[param]) == list:
                    audio_data_list.append(str(audio_type.to_data()[param][0]))
                else:
                    audio_data_list.append(str(audio_type.to_data()[param]))
            except KeyError:
                if param == 'other_bit_rate':
                    audio_data_list.append(audio_type.to_data()['other_bit_rate_mode'][0])
                elif param == 'other_language':
                    pass
                    # audio_data_list.append('')
                else:
                    pass
                    # audio_data_list.append('')
        extracted_audio_data += 'Audio #' + str(count + 1) + ": " + ', '.join(audio_data_list)
    return extracted_audio_data


if __name__ == '__main__':
    import easygui
    audio_params_list = ['other_language', 'format', 'other_bit_rate',
                         'other_sampling_rate', 'other_channel_s']
    print(get_audio_data(easygui.fileopenbox(filetypes=["*.*"]), audio_params_list))
