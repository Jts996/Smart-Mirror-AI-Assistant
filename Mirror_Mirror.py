import tkinter as tk
import time
from threading import Thread
from PIL import Image, ImageTk
from itertools import count, cycle

app = tk.Tk()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()


# This class deals with initiating everything for the application GUI and starting the
# assistant thread
class Application:

    # This function deals with starting the GUI
    #
    # sets the width and height of the window and the background colour
    # It also defines the Label and it parameters for the UI GIF to be contained
    @staticmethod
    def open_window():

        app.geometry(str(screen_width) + 'x' + str(screen_height))
        app.configure(background='black')

        # Creating the Label in which to hold the Gif
        gif_label = tk.Label(borderwidth=0, highlightthickness=0)
        # Calculating where the center of the screen is
        mid_width = screen_width / 3.2
        mid_height = screen_height / 6
        # Placing the Label in the center of the screen
        gif_label.place(x=mid_width, y=mid_height)
        lbl = ImageLabel(gif_label)
        lbl.pack()
        lbl.load('listening_gif.gif')

        # Starting the window
        app.mainloop()

    # Function which starts the thread which handles:
    #
    # listening for wake word,
    # receiving the user request and
    # finding the required response
    #
    # See the functions for more details
    @staticmethod
    def start_assistant_thread():

        from listening import Listening

        thread_heard = Thread(target=Listening.wake_word_detection)
        thread_heard.start()


# Class for dealing with the iterations over the different frames of the GIF
class ImageLabel(tk.Label):

    # Function which loads the file
    #
    # It firstly checks that if the file exists
    def load(self, im):

        # Checks to see if the file exists
        if isinstance(im, str):
            im = Image.open(im)
        frames_list = []

        try:
            # Loading all the frames of the gif
            # and appending them to the frames list
            # This allows for quick access to the frames for real time playing
            for i in count(1):
                frames_list.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        # This iterates over all the gif frames stored in the "frames" list
        # once it reaches the end, it with repeat
        self.frames = cycle(frames_list)

        # Setting a delay to alter the speed of the gif
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        # Returns next frame
        # "next" allows for the gif to continue in the loop, thus stopping
        # the program from raising a StopIteration
        if len(frames_list) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    # Adds the next frame to the Tkinter window
    def next_frame(self):
        time.sleep(0.002)
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)


if __name__ == '__main__':
    # Start the thread that deals with the users voice interactions
    print("-------------------------------------------------")
    print("Assistant starting")
    Application.start_assistant_thread()

    # Open the application GUI
    print("GUI Opening")
    Application.open_window()
