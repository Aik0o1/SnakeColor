import pygame
import random
from pygame.locals import *

def main():
    teal = (0, 128, 128)
    purple = (128, 0, 128)
    green = (0, 128, 0)
    olive = (128, 128, 0)
    white = (255, 255, 255)  
    red = (255, 0, 0)  
    blue = (0, 0, 255)  
    black = (0, 0, 0)   
    yellow = (255, 255, 0)
    magenta = (255, 0, 255)
    gray = (128, 128, 128)
    dark_red = (128, 0, 0)
    dark_green = (0, 128, 0)
    orange = (255, 165, 0)
    brown = (165, 42, 42)

    up = 37
    left = 38
    right = 39
    down = 40

    color_list = [
        teal, purple, green, olive, red, blue, black , yellow, magenta, gray,
        dark_red, dark_green, orange, brown]

    def posRandom():
        x = random.randint(20, 500)
        y = random.randint(20, 500)
        return (x // 20 * 20, y // 20 * 20)

    def colisaoComida(posCabecaCobra, posComida):
        return posCabecaCobra == posComida
    
    def colisaoConsigoMesmo():
        try:
            for i in range (len(snake)-1):
                if (snake[0]['pos'][0] == snake[i+1]['pos'][0]) and (snake[0]['pos'][1] == snake[i+1]['pos'][1]):
                    showTryAgainScreen()
                i += 1
        except:
            print('Game OVER')
    
    #cria a comida
    def comidasColoridas():
        comidaPos = posRandom()
        comida = pygame.Surface((20, 20)) #tamanho
        cor = color_list[random.randint(0,13)]
        comida.fill(cor)
        return {'comida': comida, 'pos': comidaPos, 'cor': cor}
    
    #cria os blocos que serão parte do corpo da cobra
    def pedacoCorpoSnake(pos, cor):
        snakeCorpo = pygame.Surface((20,20))
        snakeCorpo.fill(cor)
        return {'pos': pos, 'snakeCorpo':snakeCorpo, 'cor': cor }

    #painel de pontuaçao
    def showScore():
        fonte = pygame.font.SysFont('comicsansms', 24)
        surface = fonte.render(f'Pontuação: {score}', True, black)
        retangulo = surface.get_rect()
        retangulo.midtop=(70,20)
        screen.blit(surface, retangulo)
    
    # botao try again
    def showTryAgainScreen():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    retanguloBotao = pygame.Rect(200,200,200,50)
                    if retanguloBotao.collidepoint(mousePos):
                        main()

            retanguloBotao = pygame.Rect(180,200,250,50)
            pygame.draw.rect(screen, black, retanguloBotao)

            fonte = pygame.font.Font(None, 36)
            texto = fonte.render(f'Tentar Novamente', True, (255,255,255))
            retanguloTexto = texto.get_rect(center=(300,220))
            screen.blit(texto, retanguloTexto)

            pygame.display.flip()

    # array que guardará as informações de todos blocos de comida
    comidas = [comidasColoridas() for _ in range(5)]

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('SnakeColor')

    # array snake que guardará informações do corpo da cobra(blocos)
    snake = [pedacoCorpoSnake((500,200),green), pedacoCorpoSnake((520,200),red), pedacoCorpoSnake((540,200),blue)]
    direcaoCobra = left # direçao inicial
    velocidade = 10 #velocidade inicial

    score = 0
    
    while True:
        pygame.time.Clock().tick(velocidade)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    if direcaoCobra != down:
                        direcaoCobra = up
                elif event.key == K_DOWN:
                    if direcaoCobra != up:
                        direcaoCobra = down
                elif event.key == K_LEFT:
                    if direcaoCobra != right:
                        direcaoCobra = left
                elif event.key == K_RIGHT:
                    if direcaoCobra != left:
                        direcaoCobra = right

        # verificando colisão com todas as comidas
        for comida in comidas:
            if colisaoComida(snake[0]['pos'], comida['pos']):
                comida['pos'] = posRandom()
                cor = color_list[random.randint(0,6)]
                comida['comida'].fill(cor)

                # implementaçao da fila
                if comida['cor'] == snake[0]['cor']:
                    snake.pop(0) # remove o elemento do inicio da fila ao colidar com bloco de cor igual
                    score -= 1
                else:
                    snake.append(pedacoCorpoSnake((0, 0), comida['cor'])) # adiciona o elemento no final da fila
                    score += 1
                comida['cor'] = cor
                velocidade += 0.5

        # movimento corpo snake
        for i in range(len(snake) - 1, 0, -1):
            snake[i]['pos'] = snake[i - 1]['pos']

        if direcaoCobra == up:
            snake[0]['pos'] = (snake[0]['pos'][0], snake[0]['pos'][1] - 20)
        elif direcaoCobra == down:
            snake[0]['pos'] = (snake[0]['pos'][0], snake[0]['pos'][1] + 20)
        elif direcaoCobra == right:
            snake[0]['pos'] = (snake[0]['pos'][0] + 20, snake[0]['pos'][1])
        elif direcaoCobra == left:
            snake[0]['pos'] = (snake[0]['pos'][0] - 20, snake[0]['pos'][1])

        screen.fill(white)
        showScore()
        colisaoConsigoMesmo()

        for comida in comidas:
            screen.blit(comida['comida'], comida['pos']) 

        for item in snake:
            x, y = item['pos']
            screen.blit(item['snakeCorpo'], (x, y))

        # colisao com a parede
        if snake[0]['pos'][0] == 600 or snake[0]['pos'][0] == -20 or snake[0]['pos'][1] == 600 or snake[0]['pos'][1] == -20:
            showTryAgainScreen()

        pygame.display.update()

main()