import pygame
import random #외계인을 랜덤으로 출력시키기 위해
import time
from datetime import datetime
import sys

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [400, 750]
screen = pygame.display.set_mode(size)

title = "Shooting Game"
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()


class obj :
    def __init__(self):  #init으로 객체생성 후 x,y좌표만들기
        self.x = 0
        self.y = 0
        self.move = 0
        
    def put_img(self, address):
        if address[-3:] == "png": #이미지 이름이 "뒤에서 3번째부터 끝까지"의 문자가 "png"라면
            self.img = pygame.image.load(address).convert_alpha() #jpg가 아닌 png파일 일때만 쓰는 함수.
        else :
            self.img = pygame.image.load(address)
        self.xx, self.yy = self.img.get_size() #불러온 이미지의 사이즈를 x(가로),y(세로)로 받아서 저장
        
    def change_size(self, xx, yy):
        self.img = pygame.transform.scale(self.img,(xx, yy)) #불러온 이미지의 크기지정
        self.xx, self.yy = self.img.get_size() #불러온 이미지의 사이즈를 지정한 크기(x(가로),y(세로))로 받아서 다시 저장

    def show(self): #airplane이미지를 위에서 선언한 airplane.x,airplane.y의 위치에 이미지를 나타냄 (blit함수는 그래픽을 화면에 나타낼 때 사용)
        screen.blit(self.img, (self.x, self.y))

#충돌판정함수 : 사각형 이미지라고 간주했을 때
    # 충돌 판정되는 b.x, b.y의 범위
    #a.x-b.xx <= b.x <= a.x+a.xx
    #a.y-b.yy <= b.y <= a.y+a.yy    
def crash(a,b):
    if (a.x-b.xx <= b.x) and (b.x <= a.x+a.xx):
        if (a.y-b.yy <= b.y) and (b.y <= a.y+a.yy):
            return True
        else:
            return False
    else :
        return False


#1.클래스선언 -> 객체생성
airplane = obj()

#2.이미지 삽입 및 크기저장
# airplane = pygame.image.load("/Users/hanjuhyeon/Workspace/Pygame/Shooting Game/airplane.png").convert_alpha() #.convert_alpha(): jpg가 아닌 png파일 일때만 쓰는 함수.
airplane.put_img("/Users/hanjuhyeon/Workspace/Pygame/1.Shooting game/airplane.png")

#3.지정한 사이즈로 이미지 저장
# airplane = pygame.transform.scale(airplane, (50,80)) #불러온 이미지의 크기지정
# airplane_xx, airplane_yy = airplane.get_size() #이미지의 사이즈를 x(가로),y(세로)로 받아서 저장
airplane.change_size(50, 80)

#4.이미지에 따른 x,y좌표 위치 지정하여 화면에서의 위치 맞추기
# airplane_x = round(size[0]/2 - airplane_xx/2) #이미지의 x좌표 (size[0] = 게임창옵션에서 선언한 size배열의 0번째 = 400)위치 지정 , 가로의 중앙에 배치하기위해 /2를 하고, 오른쪽으로 살짝 쏠려있어서 비행기크기의 절반(airplane_xx/2)만큼만 왼쪽(-)으로 이동하기위해 -뺐음. 숫자 딱 안떨어질수도있으니 round함수 사용
# airplane_y = size[1] -airplane_yy -20 #이미지의 y좌표(위치)지정 (size[1] = 게임창옵션에서 선언한 size배열의 1번째 = 900)위치 지정, 세로에서 조금 위쪽에 배치하기위해 이미지의 세로길이만큼 '- airplane_yy' 뺐음 (여기서 더 빼도 되고 안빼도 되는데 아래쪽 프레임이랑 너무 붙어서 20만큼 더 뺐음.)
airplane.x = round(size[0]/2 - airplane.xx/2)
airplane.y = size[1] -airplane.yy -20
airplane.move = 5


