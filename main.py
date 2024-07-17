import pyaudio
from tkinter import *
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog
import speech_recognition as sr
from googletrans import Translator
from symbols import *

# Global variables
Titile_of_project = "Speech To Text with GUI"
saved_text_file = r".\saved_text.txt"

try:
    icon_path = "./assets/favicon.ico"
except:
    print('Favicon is missing!!')

myFont = "Courier"
buttonFont = "Helvetica"
myFontSize = 12

energy_threshold = 1000
sample_rate = 44100
chunk_size = 512

translator = Translator()

# Define available languages
languages = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Kannada": "kn-IN"
}

current_language = "English"

def replace_symbol(txt):
    mtxt = txt.split(" ")
    for word in mtxt:
        for key in symbol.keys():
            if word.lower() == key:
                mtxt[mtxt.index(word)] = symbol[key]
    return " ".join(mtxt)

def s2t():
    global speaker_output
    try:
        fi_le = open(saved_text_file, "a+", encoding="utf-8")
    except FileNotFoundError:
        fi_le = open(saved_text_file, "w+", encoding="utf-8")

    r = sr.Recognizer()
    r.energy_threshold = energy_threshold

    with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        print('Say Something!')
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language=languages[current_language])
            text = replace_symbol(text)
            print('You said : {} '.format(text))
            speaker_output += '\n' + text
            fi_le.write(text + '\n')
            fi_le.close()
            update_display()
            return text
        except sr.UnknownValueError:
            print("Speech is unintelligible")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            return None

def update_display():
    for widget in DisplayFrame.winfo_children():
        widget.destroy()
    textFrame = LabelFrame(DisplayFrame, font=(myFont, myFontSize), text="Conversion Output")
    textFrame.pack(fill="both", expand=True)
    showText = ScrollableFrame(textFrame)
    Text = Label(showText.scrollable_frame, padx=10, pady=5, justify=LEFT, font=(myFont, myFontSize), text=speaker_output)
    Text.pack(fill="both", expand=True)
    showText.pack(fill="both", expand=True)

def add_custom_symbol():
    symbol_word = simpledialog.askstring("Input", "Enter the word:")
    symbol_char = simpledialog.askstring("Input", "Enter the symbol:")
    if symbol_word and symbol_char:
        symbol[symbol_word.lower()] = symbol_char
        with open("symbols.py", "a") as sym_file:
            sym_file.write(f"'{symbol_word}': '{symbol_char}',\n")

def export_text():
    export_format = simpledialog.askstring("Input", "Enter the format (txt/pdf/docx):")
    if export_format and export_format.lower() in ["txt", "pdf", "docx"]:
        filename = filedialog.asksaveasfilename(defaultextension=f".{export_format}")
        if filename:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(speaker_output)

def change_language():
    global current_language
    selected_language = simpledialog.askstring("Input", "Enter the language (English, Hindi, Spanish, French):")
    if selected_language and selected_language in languages:
        current_language = selected_language
        print(f"Language changed to {current_language}")

speaker_output = ""

# GUI setup
if __name__ == '__main__':
    root = Tk()
    root.title(Titile_of_project)
    try:
        root.iconbitmap(icon_path)
    except:
        print('Favicon is missing!!')
    root.geometry("720x520")

    menubar = Menu(root)
    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label="Help Index", command=lambda: help_frame('help'))
    help_menu.add_command(label="About...", command=lambda: help_frame('about'))
    help_menu.add_separator()
    help_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="Help", menu=help_menu)
    root.config(menu=menubar)

    defaultFrame = Frame(root)
    defaultFrame.pack(fill="both", expand=True, padx=5, pady=5)
    TopFrame = Frame(defaultFrame, bd=2, width=480, height=300, padx=10, pady=10, relief=RIDGE, bg="light grey")
    TopFrame.pack(fill="both", expand=True)
    MainFrame = Frame(TopFrame)
    MainFrame.pack(fill="both", expand=True)
    DisplayFrame = Frame(MainFrame, bd=5, width=720, height=360, padx=2, relief=RIDGE, bg="cadet blue")
    DisplayFrame.pack(fill="both", expand=True)
    ButtonFrame = Frame(MainFrame, bd=5, width=720, height=80, padx=2, relief=RIDGE, bg="sky blue")
    ButtonFrame.pack(fill="both", expand=True)

    Button = Button(ButtonFrame, text="Record", padx=20, pady=10, command=s2t, fg="#ffffff", bg="#007bff", relief=RAISED, font=(buttonFont, 14, "bold"))
    Button.pack(side=LEFT, padx=30, pady=10)

    exportButton = Button(ButtonFrame, text="Export", padx=20, pady=10, command=export_text, fg="#ffffff", bg="#28a745", relief=RAISED, font=(buttonFont, 14, "bold"))
    exportButton.pack(side=LEFT, padx=30, pady=10)

    changeLangButton = Button(ButtonFrame, text="Change Language", padx=20, pady=10, command=change_language, fg="#ffffff", bg="#dc3545", relief=RAISED, font=(buttonFont, 14, "bold"))
    changeLangButton.pack(side=LEFT, padx=30, pady=10)

    customSymbolButton = Button(ButtonFrame, text="Add Custom Symbol", padx=20, pady=10, command=add_custom_symbol, fg="#ffffff", bg="#ffc107", relief=RAISED, font=(buttonFont, 14, "bold"))
    customSymbolButton.pack(side=LEFT, padx=30, pady=10)

    root.mainloop()

class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def help_frame(option):
    frame = Toplevel()
    frame.title(Titile_of_project)
    try:
        frame.iconbitmap(icon_path)
    except:
        print('Favicon is missing!!')
    frame.geometry("720x480")
    if option == 'help':
        defaultFrame = Frame(frame)
        defaultFrame.pack(fill="both", expand=True, padx=1, pady=1)
        TopFrame = LabelFrame(defaultFrame, bd=2, width=480, height=300, padx=50, pady=50, relief=RIDGE, bg="#666666", fg="#ffffff", text="Help")
        TopFrame.pack(fill="both", expand=True)
        helpText = Label(TopFrame, bg="#666666", fg="#ffffff", font=(myFont, myFontSize), text="myHelp")
        helpText.pack(fill="both", expand=True, padx=5, pady=5)
    if option == 'about':
        defaultFrame = Frame(frame)
        defaultFrame.pack(fill="both", expand=True, padx=1, pady=1)
        TopFrame = LabelFrame(defaultFrame, bd=2, width=480, height=300, padx=50, pady=50, relief=RIDGE, bg="#7280ab", fg="#ffffff", text="About")
        TopFrame.pack(fill="both", expand=True)
        aboutText = Label(TopFrame, fg="#ffffff", bg="#7280ab", font=(myFont, myFontSize), text="myAbout")
        aboutText.pack(fill="both", expand=True, padx=5, pady=5)
