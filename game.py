import pygame
from sys import exit
from random import randint, choice

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        __Ship = pygame.image.load('assets/Ships/Ship.png')
        __ShipMoveL = pygame.image.load('assets/Ships/ShipMoveLeft.png')
        __ShipMoveR = pygame.image.load('assets/Ships/ShipMoveRight.png')
        __Ship = pygame.transform.scale(__Ship, (32, 32))
        __ShipMoveL = pygame.transform.scale(__ShipMoveL, (32, 32))
        __ShipMoveR = pygame.transform.scale(__ShipMoveR, (32, 32))
        self.__shootSound = pygame.mixer.Sound('assets/Sound/Shoot.mp3')
        self.__shootSound.set_volume(0.01)
        self.__coolDown = 0
        self.hp = 60
        self.__imgIndex = 0
        self.__ship = [__Ship, __ShipMoveL, __ShipMoveR]
        self.image = self.__ship[self.__imgIndex]
        self.rect = self.image.get_rect(midbottom = (275, 630))

    def movement(self):
        key = pygame.key.get_pressed()
  
        if key[pygame.K_a]:
            if self.rect.x >= 0:
                self.rect.x -= 4  
                self.__imgIndex = 1   
            self.image = self.__ship[self.__imgIndex]   
        
        elif key[pygame.K_d]:
            if self.rect.x <= 515:
                self.rect.x += 4
                self.__imgIndex = 2
            self.image = self.__ship[self.__imgIndex]  

        else:  
            self.__imgIndex = 0
            self.image = self.__ship[self.__imgIndex]

    def shoot(self):
        key = pygame.key.get_pressed()
        self.__coolDown -= 1

        if self.__coolDown < 0:
            if key[pygame.K_SPACE]:
                playerProjectileGroup.add(PlayerProjectiles(self.rect.center[0]))
                self.__shootSound.play()
                self.__coolDown = 20

    def collision(self):
        if self.hp > 0:
            if pygame.sprite.spritecollide(playerShip.sprite, StrongEnemyProjectileGroup, True):
                self.hp -= 15
            if pygame.sprite.spritecollide(playerShip.sprite, NormalEnemyProjectileGroup, True):
                self.hp -= 6
            if pygame.sprite.spritecollide(playerShip.sprite, WeakEnemyProjectileGroup, True):
                self.hp -= 3
        else:
            self.reset()
        
    def reset(self):
        self.kill()
        normalEnemyGroup.empty()
        weakEnemyGroup.empty()
        strongEnemyGroup.empty()
        playerProjectileGroup.empty()
        NormalEnemyProjectileGroup.empty()
        WeakEnemyProjectileGroup.empty()
        StrongEnemyProjectileGroup.empty()
        music.stop()
        gameState.gameActive = False
        
    def hpBar(self):
        pygame.draw.line(display, 'Red', (470, 30), (470 + self.hp, 30), 13)

    def update(self):
        self.movement()
        self.shoot()
        self.collision()
        self.hpBar()

