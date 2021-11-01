from MainGame import *
from config import amount as y, architecture, margin
import pickle as p
from pathlib import Path
from GeneticMutator import mutator_w, mutator_b

gen = 1
frames = 0


def amount_cutter():
    global y

    if gen >= 2:
        if y > 5:
            y *= (0.5 ** (gen / 2))
            y = int(y)

            if y < 5:
                y = 5


def margin_changer():
    global margin

    if margin > 1:
        if gen >= 2:
            margin *= 0.5
            margin = int(margin)

            if margin < 1:
                margin = 1


def generation():
    y = f'Generation:{str(int(gen))}'
    gen_text = font_2.render(y, bool(1), pygame.Color("black"))
    return gen_text


def margins():
    u = f'Current Margin:{str(int(margin))}'
    gen_text = font_2.render(u, bool(1), pygame.Color("black"))
    return gen_text


def gameloop():

    global gen
    global frames

    all_sprites = pygame.sprite.Group()

    def instance_amount():

        x = f'Cars alive:{str(int(len(all_sprites) - 2))}'
        instance_text = font_2.render(x, bool(1), pygame.Color("black"))
        return instance_text

    if __name__ == '__main__':

        strecke = pygame.image.load(gA("rennstrecke_weg.png")).convert_alpha()
        rand = Rand()
        ziel = Ziel()

        car_list = []

        if Path('cached_network.pickle').exists():
            with open('cached_network.pickle', "rb") as f:
                w, b, gen = p.load(f)

                car = Car(1, rand, ziel, Network.new(w, b, architecture))
                car_list.append(car)

                for n in range(2, y + 1):
                    car = Car(n, rand, ziel, Network.new(mutator_w(w, margin), mutator_b(b, margin), architecture))
                    car_list.append(car)

        else:

            for n in range(1, y + 1):
                car = Car(n, rand, ziel, Network(architecture=architecture))
                car_list.append(car)

        all_sprites.add(ziel, rand, *car_list)

        # engine

        loop = True

        car_image = pygame.image.load(gA("car_2.png")).convert_alpha()
        car_image_rot = pygame.transform.rotate(car_image, 90)

        pygame.display.set_caption('Alex Maturarbeit')

        while loop:

            key = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                elif key[K_p]:
                    for i, car in enumerate(car_list):
                        car.kill()
                    for u in range(1, len(car_list)):
                        car_list.pop()

            if len(all_sprites) == 2:
                clock.tick(60)

                break

            if len(car_list) > 1:

                for i, car in enumerate(car_list):

                    if not car.alive:
                        car.kill()
                        car_list.pop(i)
                        continue

            elif len(car_list) == 1:

                for i, car in enumerate(car_list):

                    if not car.alive:
                        car.kill()
                        continue

            all_sprites.update(frames)

            screen.blit(strecke, (0, 0))
            all_sprites.draw(screen)

            # screen.blit(car_image_rot, (260, -350))

            # pygame.draw.line(screen, blue, (car.position), (car.sensor_f_hit), width=2)
            # pygame.draw.line(screen, blue, (car.position), (car.sensor_f_R_hit), width=2)
            # pygame.draw.line(screen, blue, (car.position), (car.sensor_f_L_hit), width=2)
            # pygame.draw.line(screen, blue, (car.position), (car.sensor_s_R_hit), width=2)
            # pygame.draw.line(screen, blue, (car.position), (car.sensor_s_L_hit), width=2)
            # pygame.draw.line(screen, blue, (car.position - 4 * car.vel), (car.sensor_R_hit), width=2)
            # pygame.draw.line(screen, blue, (car.position - 4 * car.vel), (car.sensor_L_hit), width=2)

            screen.blit(instance_amount(), (15, 15))
            screen.blit(generation(), (15, 35))
            screen.blit(margins(), (15, 55))
            screen.blit(car_list[0].update_alive_timer(), (15, 75))

            # screen.blit(car.update_distance_f(), (607, 220))
            # screen.blit(car.update_distance_f_R(), (644, 240))
            # screen.blit(car.update_distance_f_L(), (570, 240))
            # screen.blit(car.update_distance_b_R(), (570, 295))
            # screen.blit(car.update_distance_b_L(), (644, 295))

            # screen.blit(car.update_death_time(car.death_time), (10, 50))
            # screen.blit(update_timer(), (10, 30))

            pygame.display.update()

            clock.tick(60)
            frames += 1

        gen += 1
        with open('cached_network.pickle', "wb") as f:
            p.dump((car.network.weights, car.network.biases, gen), f)


while True:
    amount_cutter()
    margin_changer()
    gameloop()
