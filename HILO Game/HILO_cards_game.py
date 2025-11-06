import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import os
import sys
import random
from tkinter import messagebox

user_amount = 500
cn = random.randint(1, 13)
pn = "_"
root = None

rank_names = {
    1: "ace", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
    8: "8", 9: "9", 10: "10", 11: "jack", 12: "queen", 13: "king"
}
suits = ["hearts", "diamonds", "clubs", "spades"]

def pick_random_card():
    r = random.randint(1, 13)
    s = random.choice(suits)
    filename = f"{rank_names[r]}_of_{s}.png"
    return r, s, filename

def open_second_window():
    global cn, pn, second_window, card_images, card_labels, back_img,label_img1
    global btn_high, btn_low
    start_amount = user_amount
    r, s, filename = pick_random_card()
    cn = r

    root.destroy()
    second_window = tk.Tk()
    second_window.title("High-Low Bet Game")
    second_window.geometry("500x350")
    second_window.resizable(False, False)
    second_window.configure(bg="#1e1e1e")

    positions = [(30, 80), (65, 80), (100, 80), (225, 80)]

    canvas = tk.Canvas(second_window, width=500, height=350, bg="#dfe6e9", highlightthickness=0)
    canvas.place(x=0, y=0)

    bottom_panel = Frame(second_window, bg="#2ecc71", width=600, height=80)
    bottom_panel.place(x=0, y=195)

    back_path = os.path.join("cards", "card_back_side.png")
    back_img = ImageTk.PhotoImage(Image.open(back_path).resize((75, 100)))

    img2_path = os.path.join("cards", filename)
    img2 = ImageTk.PhotoImage(Image.open(img2_path).resize((75, 100)))

    card_images = [
        back_img,
        back_img,
        back_img,
        img2
    ]

    card_labels = []
    for (x, y), img in zip(positions, card_images):
        lbl = Label(second_window, image=img, bg="#dfe6e9", borderwidth=0, highlightthickness=0)
        lbl.place(x=x, y=y)
        lbl.image = img
        card_labels.append(lbl)

    label_img1 = Label(second_window, image=back_img, bg="#dfe6e9", borderwidth=0, highlightthickness=0)
    label_img1.place(x=350, y=80)
    label_img1.image = back_img

    tk.Label(second_window, text="Hi-LO", font=("Arial", 18, "bold"), fg="purple", bg="#dfe6e9").place(x=30, y=10)

    global label_balance, label_status, label_multiplier_high, label_multiplier_low

    label_balance = tk.Label(second_window, text=f"Balance: ₹ {user_amount:.2f}", font=("Arial", 12, "bold"),
                             fg="green", bg="#dfe6e9")
    label_balance.place(x=320, y=10)

    tk.Label(second_window, text="[ Prev ]", font=("Arial", 13), bg="#dfe6e9").place(x=120, y=50)
    tk.Label(second_window, text="[ Current ]", font=("Arial", 13), bg="#dfe6e9").place(x=223, y=50)
    tk.Label(second_window, text="[ Next ]", font=("Arial", 13), bg="#dfe6e9").place(x=360, y=50)

    btn_high = tk.Button(second_window, command=check_high,
                         text="HIGH or EQUAL ↑",
                         width=16,
                         font=("Arial", 14), fg="red", bg="#81ecec",
                         activebackground="#74b9ff", activeforeground="black")
    btn_high.place(x=40, y=210)

    btn_low = tk.Button(second_window, command=check_low,
                        text="LOW or EQUAL ↓",
                        width=16,
                        font=("Arial", 14), fg="blue", bg="#81ecec",
                        activebackground="#74b9ff", activeforeground="black")
    btn_low.place(x=280, y=210)

    label_multiplier_high = tk.Label(second_window, text=f"(× )", font=("Arial", 10), bg="#2ecc71")
    label_multiplier_high.place(x=118, y=251)

    label_multiplier_low = tk.Label(second_window, text=f"(× )", font=("Arial", 10), bg="#2ecc71")
    label_multiplier_low.place(x=340, y=251)

    label_status = tk.Label(second_window, text="Status:", font=("Arial", 13), bg="#dfe6e9")
    label_status.place(x=130, y=275)

    label_startingbid = tk.Label(second_window, text=f"Starting Bid: ₹ {start_amount}", font=("Arial", 13), bg="#dfe6e9")
    label_startingbid.place(x=130, y=305)

    tk.Button(second_window, text="Exit", command=sys.exit, font=("Arial", 14), bg="#fab1a0").place(x=30, y=280)
    update_multipliers()
    update_button_text()
    second_window.mainloop()


def update_multipliers():
    global cn, label_multiplier_high, label_multiplier_low
    prob_high = (13 - cn + 1) / 13
    prob_low = cn / 13
    multiplier_high = round((1 / prob_high) * 0.5, 2)
    multiplier_low = round((1 / prob_low) * 0.5, 2)

    label_multiplier_high.config(text=f"(×{multiplier_high})")
    label_multiplier_low.config(text=f"(×{multiplier_low})")

def slide_cards(new_photo):
    global card_images, card_labels

    card_images[0] = card_images[1]
    card_images[1] = card_images[2]
    card_images[2] = card_images[3]
    card_images[3] = new_photo

    for lbl, img in zip(card_labels, card_images):
        lbl.config(image=img)
        lbl.image = img

def update_button_text():
    global cn, btn_high, btn_low
    if cn == 1:
        btn_high.config(text="High ↑")
        btn_low.config(text="Equal =")
    elif cn == 13:
        btn_high.config(text="Equal =")
        btn_low.config(text="Low ↓")
    else:  # Other cards
        btn_high.config(text="High or Equal ↑")
        btn_low.config(text="Low or Equal ↓")


