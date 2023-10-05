from googleapiclient.discovery import build


def get_list_video(api_key, channel_id):
    videos = []
    youtube = build("youtube", "v3", developerKey=api_key)
    next_page_token = None
    while True:
        request = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            type="video",
            maxResults=50,
            order="viewCount",
            pageToken=next_page_token,
        )
        response = request.execute()

        for item in response["items"]:
            video_id = item["id"]["videoId"]
            video_info = youtube.videos().list(part="statistics", id=video_id).execute()
            view_count = int(video_info["items"][0]["statistics"]["viewCount"])
            if view_count >= numberView:
                videos.append(
                    {
                        "title": item["snippet"]["title"],
                        "video_id": video_id,
                        "view_count": view_count,
                    }
                )
        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break
    return videos


def display(videos):
    for video in videos:
        print(f"Tiêu đề: {video['title']}")
        print(f"Video ID: {video['video_id']}")
        print(f"Số lượng view: {video['view_count']}")
    print("\n")
    print(f"Tổng số video có số lượt xem trên {numberView} lượt xem: {len(videos)}")


# API key
api_key = "AIzaSyCAYN34J0eA7fwuvpsP45ZDHy4KM-QE2Ns"  # thay đổi

# ID kênh muốn lọc vieo: giả sử kênh sơn tùng: https://youtube://www.youtube.com/channel/UClyA28-01x4z60eWQ2kiNbA
channel_id = "UClyA28-01x4z60eWQ2kiNbA"  # thay đổi

# Số lượt xem cần kiểm tra
numberView = 1000000  # thay đổi

videos = get_list_video(api_key, channel_id)
display(videos)

# kênh nhiều video thì cố gắng đợi 5s -> 10s
