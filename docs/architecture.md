# Architecture Overview

## System Architecture

HarstemsAunt follows a modular, event-driven architecture built on top of the BurnySC2 framework. The bot is structured as a collection of specialized components that handle different aspects of StarCraft II gameplay.

## Core Architecture Components

### Main Bot Class (`HarstemsAunt`)

The central `HarstemsAunt` class inherits from `BotAI` and orchestrates all bot activities:

```python
class HarstemsAunt(BotAI):
    """Main class of the Bot"""
    macro: Macro
    pathing: Pathing
    map_data: MapData
    
    def __init__(self, debug=False, benchmark=False):
        self.name = "HarstemsAunt"
        self.version = "1.1_dev"
        self.race = Race.Protoss
```

**Key Responsibilities:**
- Game state management and event handling
- Component initialization and coordination
- Debug output and performance monitoring
- Match data collection and analysis

### Macro Management System

The macro system handles economic and production decisions:

#### Macro Class
- **Purpose**: Coordinates all macro-economic activities
- **Key Methods**:
  - `__call__()`: Main execution loop called each game tick
  - `handle_instructions()`: Processes build order commands
  - `build_supply()`: Manages supply building
  - `build_probes()`: Worker production management

#### Build Order System
- **BuildOrder Class**: Manages predefined build sequences
- **BuildInstruction Class**: Individual build commands
- **InstructionType Enum**: Distinguishes between structures and units

```python
class BuildInstruction:
    def __init__(self, type_id: UnitTypeId, position: Point2, accuracy: int = 0):
        self.type_id = type_id
        self.position = position
        self.accuracy = accuracy
```

### Army Management System

Military unit control is handled through a hierarchical system:

#### Army Group Class
- **Purpose**: Manages collections of military units
- **Group Types**: Army groups vs. Run-by groups
- **Group Status**: Attacking, Defending, Retreating, Regrouping
- **Key Features**:
  - Coordinated movement and positioning
  - Target allocation and priority systems
  - Formation management
  - Combat effectiveness tracking

#### Combat Units
Specialized classes for different unit types:

- **CombatUnit**: Base class for ground units
- **Stalker**: Blink micro and kiting behavior  
- **Zealot**: Charge timing and engagement optimization
- **Immortal**: Hardened shield management and positioning
- **CombatFlyer**: Air unit coordination (Phoenix, Void Ray)
- **Warpprism**: Support unit positioning and micro

```python
class CombatUnit:
    def __init__(self, unit: Unit, bot: BotAI):
        self.unit = unit
        self.bot = bot
        self.fight_status = FightStatus.IDLE
        self.target = None
```

### Map Analysis System

The bot includes a comprehensive map analysis framework:

#### MapData Integration
- **Region Analysis**: Map divided into strategic regions
- **Pathfinding**: A* pathfinding with terrain awareness
- **Choke Point Detection**: Critical terrain feature identification
- **Height Map Analysis**: Elevation advantage calculations

#### Pathing Class
- **Purpose**: Advanced pathfinding and movement coordination
- **Features**:
  - Multi-unit pathfinding
  - Obstacle avoidance
  - Formation preservation
  - Efficient route calculation

### Utility Systems

#### UnitMarker System
- **Purpose**: Track unit states and behaviors over time
- **Applications**: Combat effectiveness analysis, debugging
- **Lifecycle Management**: Automatic cleanup of expired markers

#### Debug Tools
- **Visual Debugging**: On-screen information display
- **Performance Monitoring**: Real-time performance metrics
- **State Visualization**: Game state representation

## Data Flow Architecture

### Game Loop Integration

The bot operates within StarCraft II's game loop structure:

1. **Event Reception**: Game events (unit deaths, construction completion)
2. **State Analysis**: Current game state evaluation
3. **Decision Making**: Strategic and tactical decisions
4. **Action Execution**: Unit commands and macro actions
5. **State Update**: Internal state synchronization

### Component Communication

Components communicate through well-defined interfaces:

```python
# Macro requests army composition
self.production_buffer.add_request(ProductionRequest(UnitTypeId.STALKER, 5))

# Army groups coordinate with pathing
target_position = self.pathing.get_safe_path(start, destination)

# Combat units report to army groups  
self.army_group.report_engagement(self.unit, enemy_target)
```

## Design Patterns

### Strategy Pattern
Different combat behaviors and build orders implemented as interchangeable strategies:

```python
class Build(Enum):
    CANNON_RUSH = 1
    FOUR_GATE = 2
    BLINK_STALKER = 3
```

### Observer Pattern
Event-driven architecture with game event handlers:

```python
async def on_unit_destroyed(self, unit_tag):
    # Notify relevant components of unit loss
    self.army_groups.handle_unit_loss(unit_tag)
    self.macro.production_buffer.replace_lost_unit(unit_tag)
```

### Factory Pattern
Unit creation and management through specialized factories:

```python
def create_combat_unit(self, unit: Unit) -> CombatUnit:
    match unit.type_id:
        case UnitTypeId.STALKER:
            return Stalker(unit, self.bot)
        case UnitTypeId.ZEALOT:
            return Zealot(unit, self.bot)
```

## Performance Considerations

### Computational Efficiency
- **Caching**: Expensive calculations cached using `@cached_property`
- **Spatial Indexing**: Efficient nearest neighbor queries
- **Early Termination**: Algorithms designed to minimize computation

### Memory Management
- **Object Pooling**: Reuse of frequently created objects
- **Automatic Cleanup**: Expired objects automatically removed
- **Efficient Data Structures**: Optimized for frequent access patterns

### Real-time Constraints
- **Time Budgeting**: Each component has time limits per game tick
- **Priority Systems**: Critical decisions processed first
- **Graceful Degradation**: Reduced functionality under time pressure

## Error Handling and Robustness

### Exception Management
- **Graceful Failure**: Bot continues operating despite component failures
- **Error Logging**: Comprehensive error reporting and analysis
- **Recovery Mechanisms**: Automatic recovery from common failure modes

### Input Validation
- **Game State Validation**: Verify game state consistency
- **Command Validation**: Ensure commands are valid before execution
- **Boundary Checking**: Prevent out-of-bounds errors

## Testing Architecture

### Unit Testing
- **Component Testing**: Individual component functionality
- **Mock Objects**: Isolated testing with game state simulation
- **Performance Testing**: Computational efficiency verification

### Integration Testing
- **System Testing**: Full bot behavior validation
- **Scenario Testing**: Specific game situation testing
- **Regression Testing**: Prevent feature degradation

## Configuration Management

### Configuration System
- **JSON Configuration**: Human-readable configuration files
- **Environment Variables**: Runtime behavior modification  
- **Default Values**: Fallback configuration for robustness

```json
{
    "debug": false,
    "benchmark": true,
    "army_composition": {
        "stalker_ratio": 0.6,
        "zealot_ratio": 0.3,
        "immortal_ratio": 0.1
    }
}
```

This architecture enables the bot to handle the complexity of StarCraft II while maintaining code quality and performance standards.