left_go = False
right_go = False
space_go = False

bullet_list = [] # 발사되는 투사체들을 리스트에 담는다. 리스트가 없으면 투사체가 한개밖에 없어서 발사중에 키보드를 누르면 다시 새로 발사되고 이미 발사된 투사체는 끝까지 안감. while문 밖에 있어야 한다.
alien_list = []

black = (0,0,0)
white = (255,255,255)
k = 0

GAMEOVER = 0
kill = 0
loss = 0


# 4-0. 게임 시작 대기 화면
waiting_screen = 0 #나가기버튼이 False일때
while waiting_screen == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                waiting_screen = 1
    screen.fill(black)
    Font = pygame.font.Font("/System/Library/Fonts/Supplemental/Chalkboard.ttc", 15) #폰트저장주소, 폰트크기
    text = Font.render("PRESS SPACE KEY TO START THE GAME",True,(255,255,255)) #표시할 이미지내용(만든 폰트를 렌더링(텍스트를 이미지화)해서 포맷함수로 구현), True는 항상 키면됨(글자가 덜깨지게 매끄럽게 나오게함),RGB값(노란색:255,255,0)
    screen.blit(text,(60, round(size[1]/2-50))) #이미지화 된 text를 40(x좌표),size[1]=750의 절반에서 -50픽셀만큼 위에(y좌표)에 위치시킨다. round함수로 반올림함.
    pygame.display.flip()


# 4. 메인 이벤트

