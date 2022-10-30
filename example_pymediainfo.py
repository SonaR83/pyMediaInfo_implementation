from src.classMediaInfo import Media
# import easygui
import json


#
# path = ''
# media_file = Media(path)

def init_class_object(path):
    media_file = Media(path)
    return media_file


def get_video_stream_data(path):
    media_file = Media(path)
    return media_file.get_video_stream_info_alt()


def get_audio_stream_data(path):
    media_file = Media(path)
    return media_file.get_audio_stream_info()


def get_media_file_info(path):
    media_file = Media(path)
    return media_file.get_general_data_info()


def get_subtitles_info(path):
    media_file = Media(path)
    return media_file.get_subtitles_info()


def get_media_info(path):
    media_file = Media(path)
    output_data = {'video': media_file.get_video_stream_info_alt(), 'audio': media_file.get_audio_stream_info(),
                   'file': media_file.get_general_data_info(), 'subtitles': media_file.get_subtitles_info()}
    return json.dumps(output_data)


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
        # print(movie_data.get_audio_stream_info())
        # print(movie_data.get_general_data_info())
        # print(movie_data.get_subtitles_info())
