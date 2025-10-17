# Debug Tools System

The `DebugTools` class provides comprehensive debugging and visualization capabilities for the HarstemsAunt bot, enabling real-time analysis of game state, unit behavior, and system performance.

## Overview

The debug system provides:

- **Visual Debugging**: 3D rendering of game elements and data
- **Performance Monitoring**: Step time analysis and optimization tracking  
- **Unit Analysis**: Behavior visualization and state inspection
- **System Testing**: Automated unit creation and scenario setup

## Core Class

```python
class DebugTools:
    """Collection of debug tools"""
    
    def __init__(self, bot: BotAI) -> None:
        self.bot = bot
```

The debug tools maintain a reference to the bot instance for access to game state and rendering capabilities.

## Visual Debugging System

### Position Visualization

#### `debug_pos(pos, radius, color)`

```python
def debug_pos(self,
              pos: Union[Point2, Point3, Pointlike],
              radius: float = .2,
              color: Tuple[int, int, int] = (255, 255, 0)
              ):
    """Draws sphere at given position"""
    pos_3d = Utils.create_3D_point(self.bot, pos)
    self.bot.client.debug_sphere_out(pos_3d, radius, color)
```

**Purpose:** Mark specific positions with colored spheres  
**Use Cases:** Build position validation, waypoint marking, area highlighting

### Game Information Display

#### `draw_gameinfo()`

```python
def draw_gameinfo(self):
    """Draws game information to screen"""
    text: str = ""
    supply: int = self.bot.supply_army
    enemy_supply: int = self.bot.enemy_supply
    text = text + (f"supply: {supply}\nenemy_supply: {enemy_supply}\n")
    minerals: int = self.bot.minerals
    gas: int = self.bot.vespene
    text = text + (f"\nIncome: {minerals, gas}\n")
    self.bot.client.debug_text_screen(str(text), (0, .125), color=None, size=14)
```

**Information Displayed:**
- Current army supply vs enemy supply
- Resource counts (minerals and gas)
- Economic comparison metrics

### Performance Monitoring

#### `draw_step_time_label()`

```python
def draw_step_time_label(self):
    """Draws step time min, avg, max and last"""
    labels = ["min_step", "avg_step", "max_step", "last_step"]
    for i, value in enumerate(self.bot.step_time):
        if value > 34:
            color = (0, 0, 255)  # Red for slow frames
        else:
            color = (0, 255, 0)  # Green for good performance
        self.bot.client.debug_text_screen(f"{labels[i]}: {round(value,3)}", 
            (0, 0.025+(i*0.025)), color=color, size=DEBUG_FONT_SIZE)
```

**Performance Metrics:**
- **Minimum Step Time**: Fastest frame processing
- **Average Step Time**: Overall performance baseline
- **Maximum Step Time**: Worst-case processing time  
- **Last Step Time**: Most recent frame performance

**Alert System:** Red highlighting when frame time exceeds 34ms (performance threshold)

## Unit Analysis Tools

### Unit Information Display

#### `unit_label(unit)`

```python
def unit_label(self, unit: Unit):
    """Draws information about the unit in a label at the unit"""
    text: str = f"Type: {unit.type_id}\nHealth: {unit.health}\nOrders: {unit.orders}\nPos {unit.position3d}"
    self.bot.client.debug_text_world(text, unit, color=(255,90,0), size=12)
```

**Displayed Information:**
- Unit type identification
- Current health status
- Active orders and commands
- 3D position coordinates

### Combat Range Visualization

#### `unit_range(unit)`

```python
def unit_range(self, unit: Unit):
    """Draws range of unit"""
    if unit.can_attack_ground:
        self.bot.client.debug_sphere_out(unit, unit.ground_range, (0,255,0))
    if unit.can_attack_air:
        self.bot.client.debug_sphere_out(unit, unit.air_range, (255,0,25))
```

**Range Types:**
- **Ground Range**: Green sphere showing ground attack range
- **Air Range**: Red sphere showing anti-air attack range
- **Dual Display**: Both ranges for units with mixed capabilities

