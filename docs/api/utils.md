# Utility Functions

The `Utils` class provides a comprehensive collection of utility functions used throughout the HarstemsAunt bot. These functions handle mathematical calculations, position analysis, building requirements, and geometric operations.

## Overview

The utility system provides:

- **Build Requirements**: Technology and resource checks
- **Position Calculations**: Geometric operations and positioning
- **Proximity Detection**: Distance-based unit analysis  
- **Mathematical Functions**: Specialized calculations for gameplay

## Core Class

```python
class Utils:
    """Utility class containing a collection of static methods"""
```

All methods are static, making this a pure utility class with no state.

## Build and Production Utilities

### Structure Building Checks

#### `can_build_structure(bot, structure_id)`

```python
@staticmethod
def can_build_structure(bot: BotAI, structure_id: UnitTypeId) -> bool:
    """Checks if bot can build structure"""
    return bot.can_afford(structure_id) and bot.tech_requirement_progress(structure_id)
```

**Purpose:** Validates building requirements  
**Checks:** Resource availability and tech requirements  
**Usage:** Used by macro system for building decisions

### Unit Production Checks

#### `can_build_unit(bot, unit_id)`

```python
@staticmethod  
def can_build_unit(bot: BotAI, unit_id: UnitTypeId) -> bool:
    """Checks if bot can build unit"""
    return bot.can_afford(unit_id) and bot.can_feed(unit_id) \
        and bot.tech_requirement_progress(unit_id)
```

**Validation Criteria:**
- **Resources:** Minerals and gas availability
- **Supply:** Population cap requirements  
- **Technology:** Research prerequisites

### Research Validation

#### `can_research_upgrade(bot, upgrade_id)`

```python
@staticmethod
def can_research_upgrade(bot: BotAI, upgrade_id: UpgradeId) -> bool:
    """Checks if bot can research upgrade"""
    return bot.can_afford(upgrade_id) and not bot.already_pending_upgrade(upgrade_id)\
        and bot.tech_requirement_progress(upgrade_id)
```

**Safety Checks:**
- Resource requirements met
- Not already researching
- Tech prerequisites satisfied

## Position and Building Management

### Build Position Selection

#### `get_build_pos(bot)`

```python
@staticmethod
def get_build_pos(bot: BotAI) -> Union[Point2, Point3, Unit]:
    """Returns build position based on game state"""
```

**Priority Logic:**
1. **Early Game:** Pylon at main base ramp
2. **Gateway Phase:** Protoss wall warp-in position  
3. **Late Game:** Near Nexus toward map center

**Implementation:**
```python
if not bot.structures(UnitTypeId.PYLON):
    return bot.main_base_ramp.protoss_wall_pylon
elif not bot.structures(UnitTypeId.GATEWAY) and not bot.already_pending(UnitTypeId.GATEWAY):
    return bot.main_base_ramp.protoss_wall_warpin
else:
    return bot.structures(UnitTypeId.NEXUS)[0]\
        .position3d.towards(bot.game_info.map_center, 5)
```

### Warp-In Positioning

#### `get_warp_in_pos(bot)`

```python
@staticmethod
def get_warp_in_pos(bot: BotAI) -> Union[Point2, Point3, Unit]:
    """Returns optimal warp-in position"""
```

**Strategic Selection:**

**Without Warp Prism:**
```python
if bot.supply_army > 10:
    # Find pylon closest to army
    return bot.structures(UnitTypeId.PYLON)\
        .in_closest_distance_to_group([x for x in bot.units if x not in bot.workers])
else:
    # Early game: forward pylon
    return bot.structures(UnitTypeId.PYLON)\
        .closest_to(bot.enemy_start_locations[0])
```

**With Warp Prism:**
```python
if bot.enemy_units:
    active_prism = bot.units(UnitTypeId.WARPPRISM).closest_to(bot.enemy_units.center)
else:
    active_prism = bot.units(UnitTypeId.WARPPRISM).closest_to(bot.enemy_start_locations[0])
return active_prism.position
```

