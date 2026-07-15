from py_compile import main
import tkinter as tk
import random

def run_game():
    global score, time_left, life, game_running, balloons

    score = 0
    time_left = GAME_TIME
    life = MAX_LIFE
    game_running = True

    balloons.clear()
    canvas.delete("all")

    score_label.config(text="Score: 0")
    time_label.config(text=f"Time: {GAME_TIME}")
    update_life()

    restart_btn.pack_forget()

    spawn_loop()
    move_balloons()
    update_time()
# ----------------- ตั้งค่าเกม -----------------
WIDTH = 600
HEIGHT = 500
GAME_TIME = 30
MAX_LIFE = 3

# ----------------- ตัวแปร -----------------
score = 0
time_left = GAME_TIME
life = MAX_LIFE
game_running = True
balloons = []

# ----------------- หน้าต่าง -----------------
root = tk.Tk()
root.title("🎈 Balloon Shooter Deluxe")
root.geometry(f"{WIDTH}x{HEIGHT}")

# ----------------- UI -----------------
top_frame = tk.Frame(root)
top_frame.pack()

score_label = tk.Label(top_frame, text="Score: 0", font=("Arial", 14))
score_label.pack(side="left", padx=10)

time_label = tk.Label(top_frame, text="Time: 30", font=("Arial", 14))
time_label.pack(side="left", padx=10)

life_label = tk.Label(top_frame, text="Life: ❤️❤️❤️", font=("Arial", 14))
life_label.pack(side="left", padx=10)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT-50, bg="skyblue")
canvas.pack()

# ----------------- ฟังก์ชัน -----------------

def create_balloon():
    x = random.randint(50, WIDTH-50)
    balloon = canvas.create_oval(x-20, HEIGHT, x+20, HEIGHT-40, fill=random.choice(["red","blue","yellow","pink"]))
    speed = random.randint(2, 5)
    balloons.append([balloon, speed])

def move_balloons():
    global life, game_running

    if not game_running:
        return

    for b in balloons[:]:
        canvas.move(b[0], 0, -b[1])
        x1, y1, x2, y2 = canvas.coords(b[0])

        # หลุดจอ = เสียชีวิต
        if y2 < 0:
            canvas.delete(b[0])
            balloons.remove(b)
            life -= 1
            update_life()

            if life <= 0:
                end_game()

    root.after(30, move_balloons)

def spawn_loop():
    if game_running:
        create_balloon()
        root.after(800, spawn_loop)

def pop(event):
    global score

    if not game_running:
        return

    for b in balloons[:]:
        x1, y1, x2, y2 = canvas.coords(b[0])

        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            canvas.delete(b[0])
            balloons.remove(b)

            score += 1
            score_label.config(text=f"Score: {score}")
            break

def update_time():
    global time_left, game_running

    if not game_running:
        return

    if time_left > 0:
        time_left -= 1
        time_label.config(text=f"Time: {time_left}")
        root.after(1000, update_time)
    else:
        end_game()

def update_life():
    life_label.config(text="Life: " + "❤️"*life)

def end_game():
    global game_running
    game_running = False

    canvas.create_text(WIDTH/2, HEIGHT/2,
                       text=f"GAME OVER\nScore: {score}",
                       font=("Arial", 24),
                       fill="red")

    restart_btn.pack(pady=10)

def restart():
    global score, time_left, life, game_running, balloons

    score = 0
    time_left = GAME_TIME
    life = MAX_LIFE
    game_running = True

    balloons.clear()
    canvas.delete("all")

    score_label.config(text="Score: 0")
    time_label.config(text="Time: 30")
    update_life()

    restart_btn.pack_forget()

    spawn_loop()
    move_balloons()
    update_time()

# ----------------- ปุ่ม -----------------
restart_btn = tk.Button(root, text="Restart 🔁", font=("Arial", 14), command=restart)

# ----------------- เริ่มเกม -----------------
canvas.bind("<Button-1>", pop)

spawn_loop()
move_balloons()
update_time()

root.mainloop()

if __name__ == "__main__":
    main()