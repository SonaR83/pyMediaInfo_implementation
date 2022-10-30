from pymediainfo import MediaInfo
from datetime import datetime
import json


def get_video_stream(path):
    video_stream = {}
    parse_video_list = ['format', 'codec_id', 'internet_media_type', 'height', 'width',
                        'scan_type', 'frame_rate_mode', 'bit_rate', 'other_display_aspect_ratio']
    video_stream_data = MediaInfo.parse(path)
    for video_data in video_stream_data.video_tracks:
        print(video_data.to_data())
        for data_type in parse_video_list:
            try:
                video_stream[data_type] = str(video_data.to_data()[data_type])
            except KeyError:
                pass

        # print(video_data.to_data())
    return json.dumps(video_stream)


if __name__ == '__main__':
    import easygui

    print(get_video_stream(easygui.fileopenbox(filetypes=["*.*"])))
