# HarstemsAunt Main Class

The `HarstemsAunt` class is the central component of the bot, inheriting from BurnySC2's `BotAI` class and orchestrating all bot activities.

## Class Definition

```python
class HarstemsAunt(BotAI):
    """Main class of the Bot"""
    
    def __init__(self, debug: bool = False, benchmark: bool = False, 
                 benchmark_message: str = None) -> None:
        super().__init__()
        self.name = "HarstemsAunt"
        self.version = "1.1_dev"  
        self.race = Race.Protoss
```

## Key Attributes

### Core Components

| Attribute | Type | Description |
|-----------|------|-------------|
| `macro` | `Macro` | Economic management and build orders |
| `pathing` | `Pathing` | Advanced pathfinding system |
| `map_data` | `MapData` | Map analysis and terrain data |
| `army_groups` | `List[ArmyGroup]` | Military unit group management |
| `unitmarkers` | `List[UnitMarker]` | Unit state tracking for debugging |

### Configuration

| Attribute | Type | Description |
|-----------|------|-------------|
| `debug` | `bool` | Enable debug output and visualizations |
| `benchmark` | `bool` | Enable performance benchmarking |
| `benchmark_message` | `str` | Custom message for benchmark data |

### Game State

| Attribute | Type | Description |
|-----------|------|-------------|
| `enemy_supply` | `int` | Tracked enemy supply count |
| `last_tick` | `int` | Previous game loop iteration |
| `iteration` | `int` | Current game loop iteration |

## Properties

### Game Information

#### `match_id`
```python
@property
def match_id(self) -> str:
    """Unique identifier of the game"""
```
Returns a unique identifier for the current match, used for data storage and analysis.

#### `data_path`
```python
@property  
def data_path(self) -> str:
    """Path where information about the match will be stored"""
```
Returns the file system path where match data should be saved.

#### `map_data_path`
```python
@property
def map_data_path(self) -> str:
    """Path to where data about the map can be stored"""
```
Returns the path for map-specific analysis data.

#### `opponent_data_path`
```python
@property
def opponent_data_path(self) -> str:
    """Path to where data about the opponent can be stored"""
```
Returns the path for opponent-specific data and analysis.

### Strategic Information

#### `get_attack_target`
```python
@property
def get_attack_target(self) -> Point2:
    """Target of the main army group"""
```
Determines the primary attack target based on enemy units and structures:
- Prioritizes enemy units (excluding workers and hallucinations)
- Falls back to enemy structures if no valid units found
- Defaults to enemy start location early in game

#### `state_dict`
```python
@property
def state_dict(self) -> Dict:
    """Creates dict from self.state.score.summary"""
```
Converts the game state score summary into a dictionary for easy access.

#### `greeting`
```python
@property
def greeting(self) -> str:
    """Message that is supposed to be sent at start"""
```
Returns the initial chat message to send at game start.

## Core Methods

### Initialization

#### `__init__`
```python
def __init__(self, debug: bool = False, benchmark: bool = False, 
             benchmark_message: str = None) -> None:
```

**Parameters:**
- `debug`: Enable debug mode with visual overlays and detailed logging
- `benchmark`: Enable benchmarking system for performance analysis  
- `benchmark_message`: Custom message to include with benchmark data

Initializes all bot components and sets up the game state tracking.

### Game Loop Events

#### `on_start`
```python
async def on_start(self) -> None:
    """Coroutine run at the start of the game"""
```
Handles initial game setup:
- Initializes map analysis system
- Sets up pathing and region data
- Configures component dependencies
- Sends greeting message

#### `on_step`
```python
async def on_step(self, iteration: int) -> None:
    """Main game loop executed every game tick"""
```
Core game logic execution:
1. Updates iteration counter and game state
2. Executes macro management (`self.macro()`)
3. Processes army group behaviors
4. Updates unit markers and debug information
5. Handles benchmarking if enabled

#### `on_end`
```python
async def on_end(self, game_result: Result) -> None:
    """Coroutine called when the game ends"""
```
Handles game completion:
- Saves match data and statistics
- Processes benchmark results
- Logs final game state information

