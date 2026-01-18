"""
GUI version of Voice Translator using Tkinter and pygame
File: gui_app.py (Updated with full language support using free APIs)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import tempfile
import threading
import requests
from googletrans import Translator

class VoiceTranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Language Voice Translator")
        self.root.geometry("1000x850")
        self.root.resizable(True, True)
        
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
        # Initialize pygame mixer with error handling
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Mixer initialization warning: {e}")
            try:
                pygame.mixer.quit()
                pygame.mixer.init()
            except Exception as e2:
                print(f"Mixer init fallback failed: {e2}")
        
        self.languages = {
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Hindi': 'hi',
            'Telugu': 'te',
            'Chinese': 'zh',
            'Japanese': 'ja',
            'Arabic': 'ar',
            'Portuguese': 'pt',
            'Russian': 'ru',
            'Italian': 'it',
            'Korean': 'ko'
        }
        
        self.create_widgets()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def translate_text(self, text, target_lang_code):
        """Translate text using Google Translate API"""
        if not text or not text.strip():
            return text
        
        # If target is English, no translation needed
        if target_lang_code == 'en':
            return text
        
        try:
            # Map language codes to language names
            lang_names = {
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
            
            target_name = lang_names.get(target_lang_code, target_lang_code)
            
            # Use Google Translate
            try:
                translator = Translator()
                result = translator.translate(text, dest=target_lang_code)
                translated = result.text
                
                if translated and translated.strip():
                    print(f"Original: {text}")
                    print(f"Translated to {target_name}: {translated}")
                    return translated
                else:
                    return text
                    
            except Exception as e:
                print(f"Google Translate error: {e}")
                # Fallback to MyMemory API if Google fails
                try:
                    from urllib.parse import quote
                    
                    lang_map = {
                        'es': 'es-ES',
                        'fr': 'fr-FR',
                        'de': 'de-DE',
                        'hi': 'hi',
                        'te': 'te',
                        'zh': 'zh-CN',
                        'ja': 'ja',
                        'ar': 'ar',
                        'pt': 'pt-BR',
                        'ru': 'ru-RU',
                        'it': 'it-IT',
                        'ko': 'ko-KR'
                    }
                    
                    target = lang_map.get(target_lang_code, target_lang_code)
                    encoded_text = quote(text)
                    url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair=en|{target}"
                    
                    response = requests.get(url, timeout=10)
                    data = response.json()
                    
                    if data.get('responseStatus') == 200:
                        translated = data['responseData']['translatedText']
                        if translated and translated != text:
                            print(f"Original: {text}")
                            print(f"Translated to {target_name} (via MyMemory): {translated}")
                            return translated
                except Exception as e2:
                    print(f"MyMemory fallback error: {e2}")
            
            # Return original text if all translation fails
            print(f"Translation for {target_name} not available, using original text")
            return text
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text
        
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def create_widgets(self):
        # Header
        header = tk.Label(
            self.root,
            text="🎤 Voice Translator 🔊",
            font=("Arial", 20, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Main container
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Language Selection
        lang_frame = tk.LabelFrame(main_frame, text="Language Selection", font=("Arial", 12, "bold"), padx=10, pady=10)
        lang_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(lang_frame, text="Select Language:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        
        self.language_var = tk.StringVar(value="English")
        language_dropdown = ttk.Combobox(
            lang_frame,
            textvariable=self.language_var,
            values=list(self.languages.keys()),
            state="readonly",
            width=20,
            font=("Arial", 10)
        )
        language_dropdown.grid(row=0, column=1, padx=10, pady=5)
        
        # Voice to Text Section
        v2t_frame = tk.LabelFrame(main_frame, text="Voice to Text", font=("Arial", 12, "bold"), padx=10, pady=10)
        v2t_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.listen_btn = tk.Button(
            v2t_frame,
            text="🎤 Start Listening",
            command=self.start_listening,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.listen_btn.pack(pady=10)
        
        tk.Label(v2t_frame, text="Recognized Text:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        self.text_output = tk.Text(v2t_frame, height=5, font=("Arial", 10), wrap=tk.WORD)
        self.text_output.pack(fill=tk.BOTH, expand=True)
        
        # Text to Voice Section
        t2v_frame = tk.LabelFrame(main_frame, text="Text to Voice", font=("Arial", 12, "bold"), padx=10, pady=10)
        t2v_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(t2v_frame, text="Enter Text:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 5))
        
        self.text_input = tk.Text(t2v_frame, height=4, font=("Arial", 10), wrap=tk.WORD)
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Play button below text field (Main Action Button)
        self.play_btn = tk.Button(
            t2v_frame,
            text="▶️ PLAY AUDIO",
            command=self.speak_text,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=12,
            cursor="hand2",
            relief=tk.RAISED,
            bd=2
        )
        self.play_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Additional options frame
        options_frame = tk.Frame(t2v_frame)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Slow speed checkbox
        self.slow_var = tk.BooleanVar(value=False)
        slow_check = tk.Checkbutton(
            options_frame,
            text="🐢 Slow Speed",
            variable=self.slow_var,
            font=("Arial", 10),
            bg=options_frame["bg"]
        )
        slow_check.pack(side=tk.LEFT, padx=5)
        
        # Buttons frame
        btn_frame = tk.Frame(t2v_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.speak_btn = tk.Button(
            btn_frame,
            text="🔊 Speak",
            command=self.speak_text,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.speak_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = tk.Button(
            btn_frame,
            text="💾 Save Audio",
            command=self.save_audio,
            bg="#FF9800",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.echo_btn = tk.Button(
            btn_frame,
            text="🔄 Echo Mode",
            command=self.echo_mode,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.echo_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9),
            bg="#f0f0f0"
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def start_listening(self):
        if self.is_listening:
            return
        
        self.is_listening = True
        self.listen_btn.config(state="disabled", text="🎤 Listening...")
        self.status_var.set("Listening for speech...")
        
        # Run in separate thread to avoid freezing GUI
        thread = threading.Thread(target=self.voice_to_text)
        thread.daemon = True
        thread.start()
    
    def voice_to_text(self):
        lang_code = self.languages[self.language_var.get()]
        
        with sr.Microphone() as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                self.status_var.set("Processing speech...")
                text = self.recognizer.recognize_google(audio, language=lang_code)
                
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(1.0, text)
                self.status_var.set("Speech recognized successfully!")
                
            except sr.WaitTimeoutError:
                messagebox.showwarning("Timeout", "No speech detected. Please try again.")
                self.status_var.set("Ready")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio.")
                self.status_var.set("Ready")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"API error: {e}")
                self.status_var.set("Ready")
            finally:
                self.is_listening = False
                self.listen_btn.config(state="normal", text="🎤 Start Listening")
    
    def speak_text(self):
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter text to speak!")
            return
        
        self.speak_btn.config(state="disabled")
        self.status_var.set("Converting text to speech...")
        
        thread = threading.Thread(target=self._speak_text_thread, args=(text,))
        thread.daemon = True
        thread.start()
    
    def _speak_text_thread(self, text):
        lang_code = self.languages[self.language_var.get()]
        slow = self.slow_var.get()
        
        try:
            # Validate text is not empty
            if not text or not text.strip():
                messagebox.showwarning("Warning", "Please enter text to speak!")
                self.status_var.set("Ready")
                self.speak_btn.config(state="normal")
                return
            
            # Translate text to target language
            self.status_var.set(f"Translating to {self.language_var.get()}...")
            translated_text = self.translate_text(text, lang_code)
            
            # Verify translation actually happened
            if translated_text == text and lang_code != 'en':
                messagebox.showwarning("Translation Warning", 
                    f"Text may not have translated properly to {self.language_var.get()}.\n"
                    f"Original: {text[:50]}...")
            
            self.status_var.set("Converting to speech...")
            
            # Convert translated text to speech in target language
            tts = gTTS(text=translated_text, lang=lang_code, slow=slow)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            tts.save(temp_file.name)
            self.status_var.set("Playing audio...")
            
            # Play audio using pygame
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up
            pygame.mixer.music.unload()
            os.unlink(temp_file.name)
            self.status_var.set("Playback complete!")
            
        except Exception as e:
            print(f"Error details: {str(e)}")
            messagebox.showerror("Error", f"Failed to convert text to speech:\n{str(e)}")
            self.status_var.set("Ready")
        finally:
            self.speak_btn.config(state="normal")
    
    def save_audio(self):
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter text to convert!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        lang_code = self.languages[self.language_var.get()]
        slow = self.slow_var.get()
        
        try:
            self.status_var.set("Translating and saving audio file...")
            
            # Translate text to target language
            translated_text = self.translate_text(text, lang_code)
            
            # Convert translated text to speech in target language
            tts = gTTS(text=translated_text, lang=lang_code, slow=slow)
            tts.save(filename)
            messagebox.showinfo("Success", f"Audio saved to:\n{filename}")
            self.status_var.set("Ready")
        except Exception as e:
            print(f"Error details: {str(e)}")
            messagebox.showerror("Error", f"Failed to save audio:\n{str(e)}")
            self.status_var.set("Ready")
    
    def echo_mode(self):
        """Voice to Text to Voice - Echo Mode"""
        if self.is_listening:
            messagebox.showwarning("Warning", "Already listening. Please wait.")
            return
        
        self.is_listening = True
        self.echo_btn.config(state="disabled", text="🔄 Recording...")
        self.status_var.set("Listening in Echo Mode...")
        
        thread = threading.Thread(target=self._echo_mode_thread)
        thread.daemon = True
        thread.start()
    
    def _echo_mode_thread(self):
        lang_code = self.languages[self.language_var.get()]
        slow = self.slow_var.get()
        
        with sr.Microphone() as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                self.status_var.set("Processing speech...")
                text = self.recognizer.recognize_google(audio, language='en')
                
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(1.0, text)
                
                # Translate recognized English text to target language
                self.status_var.set("Translating and playing back...")
                translated_text = self.translate_text(text, lang_code)
                print(f"Recognized: {text}")
                print(f"Translated: {translated_text}")
                
                # Now play the translated text in the target language
                tts = gTTS(text=translated_text, lang=lang_code, slow=slow)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                temp_file.close()
                
                tts.save(temp_file.name)
                
                # Play audio using pygame
                pygame.mixer.music.load(temp_file.name)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                # Clean up
                pygame.mixer.music.unload()
                os.unlink(temp_file.name)
                self.status_var.set("Echo mode complete!")
                
            except sr.WaitTimeoutError:
                messagebox.showwarning("Timeout", "No speech detected. Please try again.")
                self.status_var.set("Ready")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio.")
                self.status_var.set("Ready")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"API error: {e}")
                self.status_var.set("Ready")
            except Exception as e:
                messagebox.showerror("Error", f"Echo mode failed: {e}")
                self.status_var.set("Ready")
            finally:
                self.is_listening = False
                self.echo_btn.config(state="normal", text="🔄 Echo Mode")
    
    def on_closing(self):
        """Handle window close event"""
        try:
            pygame.mixer.quit()
        except:
            pass
        self.root.destroy()

def main():
    root = tk.Tk()
    app = VoiceTranslatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()