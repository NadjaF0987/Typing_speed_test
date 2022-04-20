from tkinter import *
from functionality import TypeTest

FONT_TIMER = "Courier"
FONT_TEXT = "Arial"
BACKGROUND_COL = "#9bdeac"
DARK_BLUE = "#1163AA"
PINK = "#D91657"
TEST_SEC = 3


class Interface:
    def __init__(self, functionality: TypeTest):
        # initialise with the functionality
        self.test = functionality
        # window and canvas setup
        self.window = Tk()
        self.window.title("Test your Typing Speed")
        self.window.config(padx=50, pady=50)
        self.window.minsize(width=300, height=300)
        self.canvas = Canvas(width=200, height=75, bg=BACKGROUND_COL)
        # UI START PAGE
        self.timer_text = Label(text=f"time left: {TEST_SEC} sec", font=(FONT_TIMER, 12), fg=PINK)
        self.timer_text.grid(column=1, row=0, sticky=E)
        self.timer = None
        self.text_widget = Text(self.window,
                                height=10, width=50, bg="white", font=(FONT_TEXT, 16), wrap=WORD, spacing2=3, padx=3)
        self.text_widget.insert(END, self.test.words_to_type)
        self.text_widget.config(state=DISABLED)
        self.text_widget.grid(column=0, row=1, columnspan=2)
        # Note KeyPress event is bound to the input field.
        self.input_field = Text(self.window, height=10, width=50, font=("Arial", 16), fg=DARK_BLUE)
        self.input_field.grid(column=0, row=2, columnspan=2)
        self.input_field.bind('<KeyPress>', lambda event: self.count_down(event, TEST_SEC))
        self.input_field.focus()
        # UI FINISH PAGE - Hidden
        self.score_label = Label(self.window, text=None, font=(FONT_TEXT, 20))
        self.score_label.grid_forget()
        self.spelling_label = Label(self.window, text=None, font=(FONT_TEXT, 20))
        self.spelling_label.grid_forget()
        self.restart_label = Label(self.window, justify=CENTER, text="Do you wanna try again?", font=(FONT_TEXT, 20))
        self.restart_label.grid_forget()
        self.yes_btn = Button(text="Yes", width=10, command=self.restart)
        self.yes_btn.grid_forget()
        self.no_btn = Button(text="No", width=10, command=self.close)
        self.no_btn.grid_forget()

        self.window.mainloop()

    def restart(self):
        """ Restarts the test. Resets the timer, UI and fetches new words. """
        # Reset the functionality
        self.test.start_again()
        # UI START PAGE.
        self.timer_text.config(text=f"time left: {TEST_SEC} sec")
        self.timer_text.grid(column=1, row=0, sticky=E)
        self.timer = None
        # delete the old words to copy. And insert new words to copy.
        self.text_widget.config(state=NORMAL)
        self.text_widget.delete("1.0", END)
        self.text_widget.insert(END, self.test.words_to_type)
        self.text_widget.grid(column=0, row=1, columnspan=2)
        self.input_field.grid(column=0, row=2, columnspan=2)
        self.input_field.delete('1.0', END)
        self.input_field.bind('<KeyPress>', lambda event: self.count_down(event, TEST_SEC))
        self.input_field.focus()
        # UI FINISH PAGE - Hidden
        self.score_label.grid_forget()
        self.spelling_label.grid_forget()
        self.restart_label.grid_forget()
        self.yes_btn.grid_forget()
        self.no_btn.grid_forget()

    def close(self):
        """ Quit and close the window and code. """
        self.window.quit()

    def count_down(self, event, time):
        """ Count down functionality.
        After test time/TEST_SEC the type_speed function is called and the UI is changed """
        self.input_field.unbind('<KeyPress>')
        if time < 10:
            time_left = f"0{time}"
        else:
            time_left = time
        self.timer_text.config(text=f"time left: {time_left} sec")
        if time > 0:
            self.timer = self.window.after(1000, self.count_down, event, time - 1)
        else:
            # Find words per minute and spell check
            self.type_speed()
            # Hide the UI Start page
            self.timer_text.grid_forget()
            self.text_widget.grid_forget()
            self.input_field.grid_forget()
            # Show the UI Finish page
            self.restart_label.grid(column=0, row=2, columnspan=2, pady=(100, 10))
            self.yes_btn.grid(column=0, row=3, pady=(0, 20))
            self.no_btn.grid(column=1, row=3, pady=(0, 20))

    def type_speed(self):
        """ Fetches the user inputted words, uses the functionality to calculate the type speed and displays it.
          Calls the correct_spelled function. """
        inputted_words = self.input_field.get(1.0, END)
        wpm = self.test.word_per_minute(inputted_words)
        self.score_label.config(text=f"Your score: {wpm} WPM")
        self.score_label.grid(column=0, row=0, columnspan=2, sticky=W, pady=(20, 30))
        # Spell check
        self.correct_spelled()

    def correct_spelled(self):
        """ Uses the functionality to get the amount of misspelled words and display it. """
        result = self.test.spell_check(self.test.word_count, self.test.inputted_words_list)
        self.spelling_label.config(text=result, justify=LEFT)
        self.spelling_label.grid(column=0, row=1, columnspan=2, sticky=W)
