import os,random
from package.images import *
from package.voices import *

def main():
    while True:
        AUDIOS["start"].play()
        IMAGES["bgpic"]=IMAGES[random.choice(["day","night"])]
        color=random.choice(["red","yellow","blue"])
        IMAGES["birds"]=[IMAGES[color+"-up"],IMAGES[color+"-mid"],IMAGES[color+"-down"]]
        pipe=IMAGES[random.choice(["green-pipe","red-pipe"])]
        IMAGES["pipes"]=[pipe,pygame.transform.flip(pipe,False,True)]
        
        menu_window()
        result=game_window()
        end_window(result)

def menu_window():
    #实现滚动地板画面
    floor_gap=IMAGES["floor"].get_width()-W
    floor_x=0
    
    #实现小鸟上下漂浮画面
    bird_x=W*0.2;bird_y=(H-IMAGES["birds"][0].get_height())/2
    bird_y_vel=1 #小鸟y方向移动速度,1像素/帧
    bird_y_range=[bird_y-8,bird_y+8] #小鸟y方向移动范围

    #实现小鸟扇翅膀画面
    idx=0
    frames=[0,0,0,0,0,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1]

    #实现背景板画面
    guide_x=(W-IMAGES["guide"].get_width())/2;guide_y=(FLOOR_Y-IMAGES["guide"].get_height())/2

    while True:
        for event in pygame.event.get():
            #鼠标左键单击×,退出游戏
            if event.type == pygame.QUIT:
                quit()
            #按空格键,开始游戏
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
                return

        #实现滚动地板画面
        floor_x-=4
        if floor_x <= -floor_gap:
            floor_x=0
        
        #实现小鸟上下漂浮画面
        bird_y+=bird_y_vel
        if bird_y<bird_y_range[0] or bird_y>bird_y_range[1]:
            bird_y_vel*=-1

        #实现小鸟扇翅膀画面
        idx += 1
        idx %= len(frames)

        #实现开始菜单画面
        SCREEN.blit(IMAGES["bgpic"],(0,0))
        SCREEN.blit(IMAGES["floor"],(floor_x,FLOOR_Y))
        SCREEN.blit(IMAGES["guide"],(guide_x,guide_y))
        SCREEN.blit(IMAGES["birds"][frames[idx]],(bird_x,bird_y))

        pygame.display.update()
        CLOCK.tick(FPS)

def game_window():
    score=0

    AUDIOS["flap"].play()
    #实现滚动地板画面
    floor_gap=IMAGES["floor"].get_width()-W
    floor_x=0

    bird=Bird(W*0.2,H*0.4)

    n_pairs=4
    distance=150
    pipe_gap=100
    pipe_group=pygame.sprite.Group()
    for i in range(n_pairs):
        pipe_y=random.randint(int(H*0.3),int(H*0.7))
        pipe_up=Pipe(W+i*distance,pipe_y,True)
        pipe_down=Pipe(W+i*distance,pipe_y-pipe_gap,False)
        pipe_group.add(pipe_up)
        pipe_group.add(pipe_down)

    while True:
        flap=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.type==pygame.KEYDOWN:
                    flap=True
                    AUDIOS["flap"].play()

        #实现滚动地板画面
        floor_x-=4
        if floor_x <= -floor_gap:
            floor_x=0

        #小鸟操作
        bird.update(flap)

        first_pipe_up=pipe_group.sprites()[0]
        first_pipe_down=pipe_group.sprites()[1]
        if first_pipe_up.rect.right<0:
            pipe_y=random.randint(int(H*0.3),int(H*0.7))
            new_pipe_up=Pipe(first_pipe_up.rect.x+n_pairs*distance,pipe_y,True)
            new_pipe_down=Pipe(first_pipe_down.rect.x+n_pairs*distance,pipe_y-pipe_gap,False)
            pipe_group.add(new_pipe_up)
            pipe_group.add(new_pipe_down)
            first_pipe_up.kill()
            first_pipe_down.kill()

        pipe_group.update()

        #死亡判定
        if bird.rect.y>FLOOR_Y or bird.rect.y<0:
            bird.dying=True
            AUDIOS["hit"].play()
            AUDIOS["die"].play()
            result={"bird":bird,"pipe_group":pipe_group,"score":score} #重要数据结果
            return result

        #得分判定
        if bird.rect.left+first_pipe_up.x_vel<first_pipe_up.rect.centerx<bird.rect.left:
            AUDIOS["score"].play()
            score+=1

        #碰撞检测(不用封装了)
        for pipe in pipe_group.sprites():
            right_to_left=max(bird.rect.right,pipe.rect.right)-min(bird.rect.left,pipe.rect.left)
            bottom_to_top=max(bird.rect.bottom,pipe.rect.bottom)-min(bird.rect.top,pipe.rect.top)
            if right_to_left<bird.rect.width+pipe.rect.width and bottom_to_top<bird.rect.height+pipe.rect.height:
                bird.dying=True
                AUDIOS["hit"].play()
                AUDIOS["die"].play()
                result={"bird":bird,"pipe_group":pipe_group,"score":score}
                return result

        #实现游戏画面
        SCREEN.blit(IMAGES["bgpic"],(0,0))
        pipe_group.draw(SCREEN)
        show_score(score)
        SCREEN.blit(IMAGES["floor"], (floor_x,FLOOR_Y))
        SCREEN.blit(bird.image,bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)

