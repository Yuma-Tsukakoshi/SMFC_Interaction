import tkinter as tk
import random
from PIL import Image, ImageTk
import serial
import time

#============
ser = serial.Serial('COM6', 9600)  
time.sleep(2)  # 接続が安定するまで待機

# グローバル変数で制御フラグを保持
move_left = False
move_right = False
attack = False
attack_time = 0
def read_serial():
    global move_left, move_right, attack, attack_time
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        left, right, bom = map(float, line.split(","))  
        move_left = left > 0
        move_right = right > 0
        attack = bom > 0 and time.time() - attack_time > 0.5

    root.after(10, read_serial)  # 10ミリ秒ごとにシリアルデータを読み取る

#============

WINDOW_HEIGHT = 800  # ウィンドウの高さ
WINDOW_WIDTH = 800   # ウィンドウの幅

CANNON_Y = 550       # 自機のy座標

ENEMY_SPACE_X = 100  # 敵の間隔(x座標)
ENEMY_SPACE_Y = 60   # 敵の間隔(y座標)
ENEMY_MOVE_SPACE_X = 20  # 敵の移動間隔(x座標)
ENEMY_MOVE_SPEED = 2000  # 敵の移動スピード(2000 ms)
NUMBER_OF_ENEMY = 8     # 敵の数
ENEMY_SHOOT_INTERVAL = 1000  # 敵がランダムに弾を打ってくる間隔

COLLISION_DETECTION = 300  # 当たり判定

BULLET_HEIGHT = 10  # 弾の縦幅
BULLET_WIDTH = 2    # 弾の横幅
BULLET_SPEED = 10   # 弾のスピード(10 ms)

TEXT_GOOD_SIZE = 10             # goodのサイズ
TEXT_CONGRATULATIONS_SIZE = 50  # congratularionsのサイズ
TEXT_GAMECLEAR_SIZE = 60        # gameclearのサイズ
TEXT_GAMEOVER_SIZE = 90         # gameoverのサイズ


class Cannon:  # 自機

    def __init__(self, x, y=CANNON_Y):
        self.x = x
        self.y = y
        self.draw()

    def draw(self):
        self.id = cv.create_image(self.x, self.y, image=cannon_tkimg, tag="cannon")

    def move_left(self):
        if self.x > 0:
            self.x -= 5  # 移動距離
            cv.coords(self.id, self.x, self.y)

    def move_right(self):
        if self.x < WINDOW_WIDTH:
            self.x += 5  # 移動距離
            cv.coords(self.id, self.x, self.y)

    def attack(self):
        mybullet = MyBullet(self.x, self.y)
        mybullet.draw()
        mybullet.shoot()

    def destroy(self):
        cv.delete(self.id)


class MyBullet:  # 自分の弾

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        self.id = cv.create_rectangle(
            self.x-BULLET_WIDTH, self.y+BULLET_HEIGHT, self.x+BULLET_WIDTH, self.y-BULLET_HEIGHT, fill="blue")

    def shoot(self):
        if self.y >= 0:
            cv.move(self.id, 0, -BULLET_HEIGHT)
            self.y -= BULLET_HEIGHT
            self.defeat()
            root.after(BULLET_SPEED, self.shoot)

    def defeat(self):
        for enemy in enemies:
            if ((self.x-enemy.x)**2+(self.y-enemy.y)**2) < COLLISION_DETECTION:
                enemy.exist = False
                enemy.destroy()
                cv.create_text(enemy.x, enemy.y, text="good!", fill="cyan", font=(
                    "System", TEXT_GOOD_SIZE), tag="good")

    def destroy(self):
        cv.delete(self.id)


