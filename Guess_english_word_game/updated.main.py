import pandas as pd
from tkinter import *
import math
import random
import difflib


background = "#B1DDC6"
easy_color = "#8ada43"
normal_color = "#06b36e"
hard_color = "#d13a3f"
points = 0
entered_word = ""



# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def counting_before_game(level_window, count, level_sec):
    canvas.itemconfig(word_title, text=f"{count}")
    start_button.grid_forget()
    if count > 0:
        level_window.after(1200, counting_before_game, level_window, count - 1, level_sec)
    else:
        canvas.itemconfig(language_title, text="English")
        canvas.itemconfig(word_title, text=f"{random_word}")
        enter_answer()
        start_game(level_sec)
        canvas.itemconfig(example_title, fill="black")
        canvas.itemconfig(example_title, state="normal",
                          text=f"{file.loc[file['english'] == random_word, 'example'].values[0]}")



def counting_over_game(over_window, level_window, count, level_sec):
    global points, random_word, lithuanian_translation
    wrong_button.grid(column=0, row=2)
    right_buttom.grid(column=1, row=2)
    enter_answ.grid(column=0, row=1, columnspan=2)
    enter_answ.delete(0, END)
    enter_answ.insert(END, "ENTER THE ANSWER")
    lithuanian_translation = []
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    points = 0
    canvas.itemconfig(points_title, text=f"SCORE: {points}")
    canvas.itemconfig(word_title, text=f"{count}")
    over_window.destroy()
    start_button.grid_forget()
    random_en_word()
    random_word = random_en_word()
    canvas.itemconfig(example_title, state="hidden",
                      text=f"{file.loc[file['english'] == random_word, 'example'].values[0]}")
    if count > 0:
        level_window.after(1200, counting_before_game, level_window, count - 1, level_sec)
    else:
        canvas.itemconfig(language_title, text="English")
        canvas.itemconfig(word_title, text=f"{random_word}")
        enter_answer()
        start_game(level_sec)
        canvas.itemconfig(example_title, fill="normal",
                          text=f"{file.loc[file['english'] == random_word, 'example'].values[0]}")


def count_down(count):
    global points
    count_min = math.floor(count / 60)
    if count_min <= 9:
        count_min = f"0{count_min}"
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        enter_answ.delete(0, END)
        enter_answ.insert(END, "ENTER THE ANSWER")
        window.after_cancel(timer)
        enter_answ.grid_forget()
        wrong_button.grid_forget()
        right_buttom.grid_forget()
        game_over()

def start_game(level_sec):
    count_down(level_sec)

# ---------------------------- words ------------------------------- #
file = pd.read_csv("english_words.csv")
english_words_list = file.english.to_list()

def random_en_word():
    random_word = random.choice(english_words_list)
    if len(random_word) > 13:
        canvas.itemconfig(font = ("ForoRounded-ExtraBold", 45, "bold"))
    return random_word


random_word = random_en_word()


# ---------- words (check answer) -------------- #
def calculate_similarity(word1, word2):
    return difflib.SequenceMatcher(None, word1, word2).ratio()
def check_answer():
    global points, entered_word, random_word, lithuanian_translation
    lithuanian_translation = []
    first_lt_word = file.loc[file['english'] == random_word, 'lithuanian'].values[0]
    lithuanian_translation.append(first_lt_word)
    try:
        third_lt_word = file.loc[file['english'] == random_word, 'lithuanian2'].values[0]
        fourth_lt_word = file.loc[file['english'] == random_word, 'lithuanian3'].values[0]
        fifth_lt_word = file.loc[file['english'] == random_word, 'lithuanian4'].values[0]
    except:
        pass
    else:
        lithuanian_translation.append(third_lt_word)
        lithuanian_translation.append(fourth_lt_word)
        lithuanian_translation.append(fifth_lt_word)

    similarity = 0
    for i in lithuanian_translation:
        try:
            number = calculate_similarity(entered_word, i)
        except:
            pass
        else:
            if number > similarity:
                similarity = number

    if similarity >= 0.7:
        points += 1
        random_en_word()
        random_word = random_en_word()
        canvas.itemconfig(word_title, text=f"{random_word}")
        canvas.itemconfig(example_title, state="normal",
                          text=f"{file.loc[file['english'] == random_word, 'example'].values[0]}")
        window.after_cancel(timer)
        count_down(25)
    else:
        canvas.itemconfig(wrong_title, state="normal")
        window.after(500, hide_wrong_title)
    # Update points display
    canvas.itemconfig(points_title, text=f"SCORE: {points}")

