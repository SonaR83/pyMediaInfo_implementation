from pymediainfo import MediaInfo
from datetime import datetime
import re
import json


class Media:
    def __init__(self, destination=''):
        self.destination = destination
        self.file_data = MediaInfo.parse(self.destination)
        self.audio_data = self.file_data.audio_tracks
        self.general_data = self.file_data.general_tracks
        self.video_data = self.file_data.video_tracks
        self.subtitles_data = self.file_data.text_tracks

    def get_video_stream_info(self):
        video_stream = {}
        parse_video_list = [
            {'format': 'video_format'},
            {'encoded_library_name': 'codec'},
            {'internet_media_type': 'media_type'},
            {'height': 'height'},
            {'width': 'width'},
            {'scan_type': 'scan_type'},
            {'frame_rate_mode': 'frame_rate'},
            {'other_bit_rate_mode': 'bit_rate'},
            {'other_bit_rate': 'bit_rate'},
            {'other_display_aspect_ratio': 'aspect_ratio'}
        ]
        for video_data in self.video_data:
            # print(video_data.to_data())
            for data_type in parse_video_list:
                try:
                    # print(data_type)
                    if type(video_data.to_data()[list(data_type)[0]]) == list:
                        video_stream[data_type[list(data_type.keys())[0]]] = \
                            str(video_data.to_data()[list(data_type)[0]][0])

                    if type(video_data.to_data()[list(data_type)[0]]) == str:
                        video_stream[data_type[list(data_type.keys())[0]]] = \
                            str(video_data.to_data()[list(data_type)[0]])

                    if type(video_data.to_data()[list(data_type)[0]]) == int:
                        video_stream[data_type[list(data_type.keys())[0]]] = \
                            str(video_data.to_data()[list(data_type)[0]])
                except KeyError:
                    # print(list(data_type.keys())[0])
                    if list(data_type.keys())[0] == "encoded_library_name":
                        pass
                    if list(data_type.keys())[0] == 'other_bit_rate':
                        pass
                    else:
                        video_stream[data_type[list(data_type.keys())[0]]] = 'undefined'
        if video_stream['bit_rate'] == 'Variable':
            video_stream['bit_rate'] = 'VBR'
        else:
            pass
        return video_stream

    def get_video_stream_info_alt(self):
        format_array = []
        bitrate_array = []
        video_codec_array = []
        parse_video_format = ['format', 'other_format', 'commercial_name']
        parse_video_bitrate = ['other_bit_rate', 'bit_rate', 'other_bit_rate_mode', 'other_nominal_bit_rate']
        parse_video_codec = ['codec_id', 'encoded_library_name']
        for video_data in self.video_data:
            # print(video_data.to_data())
            for video_format in parse_video_format:
                val = ''
                try:
                    if type(video_data.to_data()[video_format]) == list:
                        val = video_data.to_data()[video_format][0]
                    else:
                        val = video_data.to_data()[video_format]
                except KeyError:
                    pass
                finally:
                    format_array.append(val)
            for bitrate in parse_video_bitrate:
                try:
                    if type(video_data.to_data()[bitrate]) == list:
                        # print(bitrate)
                        bitrate_array.append(video_data.to_data()[bitrate][0])

                    else:
                        # print(bitrate)
                        bitrate_array.append(video_data.to_data()[bitrate])

                except KeyError:
                    pass
            # Проверка того, что в массиве bitrate_array что-то присутствует
            try:
                bitrate_array[0]
            except IndexError:
                print('Index Error')
                bitrate_array.append('Unknown')

            for video_codec in parse_video_codec:
                try:
                    if type(video_data.to_data()[video_codec]) == list:
                        video_codec_array.append(video_data.to_data()[video_codec][0])
                    else:
                        video_codec_array.append(video_data.to_data()[video_codec])
                except KeyError:
                    pass

                try:
                    _scan = video_data.to_data()['scan_type']
                except KeyError:
                    _scan = 'Undefined'

                return {'format': format_array[0],
                        'bit_rate': bitrate_array[0],
                        'width': video_data.to_data()['width'],
                        'height': video_data.to_data()['height'],
                        'scan_type': _scan,
                        'video_codec': ','.join(video_codec_array)
                        }

    def get_audio_stream_info(self):
        audio_stream = []
        audio_params_list = \
            [{'other_language': 'language'},
             {'format': 'format'},
             {'bit_rate_mode': 'bit_rate'},
             {'other_sampling_rate': 'sampling_rate'},
             {'other_channel_s': 'channels'}]

        for count, audio_type in enumerate(self.audio_data):
            audio_data_file = {}
            # print(audio_type.to_data())
            # print(audio_type.to_data()['bit_rate_mode'])
            for audio_param in audio_params_list:
                try:
                    if type(audio_type.to_data()[list(audio_param)[0]]) == list:
                        audio_data_file[audio_param[list(audio_param.keys())[0]]] = \
                            str(audio_type.to_data()[list(audio_param)[0]][0])
                    else:
                        audio_data_file[audio_param[list(audio_param.keys())[0]]] = \
                            str(audio_type.to_data()[list(audio_param)[0]])
                except KeyError:
                    # print(audio_param)
                    if list(audio_param.keys())[0] == "other_bit_rate":
                        pass
                    else:
                        audio_data_file[audio_param[list(audio_param.keys())[0]]] = 'undefined'
            # print(audio_data_file)
            if audio_data_file['bit_rate'] == 'CBR':
                # print("Constant")
                audio_data_file['bit_rate'] = audio_type.to_data()['other_bit_rate'][0]
            else:
                pass
                # print('Variable')
            audio_stream.append(audio_data_file)
        return audio_stream

    def get_general_data_info(self):
        general_data_file = {}
        parse_general_list = \
            [{'file_extension': 'extension'}, {'other_file_size': 'size'}, {'other_duration': 'duration'}]
        for g_data in self.general_data:
            # print(g_data.to_data())
            for general_data in parse_general_list:
                try:
                    if type(g_data.to_data()[list(general_data)[0]]) == list:
                        general_data_file[general_data[list(general_data.keys())[0]]] = \
                            str(g_data.to_data()[list(general_data)[0]][0])
                    if type(g_data.to_data()[list(general_data)[0]]) == list and \
                            list(general_data)[0] == 'other_duration':
                        general_data_file[general_data[list(general_data.keys())[0]]] = \
                            datetime.strptime(str(g_data.to_data()[list(general_data)[0]][3]),
                                              '%H:%M:%S.%f').strftime("%H:%M:%S")
                    if type(g_data.to_data()[list(general_data)[0]]) == str:
                        general_data_file[general_data[list(general_data.keys())[0]]] = \
                            str(g_data.to_data()[list(general_data)[0]])
                    else:
                        pass
                except KeyError:
                    print('except')

            general_data_file['size'] = general_data_file['size'].replace('i', '')
            return general_data_file

    def get_subtitles_info(self):
        subtitles_stream = {'have_subtitles': False, 'have_rus_subtitles': False}
        subtitles_dictionary = ['ru', 'rus', 'russian']
        if len(self.subtitles_data) > 0:
            subtitles_stream['have_subtitles'] = True
            for text in self.subtitles_data:
                try:
                    for name in subtitles_dictionary:
                        # print(text.to_data()['language'])
                        if str(text.to_data()['language']).lower() == name:
                            subtitles_stream['have_rus_subtitles'] = True
                            break
                        else:
                            pass
                except KeyError:
                    pass
        return subtitles_stream


if __name__ == '__main__':
    import easygui

    try:
        movie_data = Media(easygui.fileopenbox(filetypes=["*.*"]))
    except OSError:
        print('Cancelled by user')
    # list_data=[{'format': 'Формат'}, {'codec': 'Кодек'}]
    # print(list_data[1][list(list_data[1].keys())[0]])
    else:
        print(movie_data.get_video_stream_info_alt())
        print(movie_data.get_audio_stream_info())
        print(movie_data.get_general_data_info())
        print(movie_data.get_subtitles_info())