## Proximity Detection System

### Point-Based Proximity

#### `unittype_in_proximity_to_point(bot, type_id, point, max_distance)`

```python
@staticmethod
def unittype_in_proximity_to_point(bot: BotAI,
                                   type_id: UnitTypeId,
                                   point: Union[Point2,Point3,Unit],
                                   max_distance: float = .5
                                   ) -> bool:
    """Returns true if a unit of type is in radius around point"""
    return bot.units(type_id).filter(lambda unit: unit.distance_to(point)<max_distance)
```

**Use Cases:**
- Detector placement validation
- Unit clustering analysis
- Formation checking

### Structure Proximity

#### `structure_in_proximity(bot, structure_type, structure, max_distance)`

```python
@staticmethod
def structure_in_proximity(bot: BotAI,
                           structure_type: UnitTypeId,
                           structure: Unit,
                           max_distance: float
                           ) -> bool:
    """Checks if structures of type are near another structure"""
```

**Applications:**
- Pylon power field overlap
- Defensive structure clustering
- Production facility organization

### Unit Proximity

#### `unit_in_proximity(bot, unit_type, unit, max_distance)`

```python
@staticmethod
def unit_in_proximity(bot: BotAI, unit_type: UnitTypeId, unit: Unit, max_distance: float) -> bool:
    """Checks if specific unit type is near a unit"""
```

### Direct Distance Checks

#### `in_proximity_to_point(unit, point, max_distance)`

```python
@staticmethod
def in_proximity_to_point(unit: Unit, point: Union[Point2, Point3], max_distance: float) -> bool:
    """Checks if unit is in proximity to a point"""
    if isinstance(point, Units):
        return False
    return unit.distance_to(point) < max_distance
```

#### `is_close_to_unit(unit_1, unit_2, max_distance)`

```python
@staticmethod
def is_close_to_unit(unit_1: Unit, unit_2: Unit, max_distance: float) -> bool:
    """Checks if two units are close to each other"""
    return unit_1.distance_to(unit_2) <= max_distance
```

## Mathematical Functions

### Circle Intersection Calculation

#### `get_intersections(p0, r0, p1, r1)`

```python
@staticmethod
def get_intersections(p0: Point2, r0: float, p1: Point2, r1: float) -> Iterable[Point2]:
    """Yield the intersection points of 2 circles"""
```

**Mathematical Implementation:**
```python
p01 = p1 - p0
d = np.linalg.norm(p01)

# Handle edge cases
if d == 0: return  # intersection is empty or infinite
if d < abs(r0 - r1): return  # circles inside each other  
if r0 + r1 < d: return  # circles too far apart

# Calculate intersection points
a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
h = math.sqrt(r0 ** 2 - a ** 2)
pm = p0 + (a / d) * p01
po = (h / d) * np.array([p01.y, -p01.x])

yield pm + po
yield pm - po
```

**Use Cases:**
- Overlapping unit ranges
- Formation positioning
- Area denial calculations

### Activation Functions

#### `sigmoid(x)`

```python
@staticmethod
def sigmoid(x: float) -> float:
    """Sigmoid function using numpy for array compatibility"""
    return 1/(1 + np.exp(-x))
```

**Applications:**
- Smooth value transitions
- Decision making weights
- Probability calculations

### Coordinate Transformations

#### `create_3D_point(bot, point)`

```python
@staticmethod
def create_3D_point(bot: BotAI, point: Point2) -> Point3:
    """Creates Point3 from Point2 using terrain height"""
    z = bot.get_terrain_z_height(point) + 0.01
    x, y = point.x, point.y
    return Point3((x, y, z))
```

**Purpose:** Converts 2D coordinates to 3D for rendering and spatial calculations

#### `angle_between_points(p_1, p_2)`

```python
@staticmethod
def angle_between_points(p_1: Point2, p_2: Point2) -> float:
    """Calculates the θ between two points"""
    delta_x: float = p_1.x - p_2.x
    delta_y: float = p_1.y - p_2.y
    theta: float = math.atan2(delta_x, delta_y)
    return theta
```

