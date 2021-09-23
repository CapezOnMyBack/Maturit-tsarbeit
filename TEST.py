import pygame


class Person(pygame.sprite.Sprite):
    def __init__(self, n):
        super(Person, self).__init__()
        self.name = n

    def __repr__(self):
        return f'<Person({self.name})>'

    def __str__(self):
        return self.__repr__()


guest_list = []
for n in range(1, 5):
    guest_list.append(Person(n))

print(guest_list)
