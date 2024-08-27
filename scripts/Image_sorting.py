import os
import shutil
import pygame


def move_image_to_folder(image_file, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    shutil.move(image_file, target_folder)


def load_and_scale_image(image_file, screen_size):
    image = pygame.image.load(image_file)
    return pygame.transform.scale(image, screen_size)


def main():
    image_dir = r'C:\Users\recod\programs\splatoon3_highlight_collector\model_build\data\raw\image'
    folders = {
        pygame.K_LEFT: os.path.join(image_dir, 'death'),
        pygame.K_UP: os.path.join(image_dir, 'finish'),
        pygame.K_DOWN: os.path.join(image_dir, 'kill'),
        pygame.K_RIGHT: os.path.join(image_dir, 'start'),
        pygame.K_o: os.path.join(image_dir, 'other')
    }

    # Pygameの初期化
    pygame.init()
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Image Sorting')

    # 画像ファイルリストを取得
    image_files = sorted(
        [f for f in os.listdir(image_dir) if f.endswith('.png')])

    if not image_files:
        print("移動する画像ファイルがありません。")
        return

    index = 0
    while True:
        screen.fill((255, 255, 255))

        # 画像ファイルの読み込みとスケーリング
        image_file = os.path.join(image_dir, image_files[index])
        image = load_and_scale_image(image_file, screen_size)

        # 画像を画面に表示
        screen.blit(image, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key in folders:
                    move_image_to_folder(image_file, folders[event.key])
                    index += 1
                    if index >= len(image_files):
                        print("全ての画像ファイルを移動しました。")
                        pygame.quit()
                        return


if __name__ == "__main__":
    main()
