# transcript_downloader.py
# Description: YouTube transcript downloader using youtube-transcript.io API
# Supports TXT and SRT format exports with optional proxy configuration

import os
import re
import requests
import sys
import time
from urllib.parse import urlparse, parse_qs
from colorama import init, Fore, Style

# --- ⚙️ CONFIGURATION ---------------------------------------------------
API_KEY = 'YOUR-API-KEY'
API_ENDPOINT = 'https://www.youtube-transcript.io/api/transcripts'

# --- Proxy Settings ---
USE_PROXY = False
PROXY_URL = ""

# --- Rate Limiting ---
REQUEST_DELAY = 1  # seconds between requests
# -----------------------------------------------------------------------

init(autoreset=True)

proxies_dict = None
if USE_PROXY:
    proxies_dict = {
        'http': PROXY_URL,
        'https': PROXY_URL
    }

def display_header():
    """Prints the application header."""
    print(Style.BRIGHT + Fore.MAGENTA + "=" * 60)
    print(Style.BRIGHT + Fore.CYAN + "      ▶️  YouTube Transcript Downloader ▶️")
    print(Style.BRIGHT + Fore.MAGENTA + "=" * 60)
    print()

def extract_video_id(input_str: str) -> str | None:
    """
    Extracts YouTube video ID from URL or returns ID if already provided.
    """
    try:
        if 'youtube.com' in input_str or 'youtu.be' in input_str:
            parsed = urlparse(input_str)
            
            if 'youtube.com' in parsed.netloc:
                query = parse_qs(parsed.query)
                if 'v' in query:
                    return query['v'][0]
                if parsed.path.startswith('/embed/'):
                    return parsed.path.split('/')[2]
            
            if 'youtu.be' in parsed.netloc:
                video_id = parsed.path[1:]
                return video_id.split('?')[0]
        
        return input_str.strip()
    
    except Exception as e:
        print(f"{Fore.RED}❌ Error parsing input: {e}")
        return None

def sanitize_filename(name: str) -> str:
    """Removes invalid characters for file/folder names."""
    sanitized = re.sub(r'[\\/*?:"<>|]', "", name)
    sanitized = " ".join(sanitized.split()).strip()
    return sanitized if sanitized else "default_video_name"

def fetch_transcript_from_api(video_id: str) -> dict | None:
    """
    Fetches transcript using youtube-transcript.io API.
    
    Returns: {
        'title': str,
        'transcript': list of dict with 'text' and timestamps
    }
    """
    headers = {
        'Authorization': f'Basic {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'ids': [video_id]
    }
    
    try:
        print(f"{Fore.CYAN}📡 Fetching transcript from API...")
        time.sleep(REQUEST_DELAY)
        
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers=headers,
            proxies=proxies_dict,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        if not isinstance(data, list) or len(data) == 0:
            print(f"{Fore.YELLOW}⚠️  Empty response from API")
            return None
        
        if 'tracks' not in data[0] or len(data[0]['tracks']) == 0:
            print(f"{Fore.YELLOW}⚠️  No transcript tracks found")
            return None
        
        if 'transcript' not in data[0]['tracks'][0]:
            print(f"{Fore.YELLOW}⚠️  No transcript data in track")
            return None
        
        title = data[0].get('title', video_id)
        transcript_entries = data[0]['tracks'][0]['transcript']
        
        print(f"{Fore.GREEN}✅ Successfully fetched transcript!")
        print(f"{Fore.GREEN}📺 Video Title: {Style.BRIGHT}{title}")
        print(f"{Fore.GREEN}📝 Transcript entries: {len(transcript_entries)}")
        
        return {
            'title': title,
            'transcript': transcript_entries,
            'video_id': video_id
        }
    
    except requests.exceptions.HTTPError as e:
        print(f"{Fore.RED}❌ HTTP Error {e.response.status_code}: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}❌ Network Error: {e}")
        return None
    except (KeyError, IndexError, TypeError) as e:
        print(f"{Fore.RED}❌ Invalid API response structure: {e}")
        return None

