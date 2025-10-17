# Development Guide

This guide provides comprehensive information for developers who want to contribute to, modify, or extend the HarstemsAunt bot.

## Getting Started

### Prerequisites

Before contributing to HarstemsAunt, ensure you have:

- **Python 3.12.5+** with development tools
- **StarCraft II** full installation
- **Git** for version control
- **IDE** with Python support (VS Code, PyCharm recommended)
- **Basic StarCraft II Knowledge** (unit types, game mechanics)

### Development Environment Setup

1. **Clone the Repository**
```bash
git clone https://github.com/FredNoonienSingh/HarstemsAunt-SC2-AI.git
cd HarstemsAunt-SC2-AI
```

2. **Create Virtual Environment**
```bash
python -m venv dev_env
source dev_env/bin/activate  # On Windows: dev_env\Scripts\activate
```

3. **Install Development Dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

4. **Install Pre-commit Hooks**
```bash
pip install pre-commit
pre-commit install
```

5. **Verify Installation**
```bash
python -m pytest tests/ -v
python verify_installation.py
```

## Project Structure

### Core Directories

```text
HarstemsAunt/
├── bot/                    # Main bot implementation
│   ├── HarstemsAunt/      # Core bot logic
│   │   ├── main.py        # Main bot class
│   │   ├── macro.py       # Economic management
│   │   ├── army_group.py  # Military coordination
│   │   └── ...            # Other components
│   ├── map_analyzer/      # Map analysis framework
│   └── training_bots/     # Training opponents
├── benchmarks/            # Performance testing
│   ├── benchmark.py       # Main benchmark system
│   ├── configs/           # Benchmark configurations
│   └── ...               # Benchmark components
├── tests/                 # Unit and integration tests
├── docs/                  # Documentation
├── data/                  # Game data and results
└── dev_notebooks/         # Jupyter development notebooks
```

### Key Files

| File | Purpose |
|------|---------|
| `bot/HarstemsAunt/main.py` | Main bot class and game loop |
| `bot/HarstemsAunt/macro.py` | Economic management system |
| `bot/HarstemsAunt/army_group.py` | Military unit coordination |
| `benchmarks/benchmark.py` | Performance testing framework |
| `setup.py` | Package configuration |
| `requirements.txt` | Python dependencies |

## Development Workflow

### 1. Branch Management

Use Git Flow branching model:

```bash
# Feature development
git checkout -b feature/new-stalker-micro
git push -u origin feature/new-stalker-micro

# Bug fixes  
git checkout -b bugfix/fix-crash-issue
git push -u origin bugfix/fix-crash-issue

# Hotfixes
git checkout -b hotfix/critical-fix
git push -u origin hotfix/critical-fix
```

### 2. Code Changes

Follow this development cycle:

1. **Write Tests First** (TDD approach)
2. **Implement Feature** with minimal viable functionality
3. **Run Tests** to ensure functionality works
4. **Benchmark Performance** to check for regressions
5. **Update Documentation** to reflect changes
6. **Code Review** before merging

### 3. Testing Strategy

#### Unit Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_stalker.py -v

# Run with coverage
python -m pytest tests/ --cov=bot --cov-report=html
```

#### Integration Tests
```bash
# Run full bot integration tests
python -m pytest tests/integration/ -v

# Test against specific opponents
python test_against_computer.py --difficulty=VeryHard --games=10
```

#### Performance Tests
```bash
# Run benchmark suite
python -m pytest benchmarks/test_performance.py

# Run specific benchmark
python benchmarks/run_benchmark.py --scenario=stalker_micro
```

## Code Style and Standards

### Python Style Guide

Follow PEP 8 with these specific guidelines:

```python
# Good: Clear, descriptive names
def calculate_stalker_blink_timing(unit: Unit, enemy_position: Point2) -> bool:
    """Determine if stalker should blink to engage enemy"""
    pass

# Bad: Unclear abbreviations  
def calc_stlk_blnk(u, pos):
    pass
```

### Type Hints

Use comprehensive type hints:

```python
from typing import List, Dict, Optional, Union
from sc2.unit import Unit
from sc2.units import Units

class ArmyGroup:
    def __init__(self, bot: BotAI, units: Units) -> None:
        self.units: Units = units
        self.target: Optional[Point2] = None
        
    def add_units(self, new_units: Union[Unit, Units]) -> None:
        """Add units to the army group"""
        pass
```

### Documentation Standards

#### Function Documentation
```python
def execute_stalker_micro(self, stalker: Unit, enemies: Units) -> None:
    """Execute micro-management for a stalker unit.
    
    Args:
        stalker: The stalker unit to control
        enemies: Nearby enemy units to consider
        
    Returns:
        None
        
    Raises:
        ValueError: If stalker is not a valid stalker unit
        
    Example:
        >>> execute_stalker_micro(stalker_unit, nearby_enemies)
    """
```

#### Class Documentation
```python
class CombatUnit:
    """Base class for all combat unit controllers.
    
    This class provides common functionality for unit micro-management
    including target selection, positioning, and ability usage.
    
    Attributes:
        unit: The SC2 unit being controlled
        bot: Reference to the main bot instance
        target: Current target for the unit
        
    Example:
        >>> combat_unit = CombatUnit(stalker_unit, bot_instance)
        >>> combat_unit.execute_micro()
    """