### Unit Behavior Analysis

#### `debug_fighting_status(combat_unit)`

```python
def debug_fighting_status(self, combat_unit: CombatUnit) -> None:
    """Draws colored sphere around unit based on fight status"""
    if combat_unit.unit:
        color: tuple = (0,0,255) if combat_unit.fight_status == FightStatus.RETREATING else (0,255,0)
        self.bot.client.debug_sphere_out(combat_unit.position3d, .75, color)
```

**Status Indicators:**
- **Green Sphere**: Unit is engaging/attacking
- **Blue Sphere**: Unit is retreating
- **Visual Feedback**: Real-time combat decision display

### Targeting Visualization

#### `debug_targeting(unit, target)`

```python
def debug_targeting(self, unit: Unit, target: Union[Unit, Point2]) -> None:
    """Draws line to current target with target sphere"""
    unit_position: Point3 = unit.position3d
    if isinstance(target, Point2):
        target = Utils.create_3D_point(self.bot, target)
    if isinstance(target, Unit):
        target = target.position3d
    self.bot.client.debug_line_out(unit_position, target, (0,0,255))
    self.bot.client.debug_sphere_out(target, .75, (0,0,255))
```

**Visual Elements:**
- **Blue Line**: Connection from unit to target
- **Blue Sphere**: Target location marker
- **Real-time Updates**: Shows current targeting decisions

## Army Group Debugging

### Group Status Display

#### `draw_army_group_label(iterator, group)`

```python
def draw_army_group_label(self, iterator: int, group: ArmyGroup) -> None:
    """Draws ArmyGroup information on screen"""
    self.bot.client.debug_text_screen(f"{group.group_type_id}: {group.attack_target}",
        (.25+(iterator*0.25), 0.025), color=(255,255,255), size=DEBUG_FONT_SIZE)
    self.bot.client.debug_text_screen(f"Supply:{group.supply} Enemy Supply:{group.enemy_supply_in_proximity}",
        (.25+(iterator*0.27), 0.05), color=(255,255,255), size=DEBUG_FONT_SIZE)
    self.bot.client.debug_text_screen(f"requested:{group.requested_units}",
        (.25+(iterator*0.27), 0.075), color=(255,255,255), size=DEBUG_FONT_SIZE)
    self.bot.client.debug_text_screen(f"enemies in proximity {group.enemies_in_proximity}",
        (.25+(iterator*0.27), .1), color=(255,255,255), size=DEBUG_FONT_SIZE)
```

**Group Information Display:**
- **Group Identity**: Type and current target
- **Supply Comparison**: Own vs enemy forces nearby
- **Unit Requests**: Production queue status
- **Tactical Situation**: Proximity analysis
- **Regional Data**: Map sector information

## Legacy Systems

### Vision Analysis (DEPRECATED)

#### `render_unit_vision(unit)`

```python
def render_unit_vision(self, unit: Unit):
    """Draws unit vision using old raycasting approach (no longer in use)"""
    # Legacy vision rendering system
    # Note: This is very old -> copied from Lore, raycasting approach no longer used
```

**Note:** This system is deprecated and maintained only for historical reference. Modern vision analysis uses different approaches.

## Development and Testing Tools

### Automated Unit Creation

#### `debug_micro()`

```python
async def debug_micro(self) -> None:
    """Build Stalker/Zealot for both players to debug unit behavior"""
    units_dict: dict = {
        Race.Zerg: [UnitTypeId.ZERGLING, UnitTypeId.ROACH],
        Race.Terran: [UnitTypeId.MARINE, UnitTypeId.MARAUDER],
        Race.Protoss: [UnitTypeId.STALKER, UnitTypeId.IMMORTAL]
    }
    units: list = units_dict.get(self.bot.enemy_race)
    
    await self.bot.client.debug_tech_tree()
    await self.bot.client.debug_create_unit([[UnitTypeId.STALKER, 5, self.bot.start_location, 1]])
    await self.bot.client.debug_create_unit([[UnitTypeId.IMMORTAL, 3, self.bot.start_location, 1]])
    await self.bot.client.debug_create_unit([[units[0], 5, self.bot.enemy_start_locations[0], 2]])
    await self.bot.client.debug_create_unit([[units[1], 3, self.bot.enemy_start_locations[0], 2]])
```

