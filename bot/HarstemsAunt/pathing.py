""" Class Handling Pathing, needs to be cleaned up."""
#TODO: #52 clean up Pathing Class

from typing import Dict, List, Optional, Union
import numpy as np
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.unit import Unit
from scipy import spatial

import matplotlib.pyplot as plt

# pylint: disable=E0401
# pylint: disable=E0402
from map_analyzer import MapData
from .unitmarker import UnitMarker
from .common import ALL_STRUCTURES, INFLUENCE_COSTS,RANGE_BUFFER


class Pathing:
    """ Pathing class """
    def __init__(self, bot:BotAI, debug:bool, fade_rate:float = 3.0) -> None:
        self.bot: BotAI = bot
        self.debug: bool = debug

        self.map_data: MapData = MapData(bot)
        self.climber_grid: np.ndarray = self.map_data.get_climber_grid()
        self.units_grid: np.ndarray = self.map_data.get_pyastar_grid()
        self.ground_grid: np.ndarray = self.map_data.get_pyastar_grid()
        self.detection_grid: np.ndarray = self.map_data.get_pyastar_grid()
        self.air_grid: np.ndarray = self.map_data.get_clean_air_grid()
        self.influence_fade_rate:float = fade_rate

    def update(self, iteration) -> None:
        """ runs every frame 
            
            I want to add a sigmoid function to the grid to 'squach' the value, 

            also i need to save the grids frame by frame in a fast way to use the resulting data
            to train a model predicting the grid at the next frame, which will make the fade rate obsolete


        """

        self.ground_grid = self.map_data.get_pyastar_grid()
        self.air_grid = self.map_data.get_clean_air_grid()
        self.detection_grid = self.map_data.get_pyastar_grid()
        for unit in self.bot.all_enemy_units:
            if unit.type_id in ALL_STRUCTURES:
                self._add_structure_influence(unit)
            else:
                self._add_unit_influence(unit)

        for marker in self.bot.unitmarkers:
            self._add_unit_influence(marker)

        # self.add_positional_costs()

    def find_closest_safe_spot(
            self, from_pos: Point2, grid: np.ndarray, radius: int = 15
        ) -> Point2:
        """
        @param from_pos:
        @param grid:
        @param radius:
        @return:
        """
        all_safe: np.ndarray = self.map_data.lowest_cost_points_array(
            from_pos, radius, grid
        )
        # type hint wants a numpy array but doesn't actually need one - this is faster
        all_dists = spatial.distance.cdist(all_safe, [from_pos], "sqeuclidean")
        min_index = np.argmin(all_dists)

        # safe because the shape of all_dists (N x 1) means argmin will return an int
        return Point2(all_safe[min_index])

    def find_path_next_point(
            self,
            start: Point2,
            target: Point2,
            grid: np.ndarray,
            sensitivity: int = 2,
            smoothing: bool = False,
        ) -> Point2:
        """
        Most commonly used, we need to calculate the right path for a unit
        But only the first element of the path is required
        @param start:
        @param target:
        @param grid:
        @param sensitivity:
        @param smoothing:
        @return: The next point on the path we should move to
        """
        # Note: On rare occasions a path is not found and returns `None`
        path: Optional[List[Point2]] = self.map_data.pathfind(
            start, target, grid, sensitivity=sensitivity, smoothing=smoothing
        )
        if not path or len(path) == 0:
            return target
        else:
            return path[0]

    @staticmethod
    def is_position_safe(
            grid: np.ndarray,
            position: Point2,
            weight_safety_limit: float = 1.0
        ) -> bool:
        """
        Checks if the current position is dangerous by
        comparing against default_grid_weights
        @param grid: Grid we want to check
        @param position: Position of the unit etc
        @param weight_safety_limit: The threshold at which we declare the position safe
        @return:
        """
        position = position.rounded
        weight: float = grid[position.x, position.y]
        # np.inf check if drone is pathing near a spore crawler
        return weight == np.inf or weight <= weight_safety_limit

    def _add_unit_influence(self, enemy: Union[Unit, UnitMarker]) -> None:

        if enemy.type_id in INFLUENCE_COSTS:
            values: Dict = INFLUENCE_COSTS[enemy.type_id]
            (self.climber_grid,self.ground_grid, self.air_grid) = self._add_cost_to_multiple_grids(
                enemy.position,
                values["GroundCost"],
                values["GroundRange"] + RANGE_BUFFER,
                [self.climber_grid,self.ground_grid,self.air_grid],
            )

        elif enemy.can_attack_ground and not enemy.can_attack_air:
            (self.climber_grid,self.ground_grid) = self._add_cost_to_multiple_grids(
                enemy.position,
                enemy.ground_dps,
                enemy.ground_range + RANGE_BUFFER,
                [self.climber_grid,self.ground_grid],
            )

        elif enemy.can_attack_air and not enemy.can_attack_ground:
            (self.air_grid) = self._add_cost_to_multiple_grids(
                enemy.position,
                enemy.air_dps,
                enemy.air_range + RANGE_BUFFER,
                [self.air_grid]
            )

        elif enemy.can_attack_both:
            (self.climber_grid,self.ground_grid, self.air_grid) = self._add_cost_to_multiple_grids(
                enemy.position,
                enemy.ground_dps,
                enemy.ground_range + RANGE_BUFFER,
                [self.climber_grid,self.ground_grid, self.air_grid]
            )

        if enemy.is_detector:
            (self.detection_grid) = self._add_cost(
                enemy.position,
                12,
                enemy.detect_range + RANGE_BUFFER,
                self.detection_grid
            )

    def _add_structure_influence(self, structure: Unit) -> None:
        """
        Add structure influence to the relevant grid.
        """

        if not structure.is_ready:
            return

        if structure.type_id in INFLUENCE_COSTS:
            values: Dict = INFLUENCE_COSTS[structure.type_id]
            self.ground_grid = self._add_cost(
                structure.position,
                values["GroundCost"],
                values["GroundRange"] + RANGE_BUFFER,
                [self.ground_grid],
            )
            if structure.can_attack_air:
                self.air_grid = self._add_cost(
                    structure.position,
                    values["AirCost"],
                    values["AirRange"] + RANGE_BUFFER,
                    [self.air_grid]
                )

        if structure.is_detector:
            self.detection_grid = self._add_cost(
                structure.position,
                12,
                structure.detect_range + RANGE_BUFFER,
                [self.detection_grid]
            )

    def _add_cost(
            self,
            pos: Point2,
            weight: float,
            unit_range: float,
            grid: np.ndarray,
            initial_default_weights: int = 0,
        ) -> np.ndarray:

        grid = self.map_data.add_cost(
            position=(int(pos.x), int(pos.y)),
            radius=unit_range,
            grid=grid,
            weight=int(weight),
            initial_default_weights=initial_default_weights,
        )
        return grid

    def _add_cost_to_multiple_grids(
            self,
            pos: Point2,
            weight: float,
            unit_range: float,
            grids: List[np.ndarray],
            initial_default_weights: int = 0,
        ) -> List[np.ndarray]:
        """
        Similar to method above, but add cost to multiple grids at once
        This is much faster then doing it one at a time
        """

        grids = self.map_data.add_cost_to_multiple_grids(
            position=(int(pos.x), int(pos.y)),
            radius=unit_range,
            grids=grids,
            weight=int(weight),
            initial_default_weights=initial_default_weights,
        )
        return grids

    #TODO: #36 Add weights to points close to the edges, and points on Ramps
    def _add_positional_costs(self):
        pass

    def save_plot(self, iteration:int):
        unit_postions = [unit.position_tuple for unit in self.bot.units]
        y_positions, x_positions = zip(*unit_postions)
        influence_map = self.ground_grid
        fig, ax = plt.subplots()
        plt.imshow(influence_map, cmap='jet')
        plt.scatter(x_positions, y_positions, color='green', marker='x', s=1)
        plt.grid(True)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Influence Map')
        plt.plot()
        plt.savefig(f"{self.bot.data_path}/influence_{iteration}.png")


