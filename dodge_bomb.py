import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量のタプルをキー、それに対応する角度・反転処理を行った
    こうかとんSurfaceを値とした辞書を作成して返す関数

    戻り値:
        dict[tuple[int, int], pg.Surface]: (移動量x, 移動量y) -> こうかとんSurface の辞書
    """
    # 基本のこうかとん画像（左向き）
    base_img = pg.image.load("fig/3.png")

    # 左右反転した画像（右向き）
    flip_img = pg.transform.flip(base_img, True, False)

    kk_dict = {
        ( 0,  0): pg.transform.rotozoom(base_img, 0, 0.9),       # 静止時（左向き）
        (-5,  0): pg.transform.rotozoom(base_img, 0, 0.9),       # 左
        (-5, -5): pg.transform.rotozoom(base_img, -45, 0.9),    # 左上
        ( 0, -5): pg.transform.rotozoom(flip_img, 90, 0.9),      # 上
        (+5, -5): pg.transform.rotozoom(flip_img, 45, 0.9),     # 右上
        (+5,  0): pg.transform.rotozoom(flip_img, 0, 0.9),      # 右
        (+5, +5): pg.transform.rotozoom(flip_img, -45, 0.9),    # 右下
        ( 0, +5): pg.transform.rotozoom(flip_img, -90, 0.9),    # 下
        (-5, +5): pg.transform.rotozoom(base_img, 45, 0.9),     # 左下
    }
    return kk_dict

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    10段階の大きさに合わせた爆弾Surfaceのリストと、
    10段階の加速度のリストを作成して返す関数

    戻り値:
        tuple[list[pg.Surface], list[int]]: (爆弾Surfaceリスト, 加速度リスト)
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))  # 黒色部分を透過処理
        bb_imgs.append(bb_img)

    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def gameover(screen: pg.Surface) -> None:

    bo_img = pg.Surface((WIDTH, HEIGHT))
    bo_img.set_alpha(200)
    pg.draw.rect(bo_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    screen.blit(bo_img, [0, 0])

    font = pg.font.Font(None, 80)
    txt_img = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt_img.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2
    screen.blit(txt_img, txt_rct)

    kk_crying_img = pg.image.load("fig/8.png")
    
    kk_rct1 = kk_crying_img.get_rect()
    kk_rct1.center = WIDTH // 2 - 200, HEIGHT // 2
    screen.blit(kk_crying_img, kk_rct1)

    kk_rct2 = kk_crying_img.get_rect()
    kk_rct2.center = WIDTH // 2 + 200, HEIGHT // 2
    screen.blit(kk_crying_img, kk_rct2)

    pg.display.update()
    import time
    time.sleep(5)
    

def check_bound(rect: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko,tate=True,True
    if rect.left<0 or WIDTH < rect.right:
        yoko=False
    if rect.top <0 or HEIGHT <rect.bottom:
        tate = False
    return yoko, tate        

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img=pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct=bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx,vy=+5,+5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k,tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0]+=tpl[0]
                sum_mv[1]+=tpl[1]
        kk_img = kk_imgs[tuple(sum_mv)]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        screen.blit(kk_img, kk_rct)

        idx = min(tmr // 500, 9)

        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]

        bb_img = bb_imgs[idx]
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        bb_rct.move_ip(avx,avy)
        yoko,tate=check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
