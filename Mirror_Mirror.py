import tkinter as tk
import threading
from Assistant_responses import record_audio
import listening

app = tk.Tk()


class Gui(tk.Frame):

    @staticmethod
    def open_window():
        # global app
        Gui.start_thread()

        app.mainloop()

    @staticmethod
    def start_thread():
        thread1 = threading.Thread(target=listening.Listening.heard)
        thread1.start()

    @staticmethod
    def close_window():
        # global app
        app.withdraw()

    @staticmethod
    def wake_word_detection():
        from Assistant_responses import start

        waiting = True
        print("-------------------------------------------------")
        print("Wake word detection initiated")
        while waiting:
            print("Waiting for wake word")
            wake_word = record_audio()
            print("Checking wake word")
            # print(str(wake_word))
            if wake_word == "mirror mirror":
                print("Said")
                start()
                #Gui.open_window()
                Gui.start_thread()
                waiting = False


if __name__ == '__main__':
    Gui.wake_word_detection()

