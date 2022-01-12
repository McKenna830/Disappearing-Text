from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
WHITE = "#F5F5F5"
RED = "#F05454"
BLUE = "#30475E"
BLACK = "#121212"
FONT_NAME = "Times New Roman"
WORK_MIN = 5
timer = None
timeout = None
comparison = None
typing = False

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    elif count == 0:
        save_input()
        end_session()
    else:
        start_timer()


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    work_sec = WORK_MIN * 60
    count_down(work_sec)
    inactive(5)
    compare_inputs("")
    title_label.config(text="Write!")
    title_label.grid(column=2, row=1, columnspan=1)
    canvas.grid(column=1, row=1)
    reset_button.grid(column=3, row=1)
    user_input.grid(column=1, row=2, columnspan=4)
    start_button.grid_forget()
    instruction_label.grid_forget()


def end_session():
    window.after_cancel(timeout)
    window.after_cancel(comparison)
    user_input.delete(1.0, END)
    title_label.config(text="Well Done!")
    title_label.grid(column=1, row=0, columnspan=2)
    instruction_label.config(text="Text has been copied to clipboard.\nWould you like to start again?")
    instruction_label.grid(column=1, row=1, columnspan=2)
    start_button.grid(column=1, row=2, columnspan=2)
    user_input.grid_forget()
    canvas.grid_forget()
    reset_button.grid_forget()


# ---------------------------- INACTIVITY COUNTDOWN ------------------------------- #

def inactive(inactive_time_remaining):
    global timeout
    timeout = window.after(1000, inactive, inactive_time_remaining - 1)
    if inactive_time_remaining > 2:
        title_label.config(fg=BLUE)
        user_input.config(bg=WHITE)
    if inactive_time_remaining == 0:
        user_input.delete(1.0, END)
        window.after_cancel(timer)
        reset_button.focus_force()
        window.after_cancel(timeout)
        window.after_cancel(comparison)
        title_label.config(text="Try Again")
    if 0 < inactive_time_remaining < 3:
        user_input.config(bg=RED)
        title_label.config(fg=RED)


# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    window.after_cancel(timeout)
    window.after_cancel(timer)
    window.after_cancel(comparison)
    title_label.config(text="Instructions", fg=BLUE)
    title_label.grid(column=2, row=0)
    instruction_label.grid(column=2, row=2)
    start_button.grid(column=1, row=3, columnspan=2)
    user_input.grid_forget()
    reset_button.grid_forget()
    canvas.grid_forget()


# ---------------------------- INPUT MONITORING & MANAGEMENT ------------------------------- #

def compare_inputs(previous_input):
    global comparison
    global typing
    comparison = window.after(1000, compare_inputs, user_input.get(1.0, END))
    current_input = user_input.get(1.0, END)
    if previous_input != current_input:
        typing = True
        window.after_cancel(timeout)
        user_input.config(bg=WHITE)
        instruction_label.config(fg=BLUE)
    else:
        if typing:
            window.after_cancel(timeout)
            typing = False
            inactive(5)


def save_input():
    window.clipboard_clear()
    window.clipboard_append(user_input.get(1.0, END))
    window.update()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Don't Stop. Write It, Write It")
window.config(padx=100, pady=50, bg=WHITE)

canvas = Canvas(width=110, height=64, bg=WHITE, highlightthickness=0)
timer_text = canvas.create_text(55, 30, text=f"You must type for {WORK_MIN} minutes."
                                             f"\nIf you pause for more than 5 seconds, your work will be deleted."
                                             f"\nComplete the challenge and your work will be automatically copied to the clipboard.",
                                fill=BLACK, font=(FONT_NAME, 40, "normal"))

title_label = Label(text="Instructions", font=(FONT_NAME, 60), fg=BLUE, bg=WHITE, )
title_label.grid(column=1, row=0, columnspan=2)

instruction_label = Label(text=f"You must type for {WORK_MIN} minutes."
                               f"\nIf you pause for more than 5 seconds, your work will be deleted."
                               f"\nComplete the challenge and your work will be automatically copied to the clipboard.",
                          fg=BLACK, bg=WHITE, font=(FONT_NAME, 22, "normal"), pady=30)
instruction_label.grid(column=1, row=1, columnspan=2)

start_button = Button(text="Start", font=(FONT_NAME, 40, "bold"), fg=BLUE,
                      command=lambda: [start_timer(), user_input.focus()])
start_button.grid(column=1, row=2, columnspan=2)

reset_button = Button(text="Reset", font=(FONT_NAME, 35), highlightthickness=0, command=reset_timer)

user_input = Text(window, bg=WHITE, font=(FONT_NAME, 15), fg=BLUE)

window.mainloop()