start_time=datetime.now()#while문이 반복될동안(게임시작과동시에시간이흐른다.)
EXIT_button = 0 #나가기버튼이 False일때
while EXIT_button == 0:

    # 4-1. FPS(Frame per second) 설정 :#1초에 몇번 이미지를 업데이트 할것이냐, 숫자가 높을수록 화면이 부드럽게 전환
    clock.tick(60) # 1초에 60번 while문이 돌도록 하겠다.
 
    # 4-2. 각종 입력 감지 (입력장치 :마우스, 키보드 에서 어떤 입력이 발생했는지 감지)
    # pygame.event.get() : 실시간으로 입력장치의 동작을 받는다.
    for event in pygame.event.get():  # 실시간으로 동작(이벤트)를 리스트로 담는다.
        if event.type == pygame.QUIT:
            EXIT_button = 1
        if event.type == pygame.KEYDOWN: #키보드가 눌렸을 때
            if event.key == pygame.K_LEFT: #왼쪽키
                left_go = True
            elif event.key == pygame.K_RIGHT: #오른쪽키
                right_go = True
            elif event.key == pygame.K_SPACE:
                space_go = True
                k = 0 #스페이스를 누를때마다 발사하기위해 k를 0으로 초기화 -> if space_go == True and k % 6 == 0: 를 성립시키기 위함
        elif event.type == pygame.KEYUP: #키보드가 안눌렸을 때
            if event.key == pygame.K_LEFT: #왼쪽키
                left_go = False
            elif event.key == pygame.K_RIGHT: #오른쪽키
                right_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False



    # 4-3. 입력, 시간에 따른 변화
    now_time = datetime.now()#현재시간
    delta_time = round((now_time - start_time).total_seconds()) #delta_time:시간차, totla_seconds()함수:시간을 초로 계산함 ->round()함수로 반올림함

    
    # 키보드_입력에 따른 변화
    if left_go == True:
        airplane.x -= airplane.move
        if airplane.x <=0: #바탕화면의왼쪽테두리(=0)로부터 이미지가 벗어나거나 같아지면
            airplane.x = 0 #이미지 위치를 왼쪽테두리(=0)에 위치시킨다. = 왼쪽테두리를 벗어나지 못함
    elif right_go == True:
        airplane.x += airplane.move
        if airplane.x >=size[0] - airplane.xx:
            airplane.x = size[0] - airplane.xx #size[0] = 게임창옵션에서 선언한 size배열의 0번째 = 400 = 가장오른쪽테두리 에서 이미지크기만큼 빼줘야함(이미지의 가장 왼쪽부분을 중심(0)으로하기 때문) , 빼주지 않으면 비행기 크기만큼 화면에서 오른쪽으로 벗어남
    
    
    
    # 미사일
    # 1. 미사일 생성
    if space_go == True and k % 6 == 0: #투사체가 1초에 60번발사돼서 너무 빠르고 많음- >천천히 나가게 하기 위해 k가 0일때, 6의배수일때 발사(True) -> 발사비율을 6분의1로 줄임  
        bullet = obj() #스페이스가 눌릴때마다 미사일 객체 생성
        bullet.put_img("/Users/hanjuhyeon/Workspace/Pygame/1.Shooting game/bullet.png")
        bullet.change_size(5,15)
        bullet.x = round(airplane.x + airplane.xx/2 - bullet.xx/2) #미사일을 이미지 중앙에 위치시키기 : 둘다 왼쪽을 기준으로 정렬되어있음 -> 이미지의 반 만큼 총알을 오른쪽으로 이동시키고 총알의 반만큼 왼쪽으로 이동시킴.
        bullet.y = airplane.y - bullet.yy - 10 #이미지(airplane.y)위치에서 총알(bullet.yy)의 크기만큼 뺀 거리에 위치 -> 이미지(airplane)와 총알(bullet)이 붙어있음 -> -10만큼 더 빼서 띄워준다.
        bullet.move = 15 #이미지보다 투사체를 빠르게 동작시킴
        bullet_list.append(bullet) #발사되는 투사체들을 리스트에 추가
    k +=1

    # 2. 미사일 이동
    deleate_list = [] #화면을 넘어간 미사일의 리스트
    for i in range(len(bullet_list)): #len(bullet_list): bulliet_list에 담긴 미사일의 개수(len)를 i에 저장
        b=bullet_list[i]
        b.y -= b.move #미사일을 미사일의 위치보다 위로 위치시킨다. *참고 : 위방향:-, 아래방향:+
    # 3. 미사일 제거
        if b.y <= -b.yy: #미사일이 안보이려면 미사일의 위치(b.y)에서 미사일의 크기(b.yy)만큼 위(-)로 가야함
            deleate_list.append(i) #화면을 넘어간 미사일을 deleate_list에 추가 
    for d in deleate_list:
        del bullet_list[d]
    


    # 외계인
    # 1. 외계인생성
    if random.random() > 0.98 : #random.random : 0에서 1사이의 소수점
        alien = obj()
        alien.put_img("/Users/hanjuhyeon/Workspace/Pygame/1.Shooting game/alien.png")
        alien.change_size(40,40)
        alien.x = random.randrange(0,size[0]-alien.xx-round(airplane.xx/2)) #0에서400(size[0]:창의가로크기)안의 랜덤-> 외계인 기준점(왼쪽)이 화면창의 가로길이(400)까지 수렴하기 때문에-> 외계인크기만큼 빼줘야함 + 비행기 총알이 오른쪽 가장자리까지 갈 수 없으므로 비행기크기의 2분의1만큼 더 빼준다.
        alien.y = 10 #제일위(0)에서 10픽셀 아래부터 화면에 출력
        alien.move = 5
        alien_list.append(alien)
        deleate_list = [] #화면을 넘어간 미사일의 리스트
    # 2. 외계인 이동
    deleate_list = []
    for i in range(len(alien_list)): #len(alien_list): alien_list에 담긴 외계인의 개수(len)를 i에 저장
        a=alien_list[i]
        a.y += a.move #외계인을 외계인의 위치보다 아래에 위치시킨다. *참고 : 위방향:-, 아래방향:+
    # 3. 외계인 제거
        if a.y >= size[1]: #외계인의 위치(a.y)가 화면의 세로길이(size[1])와 같아지면
            deleate_list.append(i) #화면을 넘어간 외계을 deleate_list에 추가 
    for d in deleate_list:
        del alien_list[d]
        loss +=1 #화면 밖으로 나가서 없어진 외계인은 loss에 +1

        
    
    #미사일과 외계인이 충돌했을 때 제거
    db_list = []
    da_list = []
    for i in range(len(bullet_list)):
        for j in range(len(alien_list)):
            b = bullet_list[i]
            a = alien_list[j]
            if crash(b,a) == True:
                db_list.append(i)
                da_list.append(j)
    db_list = list(set(db_list)) #set:중복을 제거하는 set자료형(리스트x) -> 중복을 제거하여 리스트에 담는다.
    da_list = list(set(da_list))

    try:
        for db in db_list:
            del bullet_list[db]
        for da in da_list:
            del alien_list[da]
            kill +=1 #미사일과 외계인이 충돌했을 때 kill +1
    except:
        pass


    #외계인과 비행기가 충돌했을 때 game over
    for i in range(len(alien_list)):
        a = alien_list[i]
        if crash(a,airplane) == True:
            EXIT_button = 1
            GAMEOVER = 1 #game over가 실행.




    # 4-4. 그리기
    screen.fill(black)
    airplane.show() #screen.blit(airplane, (airplane_x,airplane_y)) #airplane이미지를 위에서 선언한 airplane_x,airplane_y의 위치에 이미지를 나타냄 (blit함수는 그래픽을 화면에 나타낼 때 사용)
    for b in bullet_list:
        b.show()
    for a in alien_list:
        a.show()

    Font = pygame.font.Font("/System/Library/Fonts/Supplemental/Chalkboard.ttc", 20) #폰트저장주소, 폰트크기
    text_kill = Font.render("killed : {} loss :{}".format(kill, loss), True,(255,255,0)) #표시할 이미지내용(만든 폰트를 렌더링(텍스트를 이미지화)해서 포맷함수로 구현), True는 항상 키면됨(글자가 덜깨지게 매끄럽게 나오게함),RGB값(노란색:255,255,0)
    screen.blit(text_kill,(10, 5)) #이미지화 된 text를 10(x좌표),5(y좌표)에 위치시킨다.


    text_time = Font.render("time : {}".format(delta_time), True,(255,255,255)) #표시할 이미지내용(만든 폰트를 렌더링(텍스트를 이미지화)해서 포맷함수로 구현), True는 항상 키면됨(글자가 덜깨지게 매끄럽게 나오게함),RGB값(흰색:255,255,255)
    screen.blit(text_time,(size[0]-100, 5)) #이미지화 된 text_time을 가로의끝(size[0]:맨오른쪽)에서 -100픽셀 뺀 위치(x좌표),5(y좌표)에 위치시킨다.


    
    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료

while GAMEOVER == 1: #game over(외계인과 비행기가 충돌)일때 -> EXIT_button, GAMEOVER = 1이 됨.
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #EXIT_button이 1일때
            GAMEOVER = 0 #0으로 만들면 while을 빠져나가서 pygame.quit()함수로 연결됨.

    Font = pygame.font.Font("/System/Library/Fonts/Supplemental/Chalkboard.ttc", 40) #폰트저장주소, 폰트크기
    text = Font.render("GAME OVER",True,(255,0,0)) #표시할 이미지내용(만든 폰트를 렌더링(텍스트를 이미지화)해서 포맷함수로 구현), True는 항상 키면됨(글자가 덜깨지게 매끄럽게 나오게함),RGB값(빨간색:255,0,0)
    screen.blit(text,(90, round(size[1]/2-50))) #이미지화 된 text를 40(x좌표),size[1]=750의 절반에서 -50픽셀만큼 위에(y좌표)에 위치시킨다. round함수로 반올림함.
    pygame.display.flip()


pygame.quit()
sys.exit()
