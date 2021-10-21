from BetterNN import direction_decision as dd
from MainGame import *


if __name__ == '__main__':
    car_list = []

    for n in range(1, 2):
        car_list.append(Car(n))

    print(car_list)
    strecke = pygame.image.load(gA("rennstrecke.png")).convert_alpha()
    all_sprites = pygame.sprite.Group()
    rand = Rand()
    ziel = Ziel()
    all_sprites.add(ziel, rand, *car_list)


    # engine
    loop = True
    car_image = pygame.image.load(gA("car_2.png")).convert_alpha()
    car_image_rot = pygame.transform.rotate(car_image, 90)
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        all_sprites.update()

        for car in car_list:

            car.collision()
            car.touchfl()
            car.timecount()
            car.sensor_front()
            car.sensor_back_R()
            car.sensor_back_L()
            car.sensor_front_R()
            car.sensor_front_L()

        screen.blit(strecke, (0, 0))
        all_sprites.draw(screen)
        dd()
        screen.blit(car_image_rot, (260, -350))

        if car.col_pos is not None:
            pygame.draw.line(screen, pink, (0, 0), car.col_pos, width = 2)

        pygame.draw.line(screen, blue, (car.position), (car.distance_f) , width=2)
        pygame.draw.line(screen, blue, (car.position), (car.distance_f_R), width=2)
        pygame.draw.line(screen, blue, (car.position), (car.distance_f_L), width=2)
        pygame.draw.line(screen, blue, (car.position - 4 * car.vel), (car.distance_R), width=2)
        pygame.draw.line(screen, blue, (car.position - 4 * car.vel), (car.distance_L), width=2)

        # screen.blit(update_fps(), (10, 10))

        screen.blit(car.update_distance_f(), (607, 220))
        screen.blit(car.update_distance_f_R(), (644, 240))
        screen.blit(car.update_distance_f_L(), (570, 240))
        screen.blit(car.update_distance_b_R(), (570, 295))
        screen.blit(car.update_distance_b_L(), (644, 295))


        # screen.blit(car.update_death_time(car.death_time), (10, 50))
        # screen.blit(update_timer(), (10, 30))

        pygame.display.set_caption('Alex Maturarbeit')
        pygame.display.update()

        clock.tick(60)