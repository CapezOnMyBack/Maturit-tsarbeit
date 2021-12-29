from MainGame import *
from config import amount as y, architecture, margin
import pickle as p
from pathlib import Path
from GeneticMutator import mutator_w, mutator_b

gen = 1
frames = 0
pop = pygame.mixer.Sound(gA("pop.wav"))
pop.set_volume(0.05)


def amount_cutter():
    global y

    if gen >= 2:
        if y > 100:
            y *= (0.75 ** (gen / 2))
            y = int(y)

            if y < 100:
                y = 100


def margin_changer():
    global margin

    if margin > 1:
        if gen >= 1.5:
            margin *= 0.9

            if margin < 1.5:
                margin = 1.5


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
    global w, b

    all_sprites = pygame.sprite.Group()

    def instance_amount():

        x = f'Cars alive:{str(int(len(all_sprites) - 2))}'
        instance_text = font_2.render(x, bool(1), pygame.Color("black"))
        return instance_text

    if __name__ == '__main__':

        strecke = pygame.image.load(gA("rennstrecke_weg_grass.png")).convert_alpha()
        rand = Border()
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
                        pop.play()
                        continue

            elif len(car_list) == 1:

                for i, car in enumerate(car_list):

                    if not car.alive:
                        car.kill()
                        pop.play()
                        continue

            all_sprites.update(frames)

            screen.blit(strecke, (0, 0))
            all_sprites.draw(screen)

            screen.blit(instance_amount(), (15, 15))
            screen.blit(generation(), (15, 35))
            screen.blit(margins(), (15, 55))
            screen.blit(car_list[0].update_alive_timer(), (15, 75))

            pygame.display.update()

            clock.tick(60)
            frames += 1

        if margin != 0:
            gen += 1
        with open('cached_network.pickle', "wb") as f:
            p.dump((car.network.weights, car.network.biases, gen), f)


while True:
    amount_cutter()
    margin_changer()
    gameloop()
