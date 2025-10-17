# API Reference

This section provides detailed API documentation for all major components of the HarstemsAunt bot.

## Core Modules

### Main Bot Class

- **[HarstemsAunt](main.md)** - Core bot implementation and game loop management
- **[Macro](macro.md)** - Economic management and build order execution  
- **[ArmyGroup](army_group.md)** - Military unit coordination and combat management

### Unit Control

- **[CombatUnit](combat_unit.md)** - Base class for all combat units
- **[Stalker](stalker.md)** - Stalker unit micro and blink management
- **[Zealot](zealot.md)** - Zealot charge timing and melee combat
- **[Immortal](immortal.md)** - Immortal positioning and hardened shields
- **[Phoenix](phoenix.md)** - Phoenix harassment and micro-management
- **[VoidRay](voidray.md)** - Void Ray positioning and prismatic alignment
- **[CombatFlyer](combat_flyer.md)** - Air unit control (Phoenix, Void Ray)
- **[Warpprism](warpprism.md)** - Support unit micro and positioning

### Strategy and Planning

- **[BuildOrder](build_order.md)** - Build order system and instruction management
- **[ProductionBuffer](production_buffer.md)** - Dynamic unit production queueing
- **[Targeting](targeting.md)** - Target selection and allocation algorithms
- **[Runner](runner.md)** - Bot execution and configuration management

### Map and Movement

- **[Pathing](pathing.md)** - Advanced pathfinding and unit movement
- **[MapSector](map_sector.md)** - Map region analysis and control
- **[EnemyUnit](enemy_unit.md)** - Enemy unit tracking and threat assessment

### Utility Systems

- **[Utils](utils.md)** - General utility functions and helpers
- **[UnitMarkers](unit_markers.md)** - Enemy unit tracking and intelligence persistence
- **[DebugTools](debug_tools.md)** - Development and debugging utilities
- **[Chatter](chatter.md)** - In-game communication system

### Support Systems

- **[Common](common.md)** - Shared constants and data structures
- **[SpeedMining](speedmining.md)** - Worker micro-management optimization

## Map Analysis Framework

- **[MapData](../map_analyzer/MapData.md)** - Core map analysis functionality
- **[Region](../map_analyzer/Region.md)** - Map region definitions and properties
- **[Constructs](../map_analyzer/constructs.md)** - Map analysis data structures

## Benchmarking System  

- **[Benchmark](../benchmarks/benchmark.md)** - Performance testing framework
- **[Scenario](../benchmarks/scenario.md)** - Test scenario definitions
- **[Result](../benchmarks/result.md)** - Benchmark result analysis

## Usage Examples

### Basic Bot Usage

```python
from bot.HarstemsAunt.main import HarstemsAunt
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

# Create bot instance
bot = HarstemsAunt(debug=False, benchmark=False)

# Run a game
run_game(
    maps.get("Acropolis AIE"),
    [
        Bot(Race.Protoss, bot),
        Computer(Race.Zerg, Difficulty.VeryHard)
    ],
    realtime=False
)
```

### Custom Configuration

```python
# Enable debug mode with custom settings
bot = HarstemsAunt(
    debug=True,
    benchmark=True, 
    benchmark_message="Testing new stalker micro"
)
```

### Accessing Bot Components

```python
class CustomBot(HarstemsAunt):
    async def on_step(self, iteration):
        # Access macro system
        await self.macro()
        
        # Get army groups
        for army_group in self.army_groups:
            await army_group.execute()
            
        # Custom logic here
        await super().on_step(iteration)
```

## Type Definitions

### Common Types

```python
from typing import Union, List, Dict, Optional
from sc2.position import Point2, Point3
from sc2.unit import Unit
from sc2.units import Units
from sc2.ids.unit_typeid import UnitTypeId

# Position types
Position = Union[Point2, Point3, Unit]

# Unit collections
UnitGroup = Union[Unit, Units, List[Unit]]

# Build targets
BuildTarget = Dict[UnitTypeId, int]
```

### Enums

```python
from enum import Enum

class GroupStatus(Enum):
    ATTACKING = 1
    DEFENDING = 2  
    RETREATING = 3
    REGROUPING = 4

class FightStatus(Enum):
    IDLE = 1
    FIGHTING = 2
    RETREATING = 3
    KITING = 4
```

## Error Handling

### Exception Types

The bot defines custom exception types for different error conditions:

```python
class BotError(Exception):
    """Base exception for bot-related errors"""
    pass

class PathfindingError(BotError):
    """Raised when pathfinding fails"""
    pass

class BuildOrderError(BotError):  
    """Raised when build order execution fails"""
    pass
```

### Error Recovery

Most bot components implement graceful error recovery:

```python
try:
    await self.macro.handle_instructions()
except BuildOrderError as e:
    self.logger.warning(f"Build order error: {e}")
    # Fall back to emergency build order
    self.macro.build_order.reset_to_emergency()
```

## Performance Considerations

### Computational Complexity

- **Unit Selection**: O(n log n) where n is number of units
- **Pathfinding**: O(V log V) where V is number of graph vertices  
- **Target Assignment**: O(n²) for n targets and n units
- **Map Analysis**: O(1) after initial preprocessing

### Memory Usage

- **Unit Tracking**: ~100 bytes per tracked unit
- **Map Data**: ~10MB for pathfinding graphs
- **History Buffers**: ~1MB for performance tracking

### Optimization Tips

1. **Use Spatial Indexing**: For efficient nearest-neighbor queries
2. **Cache Expensive Calculations**: Using `@cached_property` decorator
3. **Limit History Length**: Keep only recent performance data
4. **Batch Operations**: Process multiple units together when possible

## Testing

### Unit Tests

```python
import pytest
from bot.HarstemsAunt.stalker import Stalker
from tests.mock_objects import MockBot, MockUnit

def test_stalker_blink_timing():
    bot = MockBot()
    stalker_unit = MockUnit(UnitTypeId.STALKER)
    stalker = Stalker(stalker_unit, bot)
    
    # Test blink decision making
    should_blink = stalker.should_use_blink(enemy_position)
    assert isinstance(should_blink, bool)
```

### Integration Tests

```python
def test_full_game_simulation():
    bot = HarstemsAunt(debug=True)
    result = run_test_game(bot, Computer(Race.Zerg, Difficulty.Easy))
    
    # Verify bot completed game successfully  
    assert result is not None
    assert bot.state.game_loop > 1000  # Ran for reasonable time
```