```

### Error Handling

Implement comprehensive error handling:

```python
def safe_unit_command(unit: Unit, command: Callable) -> bool:
    """Safely execute a unit command with error handling"""
    try:
        if unit.is_ready and unit.is_alive:
            command()
            return True
    except Exception as e:
        logger.warning(f"Failed to execute command for {unit}: {e}")
        return False
    return False
```

## Adding New Features

### 1. Creating New Unit Controllers

When adding support for a new unit type:

```python
# 1. Create new unit controller class
class VoidRay(CombatFlyer):
    """Void Ray unit controller with prismatic alignment micro"""
    
    def __init__(self, unit: Unit, bot: BotAI):
        super().__init__(unit, bot)
        self.beam_target: Optional[Unit] = None
        self.charge_level = 0
    
    def execute_micro(self) -> None:
        """Execute void ray specific micro"""
        if self.should_charge_beam():
            self.maintain_beam_target()
        else:
            self.find_new_target()

# 2. Register in unit factory
def create_combat_unit(unit: Unit, bot: BotAI) -> CombatUnit:
    match unit.type_id:
        case UnitTypeId.STALKER:
            return Stalker(unit, bot)
        case UnitTypeId.VOIDRAY:  # Add new case
            return VoidRay(unit, bot)
        case _:
            return CombatUnit(unit, bot)

# 3. Add unit tests
def test_void_ray_beam_targeting():
    void_ray = VoidRay(mock_void_ray_unit, mock_bot)
    target = mock_enemy_unit
    
    void_ray.set_beam_target(target)
    assert void_ray.beam_target == target
    assert void_ray.should_maintain_beam()
```

### 2. Implementing New Strategies

Add new strategic behaviors:

```python
# 1. Define strategy enum
class StrategyType(Enum):
    BLINK_STALKER_ALL_IN = "blink_stalker_all_in"
    PHOENIX_HARASSMENT = "phoenix_harassment"
    CARRIER_TRANSITION = "carrier_transition"  # New strategy

# 2. Implement strategy class
class CarrierTransition(Strategy):
    """Strategy for transitioning to carrier-based army"""
    
    def __init__(self, bot: BotAI):
        super().__init__(bot)
        self.transition_timing = 8 * 60  # 8 minutes
        
    def execute(self) -> None:
        if self.bot.time > self.transition_timing:
            self.build_fleet_beacon()
            self.transition_army_composition()

# 3. Register strategy
def select_strategy(bot: BotAI, enemy_race: Race) -> Strategy:
    if enemy_race == Race.Protoss and bot.time > 600:
        return CarrierTransition(bot)  # Use new strategy
    # ... other strategy selection logic
```

### 3. Adding Benchmark Scenarios

Create new performance tests:

```python
# 1. Define scenario in config
{
    "name": "void_ray_vs_corruptor",
    "friendly_units": {"voidray": 6},
    "enemy_units": {"corruptor": 8},
    "repetitions": 15,
    "victory_conditions": ["units_alive", "damage_ratio"]
}

# 2. Implement scenario logic
class VoidRayScenario(Scenario):
    """Test void ray micro against air units"""
    
    def setup_units(self):
        """Set up initial unit positions"""
        # Position void rays in defensive formation
        # Position enemy corruptors for attack
        
    def check_victory_condition(self) -> bool:
        """Check if test completed successfully"""
        return self.friendly_units_alive() > 0
```

## Debugging and Profiling

### Debug Mode Features

Enable comprehensive debugging:

```python
bot = HarstemsAunt(debug=True)
```

This enables:
- Visual unit information overlay
- Army group status display
- Build order progress tracking
- Performance timing information
- Decision-making logic logging

### Profiling Performance

Profile bot performance:

```python
import cProfile
import pstats

def profile_bot_execution():
    """Profile bot execution for performance analysis"""
    profiler = cProfile.Profile()
    
    profiler.enable()
    # Run bot for specified duration
    run_test_game()
    profiler.disable()
    
    # Analyze results
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
```

### Memory Profiling

Monitor memory usage:

```python
import tracemalloc
import psutil

def monitor_memory():
    """Monitor memory usage during bot execution"""
    tracemalloc.start()
    
    # Run bot
    bot = HarstemsAunt()
    # ... execute bot logic
    
    # Get memory statistics
    current, peak = tracemalloc.get_traced_memory()
    process = psutil.Process()
    memory_info = process.memory_info()
    
    print(f"Traced memory: {current / 1024 / 1024:.1f} MB")
    print(f"Peak memory: {peak / 1024 / 1024:.1f} MB") 
    print(f"RSS memory: {memory_info.rss / 1024 / 1024:.1f} MB")
```

## Testing Guidelines

### Unit Test Structure

Follow this pattern for unit tests:

```python
import pytest
from unittest.mock import Mock, MagicMock
from bot.HarstemsAunt.stalker import Stalker