**Setup Features:**
- **Race-Specific Units**: Creates appropriate enemy units for each race
- **Balanced Forces**: Equal unit counts for fair testing
- **Tech Tree Access**: Unlocks all technologies for testing
- **Positioning**: Strategic placement of test units

### Development Acceleration

#### `speed_things_up()`

```python
async def speed_things_up(self) -> None:
    """Makes development testing faster"""
    await self.bot.client.debug_fast_build()  # Buildings take no time
    await self.bot.client.debug_all_resources()  # Free minerals and gas
```

**Development Benefits:**
- **Instant Building**: No construction time delays
- **Unlimited Resources**: Focus on logic without resource constraints
- **Rapid Iteration**: Quick testing of different scenarios

## Specialized Visualization

### Unit Marker Display

#### `draw_unit_marker(marker)`

```python
def draw_unit_marker(self, marker: UnitMarker) -> None:
    """Renders a unit marker with health-based coloring"""
    pos: Point2 = marker.position
    z = self.bot.get_terrain_z_height(pos) + 1
    x, y = pos.x, pos.y
    pos_3d = Point3((x, y, z))
    self.bot.client.debug_sphere_out(pos_3d, .2, marker.color)
```

**Color Coding:**
- **Yellow**: High health (>75%)
- **Light Blue**: Medium health (25-75%)  
- **Blue**: Low health (<25%)

### Directional Analysis

#### `debug_unit_direction(unit)`

```python
def debug_unit_direction(self, unit: Unit) -> None:
    """Renders unit facing direction"""
    distance: float = 2
    direction: float = unit.facing
    x, y = unit.position
    q_x = x + distance * cos(direction)
    q_y = y + distance * sin(direction)
    pos_3D = Utils.create_3D_point(self.bot, Point2((q_x, q_y)))
    self.bot.client.debug_sphere_out(pos_3D, .25, (0,255,0))
    self.bot.client.debug_line_out(unit.position3d, pos_3D, (0,255,0))
```

**Visual Elements:**
- **Green Line**: Shows unit facing direction
- **Green Sphere**: Direction endpoint marker
- **Distance Scale**: 2-unit projection for clarity

#### `debug_angle_to_target(unit)`

```python
def debug_angle_to_target(self, unit: Unit) -> None:
    """Renders angle to closest enemy unit"""
    # Mathematical calculation of angle to nearest threat
    # Blue visualization showing optimal facing direction
```

**Purpose:** Visualizes optimal unit orientation for engagement

## Map and Environment Tools

### Resource Visualization

#### `draw_vespene_pos()`

```python
def draw_vespene_pos(self) -> None:
    """Renders vespene geyser positions"""
    start_pos: Point2 = self.bot.start_location
    geysers = self.bot.vespene_geyser.closer_than(12, start_pos)
    for geyser in geysers:
        self.bot.client.debug_sphere_out(geyser, 2, (255,255,255))
```

**Visualization:** White spheres marking nearby vespene geysers

### Build Position Analysis

#### `debug_build_pos()`

```python
def debug_build_pos(self) -> None:
    """Draws sphere at the current build position"""
    pos: Union[Point2, Unit] = self.bot.macro.build_order.get_build_pos()
    if isinstance(pos, Unit):
        self.bot.client.debug_sphere_out(pos, 1, (255,255,0))
        return
    pos_3D = Utils.create_3D_point(self.bot, pos)
    self.bot.client.debug_sphere_out(pos_3D, 1, (255,255,0))
```

**Visualization:** Yellow sphere showing where next structure will be placed

## Drawing Utilities

### Line Rendering

#### `draw_line_from_to(origin, target, color)`