def end_window(result):
    gameover_x=(W-IMAGES["gameover"].get_width())/2
    gameover_y=(FLOOR_Y-IMAGES["gameover"].get_height())/2

    #最后重要的数据结果
    bird=result["bird"]
    pipe_group=result["pipe_group"]

    # #死亡暂停
    # if bird.dying:
    #     bird.go_die()
    # else:
    #     for event in pygame.event.get():
    #         if event.type==pygame.QUIT:
    #             quit()
    #         if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
    #             return
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
                return

        bird.go_die()

        SCREEN.blit(IMAGES["day"],(0,0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES["floor"],(0,FLOOR_Y))
        SCREEN.blit(IMAGES["gameover"],(gameover_x,gameover_y))
        a=result["score"];show_score(a)
        SCREEN.blit(bird.image,bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)

def show_score(score):
    score_str=str(score)
    n=len(score_str)
    w=IMAGES["0"].get_width()*1.1
    x=(W-n*w)/2
    y=H*0.1
    for number in score_str:
        SCREEN.blit(IMAGES[number],(x,y))
        x+=w

class Bird(object):
    def __init__(self,x,y): #小鸟位置初始化方法
        self.frames=[0,0,0,0,0,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1] #帧序号列表
        self.idx=0 #帧序号
        self.images=IMAGES["birds"]
        self.image=self.images[self.frames[self.idx]] #帧图像
        self.rect=self.image.get_rect()
        self.rect.x=x #帧x方向位置
        self.rect.y=y #帧y方向位置
        self.y_vel=-10 #小鸟的y方向速度
        self.max_y_vel=10 #小鸟在y方向上的最大速度
        self.gravity=1 #小鸟的重力加速度
        self.rotate=45 #小鸟的初始角度
        self.max_rotate=-20 #小鸟的最大角度
        self.rotate_vel=-3 #小鸟的旋转角度
        self.y_vel_after_flap=-10 #拍动翅膀后的y方向速度
        self.rotate_after_flap=45 #拍动翅膀后的头部角度
        self.dying=False

    def update(self,flap=False): #帧更新方法

        if flap: #操作小鸟
            self.y_vel=self.y_vel_after_flap
            self.rotate=self.rotate_after_flap

        self.y_vel=min(self.y_vel + self.gravity,self.max_y_vel) #更新y方向速度
        self.rect.y+=self.y_vel #更新y方向坐标
        self.rotate=max(self.rotate+self.rotate_vel,self.max_rotate) #更新旋转角度
        self.idx+=1
        self.idx%=len(self.frames)
        self.image=self.images[self.frames[self.idx]]
        self.image=pygame.transform.rotate(self.image,self.rotate) #更新角度(避免丢失清晰度)
    
    def go_die(self):
        if self.rect.y<FLOOR_Y:
            self.rect.y+=self.max_y_vel
            self.rotate=-90
            self.image=self.images[self.frames[self.idx]]
            self.image=pygame.transform.rotate(self.image,self.rotate)
        else:
            self.dying=False

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,upwards=True):
        pygame.sprite.Sprite.__init__(self)
        if upwards:
            self.image=IMAGES["pipes"][0]
            self.rect=self.image.get_rect()
            self.rect.x=x
            self.rect.top=y
        else:
            self.image=IMAGES["pipes"][1]
            self.rect=self.image.get_rect()
            self.rect.x=x
            self.rect.bottom=y
        self.x_vel=-4 #水管x方向速度
    
    def update(self):
        self.rect.x+=self.x_vel

if __name__=="__main__":
    main()