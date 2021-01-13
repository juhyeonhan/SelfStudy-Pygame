import pygame

pygame.init() #초기화(반드시 필요)

#화면 크기 설정
screen_width = 480 #가로크기
screen_height = 640 #세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Juhyeon Game") #게임이름

#이벤트 루프(항상 실행되고 있어야 창이 꺼지지 않음)
running = True #게임이 진행중인가를 확인
while running :
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가 확인
        if event.type == pygame.QUIT: #창닫기버튼 이벤트가 발생하였는가 확인
            running = False #게임이 진행중이 아님을 확인

# pygame종료
pygame.quit()


