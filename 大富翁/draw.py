import pygame.font

class Button:  # 按鈕區
    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width = 200#寬度
        self.height = 50#高度
        self.button_color = (255, 0, 0)#按鈕顏色設為紅色
        self.text_color = (255, 255, 255)#把文字顏色設為白色
        self.font = pygame.font.Font('msjh.ttc', 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

def draw_text(screen, center, text, text_size, font_type, bg_color):  # 製作文本
    text_color = (255, 0, 0)
    bg_color.a = 0
    font = pygame.font.Font(font_type, text_size)
    textSurface = font.render(text, True, text_color, bg_color)
    textRect = textSurface.get_rect()
    textRect.center = center
    screen.blit(textSurface, textRect)

# 地圖所有座標
role_score = [(150, 100), (350, 100), (150, 350), (350, 350)]
money_center = [(180, 180), (380, 180), (180, 430), (380, 430)]
gpa_center = [(180, 220), (380, 220), (180, 470), (380, 470)]
map_coordi = [(100, 8), (190, 8), (264, 8), (348, 8), (422, 8),
              (510, 8),
              (589, 8), (673, 8), (757, 8), (841, 8), (915, 8),
              (1015, 8),
              (1015, 93), (1015, 160), (1015, 235),
              (1015, 310),
              (1015, 400), (1015, 465), (1015, 540),
              (1015, 611),
              (915, 611), (831, 611), (757, 611), (673, 611), (599, 611),
              (510, 611),
              (428, 611), (344, 611), (270, 611), (186, 611), (112, 611),
              (8, 611),
              (8, 532), (8,468), (8,394),
              (8, 310),
              (8, 223), (8, 159), (8, 85),
              (8, 8)]

def draw_player(screen, player, role, stop_picture):  # 玩家圖樣以及分數
    for i in range(len(player)):
        screen.blit(role[i], map_coordi[player[i].local])
        if player[i].stop == 1:
            screen.blit(stop_picture, map_coordi[player[i].local])
        screen.blit(role[i], role_score[i])
        draw_text(screen, money_center[i], 'money:%d' % player[i].money, 20, 'msjh.ttc', pygame.Color('gold'))
        draw_text(screen, gpa_center[i], 'gpa:%.1f' % player[i].gpa, 20, 'msjh.ttc', pygame.Color('gold'))

def draw_mapstatus(screen, player, map_status):  # 顯示出某塊地被誰購買了
    for i in range(len(map_status)):
        if map_status[i].level == 0:
            draw_text(screen, map_status[i].text_local,
                      '￥%d' % map_status[i].value1, 30, 'msjh.ttc', pygame.Color('violet'))
        elif map_status[i].level == 1:
            draw_text(screen, map_status[i].text_local,
                      '%s*' % player[map_status[i].owner].name, 30, 'msjh.ttc', pygame.Color('violet'))
        elif map_status[i].level == 2:
            draw_text(screen, map_status[i].text_local,
                      '%s**' % player[map_status[i].owner].name, 30, 'msjh.ttc', pygame.Color('violet'))