class Enemy:  # 敵

    def __init__(self, x, y):
        self.x = x % WINDOW_WIDTH
        self.y = y+x//WINDOW_WIDTH*ENEMY_SPACE_Y
        self.exist = True
        self.draw()
        self.move()

    def draw(self):
        self.id = cv.create_image(self.x, self.y, image=crab_tkimg, tag="enemy")

    def enemy_shoot(self):
        if self.exist:
            enemybullet = EnemyBullet(self.x, self.y)
            enemybullet.draw()
            enemybullet.shoot()

    def move(self):
        if self.exist:
            if self.x > WINDOW_WIDTH:
                self.x -= ENEMY_MOVE_SPACE_X
                self.y += ENEMY_SPACE_Y
            elif self.x < 0:
                self.x += ENEMY_MOVE_SPACE_X
                self.y += ENEMY_SPACE_Y
            if self.y % (ENEMY_SPACE_Y*2) == ENEMY_SPACE_Y:
                self.x += ENEMY_MOVE_SPACE_X
            else:
                self.x -= ENEMY_MOVE_SPACE_X
            cv.coords(self.id, self.x, self.y)
            root.after(ENEMY_MOVE_SPEED, self.move)

    def destroy(self):
        cv.delete(self.id)


class EnemyBullet:  # 敵の弾

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        self.id = cv.create_rectangle(
            self.x-BULLET_WIDTH, self.y+BULLET_HEIGHT, self.x+BULLET_WIDTH, self.y-BULLET_HEIGHT, fill="red")

    def shoot(self):
        if self.y <= WINDOW_HEIGHT:
            cv.move(self.id, 0, BULLET_HEIGHT)
            self.y += BULLET_HEIGHT
            self.collision()
            root.after(BULLET_SPEED, self.shoot)

    def collision(self):
        if ((self.x-cannon.x)**2+(self.y-cannon.y)**2) < COLLISION_DETECTION:
            gameover()

    def destroy(self):
        cv.delete(self.id)


def gameclear():  # ゲームクリア判定
    winflag = 0
    for enemy in enemies:
        if enemy.exist == False:
            winflag += 1
    if winflag == NUMBER_OF_ENEMY:
        cv.delete("good")
        cv.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2-80, text="Congratulations!",
                       fill="lime", font=("System", TEXT_CONGRATULATIONS_SIZE))
        cv.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2+20, text="GAME CLEAR!",
                       fill="lime", font=("System", TEXT_GAMECLEAR_SIZE))
    root.after(1000, gameclear)


def gameover():  # ゲームオーバー判定
    cv.delete("cannon", "good")
    cv.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, text="GAME OVER",
                   fill="red", font=("System", TEXT_GAMEOVER_SIZE))


def enemy_randomshoot():  # ランダムに敵の弾が発射
    enemy = random.choice(enemies)
    enemy.enemy_shoot()
    root.after(ENEMY_SHOOT_INTERVAL, enemy_randomshoot)

def control_cannon():
    if move_left:
        cannon.move_left()
    if move_right:
        cannon.move_right()
    if attack:
        cannon.attack()
    root.after(50, control_cannon)  # 50ミリ秒ごとに自機を制御

if __name__ == "__main__":
    # 初期描画
    root = tk.Tk()
    root.title("invader")
    cv = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
    cv.pack()

    # 画像の読み込み
    cannon_img = Image.open("game/cannon.jpeg")
    cannon_tkimg = ImageTk.PhotoImage(cannon_img)
    crab_img = Image.open("game/crab.jpeg")
    crab_tkimg = ImageTk.PhotoImage(crab_img)

    # メニューバー
    menubar = tk.Menu(root)
    root.configure(menu=menubar)
    menubar.add_command(label="QUIT", underline=0, command=root.quit)

    # インスタンス生成
    cannon = Cannon(WINDOW_WIDTH//2, CANNON_Y)
    enemies = []
    for i in range(NUMBER_OF_ENEMY):
        enemy_i = Enemy(i*ENEMY_SPACE_X+50, ENEMY_SPACE_Y)
        enemies.append(enemy_i)

    read_serial()  # シリアルデータの読み取り開始
    control_cannon()  # 自機の制御開始

    enemy_randomshoot()
    gameclear()

    root.mainloop()

    ser.close()  # シリアルポートを閉じる
