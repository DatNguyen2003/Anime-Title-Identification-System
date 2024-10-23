from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import Formatter
from youtube_transcript_api.formatters import TextFormatter

transcript_list = YouTubeTranscriptApi.list_transcripts('MHJfd4P8kGg')

transcript = transcript_list.find_transcript(['de', 'en'])  

transcript_data = transcript.fetch()

formatter = TextFormatter()

text_formatted = formatter.format_transcript(transcript_data)

with open('./video.txt', 'w', encoding='utf-8') as text_file:
    text_file.write(text_formatted)

print("done")