class TestStalker:
    """Test cases for Stalker unit controller"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_bot = Mock()
        self.mock_unit = Mock()
        self.mock_unit.type_id = UnitTypeId.STALKER
        self.stalker = Stalker(self.mock_unit, self.mock_bot)
    
    def test_blink_decision_when_low_health(self):
        """Test blink usage when stalker has low health"""
        # Arrange
        self.mock_unit.health_percentage = 0.2
        self.mock_unit.energy = 100
        
        # Act
        should_blink = self.stalker.should_use_blink()
        
        # Assert
        assert should_blink is True
    
    def test_blink_decision_when_no_energy(self):
        """Test blink decision when stalker has no energy"""
        # Arrange
        self.mock_unit.health_percentage = 0.2
        self.mock_unit.energy = 50  # Below blink cost
        
        # Act
        should_blink = self.stalker.should_use_blink()
        
        # Assert
        assert should_blink is False
```

### Integration Test Structure

Test component interactions:

```python
def test_army_group_stalker_coordination():
    """Test that army groups properly coordinate stalker units"""
    # Create real bot instance with test configuration
    bot = create_test_bot()
    
    # Create army group with stalkers
    stalkers = create_test_stalkers(5)
    army_group = ArmyGroup(bot, stalkers)
    
    # Create enemy force
    enemy_units = create_test_enemies()
    
    # Execute coordination
    army_group.engage_enemies(enemy_units)
    
    # Verify coordination behavior
    assert army_group.is_properly_formed()
    assert all(stalker.has_valid_target() for stalker in stalkers)
```

## Performance Optimization

### Algorithmic Optimization

Optimize critical algorithms:

```python
# Before: O(n²) nearest neighbor search
def find_nearest_enemy_slow(unit: Unit, enemies: Units) -> Unit:
    min_distance = float('inf')
    nearest = None
    for enemy in enemies:
        for friendly in self.bot.units:
            distance = unit.distance_to(enemy)
            if distance < min_distance:
                min_distance = distance
                nearest = enemy
    return nearest

# After: O(n log n) with spatial indexing
def find_nearest_enemy_fast(unit: Unit, enemies: Units) -> Unit:
    return enemies.closest_to(unit)
```

### Memory Optimization

Reduce memory usage:

```python
# Use __slots__ for frequently created objects
class UnitMarker:
    __slots__ = ['unit_tag', 'position', 'timestamp', 'marker_type']
    
    def __init__(self, unit_tag: int, position: Point2):
        self.unit_tag = unit_tag
        self.position = position
        self.timestamp = time.time()

# Cache expensive calculations
@lru_cache(maxsize=128)
def calculate_path_cost(start: Point2, end: Point2) -> float:
    """Cache expensive pathfinding calculations"""
    return expensive_pathfinding_calculation(start, end)
```

### Profile-Guided Optimization

Use profiling data to optimize:

1. **Identify Bottlenecks**: Use profiling to find slow functions
2. **Optimize Hot Paths**: Focus on most frequently called code
3. **Measure Impact**: Verify optimizations improve performance
4. **Regression Testing**: Ensure optimizations don't break functionality

## Contributing Guidelines

### Pull Request Process

1. **Fork Repository** and create feature branch
2. **Write Tests** for new functionality
3. **Implement Changes** following code standards
4. **Run Test Suite** to ensure no regressions
5. **Update Documentation** as needed
6. **Submit Pull Request** with clear description

### Code Review Checklist

Before submitting code for review:

- [ ] All tests pass
- [ ] Code follows style guidelines  
- [ ] Documentation is updated
- [ ] Performance impact assessed
- [ ] Error handling implemented
- [ ] Type hints provided
- [ ] Logging added where appropriate

### Commit Message Format

Use conventional commit messages:

```bash
feat: add void ray micro-management system
fix: resolve stalker blink energy calculation bug  
docs: update API documentation for army groups
test: add integration tests for macro system
perf: optimize pathfinding algorithm performance
```

## Common Development Tasks

### Adding New Dependencies

1. **Add to requirements.txt**:
   ```text
   new-package==1.2.3
   ```

2. **Update setup.py**:
   ```python
   install_requires=[
       'BurnySC2',
       'numpy',
       'new-package>=1.2.0'
   ]
   ```

3. **Test Installation**:
   ```bash
   pip install -e .
   python -c "import new_package; print('Success')"
   ```

### Debugging Common Issues

#### Bot Crashes
```python
# Add comprehensive error handling
try:
    await self.execute_bot_logic()
except Exception as e:
    self.logger.error(f"Bot logic error: {e}")
    self.logger.error(f"Traceback: {traceback.format_exc()}")
    # Attempt graceful recovery
    self.reset_to_safe_state()
```

#### Performance Issues  
```python
# Add timing instrumentation
import time

def timed_execution(func):
    """Decorator to measure execution time"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        if execution_time > 0.016:  # Longer than one game tick
            logger.warning(f"{func.__name__} took {execution_time:.3f}s")
        return result
    return wrapper
```

This development guide provides the foundation for contributing effectively to the HarstemsAunt project. Remember to maintain code quality, comprehensive testing, and clear documentation in all contributions.
