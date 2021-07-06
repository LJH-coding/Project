import pygame
import sys
import time

from draw import Button, draw_text, draw_mapstatus, draw_player
from game import *
from player import Player


pygame.init()

screen_size = (1080, 680)  # 第一個是寬度，第二個是高度
role_size = (60, 60)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("大富翁")
map_screen = pygame.image.load('image/地圖.bmp')
stop_picture = pygame.image.load('image/禁止.jpg')
stop_picture = pygame.transform.scale(stop_picture, (20, 20))

lose_sound = pygame.mixer.Sound('sound/失敗.wav')  # 載入音效
win_sound = pygame.mixer.Sound('sound/勝利.wav')
up_sound = pygame.mixer.Sound('sound/升級.wav')
click_sound = pygame.mixer.Sound('sound/按鍵.wav')
chances_sound = pygame.mixer.Sound('sound/事件.wav')

picture_dice = []
for i in range(6):#骰子設定
    picture_dice.append(pygame.image.load('image/dice/%d.jpg'%(i+1)))

map_screen = pygame.transform.scale(map_screen, screen_size)

screen.blit(map_screen, (0, 0))

play_button = Button(screen,"開始遊戲")  # 設定開始按紐
play_button.draw_button()

status = 0  # 控制遊戲進程 0：遊戲未開始 1：選擇遊戲人數 2：擲骰子 3：玩家行走 4：觸發事件 5：買地建房 6：遊戲結束
cur_player = 0  # 當前玩家
dice_answer = 1 # 擲骰子結果
player = []
role = []

local_init = [0, 20, 12, 32]  # 四位玩家最初的位置
map_status = []
for i in range(8):
    map_status.append(Map(i))  # 儲存地產訊息，包括有者、價值、租金等

