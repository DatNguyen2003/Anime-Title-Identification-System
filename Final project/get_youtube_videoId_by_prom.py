import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import Formatter
from youtube_transcript_api.formatters import TextFormatter

# Replace with your API key
API_KEY = 'AIzaSyDpyJppA58-b-HcJmJYWn-WeCTJETr5ZSc'

def get_most_relevant_video_id(search_query):
    url = 'https://www.googleapis.com/youtube/v3/search'

    params = {
        'part': 'snippet',
        'q': search_query,          # The search query
        'type': 'video',            # Ensures we only get videos, not channels or playlists
        'maxResults': 1,            # Get only the top result
        'key': API_KEY              # Your API key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error if the request failed
        data = response.json()

        # Extract video ID from the first result
        video_id = data['items'][0]['id']['videoId']
        return video_id
    except (requests.exceptions.HTTPError, IndexError) as error:
        print(f'Error fetching video: {error}')
        return None

def get_transcript_by_video_id(video_id, languages=['de', 'en'], output_file='./video.txt'):
    try:
        # Fetch the list of transcripts available for the video
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Find the transcript in the preferred languages (e.g., 'de', 'en')
        transcript = transcript_list.find_transcript(languages)

        # Fetch the actual transcript data
        transcript_data = transcript.fetch()

        # Format the transcript text
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript_data)

        # Write the formatted transcript to the specified output file
        with open(output_file, 'w', encoding='utf-8') as text_file:
            text_file.write(text_formatted)

        print(f"Transcript saved to {output_file}")
    except Exception as e:
        print(f"Error fetching transcript: {e}")

def main():
    # Test the search query and get the most relevant video ID
    search_query = 'angel beat anime recap'
    video_id = get_most_relevant_video_id(search_query)
    
    if video_id:
        print(f"Most relevant video ID for '{search_query}': {video_id}")
        
        # Fetch and save the transcript for the found video ID
        get_transcript_by_video_id(video_id)
    else:
        print("No video found.")

# Execute the main function
if __name__ == '__main__':
    main()