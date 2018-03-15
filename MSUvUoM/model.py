'''
MSU-UoM Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo MSU UoM Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
'''

import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from MSUvUoM.agents import UoM, MSU, GrassPatch
from MSUvUoM.schedule import RandomActivationByBreed


class MSUvUoMPredation(Model):
    '''
    MSUvUoM Predation Model
    '''

    height = 20
    width = 20

    initial_UoM = 100
    initial_MSU = 50

    UoM_reproduce = 0.04
    MSU_reproduce = 0.05

    MSU_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    UoM_gain_from_food = 4

    verbose = False  # Print-monitoring

    description = 'A model for simulating MSU and UoM (predator-prey) ecosystem modelling.'

    def __init__(self, height=20, width=20,
                 initial_UoM=100, initial_MSU=50,
                 UoM_reproduce=0.04, MSU_reproduce=0.05,
                 MSU_gain_from_food=20,
                 grass=False, grass_regrowth_time=30, UoM_gain_from_food=4):
        '''
        Create a new MSU vs UoM model with the given parameters.

        Args:
            initial_UoM: Number of UoM to start with
            initial_MSU: Number of MSU to start with
            UoM_reproduce: Probability of each UoM reproducing each step
            MSU_reproduce: Probability of each MSU reproducing each step
            MSU_gain_from_food: Energy a MSU gains from eating a UoM
            grass: Whether to have the UoM eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            UoM_gain_from_food: Energy UoM gain from grass, if enabled.
        '''

        # Set parameters
        self.height = height
        self.width = width
        self.initial_UoM = initial_UoM
        self.initial_MSU = initial_MSU
        self.UoM_reproduce = UoM_reproduce
        self.MSU_reproduce = MSU_reproduce
        self.MSU_gain_from_food = MSU_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.UoM_gain_from_food = UoM_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {"MSU": lambda m: m.schedule.get_breed_count(MSU),
             "UoM": lambda m: m.schedule.get_breed_count(UoM)})

        # Create UoM:
        for i in range(self.initial_UoM):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = random.randrange(2 * self.UoM_gain_from_food)
            student = UoM((x, y), self, True, energy)
            self.grid.place_agent(student, (x, y))
            self.schedule.add(student)

        # Create MSU
        for i in range(self.initial_MSU):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = random.randrange(2 * self.MSU_gain_from_food)
            student = MSU((x, y), self, True, energy)
            self.grid.place_agent(student, (x, y))
            self.schedule.add(student)

        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = random.randrange(self.grass_regrowth_time)

                patch = GrassPatch((x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(MSU),
                   self.schedule.get_breed_count(UoM)])

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number MSU: ',
                  self.schedule.get_breed_count(MSU))
            print('Initial number UoM: ',
                  self.schedule.get_breed_count(UoM))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number MSU: ',
                  self.schedule.get_breed_count(MSU))
            print('Final number UoM: ',
                  self.schedule.get_breed_count(UoM))