while True:
    if status == 0:  # 遊戲未開始
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = event.pos
                #print(mouse_x, mouse_y)
                if click_button(mouse_x, mouse_y, 0):
                    click_sound.play()
                    num_player_button = Button(screen, '請輸入遊玩人數（2~4）')
                    num_player_button.draw_button()
                    draw_text(screen, (540, 440), '操作指南：按↑擲骰子、購買地產',
                              50, 'msjh.ttc', pygame.Color('gold'))
                    status = 1
        pygame.display.update()
    elif status == 1:  # 選擇遊戲人數
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if 258 <= event.key <= 260 or 50 <= event.key <= 52: #載入相應數量腳色
                    click_sound.play()
                    role.append(pygame.image.load('image/role/花花.jpg'))
                    role.append(pygame.image.load('image/role/泡泡.jpg'))
                    if event.key == 259 or event.key == 51:
                        role.append(pygame.image.load('image/role/毛毛.jpg'))
                    elif event.key == 260 or event.key == 52:
                        role.append(pygame.image.load('image/role/毛毛.jpg'))
                        role.append(pygame.image.load('image/role/魔人啾啾.jpg'))
                    screen.blit(map_screen, (0, 0))
                    for i in range(len(role)): #初始化玩家
                        role[i] = pygame.transform.scale(role[i], role_size)
                        player.append(Player(i))
                        player[i].local = local_init[i]
                    draw_player(screen, player, role, stop_picture)
                    status = 2
    elif status == 2: #擲骰子
        for i in range(6):  # 執行骰子動畫
            screen.blit(picture_dice[i], (500, 400))
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 273:
                    dice_answer = get_dice()
                    status = 3
        pygame.display.update()
    elif status == 3: #玩家行走
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for i in range(dice_answer):
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            player[cur_player].local = (player[cur_player].local + 1) % 40
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            click_sound.play()
            pygame.display.update()
            time.sleep(0.5)
        if Special(player[cur_player].local): #判斷是否觸發事件
            status = 4
        else:  # 普通地段，判斷要買地還是交租金
            local = player[cur_player].local
            if map_status[local2order(local)].owner == -1:
                chances_sound.play()
                draw_text(screen, (800, 340), '是否買下這塊地?（￥%d）' % map_status[local2order(local)].value1, 30,
                          'msjh.ttc', pygame.Color('grey'))
                status = 5
            elif map_status[local2order(local)].owner == cur_player and map_status[local2order(local)].level == 1:
                chances_sound.play()
                draw_text(screen, (800, 340), '是否要加蓋建築?（￥%d）' % map_status[local2order(local)].value2, 30,
                          'msjh.ttc', pygame.Color('grey'))
                status = 5
            elif map_status[local2order(local)].owner == cur_player and map_status[local2order(local)].level == 2:
                cur_player = (cur_player + 1) % len(player)  # 輪到下一個玩家擲骰子
                while player[cur_player].stop == 1:
                    player[cur_player].stop = 0
                    cur_player = (cur_player + 1) % len(player)
                status = 2
            else:
                if map_status[local2order(local)].level == 1:
                    player[cur_player].money -= map_status[local2order(local)].rent1
                    player[map_status[local2order(local)].owner].money += map_status[local2order(local)].rent1
                    screen.blit(map_screen, (0, 0))
                    screen.blit(picture_dice[dice_answer - 1], (500, 400))
                    draw_mapstatus(screen, player, map_status)
                    draw_player(screen, player, role, stop_picture)
                    draw_text(screen, (800, 340), '付租金（￥%d）' % map_status[local2order(local)].rent1, 30,
                              'msjh.ttc', pygame.Color('grey'))
                    chances_sound.play()
                elif map_status[local2order(local)].level == 2:
                    player[cur_player].money -= map_status[local2order(local)].rent2
                    player[map_status[local2order(local)].owner].money += map_status[local2order(local)].rent2
                    screen.blit(map_screen, (0, 0))
                    screen.blit(picture_dice[dice_answer - 1], (500, 400))
                    draw_mapstatus(screen, player, map_status)
                    draw_player(screen, player, role, stop_picture)
                    draw_text(screen, (800, 340), '付租金（￥%d）' % map_status[local2order(local)].rent2, 30,
                              'msjh.ttc', pygame.Color('grey'))
                    chances_sound.play()
                cur_player = (cur_player + 1) % len(player)  # 輪到下一個玩家擲骰子
                while player[cur_player].stop == 1:
                    player[cur_player].stop = 0
                    cur_player = (cur_player + 1) % len(player)
                if not game_over(player) == 0:
                    if game_over(player) > 0:
                        win_sound.play()
                    else:
                        lose_sound.play()
                    status = 6
                else:
                    status = 2
            pygame.display.update()
    elif status == 4: #觸發事件
        if player[cur_player].local == 5: #台北火車站廣場
            player[cur_player].money -= 400
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (800, 340), '在台北火車站廣場被外勞偷錢，金錢-400', 30, 'msjh.ttc', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 11: #體育館
            player[cur_player].money += 100
            player[cur_player].local = 35
            player[cur_player].stop = 1
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (800, 340), '在清大體育館打球受傷住院', 30, 'msjh.ttc', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 15: #湯瑪士小火車
            if cur_player == 0:
                player[0].stop = 1
                screen.blit(map_screen, (0, 0))
                screen.blit(picture_dice[dice_answer - 1], (500, 400))
                draw_mapstatus(screen, player, map_status)
                draw_player(screen, player, role, stop_picture)
                draw_text(screen, (750, 340), '花花沒趕上火車，暫停一次', 30, 'msjh.ttc', pygame.Color('grey'))
                chances_sound.play()
        elif player[cur_player].local == 19: #成功大學
            player[cur_player].gpa += 0.3
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (750, 340), '參觀成大校園，GPA+0.3', 30, 'msjh.ttc', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 25: #去參加燈會
            player[cur_player].money -= 200
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (800, 340), '逛愛河燈會，金錢-200', 30, 'msjh.ttc', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 31: #東港東隆宮
            player[cur_player].money -= 200
            player[cur_player].gpa += 0.5
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (750, 340), '到東港東隆宮燒香拜拜，金錢-200，GPA+0.5', 30, 'msjh.ttc', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 35: #醫院
            player[cur_player].stop = 1
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (800, 340), '醫護人員看你欠住院，所以住院一天', 30, 'msjh.ttc', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 39: #飯店
            if not cur_player == 2:
                player[cur_player].stop = 1
                player[cur_player].gpa -= 0.8
                screen.blit(map_screen, (0, 0))
                screen.blit(picture_dice[dice_answer - 1], (500, 400))
                draw_mapstatus(screen, player, map_status)
                draw_player(screen, player, role, stop_picture)
                draw_text(screen, (800, 340), '待在飯店耍廢一整天，GPA-0.8', 30, 'msjh.ttc', pygame.Color('grey'))
                chances_sound.play()
        cur_player = (cur_player + 1) % len(player) #輪到下一個玩家擲骰子
        while player[cur_player].stop == 1:
            player[cur_player].stop = 0
            cur_player = (cur_player + 1) % len(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        if not game_over(player) == 0:
            if game_over(player) > 0:
                win_sound.play()
            else:
                lose_sound.play()
            status = 6
        else:
            status = 2
    elif status == 5: #買地建房
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 273:
                    if map_status[local2order(player[cur_player].local)].level == 0:
                        player[cur_player].money -= map_status[local2order(player[cur_player].local)].value1
                        map_status[local2order(player[cur_player].local)].owner = cur_player
                        map_status[local2order(player[cur_player].local)].level = 1
                    elif map_status[local2order(player[cur_player].local)].level == 1:
                        player[cur_player].money -= map_status[local2order(player[cur_player].local)].value2
                        map_status[local2order(player[cur_player].local)].level = 2
                cur_player = (cur_player + 1) % len(player)  # 輪到下一個玩家擲骰子
                while player[cur_player].stop == 1:
                    player[cur_player].stop = 0
                    cur_player = (cur_player + 1) % len(player)
                status = 2
                screen.blit(map_screen, (0, 0))
                screen.blit(picture_dice[dice_answer - 1], (500, 400))
                draw_player(screen, player, role, stop_picture)
                draw_mapstatus(screen, player, map_status)
                up_sound.play()
                if not game_over(player) == 0:
                    if game_over(player) > 0:
                        win_sound.play()
                    else:
                        lose_sound.play()
                    status = 6
        pygame.display.update()
    elif status == 6:  # 遊戲結束
        if game_over(player) > 0:
            draw_text(screen, (540, 340), '遊戲結束，%s勝利' % player[game_over(player)-1].name,
                      50, 'msjh.ttc', pygame.Color('darkgreen'))
            draw_text(screen, (540, 440), '再來一局',
                      50, 'msjh.ttc', pygame.Color('darkgreen'))

        else :
            draw_text(screen, (540, 340), '遊戲結束，%s輸了' % player[- game_over(player) - 1].name,
                      50, 'msjh.ttc', pygame.Color('darkgreen'))
            draw_text(screen, (540, 440), '再來一局',
                      50, 'msjh.ttc', pygame.Color('darkgreen'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = event.pos
                if click_button(mouse_x, mouse_y, 1):
                    player = []
                    role = []
                    map_status = []
                    for i in range(8):
                        map_status.append(Map(i))
                    cur_player = 0
                    click_sound.play()
                    screen.blit(map_screen, (0, 0))
                    num_player_button = Button(screen, '請輸入遊玩人數（2~4）')
                    num_player_button.draw_button()
                    draw_text(screen, (540, 440), '操作指南：按↑擲骰子、購買地產',
                              50, 'msjh.ttc', pygame.Color('gold'))
                    status = 1
        pygame.display.update()

