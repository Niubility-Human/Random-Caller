#这个程序是用于随机点名
#coding:utf-8
from queue import Queue as queue
import os
import pygame
from pygame.locals import *
from random import randint as getRandom
from easygui import msgbox
from threading import Thread
QueOfUsed = None
maxQueueSize = 5
codeOfRand = "点我确定名字"
codeNotRand = "点我再抽一个"
canvas = pygame.display.set_mode((400, 425))
BACK_GROUND_COLOUR = (50,200,255)
BLACK = (0,0,0)
MAX_FPS = 114514
FONTSIZE_OF_NAME = 120
FONT_NAME = "font1.ttc"
listOfNames = []
buttons = []
isGettingRand = True#是否在抽人
clock = pygame.time.Clock()
pushing_mouse = {1:False ,2:False, 3:False}#按钮是否按动中
tipsUsing = False
textOftips = '''
这是一个NiubilityHuman制作的随机点名器

这个点名器从与它同级目录的\'names.txt\'中读取点名名单，每行一个名字

每次想要点名，则点击\"{}\"按钮即可

如果随后你想要再点一次名，则点击\"{}\"按钮即可

注意：如果一个人被点名后，他（她）在接下来的{}次点名中都不会被点到（有特例）

但是如果一个人在\'names.txt\'中的名字后面有!符号，则此人会被重点关心

被重点关心的人的名字显示为红色，被点到的概率大幅度提高，并且可能被重复多次点到
'''
def tipsPutting():
    global tipsUsing
    tipsUsing = True
    global codeOfRand,codeNotRand,maxQueueSize
    msgbox(textOftips.format(codeOfRand,codeNotRand,maxQueueSize)
           ,"说明 Written by 梁意森",
           "我已明白")
    tipsUsing = False
def fillText(text, position, size, color = BLACK,view=canvas):
    global FONT_NAME
    font_to_paint = pygame.font.Font(FONT_NAME,size)
    # font_to_paint = pygame.font.get_default_font()
    text_to_paint = font_to_paint.render(text,True,color)
    view.blit(text_to_paint,position)
class FlyingObject():#万物父类
    def __init__(self,x = 0,y = 0,width = 0,height = 0,code = "",color = BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.code = code
        self.color = color
    def paint(self,view = canvas):
        toput_x = self.x + (self.width - len(self.code) * self.height) / 2
        # 显示字体在中央，大小与高有关
        fillText(self.code, (toput_x, self.y), self.height,self.color)

mouseHitter = FlyingObject()#老鼠检测器
class Button(FlyingObject):
    def __init__(self,code,x,y,width,height,color):
        super().__init__(x,y,width,height,code,color)#父类初始化
    def paint(self,view = canvas):
        # pygame.draw.rect(view, self.color, (self.x, self.y, self.width, self.height))#打底
        super().paint()
    def canUse(self):
        if (pushing_mouse[1][0] != -1 and checkHit(self, mouseHitter)):  # 如果点击是有效值
            return True
        return False
def checkHit(a, c):#碰撞检测函数
    return a.x > c.x - a.width and a.x < c.x + c.width and a.y < c.y + c.height and a.y + a.height > c.y
# 初始化
def init():
    global QueOfUsed,canvas
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 60)
    # canvas = pygame.display.set_mode((300, 500))
    pygame.display.set_caption("随机点名器 梁意森制作")
    QueOfUsed = queue()#初始化队列
    #读入名称
    with open("names.txt","r",encoding="utf-8") as file:
        strGetter = file.read().split('\n')#由换行符分割
        for tmpstr in strGetter:
            listOfNames.append(tmpstr)
            if (tmpstr[-1] == '!'):
                for i in range(10):
                    listOfNames.append(tmpstr)

#事件控制函数
def handleEvent():
    global canvas,pushing_mouse,mouseHitter
    pushing_mouse = {1:(-1,-1) ,2:(-1,-1) ,3:(-1,-1)}
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            os._exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            pushing_mouse[event.button] = (event.pos[0],event.pos[1])
        elif event.type == MOUSEMOTION:
            mouseHitter.x = event.pos[0]
            mouseHitter.y = event.pos[1]

codeToPut = FlyingObject(y = 20,height = FONTSIZE_OF_NAME)
# def press_button():
selectionButton = Button(codeOfRand,50,300,300,50,(255,0,0))
tipsButton = Button("tips",0,380,100,25,(0,255,0))
selectedNum = 0
#主函数
def __main__():
    globals()
    isGettingRand = True
    while True:
        canvas.fill(BACK_GROUND_COLOUR)#打印背景
        handleEvent()
        fillText("fps:"+str(int(clock.get_fps())),(0,0),20)
        if isGettingRand:
            selectedNum = getRandom(0,len(listOfNames)-1)
            # codeToPut.code = getChoice(listOfNames)
            codeToPut.code = listOfNames[selectedNum]
            if codeToPut.code[-1] == '!':
                codeToPut.code = codeToPut.code[0:len(codeToPut.code)-1]
                codeToPut.color = (255,0,0)
            else:
                codeToPut.color = (0, 0, 0)
            codeToPut.width = FONTSIZE_OF_NAME * len(codeToPut.code)
            codeToPut.x = 200 - codeToPut.width/2
            if selectionButton.canUse():
                isGettingRand = False
                if codeToPut.color[0] != 255:
                    QueOfUsed.put(listOfNames[selectedNum])
                    listOfNames[selectedNum] = listOfNames[-1]
                    listOfNames.pop()#弹出队尾
                    if QueOfUsed.qsize() >= maxQueueSize:
                        tmp = QueOfUsed.get()
                        listOfNames.append(tmp)
                selectionButton.color = (255,255,255)
                selectionButton.code = codeNotRand
        else:
            if selectionButton.canUse():
                isGettingRand = True
                selectionButton.color = (255, 0,0)
                selectionButton.code = codeOfRand
        if tipsButton.canUse() and (not tipsUsing):
            threadOfMsg = Thread(target=tipsPutting)
            threadOfMsg.start()
        codeToPut.paint()
        selectionButton.paint()
        tipsButton.paint()
        clock.tick(MAX_FPS)
        pygame.display.update()

if __name__ == "__main__":
    init()
    __main__()