def check_high():
    global user_amount, pn, cn, label_balance, label_status, label_img1
    r, s, filename = pick_random_card()
    nn = r
    prob_high = (13 - cn + 1) / 13
    multiplier = round((1 / prob_high) * 0.5, 2)

    if cn == 1:
        win = (nn > cn)
    else:
        win = (nn >= cn)

    if win:
        gain = user_amount * multiplier
        user_amount += gain
        label_status.config(text=f"Status: ✅ +₹{gain:.2f}")
    else:
        user_amount = 0
        img_path = os.path.join("cards", filename)
        show_img = ImageTk.PhotoImage(Image.open(img_path).resize((75, 100)))
        label_img1.config(image=show_img)
        label_img1.image = show_img
        label_status.config(text=f"Status: ❌ You lost all!")
        choice = messagebox.askquestion("Game Over", "You lost all your balance!\nDo you want to go to the main menu?")
        second_window.destroy()
        if choice == "yes":
            open_main_menu()
        else:
            sys.exit()

    pn = cn
    cn = nn

    img_path = os.path.join("cards", filename)
    new_img = ImageTk.PhotoImage(Image.open(img_path).resize((75, 100)))
    slide_cards(new_img)

    label_balance.config(text=f"Balance: ₹ {user_amount:.2f}")
    update_multipliers()
    update_button_text()


def check_low():
    global user_amount, pn, cn, label_balance, label_status, label_img1
    r, s, filename = pick_random_card()
    nn = r
    prob_low = cn / 13
    multiplier = round((1 / prob_low) * 0.5, 2)

    if cn == 13:
        win = (nn < cn)
    else:
        win = (nn <= cn)

    if win:
        gain = user_amount * multiplier
        user_amount += gain
        label_status.config(text=f"Status: ✅ +₹{gain:.2f}")
    else:
        user_amount = 0
        img_path = os.path.join("cards", filename)
        show_img = ImageTk.PhotoImage(Image.open(img_path).resize((75, 100)))
        label_img1.config(image=show_img)
        label_img1.image = show_img
        label_status.config(text="Status: ❌ You lost all!")
        choice = messagebox.askquestion("Game Over", "You lost all your balance!\nDo you want to go to the main menu?")
        second_window.destroy()
        if choice == "yes":
            open_main_menu()
        else:
            sys.exit()

    pn = cn
    cn = nn

    img_path = os.path.join("cards", filename)
    new_img = ImageTk.PhotoImage(Image.open(img_path).resize((75, 100)))
    slide_cards(new_img)

    label_balance.config(text=f"Balance: ₹ {user_amount:.2f}")
    update_multipliers()
    update_button_text()

def store_amount():
    global user_amount, entry_amount, label_alert
    try:
        amount = float(entry_amount.get())
        user_amount = amount

        if user_amount > 16000:
            label_alert.config(text="Highest Amount: ₹ 16,000", fg="red")
        elif user_amount < 1:
            label_alert.config(text="Lowest Amount: ₹ 1", fg="red")
        else:
            open_second_window()
    except ValueError:
        label_alert.config(text="Please enter a valid number", fg="orange")

def open_main_menu():
    global root, entry_amount, label_alert
    root = tk.Tk()
    root.title("High-Low Bet Game")
    root.geometry("500x350")
    root.resizable(False, False)
    root.configure(bg="#2ecc71")

    label1 = tk.Label(root, text="Start", font=("Arial", 14), fg="#ff006f", bg="#2ecc71")
    label1.place(x=75, y=25)

    label1 = tk.Label(root, text="High", font=("Arial", 18, "bold"),fg="#3498db", bg="#2ecc71")
    label1.place(x=120, y=20)

    label1 = tk.Label(root, text="Low", font=("Arial", 18, "bold"),fg="#3498db", bg="#2ecc71")
    label1.place(x=180, y=20)

    label1 = tk.Label(root, text="Bet Game", font=("Arial", 14), fg="#ff006f", bg="#2ecc71")
    label1.place(x=235, y=25)

    label = tk.Label(root, text="Enter Bidding Amount", font=("Arial", 10), fg="blue",bg="#2ecc71")
    label.place(x=100, y=70)

    entry_amount = tk.Entry(root, font=("Arial", 14), width=7,bg="#2ecc71")
    entry_amount.place(x=100, y=110)
    entry_amount.insert(0, "500")

    label_alert = tk.Label(root, text="", font=("Arial", 10), fg="blue",bg="#2ecc71")
    label_alert.place(x=250, y=110)

    label2 = tk.Label(root, text="Rules :", font=("Arial", 10), fg="blue",bg="#2ecc71")
    label2.place(x=100, y=150)


    tk.Label(root, text="1. Max bidding amount is ₹ 16,000.", font=("Arial", 10),bg="#2ecc71").place(x=150, y=150)
    tk.Label(root, text="2. Guess card is higher or lower.", font=("Arial", 10),bg="#2ecc71").place(x=150, y=170)
    tk.Label(root, text="3. Game will generate random card from deck of 52 cards.", font=("Arial", 10),bg="#2ecc71").place(x=150, y=190)
    tk.Label(root, text="4. After every win complete balance will be on bid.", font=("Arial", 10),bg="#2ecc71").place(x=150, y=210)

    tk.Button(root, text="Next", command=store_amount, font=("Arial", 14),bg="#3498db",fg="#2ecc71").place(x=100, y=250)
    tk.Button(root, text="Exit", command=sys.exit, font=("Arial", 14),bg="#3498db", fg="Red").place(x=170, y=250)

    root.mainloop()

open_main_menu()
