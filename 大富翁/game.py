import random

class Map:  # 紀錄地產訊息
    def __init__(self, order):
        if order == 2 or order == 3 or order == 6 or order == 7:#如果人物移動左右兩邊的那兩塊地的話
            self.value1 = 300#買地的價格
            self.rent1 = 70#單純買地沒有蓋房子的過路費
            self.value2 = 600#蓋房子的價格
            self.rent2 = 300#蓋房子後的過路費
        else:#以下同上
            self.value1 = 500
            self.rent1 = 100
            self.value2 = 1000
            self.rent2 = 500
        self.owner = -1
        self.level = 0
        if order == 0:
            self.text_local = (290, 120)
        elif order == 1:
            self.text_local = (800, 120)
        elif order == 2:
            self.text_local = (940, 200)
        elif order == 3:
            self.text_local = (940, 500)
        elif order == 4:
            self.text_local = (790, 550)
        elif order == 5:
            self.text_local = (285, 550)
        elif order == 6:
            self.text_local = (138, 500)
        elif order == 7:
            self.text_local = (138, 265)

def get_dice():  # 擲骰子
    return random.randint(1, 6)

def Special(pos):  # 判斷是否觸發特殊事件
    if pos == 5 or pos == 11 or pos == 15 or pos == 19 or pos == 25 or pos == 31 or pos == 35 or pos == 39:
        return True
    else:
        return False

def click_button(pos_x, pos_y, button_id):  # 判斷滑鼠是否點擊了按鈕
    if button_id == 0:
        if 440 <= pos_x <= 640 and 315 <= pos_y <= 365:
            return True
        else:
            return False
    else:
        if 440 <= pos_x <= 640 and 415 <= pos_y <= 465:
            return True
        else:
            return False

def full_somewhere(num_local, player):  # 判斷某地是否有人
    flag = 0
    for i in range(len(player)):
        if player[i].local == num_local:
            flag = 1
    if flag == 1:
        return True
    else:
        return False

def local2order(local):  # 位置與地產座標對應
    if 0 <= local < 5:
        return 0
    elif 6 <= local < 11:
        return 1
    elif 12 <= local < 15:
        return 2
    elif 16 <= local < 19:
        return 3
    elif 20 <= local < 25:
        return 4
    elif 26 <= local < 31:
        return 5
    elif 32 <= local < 35:
        return 6
    elif 36 <= local < 39:
        return 7

def game_over(player):  # 判斷遊戲是否結束
    for i in range(len(player)):
        if player[i].money < 0 or player[i].gpa <= 1.0:
            return - (i + 1)
        if player[i].gpa >= 4.0:
            return i + 1
    return 0