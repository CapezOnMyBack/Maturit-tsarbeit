from MainGame import *
from config import amount as y
if __name__ == '__main__':

    strecke = pygame.image.load(gA("rennstrecke_weg.png")).convert_alpha()
    all_sprites = pygame.sprite.Group()
    rand = Rand()
    ziel = Ziel()

    car_list = []

    for n in range(1, y + 1):
        car = Car(n, rand, ziel)
        car_list.append(car)

    all_sprites.add(ziel, rand, *car_list)

    # engine

    loop = True

    car_image = pygame.image.load(gA("car_2.png")).convert_alpha()
    car_image_rot = pygame.transform.rotate(car_image, 90)

    pygame.display.set_caption('Alex Maturarbeit')

    while loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        if len(all_sprites) == 2:
            clock.tick(60)
            break

        if len(car_list) > 2:

            for i, car in enumerate(car_list):

                if not car.alive:
                    car.kill()
                    car_list.pop(i)
                    continue
        elif len(car_list) <= 2:

            for i, car in enumerate(car_list):

                if not car.alive:
                    car.kill()
                    continue


        all_sprites.update()

        screen.blit(strecke, (0, 0))
        all_sprites.draw(screen)

        screen.blit(car_image_rot, (260, -350))

        pygame.draw.line(screen, blue, (car.position), (car.sensor_f_hit), width=2)
        pygame.draw.line(screen, blue, (car.position), (car.sensor_f_R_hit), width=2)
        pygame.draw.line(screen, blue, (car.position), (car.sensor_f_L_hit), width=2)
        pygame.draw.line(screen, blue, (car.position - 4 * car.vel), (car.sensor_R_hit), width=2)
        pygame.draw.line(screen, blue, (car.position - 4 * car.vel), (car.sensor_L_hit), width=2)

        screen.blit(update_fps(), (10, 10))

        screen.blit(car.update_distance_f(), (607, 220))
        screen.blit(car.update_distance_f_R(), (644, 240))
        screen.blit(car.update_distance_f_L(), (570, 240))
        screen.blit(car.update_distance_b_R(), (570, 295))
        screen.blit(car.update_distance_b_L(), (644, 295))


        # screen.blit(car.update_death_time(car.death_time), (10, 50))
        # screen.blit(update_timer(), (10, 30))

        pygame.display.update()

        clock.tick(60)

    print(car_list)