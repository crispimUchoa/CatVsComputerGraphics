from tile import Tile

class Level_Controller:
    def __init__(self, surface, level=None):
        self.timer = 0
        self.total_time = 60*60*5 #5 horas do jogo -> 5 minutos da vida real
        w = 16
        sw = surface.get_width()
        sh = surface.get_height()
        self.WALLS = [
            #PAREDES DA BORDA
            Tile((0, 0), w, sh),        #ESQUERDA
            Tile((sw - w, 0), w, sh),   #DIREITA
            Tile((w, 0), (sw-2*w)//2 - 16, w),    #CIMA
            Tile((w + (sw - 2*w)//2 + 16, 0), (sw-2*w)//2 - 16, w),    #CIMA
            Tile((w, sh-w), sw-w*2, w), #BAIXO



            ]


    def iswall(self, x, y):
        for wall in self.WALLS:
            if wall.position[0] <= x <= wall.position[0] + wall.width and wall.position[1] <= y <= wall.position[1] + wall.height:
                return True
        return False  
    
    def increse_timer(self):
        self.timer+=1
    
    def get_timer_in_hm(self):
        timer = self.timer// 60
        h = (timer // 60) + 5
        m = timer % 60
        return f'{h:02d}:{m:02d}'