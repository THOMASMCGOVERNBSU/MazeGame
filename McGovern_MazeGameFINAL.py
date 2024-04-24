#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 01:39:54 2024

@author: thomasmcgovern
"""

import pygame
import sys
import random
import simpleGE

screWidth = 800
screHt = 600
cellSize = 20
ballSize = 10
trophySize = 20
W = (255, 255, 255)  # White
B = (0, 0, 0)        # Black
R = (255, 0, 0)      # Red
Bl = (0, 0, 255)     # Blue
G = (0, 255, 0)      # Green
wallProb = 0.3

class Intro(simpleGE.Scene):
    def __init__(self, score=0):
        super().__init__()
        self.setImage("WelcomeScreen2.jpg")
        self.status = "quit"
        self.score = score
        self.lblInstr = simpleGE.MultiLabel()
        self.lblInstr.textLines = [
            "How to play: Control the Blue Circle and Go to Red Square ",
            " Press R to restart if unable to reach Red Square. Good luck!"]
        self.lblInstr.center = (320, 310)
        self.lblInstr.size = (750, 100)

        self.btnPlay = simpleGE.Button()
        self.btnPlay.center = (150, 400)
        self.btnPlay.text = "Play"

        self.btnQuit = simpleGE.Button()
        self.btnQuit.center = (500, 400)
        self.btnQuit.text = "Quit"

        self.sprites = [            
            self.lblInstr,
            self.btnPlay,
            self.btnQuit
        ]

    def process(self):
        if self.btnPlay.clicked:
            self.status = "play"
            self.stop()
        if self.btnQuit.clicked:
            self.status = "quit"
            self.stop()

class MazeGame(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.screenSize = (screWidth, screHt)
        self.ballRect = pygame.Rect(0, 0, ballSize, ballSize)
        self.trophyRect = pygame.Rect(0, 0, trophySize, trophySize)
        self.isWin = False
        self.generate_maze()
        self.spawnBall()
        self.spawnTrophy()

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption("Maze Game")
        self.clock = pygame.time.Clock()
        self.runGame()

    def runGame(self):
        while True:
            if self.isWin:
                self.displayWinScreen()
                self.handleWinEvents()
            else:
                self.handleEvents()
                self.updateBall()
                self.checkCollision()
                self.drawGame()
                pygame.display.flip()
                self.clock.tick(30)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restartGame()

    def handleWinEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restartGame()

    def updateBall(self):
        targetPos = pygame.mouse.get_pos()
        direction = pygame.Vector2(targetPos) - pygame.Vector2(self.ballRect.center)
        if direction.length() > 0:
            direction.normalize_ip()
            newPos = pygame.Vector2(self.ballRect.center) + direction * 5
            nextRect = self.ballRect.copy()
            nextRect.center = newPos
            if not any([nextRect.colliderect(pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize)) for y, row in enumerate(self.maze) for x, cell in enumerate(row) if cell == 1]):
                self.ballRect.center = newPos

    def drawGame(self):
        self.screen.fill(B)
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(self.screen, W, (x * cellSize, y * cellSize, cellSize, cellSize))
        pygame.draw.circle(self.screen, Bl, self.ballRect.center, ballSize)
        pygame.draw.rect(self.screen, R, self.trophyRect)

    def generate_maze(self):
        self.maze = [[0 for _ in range(screWidth // cellSize)] for _ in range(screHt // cellSize)]
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if random.random() < wallProb and (x, y) != (0, 0) and (x, y) != (screWidth // cellSize - 1, screHt // cellSize - 1):
                    self.maze[y][x] = 1

    def checkCollision(self):
        if self.ballRect.colliderect(self.trophyRect):
            self.isWin = True

    def displayWinScreen(self):
        self.screen.fill(B)
        font = pygame.font.Font(None, 36)
        winText = font.render("You Win!", True, G)
        textRect = winText.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(winText, textRect)
        restartText = font.render("Press 'R' to Restart", True, W)
        restartRect = restartText.get_rect(center=(textRect.centerx, textRect.bottom + 50))
        self.screen.blit(restartText, restartRect)
        pygame.display.flip()

    def restartGame(self):
        self.isWin = False
        self.generate_maze()
        self.spawnBall()
        self.spawnTrophy()

    def spawnBall(self):
        while True:
            x = random.randint(0, screWidth - ballSize)
            y = random.randint(0, screHt - ballSize)
            if not any([pygame.Rect(x, y, ballSize, ballSize).colliderect(
                pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize)) for y, row in
                        enumerate(self.maze) for x, cell in enumerate(row) if cell == 1]):
                self.ballRect.topleft = (x, y)
                break

    def spawnTrophy(self):
        while True:
            x = random.randint(0, screWidth // cellSize - 1)
            y = random.randint(0, screHt // cellSize - 1)
            if self.maze[y][x] == 0:
                self.trophyRect.topleft = (x * cellSize, y * cellSize)
                break

def main():
    intro = Intro()
    intro.start()

    if intro.status == "play":
        game = MazeGame()
        game.start()

if __name__ == "__main__":
    main()