class PlayerProjectiles(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        __playerLaserProjectile = pygame.image.load('assets/Projectiles/PlayerLaser.png')
        __playerLaserProjectile = pygame.transform.scale(__playerLaserProjectile, (28, 28))   
        self.damage = 20
        self.image = __playerLaserProjectile
        self.rect = self.image.get_rect(midbottom = (x, 605))
        

    def projectileMove(self):
        self.rect.y -= 10
        if self.rect.y < -5:
            self.kill()

    def update(self):
        self.projectileMove()

class enemyProjectilesSuper():
    def projectileMove(self):
        self.rect.y += self.speed
        if self.rect.y > 750: self.kill()

class StrongEnemyProjectile(pygame.sprite.Sprite, enemyProjectilesSuper):
    def __init__(self, x):
        super().__init__()
        __enemyLaser = pygame.image.load('assets/Projectiles/EnemyStrongLaser.png')
        __enemyLaser = pygame.transform.scale(__enemyLaser, (30, 30))
        self.__enemyLaser = pygame.transform.rotate(__enemyLaser, (90))
        self.speed = 8
        self.image = self.__enemyLaser
        self.rect = self.image.get_rect(center = (x, 65))

    def update(self):
        super(StrongEnemyProjectile, self).projectileMove()

class NormalEnemyProjectile(pygame.sprite.Sprite, enemyProjectilesSuper):
    def __init__(self, x):
        super().__init__()
        __enemyLaser = pygame.image.load('assets/Projectiles/EnemyNormalLaser.png')
        __enemyLaser = pygame.transform.scale(__enemyLaser, (12, 12))
        self.__EnemyLaser = pygame.transform.rotate(__enemyLaser, 180)
        self.speed = 10
        self.image = self.__EnemyLaser
        self.rect = self.image.get_rect(midbottom = (x, 120))

    def update(self):
        super(NormalEnemyProjectile, self).projectileMove()

class WeakEnemyProjectiles(pygame.sprite.Sprite, enemyProjectilesSuper):
    def __init__(self, x):
        super().__init__()
        __enemyLaser = pygame.image.load('assets/Projectiles/EnemyWeakLaser.png')
        self.__EnemyLaser = pygame.transform.scale(__enemyLaser, (10, 12))
        self.speed = 10
        self.image = self.__EnemyLaser
        self.rect = self.image.get_rect(midbottom = (x, 140))

    def update(self):
        super(WeakEnemyProjectiles, self).projectileMove()


class enemySuper():
    def shoot(self):
        self.coolDown -= 1
        if self.coolDown <= 0:        
            self.projectileGroup.add(self.projectile(self.rect.x + self.location))
            self.coolDown = self.coolDownTime
        
    def move(self):
        if self.rect.y <= self.yLocation:
            self.rect.y += self.speed + 1
        if self.movDir == 0:
            self.rect.x += self.speed
            if self.rect.x >= self.turnLoc[1]: self.movDir = 1
        elif self.movDir == 1:
            self.rect.x -= self.speed
            if self.rect.x <= self.turnLoc[0]: self.movDir = 0

    def collision(self):
        collisions = pygame.sprite.groupcollide(playerProjectileGroup, self.group, True, False)
        for projectil, hitEnemy in collisions.items():
            hitEnemy[0].hp -= projectil.damage

    def destroyAnimation(self):
        self.animation += 1
        if self.animation <= 8:
            self.image = self.explosion1
        elif self.animation < 5:
            self.image = self.explosion2
        elif self.animation < 10:
            self.image = self.explosion3
        elif self.animation >= 13:              
            gameState.score += self.killPoint
            self.kill()

class EnemyStrong(pygame.sprite.Sprite, enemySuper):
    def __init__(self, x):
        super().__init__()
        __enemyStrongShip = pygame.image.load('assets/Enemies/EnemyStrong.png')
        __enemyStrongShip = pygame.transform.scale(__enemyStrongShip, (62, 62))
        explosion1 = pygame.image.load('assets/Misc/Explosion1.png')
        self.explosion1 = pygame.transform.scale(explosion1, (62, 62))
        explosion2 = pygame.image.load('assets/Misc/Explosion2.png')
        self.explosion2 = pygame.transform.scale(explosion2, (62, 62))
        explosion3 = pygame.image.load('assets/Misc/Explosion3.png')
        self.explosion3 = pygame.transform.scale(explosion3, (62, 62))

        self.projectile = StrongEnemyProjectile
        self.projectileGroup = StrongEnemyProjectileGroup
        self.group = strongEnemyGroup

        self.hp = 200
        self.location = 30
        self.coolDownTime = 200
        self.coolDown = 100
        self.animation = 0
        self.yLocation = 30
        self.speed = 1
        self.turnLoc = [0, 495]
        self.killPoint = 10

        self.movDir = choice([0, 1])

        self.image = __enemyStrongShip
        self.rect = self.image.get_rect(center = (x, -30))

         
    def update(self):
        super(EnemyStrong, self).shoot()
        super(EnemyStrong, self).move()
        super(EnemyStrong, self).collision()
        if self.hp <= 0:
            super(EnemyStrong, self).destroyAnimation() 

class EnemyNormal(pygame.sprite.Sprite, enemySuper):
    def __init__(self, x):
        super().__init__()
        __enemyNormalShip = pygame.image.load('assets/Enemies/EnemyNormal.png')
        __enemyNormalShip = pygame.transform.scale(__enemyNormalShip, (30, 30))
        __enemyShip = pygame.transform.rotate(__enemyNormalShip, 180)
        explosion1 = pygame.image.load('assets/Misc/Explosion1.png')
        self.explosion1 = pygame.transform.scale(explosion1, (32, 32))
        explosion2 = pygame.image.load('assets/Misc/Explosion2.png')
        self.explosion2 = pygame.transform.scale(explosion2, (32, 32))
        explosion3 = pygame.image.load('assets/Misc/Explosion3.png')
        self.explosion3 = pygame.transform.scale(explosion3, (32, 32))
        self.hp = 50
        self.movDir = choice([0, 1])
        self.animation = 0
        self.projectileGroup = NormalEnemyProjectileGroup
        self.projectile = NormalEnemyProjectile
        self.group = normalEnemyGroup
        self.coolDown = 100
        self.coolDownTime = 80
        self.location = 20
        self.yLocation = 100
        self.speed = 1
        self.turnLoc = [0, 515]
        self.killPoint = 3
        self.image = __enemyShip
        self.rect = self.image.get_rect(midbottom = (x, -10))
       
    def update(self):
        super(EnemyNormal, self).shoot()
        super(EnemyNormal, self).move()
        super(EnemyNormal, self).collision()     
        if self.hp <= 0:
            super(EnemyNormal, self).destroyAnimation()   

class EnemyWeak(pygame.sprite.Sprite, enemySuper):
    def __init__(self, x):
        super().__init__()
        __enemyWeakShip = pygame.image.load('assets/Enemies/EnemyWeak.png')
        __enemyWeakShip = pygame.transform.scale(__enemyWeakShip, (22, 22))
        __enemyShip = pygame.transform.rotate(__enemyWeakShip, 180)
        explosion1 = pygame.image.load('assets/Misc/Explosion1.png')
        self.explosion1 = pygame.transform.scale(explosion1, (28, 28))
        explosion2 = pygame.image.load('assets/Misc/Explosion2.png')
        self.explosion2 = pygame.transform.scale(explosion2, (28, 28))
        explosion3 = pygame.image.load('assets/Misc/Explosion3.png')
        self.explosion3 = pygame.transform.scale(explosion3, (28, 28))
        self.hp = 20
        self.movDir = choice([0, 1])
        self.projectileGroup = WeakEnemyProjectileGroup
        self.projectile = WeakEnemyProjectiles
        self.group = weakEnemyGroup
        self.location = 10
        self.animation = 0
        self.coolDown = 80
        self.coolDownTime = 60
        self.yLocation = 150
        self.speed = 2
        self.turnLoc = [0, 515]
        self.killPoint = 1
        self.image = __enemyShip
        self.rect = self.image.get_rect(midbottom = (x, -10))
  
    def update(self):
        super(EnemyWeak, self).shoot()
        super(EnemyWeak, self).move()
        super(EnemyWeak, self).collision()    
        if self.hp <= 0:
            super(EnemyWeak, self).destroyAnimation()  

class Stars(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        __star1 = pygame.image.load('assets/Background/star1.png')
        __star2 = pygame.image.load('assets/Background/star2.png')
        __stars = [__star1, __star2]
        self.image = __stars[choice([0, 1])]
        self.rect = self.image.get_rect(topleft = (randint(20, 530), randint(20, 680)))

starsGroup = pygame.sprite.Group()

def backGround():
    x = 0
    while x < 160:
        starsGroup.add(Stars())
        x += 1

class GameState():
    def __init__(self, score, gameState):
        self.gameActive = gameState
        self.score = score
        self.difficulty = 10

        self.normalEnemyTimer = pygame.USEREVENT + 1
        self.weakEnemyTimer = pygame.USEREVENT + 2
        self.strongEnemyTimer = pygame.USEREVENT + 3

    def enemySpawnSpeed(self):
        pygame.time.set_timer(self.weakEnemyTimer, 700 * int(self.difficulty))
        pygame.time.set_timer(self.normalEnemyTimer, 2000 * int(self.difficulty))
        pygame.time.set_timer(self.strongEnemyTimer, 12000 * int(self.difficulty))

pygame.init()
display = pygame.display.set_mode((550, 700))
pygame.display.set_caption('SPACE WAR')
music = pygame.mixer.Sound('assets/sound/Music.mp3')
music.set_volume(0.2)
clock = pygame.time.Clock()
backGround()

gameState = GameState(0, False)

textFont = pygame.font.Font('assets/font/Pixeltype.ttf', 50)

hpBar = pygame.image.load('assets/misc/HPBAR.png')
hpHeart = pygame.image.load('assets/misc/HpHeart.png')
hpHeart = pygame.transform.scale(hpHeart, (32, 32))
hpHeartRect = hpHeart.get_rect(center = (430, 30))
hpBar = pygame.transform.scale(hpBar, (82, 18))
hpBarRect = hpBar.get_rect(center = (500, 30))

hpBarFilling = pygame.draw.line(display, 'Red', (430, 30), (510, 30), 32)

gameTitle = textFont.render('SPACEWAR', False, (64, 64, 64))
gameTitleRect = gameTitle.get_rect(center = (275, 280))

gamePressPlay = textFont.render("PRESS 'SPACEBAR' TO PLAY", False, (64, 64, 64))
gamePressPlayRect = gamePressPlay.get_rect(center = (275, 360))

gameControlHelpMove = textFont.render("A, D to move", False, (64, 64, 64))
gameControlMoveRect = gameControlHelpMove.get_rect(center = (275, 500))

gameControlHelpShoot = textFont.render("SPACEBAR to shoot", False, (64, 64, 64))
gameControlShootRect = gameControlHelpShoot.get_rect(center = (275, 560))

playerShip = pygame.sprite.GroupSingle()
playerProjectileGroup = pygame.sprite.Group()

NormalEnemyProjectileGroup = pygame.sprite.Group()
WeakEnemyProjectileGroup = pygame.sprite.Group()
StrongEnemyProjectileGroup = pygame.sprite.Group()

normalEnemyGroup = pygame.sprite.Group()
strongEnemyGroup = pygame.sprite.Group()
weakEnemyGroup = pygame.sprite.Group()

difficultyTimer = pygame.USEREVENT + 4
pygame.time.set_timer(difficultyTimer, 20000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not gameState.gameActive:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                playerShip.add(Ship())
                music.play(loops=-1)
                gameState = GameState(0, True)
                gameState.enemySpawnSpeed()

        if gameState.gameActive:
            if event.type == gameState.normalEnemyTimer:
                normalEnemyGroup.add(EnemyNormal(randint(20, 510)))
            if event.type == gameState.weakEnemyTimer:
                weakEnemyGroup.add(EnemyWeak(randint(20, 510)))
            if event.type == gameState.strongEnemyTimer:
                strongEnemyGroup.add(EnemyStrong(randint(20, 510)))
            if event.type == difficultyTimer and gameState.difficulty > 2:
                gameState.difficulty -= 1
                gameState.enemySpawnSpeed()

    if gameState.gameActive:

        display.fill((0, 0, 0))
        starsGroup.draw(display) 
        gameScore = textFont.render(f'{gameState.score}', False, (164, 164, 164))
        gameScoreRect = gameScore.get_rect(center = (30, 25))
        display.blit(gameScore, gameScoreRect)
        display.blit(hpHeart, hpHeartRect)
        display.blit(hpBar, hpBarRect)

        playerShip.update()
        playerShip.draw(display)
        
        playerProjectileGroup.update()
        playerProjectileGroup.draw(display)
        
        StrongEnemyProjectileGroup.update()
        StrongEnemyProjectileGroup.draw(display)

        NormalEnemyProjectileGroup.update()
        NormalEnemyProjectileGroup.draw(display)

        WeakEnemyProjectileGroup.update()
        WeakEnemyProjectileGroup.draw(display)

        strongEnemyGroup.update()
        strongEnemyGroup.draw(display)

        normalEnemyGroup.update()
        normalEnemyGroup.draw(display)

        weakEnemyGroup.update()
        weakEnemyGroup.draw(display)

    else:       
        display.fill((94, 129, 162))

        if gameState.score > 0:
            gameScore = textFont.render(f'SCORE: {gameState.score}', False, (64, 64, 64))
            gameScoreRect = gameScore.get_rect(center = (275, 220))
            display.blit(gameScore, gameScoreRect)
            
        display.blit(gameTitle, gameTitleRect)
        display.blit(gamePressPlay, gamePressPlayRect)
        display.blit(gameControlHelpMove, gameControlMoveRect)
        display.blit(gameControlHelpShoot, gameControlShootRect)

    clock.tick(60)
    pygame.display.update()