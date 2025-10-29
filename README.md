# 🎬 YouTube Transcript Downloader

A robust Python CLI tool to download YouTube video transcripts in both **TXT** and **SRT** formats using the youtube-transcript.io API.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

---

## ✨ Features

- 📥 Download transcripts in **TXT** and **SRT** formats
- 🌐 Optional proxy support for enhanced reliability
- 🎯 Smart video ID extraction from various YouTube URL formats
- 📁 Automatic folder creation with sanitized filenames
- 🎨 Beautiful colored CLI output
- ⚡ Fast and efficient with retry logic

---

## 📋 Requirements

- Python 3.10 or higher
- Active internet connection
- API key from [youtube-transcript.io](https://www.youtube-transcript.io/)

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/youtube-transcript-downloader.git
cd youtube-transcript-downloader
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Edit the script and add your API key:

```python
API_KEY = 'YOUR_API_KEY_HERE'
API_ENDPOINT = 'https://www.youtube-transcript.io/api/transcripts'
```

---

## 📦 Dependencies

```
requests>=2.31.0
colorama>=0.4.6
```

Create a `requirements.txt` file:
```txt
requests>=2.31.0
colorama>=0.4.6
```

---

## 🎮 Usage

### Basic Usage
```bash
python transcript_downloader.py
```

### Supported Input Formats
The tool accepts multiple YouTube URL formats:

```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
VIDEO_ID (direct video ID)
```

### Example Session
```
============================================================
      ▶️  YouTube Transcript Downloader ▶️
============================================================

🌐 Proxy: http://127.0.0.1:10808
🔑 API: youtube-transcript.io

🔗 Enter YouTube URL or Video ID (Ctrl+C to exit):
>> https://www.youtube.com/watch?v=dQw4w9WgXcQ

🎬 Video ID: dQw4w9WgXcQ

📡 Fetching transcript from API...
✅ Successfully fetched transcript!
📺 Video Title: Example Video Title
📝 Transcript entries: 450

📁 Creating directory: Example Video Title

💾 Saving text version...
✅ Saved: Example Video Title\Example Video Title.txt

💾 Saving SRT version...
✅ Saved: Example Video Title\Example Video Title.srt

🎉 Download complete!
```

---

## ⚙️ Configuration

### API Settings
Configure your API key in the script:

```python
API_KEY = 'YOUR_API_KEY_HERE'
API_ENDPOINT = 'https://www.youtube-transcript.io/api/transcripts'
```

### Proxy Settings
Enable or disable proxy routing:

```python
USE_PROXY = True  # Set to False to disable proxy
PROXY_URL = "http://127.0.0.1:10808"
```

### Rate Limiting
Adjust delay between requests:

```python
REQUEST_DELAY = 1  # seconds
```

---

## 📂 Output Structure

```
Video_Title/
├── Video_Title.txt  # Plain text transcript
└── Video_Title.srt  # SRT subtitle format with timestamps
```

### TXT Format
```
Text from first segment. Text from second segment. Text from third segment...
```

### SRT Format
```
1
00:00:00,000 --> 00:00:03,500
Text from first segment

2
00:00:03,500 --> 00:00:07,200
Text from second segment
```

---

## 🛠️ Troubleshooting

### Issue: "HTTP Error 404: No transcript found"
**Solution:** The video may not have transcripts available or they're disabled by the creator.

### Issue: "Network Error: Could not connect to API"
**Solution:** 
- Check your internet connection
- Verify proxy settings if enabled
- Ensure API endpoint is accessible

### Issue: "ERROR: API Key is not configured"
**Solution:**
- Edit the script and set your `API_KEY`
- Get your API key from [youtube-transcript.io](https://www.youtube-transcript.io/)

### Issue: Proxy connection fails
**Solution:**
- Verify your proxy server is running
- Check proxy URL and port configuration
- Try disabling proxy: `USE_PROXY = False`

---

## 🔒 Security Notes

- **Never commit API keys** to public repositories
- Use environment variables for sensitive data:
  ```python
  import os
  API_KEY = os.getenv('YOUTUBE_TRANSCRIPT_API_KEY')
  ```
- Keep your `requirements.txt` updated

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[youtube-transcript.io](https://www.youtube-transcript.io/)** - Special thanks for providing an amazing and reliable transcript API service that makes this tool possible
- [Colorama](https://github.com/tartley/colorama) - For cross-platform colored terminal output
- [Requests](https://requests.readthedocs.io/) - For the excellent HTTP library

---

## 📞 Support

If you encounter any issues or have questions:

- Open an [Issue](https://github.com/yourusername/youtube-transcript-downloader/issues)
- Check existing issues for solutions
- Read the troubleshooting section above

---

## 🗺️ Roadmap

- [ ] Add support for batch processing multiple videos
- [ ] Implement language selection for transcripts
- [ ] Add VTT format export
- [ ] Create GUI version
- [ ] Add automatic subtitle translation

---

## ⭐ Star History

If you find this tool helpful, please consider giving it a star!

---

<div align="center">
Made with ❤️ for the YouTube community
</div>