def hide_wrong_title():
    canvas.itemconfig(wrong_title, state="hidden")
def submit_answer():
    global entered_word
    entered_word = enter_answ.get()
    check_answer()



# ---------------------------- Enter the answer ------------------------------- #
def select_all(event):
    global enter_answ
    enter_answ.select_range(0, END)
def get_entered_text(event):
    global entered_word
    entered_word = enter_answ.get()


def enter_answer():
    enter_answ.grid(column=0, row=1, columnspan=2)


# ---------------------------- photo switch ------------------------------- #
def save():
    global image
    new_image = PhotoImage(file="card_back.png")
    canvas.itemconfig(card_imagine, image=new_image)
    image = new_image
# ---------------------------- GAME OVER ------------------------------- #
def end_game():
    window.destroy()



def game_over():
    global points
    over_window = Toplevel(window)
    over_window.title("GAME OVER")
    over_window.config(padx=100, pady=100, bg=background)
    game_over_label = Label(over_window, text="GAME OVER", font=("ForoRounded-ExtraBold", 15), fg="#d13a3f",
                            bg=background)
    game_over_label.grid(column=0, row=0, columnspan=2)
    right_answer_label = Label(over_window, text=f"The right answer is: {file.loc[file['english'] == random_word, 'lithuanian'].values[0]}.",
                               font=("ForoRounded-ExtraBold", 15), fg="black", bg=background)
    right_answer_label.grid(column=0, row=1, columnspan=2)
    score_label = Label(over_window, text=f"Your score is {points}.", font=("ForoRounded-ExtraBold", 15), fg="black",
                            bg=background)
    score_label.grid(column=0, row=2, columnspan=2)

    new_game_button = Button(over_window, text="NEW GAME", highlightthickness=0, font=("ForoRounded-ExtraBold", 10), command=lambda: counting_over_game(over_window, window, count=3, level_sec=25))
    new_game_button.grid(column=1, row=3, pady=30)
    end_game_button = Button(over_window, text="END GAME", highlightthickness=0, font=("ForoRounded-ExtraBold", 10), command=end_game)
    end_game_button.grid(column=0, row=3, pady=30)




# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=60, pady=60, bg=background)

canvas = Canvas(width=800, height=526, bg=background, highlightthickness=0)
img = PhotoImage(file="card_front.png")
card_imagine = canvas.create_image(400, 263, image=img)
language_title = canvas.create_text(400, 150, text="Language", fill="black", font=("ForoRounded-ExtraBold", 25))
word_title = canvas.create_text(400, 230, text="Word", fill="black", font=("ForoRounded-ExtraBold", 65, "bold"))
example_title = canvas.create_text(400, 300, text=f"{file.loc[file['english'] == random_word,'example'].values[0]}", font=("ForoRounded-ExtraBold", 10), state="hidden")
timer_text = canvas.create_text(400, 340, text="00:00", fill="black", font=("ForoRounded-ExtraBold", 15))
points_title = canvas.create_text(600, 100, text=f"SCORE: {points}", font=("ForoRounded-ExtraBold", 10, "bold"))
wrong_title = canvas.create_text(400, 415, text="WRONG", state="hidden", fill="red", font=("ForoRounded-ExtraBold", 10))
canvas.grid(column=0, row=0, columnspan=2, rowspan=2)

wrong_img = PhotoImage(file="wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=game_over)
wrong_button.grid(column=0, row=2)

right_img = PhotoImage(file="right.png")
right_buttom = Button(image=right_img, highlightthickness=0, bg=background, command=submit_answer)
right_buttom.grid(column=1, row=2)

start_img = PhotoImage(file="start.png.png")
start_button = Button(window, text="Start", image=start_img,  command=lambda: counting_before_game(window, count=3, level_sec=25))
start_button.grid(column=0, row=1, columnspan=2)

enter_answ = Entry(width=20, background=background, font=("ForoRounded-ExtraBold", 14), justify="center")
enter_answ.insert(END, "ENTER THE ANSWER")
enter_answ.bind("<FocusIn>", select_all)
enter_answ.bind("<Return>", get_entered_text)
enter_answ.bind("<Return>", lambda event: submit_answer())
enter_answ.grid_forget()













window.mainloop()