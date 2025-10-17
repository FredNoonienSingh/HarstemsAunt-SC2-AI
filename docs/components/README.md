# Bot Components Documentation

This section provides detailed documentation for the individual components that make up the HarstemsAunt bot system.

## Core Components

### Economic Management

**[Macro System](macro.md)**
The macro system handles all economic aspects of the game including resource management, worker production, and build order execution.

**[Build Order System](build_order.md)**  
A sophisticated system for executing predefined build sequences and adapting to game conditions.

**[Production Buffer](production_buffer.md)**
Dynamic unit production queue management that adapts to strategic needs and resource availability.

### Military Management

**[Army Group System](army_group.md)**
Hierarchical military unit organization that coordinates large-scale army movements and combat operations.

**[Combat Units](combat_units.md)**
Individual unit control systems with specialized micro-management for each Protoss unit type:
- Stalker: Blink micro and kiting
- Zealot: Charge timing and engagement  
- Immortal: Positioning and shield management
- Phoenix: Air superiority and harassment
- Void Ray: Beam ramping and focus fire

### Movement and Positioning

**[Pathing System](pathing.md)**
Advanced pathfinding algorithms that handle unit movement across complex terrain while maintaining formations.

**[Map Analysis](map_analysis.md)**
Comprehensive map reading system that identifies strategic locations, choke points, and optimal expansion sites.

### Intelligence and Strategy

**[Enemy Tracking](enemy_tracking.md)**
Sophisticated enemy unit tracking and threat assessment system.

**[Targeting System](targeting.md)**
Intelligent target selection and allocation algorithms for optimal combat effectiveness.

**[Strategic Decision Making](strategy.md)**
High-level strategic decision making including build order adaptation and strategic transitions.

### Support Systems

**[Debug and Visualization](debug_tools.md)**
Development tools for debugging bot behavior and visualizing decision-making processes.

**[Performance Monitoring](performance.md)**
Real-time performance monitoring and optimization tools.

**[Utility Functions](utilities.md)**
Common utility functions and helper methods used throughout the bot.

## Component Architecture

### Modular Design

Each component is designed as an independent module with:
- Clear interfaces and well-defined responsibilities
- Minimal dependencies on other components  
- Robust error handling and graceful degradation
- Comprehensive logging and debugging support

### Data Flow

```text
Game Events → Main Bot → Component Updates → Decision Making → Action Execution
     ↑                                                              ↓
     └─────────────── Feedback Loop ← Performance Monitoring ←─────┘
```

### Component Lifecycle

1. **Initialization**: Components initialize during bot startup
2. **Configuration**: Load settings and establish dependencies
3. **Execution**: Process game events and execute behaviors
4. **Monitoring**: Track performance and adjust parameters
5. **Cleanup**: Graceful shutdown and data persistence

## Integration Patterns

### Event-Driven Architecture

Components communicate through event handlers:

```python
async def on_unit_created(self, unit: Unit):
    # Notify relevant components
    self.army_groups.handle_new_unit(unit)
    self.production_buffer.update_completion(unit.type_id)
    self.strategic_analyzer.assess_composition_change()
```

### Dependency Injection

Components receive dependencies through their constructors:

```python
class ArmyGroup:
    def __init__(self, bot: BotAI, pathing: Pathing, targeting: Targeting):
        self.bot = bot
        self.pathing = pathing  
        self.targeting = targeting
```

### Strategy Pattern

Behaviors are implemented as interchangeable strategies:

```python
class CombatStrategy:
    def execute(self, unit: Unit, enemies: Units) -> None:
        pass

class KitingStrategy(CombatStrategy):
    def execute(self, unit: Unit, enemies: Units) -> None:
        # Implement kiting behavior
        pass
```

## Performance Characteristics

### Computational Complexity

| Component | Initialization | Per-Step | Memory Usage |
|-----------|---------------|----------|--------------|
| Macro | O(1) | O(1) | ~1MB |
| Army Groups | O(n) | O(n log n) | ~10KB per unit |
| Pathfinding | O(V²) | O(V log V) | ~10MB |
| Map Analysis | O(n²) | O(1) | ~5MB |
| Targeting | O(1) | O(n²) | ~1MB |

Where:
- n = number of units
- V = number of pathfinding vertices

### Scalability Limits

- **Maximum Units**: 200 simultaneous units
- **Maximum Army Groups**: 10 concurrent groups
- **Map Size**: Up to 256x256 terrain tiles
- **Real-time Performance**: 16+ steps per second

## Configuration

### Component Settings

Each component supports configuration through JSON files:

```json
{
    "macro": {
        "workers_per_base": 22,
        "supply_buffer": 8
    },
    "army_groups": {
        "max_group_size": 30,
        "formation_spacing": 2.0
    },
    "pathfinding": {
        "grid_resolution": 1.0,
        "avoid_enemy_range": true
    }
}
```

### Runtime Adaptation

Components can adapt their behavior based on game conditions:

```python
def adapt_to_game_state(self):
    if self.enemy_air_threat_level > 0.7:
        self.increase_phoenix_production()
    
    if self.resource_advantage > 0.5:
        self.enable_aggressive_expansion()
```

## Testing and Validation

### Unit Testing

Each component includes comprehensive unit tests:

```python
def test_stalker_blink_decision():
    stalker = Stalker(mock_unit, mock_bot)
    enemy_position = Point2(10, 10)
    
    should_blink = stalker.should_use_blink(enemy_position)
    assert isinstance(should_blink, bool)
```

### Integration Testing

Components are tested together in realistic scenarios:

```python
def test_army_group_coordination():
    army_group = create_test_army_group()
    enemy_force = create_test_enemy_force()
    
    army_group.engage_enemy(enemy_force)
    
    assert army_group.is_properly_positioned()
    assert army_group.target_allocation_optimal()
```

### Performance Testing

Regular performance benchmarks ensure real-time operation:

```python
def test_pathfinding_performance():
    start_time = time.time()
    
    path = pathfinder.find_path(start_pos, end_pos)
    
    execution_time = time.time() - start_time
    assert execution_time < 0.016  # Must complete in one game tick
```

## Development Guidelines

### Adding New Components

1. **Define Interface**: Create clear public interface
2. **Implement Core Logic**: Focus on single responsibility
3. **Add Error Handling**: Implement graceful failure modes
4. **Write Tests**: Include unit and integration tests
5. **Document API**: Provide comprehensive documentation
6. **Performance Test**: Verify real-time performance

### Modifying Existing Components

1. **Understand Dependencies**: Identify affected components
2. **Maintain Compatibility**: Preserve public interfaces
3. **Update Tests**: Modify tests for new behavior
4. **Performance Impact**: Measure performance changes
5. **Documentation**: Update relevant documentation

### Best Practices

- **Single Responsibility**: Each component has one clear purpose
- **Loose Coupling**: Minimize dependencies between components
- **High Cohesion**: Related functionality grouped together
- **Error Resilience**: Components handle failures gracefully
- **Performance Awareness**: Consider computational costs
- **Comprehensive Testing**: Test both success and failure cases