def convert_to_text(transcript_entries: list) -> str:
    """
    Converts transcript entries to plain text.
    """
    texts = [entry['text'] for entry in transcript_entries]
    return ". ".join(texts)

def convert_to_srt(transcript_entries: list) -> str:
    """
    Converts transcript entries to SRT format with timestamps.
    """
    srt_content = []
    
    for idx, entry in enumerate(transcript_entries, 1):
        try:
            start_time = float(entry.get('start', 0))
            duration = float(entry.get('duration', 0))
            end_time = start_time + duration
            text = str(entry.get('text', '')).strip()
            
            if not text:
                continue
            
            def seconds_to_srt_time(seconds):
                try:
                    seconds = float(seconds)
                    hours = int(seconds // 3600)
                    minutes = int((seconds % 3600) // 60)
                    secs = int(seconds % 60)
                    millis = int((seconds % 1) * 1000)
                    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
                except (ValueError, TypeError):
                    return "00:00:00,000"
            
            start_str = seconds_to_srt_time(start_time)
            end_str = seconds_to_srt_time(end_time)
            
            srt_entry = f"{idx}\n{start_str} --> {end_str}\n{text}\n"
            srt_content.append(srt_entry)
        
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Skipping entry {idx} due to error: {e}")
            continue
    
    return "\n".join(srt_content)

def save_file(directory: str, filename: str, content: str):
    """Saves content to file."""
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"{Fore.GREEN}✅ Saved: {Style.BRIGHT}{filepath}")
    except IOError as e:
        print(f"{Fore.RED}❌ Cannot write file: {e}")

def main():
    """Main application loop."""
    display_header()
    
    if USE_PROXY:
        print(f"{Style.BRIGHT}{Fore.CYAN}🌐 Proxy: {PROXY_URL}")
    
    print(f"{Style.BRIGHT}{Fore.CYAN}🔑 API: youtube-transcript.io\n")

    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print(f"{Style.BRIGHT}{Fore.RED}❌ ERROR: API Key is not configured!")
        print(f"{Fore.YELLOW}Please edit the script and set your API_KEY.\n")
        sys.exit(1)

    while True:
        try:
            user_input = input(f"{Style.BRIGHT}{Fore.YELLOW}🔗 Enter YouTube URL or Video ID (Ctrl+C to exit):\n>> ").strip()
            
            if not user_input:
                continue
            
            video_id = extract_video_id(user_input)
            if not video_id:
                print(f"{Fore.RED}❌ Invalid input!\n")
                continue
            
            print(f"{Fore.CYAN}🎬 Video ID: {Style.BRIGHT}{video_id}\n")
            
            result = fetch_transcript_from_api(video_id)
            
            if not result:
                print(f"{Fore.RED}❌ Could not fetch transcript!\n")
                print(Style.BRIGHT + Fore.MAGENTA + "-" * 60)
                continue
            
            title = sanitize_filename(result['title'])
            transcript_entries = result['transcript']
            
            print(f"\n{Fore.CYAN}📁 Creating directory: {Style.BRIGHT}{title}")
            os.makedirs(title, exist_ok=True)
            
            print(f"\n{Fore.CYAN}💾 Saving text version...")
            text_content = convert_to_text(transcript_entries)
            save_file(title, f"{title}.txt", text_content)
            
            print(f"\n{Fore.CYAN}💾 Saving SRT version...")
            srt_content = convert_to_srt(transcript_entries)
            save_file(title, f"{title}.srt", srt_content)
            
            print(f"\n{Style.BRIGHT}{Fore.GREEN}🎉 Download complete!")
            print(Style.BRIGHT + Fore.MAGENTA + "-" * 60 + "\n")
        
        except KeyboardInterrupt:
            print(f"\n\n{Style.BRIGHT}{Fore.YELLOW}👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"{Style.BRIGHT}{Fore.RED}\n❌ Unexpected error: {e}")
            print(Style.BRIGHT + Fore.MAGENTA + "-" * 60 + "\n")

if __name__ == "__main__":
    main()