```python
def draw_line_from_to(self,
                      origin: Union[Point2, Point3, Unit],
                      target: Union[Point2, Point3, Unit],
                      color=(255,0,255)):
    """Renders line from origin to target with error handling"""
    # Handles different input types and coordinate conversion
    # Includes exception handling for rendering errors
```

**Features:**
- **Type Flexibility**: Accepts various position formats
- **Error Handling**: Graceful failure with logging
- **Color Customization**: Configurable line colors

## Integration Examples

### Main Bot Integration

```python
class HarstemsAunt(BotAI):
    def __init__(self):
        self.debug = DebugTools(self)
    
    async def on_step(self, iteration):
        if self.debug_mode:
            self.debug.draw_gameinfo()
            self.debug.draw_step_time_label()
            
            # Army group visualization
            for i, group in enumerate(self.army_groups):
                self.debug.draw_army_group_label(i, group)
            
            # Unit behavior analysis
            for combat_unit in self.combat_units:
                self.debug.debug_fighting_status(combat_unit)
```

### Performance Monitoring

```python
class PerformanceMonitor:
    def analyze_bottlenecks(self):
        """Use debug tools to identify performance issues"""
        if self.step_time[-1] > 34:  # Frame took too long
            self.log_performance_warning()
            # Enable detailed debugging
            self.debug.draw_step_time_label()
```

### Unit Testing Integration

```python
async def test_combat_behavior(self):
    """Set up test scenario for combat analysis"""
    await self.debug.debug_micro()  # Create test units
    await self.debug.speed_things_up()  # Accelerate testing
    
    # Monitor behavior
    for unit in self.test_units:
        self.debug.unit_range(unit)
        self.debug.debug_unit_direction(unit)
```

## Configuration and Usage

### Debug Mode Control

```python
class HarstemsAunt(BotAI):
    @property
    def debug_enabled(self) -> bool:
        """Check if debugging is enabled"""
        return self.config.get('debug_mode', False) and not self.tournament_mode
    
    def toggle_debug_features(self, feature_set: str):
        """Enable specific debug feature sets"""
        debug_configs = {
            'performance': ['step_time', 'resource_info'],
            'combat': ['unit_ranges', 'targeting', 'fight_status'],
            'macro': ['build_positions', 'army_groups'],
            'full': ['all_features']
        }
        # Configure debug features based on selection
```

### Selective Debugging

```python
def conditional_debug(self):
    """Enable debugging based on game state"""
    if self.supply_army > 50:  # Late game analysis
        for group in self.army_groups:
            self.debug.draw_army_group_label(0, group)
    
    if self.minerals < 100:  # Economic pressure
        self.debug.draw_gameinfo()
    
    if self.under_attack:  # Combat analysis
        for unit in self.army_units:
            self.debug.unit_range(unit)
```

## Best Practices

### Performance Considerations

- **Selective Rendering**: Only draw necessary debug information
- **Frame Rate Impact**: Debug rendering affects performance
- **Memory Usage**: Extensive debugging can increase memory consumption

### Development Workflow

```python
# Development cycle with debug tools
async def development_step(self):
    # 1. Enable specific debug features
    if self.test_combat_micro:
        await self.debug.debug_micro()
    
    # 2. Monitor performance
    self.debug.draw_step_time_label()
    
    # 3. Analyze specific systems
    if self.focus_area == 'targeting':
        for unit in self.army_units:
            if unit.target:
                self.debug.debug_targeting(unit, unit.target)
    
    # 4. Validate positions and ranges
    self.debug.debug_build_pos()
    for unit in self.selected_units:
        self.debug.unit_range(unit)
```

### Error Handling

```python
def safe_debug_render(self):
    """Debug rendering with error handling"""
    try:
        self.debug.draw_gameinfo()
        for unit in self.debug_units:
            self.debug.unit_label(unit)
    except Exception as e:
        logger.warning(f"Debug rendering error: {e}")
        # Continue without debug rendering
```

The debug tools system provides comprehensive visualization and analysis capabilities essential for bot development, testing, and optimization, while maintaining flexibility for different development scenarios and performance requirements.
