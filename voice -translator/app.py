"""
Multi-Language Voice to Text and Text to Voice Application
Main application file: app.py
"""

import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import os
import tempfile
from pathlib import Path
import pygame
import time

# Initialize pygame mixer for audio playback with error handling
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Mixer initialization warning: {e}")
    try:
        pygame.mixer.quit()
        pygame.mixer.init()
    except Exception as e2:
        print(f"Mixer init fallback failed: {e2}")

# Initialize translator
translator = Translator()

class VoiceTranslator:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'hi': 'Hindi',
            'te': 'Telugu',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ar': 'Arabic',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'it': 'Italian',
            'ko': 'Korean'
        }
    
    def list_languages(self):
        """Display supported languages"""
        print("\n=== Supported Languages ===")
        for code, name in self.supported_languages.items():
            print(f"{code}: {name}")
        print()
    
    def translate_text(self, text, source_language='auto', target_language='en'):
        """Translate text from source language to target language"""
        if not text:
            print("❌ No text to translate")
            return None
        
        # If target is English and source is auto, no translation needed
        if target_language == 'en' and source_language == 'auto':
            return text
        
        try:
            source_name = self.supported_languages.get(source_language, 'Auto')
            target_name = self.supported_languages.get(target_language, 'Unknown')
            print(f"\n🔄 Translating...")
            print(f"   From: {source_name} → To: {target_name}")
            print(f"   Original text: {text}")
            
            # Use googletrans with correct syntax
            result = translator.translate(text, dest=target_language)
            translated_text = result.text
            
            print(f"   ✓ Translated text: {translated_text}")
            return translated_text
        
        except Exception as e:
            print(f"❌ Translation error: {e}")
            print("💡 Make sure you have an internet connection for translation.")
            return text
    
    def voice_to_text(self, language='en'):
        """Convert voice to text"""
        print(f"\n🎤 Listening... (Language: {self.supported_languages.get(language, 'Unknown')})")
        
        with sr.Microphone() as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Speak now...")
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing...")
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio, language=language)
                print(f"\n✓ Recognized Text: {text}")
                return text
                
            except sr.WaitTimeoutError:
                print("❌ No speech detected. Please try again.")
                return None
            except sr.UnknownValueError:
                print("❌ Could not understand audio. Please speak clearly.")
                return None
            except sr.RequestError as e:
                print(f"❌ API error: {e}")
                return None
    
    def text_to_voice(self, text, language='en', slow=False):
        """Convert text to voice and play it"""
        if not text:
            print("❌ No text to convert")
            return
        
        # Validate language code
        if language not in self.supported_languages:
            print(f"❌ Language '{language}' not supported")
            print("Available languages:")
            self.list_languages()
            return
        
        print(f"\n🔊 Converting to speech...")
        print(f"   Text to speak: {text}")
        print(f"   Target Language: {self.supported_languages.get(language, 'Unknown')} (code: {language})")
        print(f"   Slow speed: {slow}")
        
        temp_file_path = None
        try:
            # Create speech with the specified language
            print("   Creating audio file with gTTS...")
            tts = gTTS(text=text, lang=language, slow=slow)
            print(f"   ✓ gTTS object created successfully")
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file_path = temp_file.name
            temp_file.close()
            
            print(f"   Saving to temp file: {temp_file_path}")
            tts.save(temp_file_path)
            print(f"   ✓ Audio file saved successfully")
            print(f"✓ Playing audio in {self.supported_languages.get(language, 'Unknown')}...")
            
            # Play the audio using pygame
            try:
                pygame.mixer.music.load(temp_file_path)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                # Stop playback and unload
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                
            except pygame.error as pe:
                print(f"⚠️  Pygame playback failed: {pe}")
                print(f"✓ Audio file saved to: {temp_file_path}")
            
            # Add delay to ensure file is released
            time.sleep(0.5)
            
            # Clean up temp file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except PermissionError:
                    pass
            
            print("✓ Playback complete")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Make sure you have an internet connection for text-to-speech conversion.")
            print(f"💡 Ensure language code '{language}' is valid for gTTS.")
    
    def save_audio_file(self, text, language='en', filename='output.mp3', slow=False):
        """Save text-to-speech to file"""
        if not text:
            print("❌ No text to convert")
            return
        
        # Validate language code
        if language not in self.supported_languages and language != 'auto':
            print(f"❌ Language '{language}' not supported")
            return
        
        try:
            print(f"🔊 Creating audio file with language: {language}")
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(filename)
            print(f"✓ Audio saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            print("💡 Make sure you have an internet connection and the language code is valid.")

def main():
    translator_app = VoiceTranslator()
    
    print("=" * 60)
    print("  Multi-Language Voice Translator")
    print("=" * 60)
    
    while True:
        print("\n=== Main Menu ===")
        print("1. Voice to Text")
        print("2. Text to Voice (with Translation)")
        print("3. Translate Text")
        print("4. Voice to Text to Translate to Voice")
        print("5. Save Text to Audio File (with Translation)")
        print("6. List Supported Languages")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            translator_app.list_languages()
            lang = input("Enter language code (default: en): ").strip() or 'en'
            text = translator_app.voice_to_text(language=lang)
            
        elif choice == '2':
            translator_app.list_languages()
            lang = input("Enter target language code (default: en): ").strip() or 'en'
            text = input("Enter text to convert to speech: ").strip()
            
            if text:
                # Translate text to target language
                translated = translator_app.translate_text(text, source_language='en', target_language=lang)
                
                if translated:
                    slow = input("Slow speed? (y/n, default: n): ").strip().lower() == 'y'
                    translator_app.text_to_voice(translated, language=lang, slow=slow)
            
        elif choice == '3':
            text = input("Enter text to translate: ").strip()
            if text:
                translator_app.list_languages()
                source_lang = input("Enter source language code (default: en): ").strip() or 'en'
                target_lang = input("Enter target language code (default: es): ").strip() or 'es'
                translator_app.translate_text(text, source_language=source_lang, target_language=target_lang)
            
        elif choice == '4':
            translator_app.list_languages()
            source_lang = input("Enter source language code (default: en): ").strip() or 'en'
            target_lang = input("Enter target language code (default: es): ").strip() or 'es'
            
            # Voice to Text
            print(f"\nStep 1: Record your speech in {translator_app.supported_languages.get(source_lang, 'Unknown')}")
            text = translator_app.voice_to_text(language=source_lang)
            
            if text:
                # Translate text
                print(f"\nStep 2: Translating to {translator_app.supported_languages.get(target_lang, 'Unknown')}...")
                translated = translator_app.translate_text(text, source_language=source_lang, target_language=target_lang)
                
                if translated:
                    # Text to Voice
                    print(f"\nStep 3: Converting translated text to voice in {translator_app.supported_languages.get(target_lang, 'Unknown')}...")
                    slow = input("Slow speed for playback? (y/n, default: n): ").strip().lower() == 'y'
                    translator_app.text_to_voice(translated, language=target_lang, slow=slow)
            
        elif choice == '5':
            translator_app.list_languages()
            lang = input("Enter target language code (default: en): ").strip() or 'en'
            text = input("Enter text to convert: ").strip()
            
            if text:
                # Translate text to target language
                translated = translator_app.translate_text(text, source_language='en', target_language=lang)
                
                if translated:
                    filename = input("Enter filename (default: output.mp3): ").strip() or 'output.mp3'
                    slow = input("Slow speed? (y/n, default: n): ").strip().lower() == 'y'
                    translator_app.save_audio_file(translated, language=lang, filename=filename, slow=slow)
            
        elif choice == '6':
            translator_app.list_languages()
            
        elif choice == '7':
            print("\nThank you for using Voice Translator!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()