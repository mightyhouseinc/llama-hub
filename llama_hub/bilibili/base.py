"""Simple Reader that reads transcript and general infor of Bilibili video."""
import warnings
from typing import Any, List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class BilibiliTranscriptReader(BaseReader):
    """Bilibili Transcript and video info reader."""

    @staticmethod
    def get_bilibili_info_and_subs(bili_url):
        import json
        import re

        import requests
        from bilibili_api import sync, video

        bvid = re.search(r"BV\w+", bili_url).group()
        # Create credential object
        v = video.Video(bvid=bvid)
        # Get video info and basic infor
        video_info = sync(v.get_info())
        if sub_list := video_info["subtitle"]["list"]:
            sub_url = sub_list[0]["subtitle_url"]
            result = requests.get(sub_url)
            raw_sub_titles = json.loads(result.content)["body"]
            raw_transcript = " ".join([c["content"] for c in raw_sub_titles])
            title = video_info["title"]
            desc = video_info["desc"]

            return f"Video Title: {title}, description: {desc}\nTranscript: {raw_transcript}"
        else:
            warnings.warn(
                f"No subtitles found for video: {bili_url}. Return Empty transcript."
            )
            return ""

    def load_data(self, video_urls: List[str], **load_kwargs: Any) -> List[Document]:
        """
        Load auto generated Video Transcripts from Bilibili, including additional metadata.

        Args:
            video_urls (List[str]): List of Bilibili links for which transcripts are to be read.

        Returns:
            List[Document]: A list of Document objects, each containing the transcript for a Bilibili video.
        """
        results = []
        for bili_url in video_urls:
            try:
                transcript = self.get_bilibili_info_and_subs(bili_url)
                results.append(Document(text=transcript))
            except Exception as e:
                warnings.warn(
                    f"Error loading transcript for video {bili_url}: {str(e)}. Skipping"
                    " video."
                )
        return results
