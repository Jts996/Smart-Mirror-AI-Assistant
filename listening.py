import threading
import time


class Listening(threading.Thread):

    def run(self):
        print("Listening for request")
        Listening.heard()

    @staticmethod
    def heard():
        from Assistant_responses import mirror_mirror
        from Assistant_responses import end
        from Assistant_responses import speak

        from Assistant_responses import record_audio
        from Mirror_Mirror import Gui

        request_not_received = True
        print("-------------------------------------------------")
        print("Heard initiated")

        # Keep count of the number of times the program loops for a request
        tries = 1
        # Once it tries up tp this limit the program will go back to waiting for the Wake word
        tries_limit = 5

        while request_not_received:
            print("recording request")
            print("Try number: " + str(tries))
            data = record_audio()
            if data is not None:
                print("The users request was: " + str(data))
                print("Finding response to user request")
                found = mirror_mirror(data)

                # Sleep to wait on the return of the find response to the user and to respond
                #  Then continue on
                print("5 second sleep")
                time.sleep(5)
                if found:
                    request_not_received = False
                    # Try up too receive user input and/or find the response up to limited number
                    # If it reaches this limit, reset back to wake_word_detection
                else:
                    if tries == tries_limit:
                        break
                    tries += 1
            else:
                if tries == tries_limit:
                    break
                tries += 1

        if tries == tries_limit:
            speak("Sorry I can't help you with that! Try again later")
            time.sleep(3.7)
        else:
            print("User request has been dealt with, now back to waiting for wake word")

        end()
        time.sleep(2)
        print("Restarting, going back to wait for wake word")
        Gui.close_window()
        Gui.wake_word_detection()
