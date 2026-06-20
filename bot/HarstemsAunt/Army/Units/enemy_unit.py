""" Wrapper for enemy Units to be able to calculate """
from math import sin, cos
from collections import deque
from typing import Optional, FrozenSet

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2,Point3

from bot.HarstemsAunt.utils import Utils
from bot.HarstemsAunt.common import UNIT_LABEL_FONT_SIZE

class EnemyUnit:

    def __init__(self, bot:BotAI, tag:int) -> None:
        self.bot = bot
        self.tag = tag
        self.last_positions = deque(maxlen=5)

    def __repr__(self) -> str:
        return f"{self.unit} at position {self.position}"

    def update(self) -> None:
        self.last_positions.append(self.position)
        if self.bot.debug:
            self.render_last_positions()
            self.render_unit_label()

    @property
    def unit(self) -> Optional[Unit]:
        return self.bot.enemy_units.find_by_tag(self.tag)

    @property
    def position(self) -> Optional[Point2]:
        if self.unit:
            return self.unit.position

    @property
    def position3d(self) -> Optional[Point3]:
        if self.unit:
            return self.unit.position3d

    @property
    def direction(self) -> Optional[float]:
        if self.unit and self.last_positions:
            return Utils.angle_between_points(self.position, self.last_positions[0])

    @property
    def ground_range(self) -> float:
        return self.unit.ground_range

    @property
    def units_in_attack_range(self) -> Units:
        return self.bot.units.closer_than(self.ground_range, self.position)

    @property
    def buffs(self) -> Optional[FrozenSet]:
        if self.unit:
            return self.unit.buffs

    @property
    def health(self) -> Optional[float]:
        if self.unit:
            return self.unit.health

    @property
    def unit_label(self) -> str:
        return f"{self.unit.type_id} at {self.position} \nhas {self.buffs} \n{self.health}"

    def render_last_positions(self) -> None:
        for pos in self.last_positions:
            self.bot.debug_tools.debug_pos(pos,radius=.05, color=(255,255,255))

    def render_unit_label(self) -> None:
        if self.unit:
            self.bot.client.debug_text_world(self.unit_label, self.position3d,\
                size=UNIT_LABEL_FONT_SIZE)

    def likely_next_pos(self) -> Point3:

        Px, Py = self.position
        distance = self.unit.real_speed
        theta = self.direction

        TargetX = Px + distance*cos(theta)
        TargetY = Py + distance*sin(theta)
        pos_3D = Utils.create_3D_point(self.bot,Point2((TargetX,TargetY)))
        self.bot.client.debug_sphere_out(pos_3D ,.5, (0,0,255))
        self.bot.client.debug_line_out(self.position3d, pos_3D, (0,0,255))