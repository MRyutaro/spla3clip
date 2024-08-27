import os
import shutil
import pygame


def move_image_to_folder(image_file, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    shutil.move(image_file, target_folder)


def delete_image(image_file):
    if os.path.exists(image_file):
        os.remove(image_file)
        print(f"削除しました: {image_file}")


def load_and_scale_image(image_file, screen_size):
    image = pygame.image.load(image_file)
    return pygame.transform.scale(image, screen_size)


def main():
    image_dir = r'C:\Users\recod\programs\splatoon3_highlight_collector\model_build\data\raw\image\start'
    folders = {
        # pygame.K_a: os.path.join(image_dir, 'death'),   # ←キーからAキーに変更
        # pygame.K_w: os.path.join(image_dir, 'finish'),  # ↑キーからWキーに変更
        # pygame.K_s: os.path.join(image_dir, 'kill'),    # ↓キーからSキーに変更
        # pygame.K_d: os.path.join(image_dir, 'start'),   # →キーからDキーに変更
        # pygame.K_o: os.path.join(image_dir, 'other')
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
                if event.key == pygame.K_LEFT:
                    index = max(0, index - 1)  # ←キーで1つ前の画像に戻る
                elif event.key == pygame.K_SPACE:
                    index += 1
                elif event.key in folders:
                    move_image_to_folder(image_file, folders[event.key])
                    index += 1
                elif event.key == pygame.K_d:
                    delete_image(image_file)
                    index += 1

                if index >= len(image_files):
                    print("全ての画像ファイルを処理しました。")
                    pygame.quit()
                    return


if __name__ == "__main__":
    main()
