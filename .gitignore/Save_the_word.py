import pygame,time,easygui
import sys,traceback
from random import *
from pygame.locals import *
from timeit import timeit
#===========================在星空创建黑洞==================================#
'''
import pygame
pygame.init()
screen=pygame.display.set_mode([1100,560])
d=pygame.image.load('Obackground.jpg').convert_alpha()
screen.blit(d,[0,0])
holes_list=[]
x=140
y=340
for num in range(1,6):
    holes_list.append([x,y])
    x+=180
    y+=180*(-1)**(num)
for h in holes_list:
    pygame.draw.circle(screen,[0,0,0],h,46,0)
pygame.display.flip()
pygame.image.save(screen,'background.png')
'''
#===========================主程序开始===================================#
#定义球体属性
class Earth(pygame.sprite.Sprite):
    def __init__(self,blackimage,blueimage,position,speed_a,speed_b,i):
        pygame.sprite.Sprite.__init__(self)
        self.blackimage=pygame.image.load(blackimage).convert_alpha()
        self.image=self.blackimage
        self.rect=self.image.get_rect()
        self.rect.center=position
        self.speed_a=speed_a
        self.speed_b=speed_b
        self.radius=self.rect.width//2
        self.speed=[self.speed_a[0]*self.speed_b[0],self.speed_a[1]*self.speed_b[1]]
        self.i=5*(i+1)
        self.control=False
        self.blueimage=pygame.image.load(blueimage).convert_alpha()
    def turn(self,move_num):
        if move_num-3<=self.i<=move_num:
            playsound(turn_sound)
            position=self.rect.center
            self.image=self.blueimage
            self.rect = self.image.get_rect()
            self.rect.center = position
            self.speed=[0,0]
            self.control=True
    def move(self):
        self.rect=self.rect.move(self.speed)
        if self.rect.centerx<-r:
            self.rect.centerx=width+r
        if self.rect.centerx>width+r:
            self.rect.centerx=-r
        if self.rect.centery<-r:
            self.rect.centery=height+r
        if self.rect.centery>height+r:
            self.rect.centery=-r