**Use Cases:**
- Unit facing calculations
- Movement vector analysis
- Tactical positioning

## Legacy and Deprecated Functions

### Army Target Selection

#### `get_army_target(bot)` - DEPRECATED

```python
@staticmethod
def get_army_target(bot: BotAI) -> Union[Point2, Point3]:
    """Get a Target for Army - not in use can be removed"""
    if bot.enemy_units:
        return bot.enemy_units.center
    else:
        return bot.enemy_start_locations[0]
```

**Note:** This function is marked for removal as army targeting is now handled by the targeting system.

### Boolean Operations

#### `and_or(a, b)` - UNCLEAR PURPOSE

```python
@staticmethod
def and_or(a: any, b: any) -> bool:
    """Just performs and/or -> here to keep lines shorter"""
    return a or b or (a and b)
```

**Note:** This function's purpose is unclear and may need refactoring for clarity.

## Integration Examples

### Macro System Integration

```python
class MacroManager:
    def can_build_next_structure(self):
        """Check if next planned structure can be built"""
        next_structure = self.build_queue[0]
        return Utils.can_build_structure(self.bot, next_structure.type_id)
    
    def get_optimal_build_location(self):
        """Get position for next structure"""
        return Utils.get_build_pos(self.bot)
```

### Army Group Integration

```python
class ArmyGroup:
    def can_warp_in_reinforcements(self):
        """Check if reinforcements can be warped in"""
        warp_pos = Utils.get_warp_in_pos(self.bot)
        return self.bot.structures(UnitTypeId.WARPGATE).ready.exists
    
    def check_unit_clustering(self, max_distance=3.0):
        """Analyze unit formation"""
        clustered_units = []
        for unit in self.units:
            nearby = [u for u in self.units 
                     if Utils.is_close_to_unit(unit, u, max_distance)]
            if len(nearby) > 3:
                clustered_units.append(unit)
        return clustered_units
```

### Combat System Integration

```python
class CombatUnit:
    def find_nearby_enemies(self, detection_range=12):
        """Find enemies within detection range"""
        nearby_enemies = []
        for enemy in self.bot.enemy_units:
            if Utils.in_proximity_to_point(enemy, self.position, detection_range):
                nearby_enemies.append(enemy)
        return nearby_enemies
    
    def calculate_retreat_position(self):
        """Calculate safe retreat position using circle intersections"""
        safe_points = []
        for ally in self.nearby_allies:
            # Find intersection of safe zones
            intersections = Utils.get_intersections(
                self.position, self.retreat_distance,
                ally.position, ally.protection_range
            )
            safe_points.extend(intersections)
        return self.select_best_retreat_point(safe_points)
```

## Performance Considerations

### Optimization Notes

**Frequent Operations:**
- Proximity checks are called many times per frame
- Consider caching results for expensive calculations
- Use squared distances where possible to avoid sqrt operations

**Memory Usage:**
- Static methods don't create object overhead
- NumPy operations can handle arrays efficiently
- Circle intersection generator avoids storing all results

### Usage Guidelines

**Best Practices:**
- Use type hints for better code clarity
- Validate inputs for geometric functions
- Consider edge cases in mathematical operations
- Cache expensive calculations when possible

**Common Patterns:**
```python
# Efficient proximity checking
if Utils.is_close_to_unit(unit1, unit2, combat_range):
    # Engage combat
    pass

# Safe building placement
build_pos = Utils.get_build_pos(self.bot)
if Utils.can_build_structure(self.bot, UnitTypeId.GATEWAY):
    # Place building
    pass

# Formation analysis
clustered_units = [unit for unit in army_units 
                  if Utils.unittype_in_proximity_to_point(
                      self.bot, UnitTypeId.STALKER, unit.position, 3.0)]
```

The utility system provides the mathematical and logical foundation for the bot's decision-making processes, from basic resource checks to complex geometric calculations used in advanced tactics.
