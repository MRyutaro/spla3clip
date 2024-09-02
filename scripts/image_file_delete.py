import os
import shutil

import pygame


def move_image_to_folder(image_file, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    shutil.move(image_file, target_folder)


def delete_image(image_file):
    os.remove(image_file)


def load_and_scale_image(image_file, screen_size):
    image = pygame.image.load(image_file)
    return pygame.transform.scale(image, screen_size)


def main():
    image_dir = r'C:\Users\recod\programs\splatoon3_highlight_collector\models_build\data\raw\image\death'

    pygame.init()
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Image Sorting')

    image_files = sorted(
        [f for f in os.listdir(image_dir) if f.endswith('.png')])

    if not image_files:
        print("移動する画像ファイルがありません。")
        return

    index = 0

    while True:
        screen.fill((255, 255, 255))

        image_file = os.path.join(image_dir, image_files[index])
        image = load_and_scale_image(image_file, screen_size)

        screen.blit(image, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:  # Delete image
                    delete_image(image_file)
                    index += 1
                elif event.key == pygame.K_SPACE:  # Move to next image
                    index += 1
                elif event.key == pygame.K_LEFT:  # Move to previous image
                    index -= 1

                if index < 0:
                    index = 0
                if index >= len(image_files):
                    print("全ての画像ファイルを処理しました。")
                    pygame.quit()
                    return


if __name__ == "__main__":
    main()