#定义玻璃台属性
class Glass(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (180, 150))
        self.rect=self.image.get_rect()
        self.rect.center=[width//2,height-self.rect.height//2-10]



class Mouse(pygame.sprite.Sprite):
    def __init__(self,image,location):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(image).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.center=location

def playsound(sound):
    soundd = pygame.mixer.Sound(sound)
    soundd.set_volume(0.4)
    soundd.play()

#主程序操作运行
def main(a):
    global width, height, r, turn_sound
    # 导入所需材料
    # 图片
    background_image='background.png'
    obackground_image='Obackground.jpg'
    blackball_image='blackball.png'
    blueball_image='blueball.png'
    glass_image='glass.png'
    mouse_image='mouse.png'
    loser_image='loser.png'
    winner_image='winner.png'
    starts_image='start.png'
    quits_image='quit.png'
    story_image='story.png'
    play_image='play.png'
    clocks_image='clock.png'
    # 音乐声响
    background_music='background.ogg'  # 背景音乐
    # background_music='mbackground.mp3'  # 测试失败短时长背景音乐
    loser_sound = 'loser.wav'  # 失败提示
    winner_sound = 'winner.wav'  # 胜利提示
    ok_sound = 'ok.wav'  # 放在正确位置提示
    turn_sound = 'turn.wav'  # 球转变提示
    laugh_sound = 'laugh.wav'  # 笑声
    crash_sound = 'crash.wav'  # 碰撞
    # 初始化定义
    r=48    #球图形半径值

    pygame.init()
    clock=pygame.time.Clock()
    size = width, height = 1100, 560
    pygame.display.set_caption('Save The Earth--My Hero')
    screen=pygame.display.set_mode(size)
    background=pygame.image.load(background_image).convert_alpha()
    obackground=pygame.image.load(obackground_image).convert()
    loser=pygame.image.load(loser_image).convert_alpha()
    winner=pygame.image.load(winner_image).convert_alpha()
    earth =pygame.image.load(blueball_image).convert_alpha()
    starts =pygame.image.load(starts_image).convert_alpha()
    quits =pygame.image.load(quits_image).convert_alpha()
    story =pygame.image.load(story_image).convert_alpha()
    play =pygame.image.load(play_image).convert_alpha()
    clocks =pygame.image.load(clocks_image).convert_alpha()
    group = pygame.sprite.Group()
    #背景音乐声响设置
    pygame.mouse.set_visible(False)
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

    #背景介绍
    screen.blit(obackground,[0,0])
    pygame.display.flip()
    pygame.time.delay(1500)
    screen.blit(background, [0, 0])
    pygame.display.flip()
    pygame.time.delay(1500)
    screen.blit(story,[165,195])
    pygame.display.flip()
    pygame.time.delay(4500)
    screen.blit(background, [0, 0])
    screen.blit(play, [165, 195])
    pygame.display.flip()
    pygame.time.delay(2500)

    # pygame.event.set_grab(True) #隐藏鼠标总不可见
    move_num=0
    lenth=1
    lose=False
    result=False
    holes=[]
    #获取各个黑洞的位置坐标
    holes_list=[]
    x=140
    y=340
    for num in range(1,6):
        holes_list.append([x,y])
        x+=180
        y+=180*(-1)**(num)
    #创建五个小球随机运动
    for i in range(1,6):
        speed_a = [choice([-1, 1]), choice([-1, 1])]
        speed_b = [a*randint(2, 6),a*randint(2, 6)]
        position=[randint(r,width-r),randint(r,height-r)]
        blackball=Earth(blackball_image,blueball_image,position,speed_a,speed_b,i)
        while pygame.sprite.spritecollide(blackball, group, False,pygame.sprite.collide_circle):
            blackball.rect.center=[randint(r,width-r),randint(r,height-r)]
        group.add(blackball)
    #时间到结束

    GAMEOVER=USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)

    MYTIMER=USEREVENT+1
    pygame.time.set_timer(MYTIMER,1000)
    pygame.key.set_repeat(100,60)
    #执行循环运行模式
    tt=1
    running = True
    while running:
        tt+=1
        screen.blit(background, [0, 0])
        play_time = pygame.mixer.music.get_pos()
        if play_time < 207000:
            screen.blit(clocks,[205,10])
            pygame.draw.rect(screen, [255, 0, 255], [250, 10, 12 * lenth, 32], 0)
            if tt % 86 == 0:
                lenth += 1
        for hole in holes:
            screen.blit(earth,[hole[0]-r,hole[1]-r+3.7])
        glass = Glass(glass_image)
        screen.blit(glass.image,glass.rect)
        location = pygame.mouse.get_pos()
        mouse = Mouse(mouse_image, location)
        if location[0] <= glass.rect.left + 10:
            mouse.rect.left = glass.rect.left+ 10
        if location[0] >= glass.rect.right - 10:
            mouse.rect.right = glass.rect.right- 10
        if location[1] <= glass.rect.top + 43:
            mouse.rect.top = glass.rect.top+ 43
        if location[1] >= glass.rect.bottom - 21:
            mouse.rect.bottom = glass.rect.bottom- 21

        screen.blit(mouse.image, mouse.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 按键检测
            #音乐完毕结束检测
            elif event.type==GAMEOVER:
                playsound(loser_sound)
                loser=pygame.image.load(loser_image).convert_alpha()
                pygame.time.delay(3000)
                playsound(laugh_sound)
                lose=True
                break
            elif event.type==pygame.MOUSEMOTION:
                move_num+=1
            elif event.type==MYTIMER:
                for one in group:
                    one.turn(move_num)
                move_num = 0
            if event.type==pygame.KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key==K_UP:
                    for each in group:
                        if each.control:
                            each.speed[1]-=1
                elif event.key==K_DOWN:
                    for each in group:
                        if each.control:
                            each.speed[1]+=1
                elif event.key==K_LEFT:
                    for each in group:
                        if each.control:
                            each.speed[0]-=1
                elif event.key==K_RIGHT:
                    for each in group:
                        if each.control:
                            each.speed[0]+=1
                elif event.key==K_SPACE:
                    for each in group:
                        if each.control:
                            for hole in holes_list:
                                if hole[0]-4<=each.rect.centerx<=hole[0]+4 \
                                        and hole[1] -4 <= each.rect.centery <= hole[1] +4:
                                    holes.append(hole)
                                    holes_list.remove(hole)
                                    group.remove(each)
                                    playsound(ok_sound)
                elif event.key==K_s and KMOD_CTRL:
                    if result:
                        lose = False
                        result=False
                        a*=1.5
                        main(a)
                elif event.key == K_e and KMOD_CTRL:
                    if result:
                        sys.exit()

        for each in group:
            group.remove(each)
            if pygame.sprite.spritecollide(each, group, False,pygame.sprite.collide_circle):
                playsound(crash_sound)
                if not each.control:
                    each.speed[0] = -each.speed[0]
                    each.speed[1] = -each.speed[1]

                if each.control:
                    playsound(turn_sound)
                    positions=each.rect.center
                    side=each.speed_a
                    each.image=each.blackimage
                    each.rect=each.image.get_rect()
                    each.rect.center=positions
                    each.speed_a[0] = -side[0]
                    each.speed_a[1] = -side[1]
                    # each.speed_a = [choice([-1, 1]), choice([-1, 1])]
                    each.speed_b = [a*randint(2, 9), a*randint(2, 9)]
                    each.speed = [each.speed_a[0] * each.speed_b[0],each.speed_a[1] * each.speed_b[1]]
                each.control = False
            group.add(each)
            each.move()
            screen.blit(each.image,each.rect)
        #成功
        if not len(holes_list):
            playsound(winner_sound)
            screen.blit(winner, [0, 0])
            result=True
            screen.blit(starts,[590,280])
            screen.blit(quits,[514,280])
        #失败
        if lose:
            playsound(loser_sound)
            playsound(laugh_sound)
            screen.blit(loser, [0, 0])
            result=True
            screen.blit(starts, [590, 280])
            screen.blit(quits, [514, 280])

        pygame.display.flip()
        clock.tick(30)

if __name__=='__main__':
    try:
        a = 1  # 难度加大速度提高
        main(a)
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()










