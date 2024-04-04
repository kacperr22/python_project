import random
from tkinter import *
from PIL import Image, ImageTk



GAME_WIDTH = 1000
GAME_HEIGHT = 800
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = '#0000CD'
FOOD_COLOR = '#A9A9A9'


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags='snake')
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")


def next_move(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text='Score:{}'.format(score))

        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_move, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if new_direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if new_direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if new_direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if new_direction != 'up':
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        print('Check')
        return True

    if y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text="GAME OVER", fill='red', tags="gameover")


def set_background():

    image_path = "C:/Users/kacperk/PycharmProjects/pythonProject4/Image/snake_bg.png"
    img = Image.open(image_path)

    # Calculate proportional image dimensions to game size
    img_width, img_height = img.size
    scale_factor = min(GAME_WIDTH / img_width, GAME_HEIGHT / img_height)
    new_width = int(img_width * scale_factor)
    new_height = int(img_height * scale_factor)

    # Proportionally reduce the image size
    img = img.resize((new_width, new_height), Image.BICUBIC)
    return img


window = Tk()
window.title("Snake")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score={}".format(score), font=("Roboto  ", 30))
label.pack()

canvas = Canvas(window, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

photo = ImageTk.PhotoImage(set_background())
canvas.create_image(0, 0, anchor="nw", image=photo)

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_width()
screen_height = window.winfo_height()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_move(snake, food)
window.mainloop()
