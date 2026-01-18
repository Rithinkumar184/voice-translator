# Multi-Language Voice Translator

A powerful Python application that translates and converts text to speech in multiple languages using Google's free APIs. Includes both CLI and GUI interfaces.

## Features

✨ **Core Features:**
- 🎤 Real-time voice-to-text conversion (Speech Recognition)
- 🔊 Text-to-speech conversion with natural voices
- 🌍 Real-time translation between 13+ languages
- 📁 Save audio files as MP3
- 🖥️ Two interfaces: Command-line (CLI) and Graphical (GUI)
- 🎯 Language selection and automatic language detection

## Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Hindi (hi)
- Telugu (te)
- Chinese (zh)
- Japanese (ja)
- Arabic (ar)
- Portuguese (pt)
- Russian (ru)
- Italian (it)
- Korean (ko)

## Installation from Scratch

### Step 1: Install Python

1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. During installation, **IMPORTANT**: Check ✅ "Add Python to PATH"
3. Complete the installation

### Step 2: Clone or Download the Project

**Option A: Using Git (Recommended)**
```bash
git clone <repository-url>
cd voice-translator
```

**Option B: Manual Download**
1. Download the project files
2. Extract to a folder (e.g., `voice-translator`)
3. Open Command Prompt/PowerShell in that folder

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

After activation, your terminal should show `(.venv)` at the beginning of the line.

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**For Windows users with PyAudio issues:**
```bash
pip install --only-binary :all: pyaudio
```

**For macOS users:**
```bash
brew install portaudio
pip install pyaudio
```

**For Linux users:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

## Usage

### Option 1: Command-Line Interface (CLI)

```bash
python app.py
```

**Menu Options:**
1. **Voice to Text** - Record speech and convert to text
2. **Text to Voice (with Translation)** - Enter text → Auto-translates → Plays in selected language
3. **Translate Text** - Just translate without speaking
4. **Voice to Text to Translate to Voice** - Full pipeline: speak → translate → hear
5. **Save Text to Audio File** - Create MP3 files
6. **List Supported Languages** - View all available languages
7. **Exit** - Close the application

**Example Usage:**
```
Enter your choice (1-7): 2
=== Supported Languages ===
en: English
es: Spanish
fr: French
...

Enter target language code (default: en): es
Enter text to convert to speech: Hello world
Slow speed? (y/n, default: n): n

🔄 Translating...
   Original text: Hello world
   ✓ Translated text: Hola mundo

🔊 Converting to speech...
   Text to speak: Hola mundo
   Target Language: Spanish (code: es)
   ✓ Playing audio in Spanish...
```

### Option 2: Graphical User Interface (GUI)

```bash
python gui_app.py
```

**Features:**
- Drop-down language selection
- Text input area
- Play audio button
- Save audio button
- Echo mode button
- Real-time status bar
- Professional interface

## How It Works

### Architecture
```
┌─────────────────┐
│  User Input     │
│  (Text/Voice)   │
└────────┬────────┘
         │
    ┌────▼────┐
    │ Speech   │
    │ Recog.   │  (Google API)
    └────┬────┘
         │
    ┌────▼──────────┐
    │ Translation   │  (Google Translate API)
    │ (if needed)   │
    └────┬──────────┘
         │
    ┌────▼────┐
    │   gTTS   │  (Google Text-to-Speech)
    │  (Audio) │
    └────┬────┘
         │
    ┌────▼─────────┐
    │  Playback/   │
    │   Save MP3   │
    └──────────────┘
```

### APIs Used (All Free!)
- **Google Speech Recognition** - Voice to text conversion
- **Google Translate** - Text translation
- **Google Text-to-Speech (gTTS)** - Text to speech conversion

No API keys required!

## Requirements

### System Requirements
- **RAM**: 2 GB minimum (4 GB recommended)
- **Disk Space**: 500 MB
- **Internet**: Required for APIs (Google Services)
- **Microphone**: Required for voice input
- **Speaker**: Required for audio output

### Python Packages
See `requirements.txt`:
```
SpeechRecognition==3.10.0
gTTS==2.4.0
pygame==2.5.2
PyAudio==0.2.14
requests
googletrans==4.0.0
```

## Troubleshooting

### Issue: Microphone not detected
**Solution:**
1. Check system microphone settings
2. Verify microphone is plugged in and enabled
3. Test microphone with system audio settings
4. Run: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_indexes())"`

### Issue: "No module named 'pyaudio'"
**Solution:**
```bash
pip install --only-binary :all: pyaudio
```
If still fails, try:
```bash
pip install pipwin
pipwin install pyaudio
```

### Issue: "API error" or "Connection error"
**Solution:**
1. Check internet connection
2. Verify Google APIs are accessible (may be blocked in some regions)
3. Restart the application

### Issue: Audio playback fails silently
**Solution:**
1. Check system audio settings
2. Install audio players:
   - **Windows**: Usually built-in
   - **macOS**: Ensure `afplay` is installed (built-in)
   - **Linux**: Install `mpg123` or `ffmpeg`:
     ```bash
     sudo apt-get install mpg123
     # or
     sudo apt-get install ffmpeg
     ```

### Issue: Translation not working correctly
**Solution:**
1. Verify internet connection
2. Check that language code is correct (use option 6 to see all codes)
3. Try with shorter text

### Issue: Text doesn't convert to actual language sound
**Solution:**
1. Ensure correct language code is selected
2. Check the debug output shows the translated text
3. The audio should automatically use the selected language (not just accent)

## Project Structure

```
voice-translator/
│
├── app.py                    # CLI version
├── gui_app.py               # GUI version with Tkinter
├── utils.py                 # Utility functions
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── README.md               # This file
│
├── audio_files/            # Saved audio files directory
│
└── tests/                  # Unit tests
    ├── __init__.py
    └── test_translator.py
```

## Common Commands

### Updating packages
```bash
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

### Deactivate virtual environment
```bash
deactivate
```

### Run with debugging
```bash
python -u app.py  # CLI
python -u gui_app.py  # GUI
```

## Tips & Tricks

1. **Faster startup**: Use GUI version for better UX
2. **Batch processing**: Use CLI with scripts for automation
3. **Better recognition**: Speak clearly and slowly
4. **Reduce noise**: Use in quiet environments
5. **Slow playback**: Enable "Slow Speed" for difficult languages
6. **Save for later**: Use "Save Audio File" option to create a library

## Performance Notes

- First run of translation: ~2-3 seconds (API connection)
- Subsequent translations: ~1-2 seconds
- Audio playback: Real-time
- API requests: Shared with Google's infrastructure

## License

MIT License - Free to use and modify

## Support

For issues:
1. Check Troubleshooting section above
2. Verify all dependencies are installed: `pip list`
3. Check internet connection
4. Test each component separately

## Future Enhancements

- [ ] Offline speech recognition
- [ ] Real-time live translation
- [ ] Custom voice models
- [ ] Batch file processing
- [ ] Web-based interface
- [ ] Cloud storage integration
- [ ] More language support
- [ ] Speech speed adjustment UI

---

**Last Updated**: January 2026
**Version**: 1.0.0#   v o i c e - a s s i s t  
 #   v o i c e - t r a n s l a t o r  
 #   v o i c e - t r a n s l a t o r  
 