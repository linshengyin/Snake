from microbit import *
import random

#精简后的贪吃蛇游戏，用于测试游戏效果

# 初始化贪吃蛇
snake = [[2, 2]]
dir = [1, 0]

# 生成食物
food = [random.randint(0, 4), random.randint(0, 4)]

# 显示初始状态
display.set_pixel(snake[0][0], snake[0][1], 9)
display.set_pixel(food[0], food[1], 5)

while True:
    # 判断按键
    if button_a.was_pressed():
        dir = [dir[1], -dir[0]]  # 左转
    elif button_b.was_pressed():
        dir = [-dir[1], dir[0]]  # 右转

    # 移动贪吃蛇
    new_head = [snake[0][0] + dir[0], snake[0][1] + dir[1]]
    if new_head == food:
        food = [random.randint(0, 4), random.randint(0, 4)]
        display.set_pixel(food[0], food[1], 5)
    else:
        tail = snake.pop()
        display.set_pixel(tail[0], tail[1], 0)
    snake.insert(0, new_head)

    # 判断游戏结束
    if new_head[0] < 0 or new_head[0] > 4 or new_head[1] < 0 or new_head[1] > 4:
        display.show(Image.SKULL)
        break
    elif new_head in snake[1:]:
        display.show(Image.SKULL)
        break

    # 显示贪吃蛇
    display.set_pixel(new_head[0], new_head[1], 9)
    sleep(500)
