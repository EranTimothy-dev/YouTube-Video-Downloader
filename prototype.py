# import pytube as pt

# url = "https://youtu.be/V2z2t938Idk?si=m3_uuPo8P3ACXwqo"

# yt = pt.YouTube(url)
# stream = yt.streams.filter(adaptive=True).get_audio_only()
# stream.download()
# # for i in stream:
# #     print(i)
    
    
# def get_resolutions(Stream):
#     args = str(Stream)
#     start_index = args.find("=",20) + 2
#     end_index = args.find('p',41) + 1
#     resolution = args[start_index:end_index]
#     return resolution

# video_quality = []
# for i in stream:
#     Resolution = get_resolutions(i)
#     video_quality.append(Resolution)


# mp4 = []
# # filter mp4 video formats
# for i in video_quality:
#     start_index = i.find("/") + 1
#     end_index = i.find('"')
#     fileType = i[start_index:end_index]
#     if (fileType == "mp4"):
#         mp4.append(i)


# print(mp4)



