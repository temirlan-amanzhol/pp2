import pygame, sys, random
pygame.init()
W,H = 640,800
S = pygame.display.set_mode((W,H))
C = pygame.time.Clock()
F = pygame.font.SysFont(None, 24)
B = pygame.font.SysFont(None, 40, bold=True)
WHITE,BLACK,GRAY,RED,GREEN,BLUE,YEL = (255,255,255),(0,0,0),(120,120,120),(220,60,60),(60,200,60),(60,120,220),(240,200,0)

class Scene:
    def handle(self,ev):...
    def update(self):...
    def draw(self,s):...

def btn(s, r, txt):
    m = pygame.mouse.get_pos()
    col = WHITE if r.collidepoint(m) else GRAY
    pygame.draw.rect(s, col, r, border_radius=10)
    pygame.draw.rect(s, BLACK, r, 2, border_radius=10)
    s.blit(B.render(txt, True, BLACK), B.render(txt, True, BLACK).get_rect(center=r.center))

class Menu(Scene):
    def __init__(self, switch):
        self.go = switch
        x = W//2-150
        self.b = {"Racer":pygame.Rect(x,270,300,70),
                  "Snake":pygame.Rect(x,360,300,70),
                  "Paint":pygame.Rect(x,450,300,70),
                  "Quit": pygame.Rect(x,540,300,70)}
    def handle(self,ev):
        for e in ev:
            if e.type==pygame.QUIT: pygame.quit();sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                for k,r in self.b.items():
                    if r.collidepoint(e.pos):
                        if k=="Racer": self.go(Racer(self.go))
                        if k=="Snake": self.go(Snake(self.go))
                        if k=="Paint": self.go(Paint(self.go))
                        if k=="Quit":  pygame.quit();sys.exit()
    def draw(self,s):
        s.fill((30,30,34))
        t = B.render("Mini Game Hub", True, WHITE); s.blit(t, t.get_rect(center=(W//2,160)))
        for k,r in self.b.items(): btn(s,r,k)
        tips = ["Racer: arrows","Snake: arrows","Paint: 1-pen 2-rect 3-circle E-eraser C-clear","ESC: back to menu"]
        for i,x in enumerate(tips): s.blit(F.render(x,True,WHITE),(20,640+i*24))

# ---- RACER ----
class Racer(Scene):
    def __init__(self, go):
        self.go=go
        self.road = pygame.Rect(W//2-140, 0, 280, H)
        self.p = pygame.Rect(W//2-20, H-120, 40, 70)
        self.v = 6; self.score=0; self.dead=False
        self.en = [pygame.Rect(random.randrange(self.road.left,self.road.right-40,50),
                               -random.randint(50,500),40,70) for _ in range(4)]
        self.co = [pygame.Rect(random.randint(self.road.left+15,self.road.right-15),-random.randint(60,600),16,16) for _ in range(4)]
    def handle(self,ev):
        for e in ev:
            if e.type==pygame.QUIT: pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: self.go(Menu(self.go))
    def update(self):
        if self.dead: return
        k=pygame.key.get_pressed()
        if k[pygame.K_LEFT]:  self.p.x-=7
        if k[pygame.K_RIGHT]: self.p.x+=7
        self.p.clamp_ip(self.road.inflate(-10,0))
        for r in self.en:
            r.y+=self.v
            if r.y>H: r.y=-random.randint(80,300); r.x=random.randrange(self.road.left,self.road.right-40,50)
            if r.colliderect(self.p): self.dead=True
        for c in self.co:
            c.y+=self.v
            if c.y>H: c.y=-random.randint(120,400); c.x=random.randint(self.road.left+15,self.road.right-15)
            if c.colliderect(self.p): self.score+=1; c.y=-random.randint(120,400)
        self.v = 6 + self.score//8
    def draw(self,s):
        s.fill((20,140,20)); pygame.draw.rect(s,(60,60,60),self.road)
        for y in range(-30,H,70): pygame.draw.rect(s,WHITE,(W//2-5,y,10,40),border_radius=6)
        pygame.draw.rect(s,BLUE,self.p,border_radius=6)
        [pygame.draw.rect(s,RED,r,border_radius=6) for r in self.en]
        [pygame.draw.circle(s,YEL,(c.centerx,c.centery),8) for c in self.co]
        s.blit(B.render(f"Coins: {self.score}",True,WHITE),(12,12))
        if self.dead: s.blit(B.render("CRASH! ESC for menu",True,WHITE), (W//2-160,H//2))

# ---- SNAKE ----
class Snake(Scene):
    def __init__(self, go, g=20):
        self.go=go; self.g=g; self.cols, self.rows = W//g, (H-60)//g; self.reset()
    def reset(self):
        self.body=[(self.cols//2,self.rows//2)]; self.dir=(1,0); self.food=self.spawn(); self.t=0; self.score=0; self.level=1
    def spawn(self):
        while True:
            f=(random.randrange(self.cols), random.randrange(self.rows))
            if f not in self.body: return f
    def handle(self,ev):
        for e in ev:
            if e.type==pygame.QUIT: pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: self.go(Menu(self.go))
                if e.key in (pygame.K_LEFT,pygame.K_a) and self.dir!=(1,0):  self.dir=(-1,0)
                if e.key in (pygame.K_RIGHT,pygame.K_d) and self.dir!=(-1,0): self.dir=(1,0)
                if e.key in (pygame.K_UP,pygame.K_w) and self.dir!=(0,1):    self.dir=(0,-1)
                if e.key in (pygame.K_DOWN,pygame.K_s) and self.dir!=(0,-1): self.dir=(0,1)
    def update(self):
        self.t+=C.get_time(); step=int(1000/(6+self.level*2))
        if self.t>=step:
            self.t=0
            hx,hy=self.body[0][0]+self.dir[0], self.body[0][1]+self.dir[1]
            if not(0<=hx<self.cols and 0<=hy<self.rows) or (hx,hy) in self.body: self.reset();return
            self.body.insert(0,(hx,hy))
            if (hx,hy)==self.food:
                self.score+=1; self.food=self.spawn()
                if self.score%4==0: self.level+=1
            else: self.body.pop()
    def draw(self,s):
        s.fill((18,18,22)); pygame.draw.rect(s,GRAY,(0,0,W,60),2)
        s.blit(B.render(f"Score:{self.score}  Lvl:{self.level}",True,WHITE),(12,12))
        pygame.draw.rect(s,(26,26,30),(0,60,W,H-60))
        fx,fy=self.food; pygame.draw.rect(s,GREEN,(fx*self.g+2,60+fy*self.g+2,self.g-4,self.g-4),border_radius=4)
        for i,(x,y) in enumerate(self.body):
            col=(180,240,255) if i else (0,200,220)
            pygame.draw.rect(s,col,(x*self.g+2,60+y*self.g+2,self.g-4,self.g-4),border_radius=6)

# ---- PAINT ----
class Paint(Scene):
    def __init__(self, go):
        self.go=go; self.canvas=pygame.Surface((W,H-60)); self.canvas.fill(WHITE)
        self.mode="pen"; self.col=BLACK; self.drawing=False; self.start=None; self.th=5
        self.palette=[BLACK,RED,GREEN,BLUE,YEL,(0,200,200),(200,0,200)]
    def handle(self,ev):
        for e in ev:
            if e.type==pygame.QUIT: pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: self.go(Menu(self.go))
                if e.key==pygame.K_1: self.mode="pen"
                if e.key==pygame.K_2: self.mode="rect"
                if e.key==pygame.K_3: self.mode="circle"
                if e.key==pygame.K_e: self.mode="eraser"
                if e.key==pygame.K_c: self.canvas.fill(WHITE)
            if e.type==pygame.MOUSEBUTTONDOWN:
                if e.button==1:
                    if self.pick(e.pos): continue
                    self.drawing=True; self.start=(e.pos[0],e.pos[1]-60)
                if e.button==4: self.th=min(60,self.th+1)
                if e.button==5: self.th=max(1,self.th-1)
            if e.type==pygame.MOUSEBUTTONUP and e.button==1:
                if self.drawing: self.finish(self.start,(e.pos[0],e.pos[1]-60))
                self.drawing=False
            if e.type==pygame.MOUSEMOTION and self.drawing and self.mode in ("pen","eraser"):
                p=(e.pos[0],e.pos[1]-60); pygame.draw.line(self.canvas, WHITE if self.mode=="eraser" else self.col, self.start, p, self.th); self.start=p
    def pick(self,pos):
        x,y=pos
        if y>60: return False
        for i,c in enumerate(self.palette):
            r=pygame.Rect(12+i*36,12,28,28)
            if r.collidepoint(pos): self.col=c; return True
        return False
    def finish(self,a,b):
        if self.mode=="rect":
            r=pygame.Rect(min(a[0],b[0]),min(a[1],b[1]),abs(a[0]-b[0]),abs(a[1]-b[1]))
            pygame.draw.rect(self.canvas,self.col,r,self.th)
        if self.mode=="circle":
            dx,dy=b[0]-a[0],b[1]-a[1]; r=int((dx*dx+dy*dy)**0.5)
            pygame.draw.circle(self.canvas,self.col,a,r,self.th)
    def draw(self,s):
        s.fill((32,32,38)); pygame.draw.rect(s,(26,26,30),(0,0,W,60))
        s.blit(B.render("Paint  1:Pen 2:Rect 3:Circle  E:Eraser  C:Clear  ESC:Menu",True,WHITE),(12,12))
        for i,c in enumerate(self.palette):
            r=pygame.Rect(12+i*36,12,28,28); pygame.draw.rect(s,c,r); pygame.draw.rect(s,WHITE if c==self.col else BLACK,r,2)
        s.blit(self.canvas,(0,60))

def main():
    cur={"scene":None}
    def switch(sc): cur["scene"]=sc
    switch(Menu(switch))
    while True:
        ev=pygame.event.get()
        cur["scene"].handle(ev)
        if hasattr(cur["scene"],"update"): cur["scene"].update()
        cur["scene"].draw(S)
        pygame.display.flip(); C.tick(60)

if __name__=="__main__": main()
