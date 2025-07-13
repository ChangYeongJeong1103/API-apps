# YouTube Channel Monitor & Transcript Fetcher

A Python automation tool that monitors YouTube channels for new videos and automatically fetches their transcripts for analysis. Perfect for tracking financial news, educational content, or any YouTube channels you follow regularly.

## 🚀 Features

- **🔍 Channel Monitoring**: Automatically checks multiple YouTube channels for new videos
- **📝 Transcript Extraction**: Fetches video transcripts in Korean and English
- **🗂️ Smart Organization**: Saves individual transcript files with clean filenames
- **📊 Multiple Output Formats**: Generates HTML and text notification files
- **💾 History Tracking**: Avoids reprocessing previously checked videos
- **🔧 Easy Configuration**: Simple text file configuration for channel IDs


## 🛠️ Installation

1. **Install required packages:**
```bash
pip install -r requirements.txt
```

2. **Set up your YouTube API key:**
   - Get a free API key from [Google Cloud Console](https://console.cloud.google.com/)
   - Enable YouTube Data API v3
   - Add your API key to your environment

3. **Configure channels to monitor:**
   - Edit `channel_ids.txt` and add YouTube channel IDs (one per line)
   - Find channel IDs from YouTube channel URLs or use online tools


## 🎯 Usage

### Basic Usage
```bash
python main.py
```

### What happens when you run it:
1. **Checks channels** listed in `channel_ids.txt`
2. **Fetches latest videos** from each channel
3. **Downloads transcripts** for any new videos found
4. **Saves transcript files** to `transcripts/` folder
5. **Generates notifications** in HTML and text format

### Example Output
```
✅ New video detected: Market Analysis: Tech Stocks Rally
📺 Channel: Financial News Today
📄 Transcript saved: transcripts/20240115_Financial_News_Today_Market_Analysis_Tech_Stocks_Rally.txt

📊 Summary:
- Checked 3 channels
- Found 1 new videos
- Results saved in 'new_videos.html' and 'new_videos.txt'
```

## 📁 File Structure

```
youtube-channel-monitor/
├── main.py                 # Main application script
├── youtube_api.py          # YouTube API integration
├── channel_ids.txt         # List of channels to monitor
├── requirements.txt        # Python dependencies
├── history.json           # Tracking processed videos
├── new_videos.html        # HTML notification output
├── new_videos.txt         # Text notification output
├── video_scripts.json     # JSON data for all videos
└── transcripts/           # Individual transcript files
    ├── 20240115_Channel_Name_Video_Title.txt
    └── ...
```

## 📊 Output Files

### 1. Transcript Files (`transcripts/`)
- **Format**: `YYYYMMDD_ChannelName_VideoTitle.txt`
- **Contains**: Video metadata, full transcript, and summary prompt
- **Use**: Copy-paste into AI tools for analysis

### 2. HTML Notifications (`new_videos.html`)
- **Format**: Clean HTML with clickable links
- **Use**: View in browser, bookmark, or share

### 3. Text Notifications (`new_videos.txt`)
- **Format**: Plain text summary
- **Use**: Command line viewing or automation

### 4. JSON Data (`video_scripts.json`)
- **Format**: Structured JSON with all video data
- **Use**: Integration with other tools or scripts