### Unit Event Handlers

#### `on_unit_created`
```python
async def on_unit_created(self, unit: Unit) -> None:
    """Called when a friendly unit is created"""
```
Handles new unit creation:
- Adds combat units to appropriate army groups
- Initializes unit-specific behaviors
- Updates unit tracking systems

#### `on_unit_destroyed`
```python
async def on_unit_destroyed(self, unit_tag: int) -> None:
    """Called when any unit is destroyed"""
```
Processes unit destruction:
- Removes units from army groups
- Updates threat assessments
- Logs unit loss statistics

#### `on_enemy_unit_entered_vision`
```python
async def on_enemy_unit_entered_vision(self, unit: Unit) -> None:
    """Called when enemy unit becomes visible"""
```
Handles enemy unit detection:
- Updates enemy unit tracking
- Adjusts strategic assessments
- Triggers appropriate responses

### Building Event Handlers

#### `on_building_construction_started`
```python
async def on_building_construction_started(self, unit: Unit) -> None:
    """Called when building construction starts"""
```
Manages build order progression:
- Increments build order step counter
- Updates production buffer
- Logs construction progress

#### `on_building_construction_complete`
```python
async def on_building_construction_complete(self, unit: Unit) -> None:
    """Called when building construction completes"""
```
Handles completed structures:
- Adds to constructed structures list
- Updates tech tree availability
- Enables new unit production

## Usage Examples

### Basic Usage

```python
from bot.HarstemsAunt.main import HarstemsAunt

# Create standard bot instance
bot = HarstemsAunt()

# Create debug instance
debug_bot = HarstemsAunt(debug=True)

# Create benchmark instance  
bench_bot = HarstemsAunt(
    benchmark=True,
    benchmark_message="Testing v1.1 stalker micro"
)
```

### Custom Subclass

```python
class CustomHarstemsAunt(HarstemsAunt):
    def __init__(self):
        super().__init__(debug=True, benchmark=False)
        self.custom_data = {}
    
    async def on_step(self, iteration):
        # Custom pre-processing
        await self.custom_analysis()
        
        # Run standard bot logic
        await super().on_step(iteration)
        
        # Custom post-processing  
        self.update_custom_data()
    
    async def custom_analysis(self):
        """Custom strategic analysis"""
        # Implement custom logic
        pass
```

### Accessing Components

```python
async def analyze_bot_state(bot: HarstemsAunt):
    # Access macro information
    build_step = bot.macro.build_order.step
    current_instruction = bot.macro.build_order.next_instruction()
    
    # Access army groups
    for group in bot.army_groups:
        print(f"Group status: {group.status}")
        print(f"Group size: {len(group.units)}")
    
    # Access map data
    regions = bot.map_data.regions
    current_region = bot.map_data.where_all(bot.units)[0]
```

## Debug Features

When debug mode is enabled:

### Visual Overlays
- Unit state information displayed on screen
- Army group formations and targets
- Build order progress and next steps
- Resource allocation and spending

### Logging Output
- Detailed decision-making information
- Performance timing data
- Error conditions and recovery actions
- Strategic state changes

### Data Collection
- Unit micro-management statistics
- Build order execution timing
- Combat effectiveness metrics
- Economic efficiency measurements

## Performance Characteristics

### Computational Complexity
- **Initialization**: O(n) where n is map size
- **Per-step execution**: O(u + g) where u is unit count and g is group count
- **Memory usage**: ~50MB baseline + ~1KB per unit

### Scalability
The bot is designed to handle:
- Up to 200 units simultaneously
- Complex pathfinding on large maps
- Real-time decision making at 16 steps/second
- Concurrent benchmarking without performance impact

## Error Handling

The main class implements comprehensive error handling:

```python
try:
    await self.macro()
except Exception as e:
    self.logger.error(f"Macro system error: {e}")
    # Continue with reduced functionality

try:
    for group in self.army_groups:
        await group.execute()
except Exception as e:
    self.logger.error(f"Army group error: {e}")
    # Fall back to individual unit control
```

This ensures the bot continues operating even if individual components encounter errors.
