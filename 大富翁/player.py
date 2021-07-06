class Player:  # 玩家類
    def __init__(self, order):
        self.money = 3000#一開始的金錢
        self.gpa = 3.0#一開始的gpa
        self.local = 0
        self.stop = 0
        if order == 0:
            self.name = '花花'
        elif order == 1:
            self.name = '泡泡'
        elif order == 2:
            self.name = '毛毛'
        elif order == 3:
            self.name = '魔人啾啾'

