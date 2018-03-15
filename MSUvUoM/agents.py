import random

from mesa import Agent

from MSUvUoM.random_walk import RandomWalker


class UoM(RandomWalker):
    '''
    A UoM that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    '''

    energy = None

    def __init__(self, pos, model, moore, energy=None):
        super().__init__(pos, model, moore=moore)
        self.energy = energy

    def step(self):
        '''
        A model step. Move, then eat grass and reproduce.
        '''
        self.random_move()
        living = True

        if self.model.grass:
            # Reduce energy
            self.energy -= 1

            # If there is grass available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell
                           if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.UoM_gain_from_food
                grass_patch.fully_grown = False

            # Death
            if self.energy < 0:
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                living = False

        if living and random.random() < self.model.UoM_reproduce:
            # Create a new UoM:
            if self.model.grass:
                self.energy /= 2
            student = UoM(self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(student, self.pos)
            self.model.schedule.add(student)


class MSU(RandomWalker):
    '''
    A MSU that walks around, reproduces (asexually) and eats UoM.
    '''

    energy = None

    def __init__(self, pos, model, moore, energy=None):
        super().__init__(pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are UoM present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        UoM_student = [obj for obj in this_cell if isinstance(obj, UoM)]
        if len(UoM_student) > 0:
            UoM_to_eat = random.choice(UoM_student)
            self.energy += self.model.MSU_gain_from_food

            # Kill the UoMUoM_student
            self.model.grid._remove_agent(self.pos, UoM_to_eat)
            self.model.schedule.remove(UoM_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if random.random() < self.model.MSU_reproduce:
                # Create a new MSU cub
                self.energy /= 2
                cub = MSU(self.pos, self.model, self.moore, self.energy)
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)


class GrassPatch(Agent):
    '''
    A patch of grass that grows at a fixed rate and it is eaten by UoM
    '''

    def __init__(self, pos, model, fully_grown, countdown):
        '''
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        '''
        super().__init__(pos, model)
        self.fully_grown = fully_grown
        self.countdown = countdown

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1
