from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from MSUvUoM.agents import MSU, UoM, GrassPatch
from MSUvUoM.model import MSUvUoMPredation


def MSU_UoM_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is UoM:
        portrayal["Shape"] = "MSUvUoM/resources/UoM.png"
        # https://icons8.com/web-app/433/UoM
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is MSU:
        portrayal["Shape"] = "MSUvUoM/resources/MSU.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "white"

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = 'green'

        else:
            portrayal["Color"] = 'chocolate'
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(MSU_UoM_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "MSU", "Color": "#AA0000"},
                             {"Label": "UoM", "Color": "#666666"}])

model_params = {"grass": UserSettableParameter('checkbox', 'Grass Enabled', True),
                "grass_regrowth_time": UserSettableParameter('slider', 'Grass Regrowth Time', 20, 1, 50),
                "initial_UoM": UserSettableParameter('slider', 'Initial UoM Population', 100, 10, 300),
                "UoM_reproduce": UserSettableParameter('slider', 'UoM Reproduction Rate', 0.04, 0.01, 1.0,
                                                         0.01),
                "initial_MSU": UserSettableParameter('slider', 'Initial MSU Population', 50, 10, 300),
                "MSU_reproduce": UserSettableParameter('slider', 'MSU Reproduction Rate', 0.05, 0.01, 1.0,
                                                        0.01,
                                                        description="The rate at which MSU agents reproduce."),
                "MSU_gain_from_food": UserSettableParameter('slider', 'MSU Gain From Food Rate', 20, 1, 50),
                "UoM_gain_from_food": UserSettableParameter('slider', 'UoM Gain From Food', 4, 1, 10)}

server = ModularServer(MSUvUoMPredation, [canvas_element, chart_element], "MSU vs UoM Predation", model_params)
server.port = 8521
