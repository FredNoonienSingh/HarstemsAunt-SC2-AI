# Installation and Setup Guide

## Prerequisites

Before setting up HarstemsAunt, ensure you have the following installed:

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.12.5 or newer
- **StarCraft II**: Full installation required
- **Memory**: 8GB RAM minimum (16GB recommended)
- **Storage**: 2GB free space for bot and dependencies

### StarCraft II Setup

1. **Install StarCraft II**:
   - Download from [Battle.net](https://starcraft2.com/)
   - Install the full game (not just the starter edition)
   - Ensure the game runs properly

2. **Enable Developer Mode**:
   - Start StarCraft II
   - Go to Options → Gameplay
   - Enable "Developer Mode" or "Allow External Applications"

## Installation Methods

### Method 1: Clone from Repository (Recommended)

```bash
# Clone the repository
git clone https://github.com/FredNoonienSingh/HarstemsAunt-SC2-AI.git
cd HarstemsAunt-SC2-AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install bot in development mode
pip install -e .
```

### Method 2: Direct Installation

```bash
# Install directly from PyPI (if published)
pip install HarstemsAunt

# Or install from source
pip install git+https://github.com/FredNoonienSingh/HarstemsAunt-SC2-AI.git
```

## Dependencies

The bot requires the following Python packages:

### Core Dependencies

```text
burnysc2==7.0.1          # StarCraft II API framework
numpy==2.0.2             # Numerical computations  
loguru==0.6.0            # Advanced logging
pillow==11.0.0           # Image processing
scipy==1.14.1            # Scientific computing
```

### Optional Dependencies

```text
jupyter                  # For development notebooks
pytest                   # For running tests
matplotlib               # For visualizations
pandas                   # For data analysis
```

## Configuration

### Bot Configuration

Create or modify configuration files in the appropriate directories:

#### Main Bot Config (`bot/configs/debug_config.json`)

```json
{
    "debug": false,
    "benchmark": false,
    "verbose_logging": true,
    "unit_composition": {
        "stalker_ratio": 0.6,
        "zealot_ratio": 0.3,
        "immortal_ratio": 0.1
    },
    "macro_settings": {
        "max_workers_per_base": 22,
        "supply_buffer": 8,
        "expansion_timing": 300
    }
}
```

#### Benchmark Config (`benchmarks/configs/config.json`)

```json
{
    "endless": false,
    "save_data": true,
    "verbose": true,
    "blind": false,
    "scenarios": [
        "stalker_vs_stalker",
        "zealot_charge_timing", 
        "immortal_positioning"
    ]
}
```

### Environment Variables

Set the following environment variables if needed:

```bash
# StarCraft II installation path (if non-standard)
export SC2PATH="/path/to/starcraft2"

# Bot data directory
export HARSTEM_DATA_PATH="/path/to/data"

# Enable debug mode
export HARSTEM_DEBUG=1
```

## Running the Bot

### Local Testing

1. **Single Game Test**:

```python
# run_bot.py
from bot.HarstemsAunt.main import HarstemsAunt
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

run_game(
    maps.get("Acropolis AIE"),
    [
        Bot(Race.Protoss, HarstemsAunt()),
        Computer(Race.Zerg, Difficulty.VeryHard)
    ],
    realtime=False
)
```

2. **Debug Mode**:

```python
bot = HarstemsAunt(debug=True, benchmark=False)
```

3. **Benchmark Mode**:

```python  
bot = HarstemsAunt(debug=False, benchmark=True, benchmark_message="Testing v1.1")
```

### AI Arena Integration

For deployment to AI Arena:

1. **Package Structure**:
   ```text
   HarstemsAunt/
   ├── bot/
   ├── run.py
   └── requirements.txt
   ```

2. **Run Script** (`run.py`):
   ```python
   from bot.HarstemsAunt.main import HarstemsAunt
   from sc2.player import Bot
   
   class CompetitiveBot:
       def __init__(self):
           self.bot = Bot(Race.Protoss, HarstemsAunt())
   ```

## Troubleshooting

### Common Issues

#### 1. StarCraft II Not Found

**Problem**: `SC2 not found` error

**Solutions**:
- Verify StarCraft II installation path
- Set `SC2PATH` environment variable
- Check that StarCraft II runs independently

#### 2. Python Version Conflicts

**Problem**: Compatibility errors with Python versions

**Solutions**:
- Use Python 3.12.5 or newer
- Create fresh virtual environment
- Update pip and setuptools: `pip install --upgrade pip setuptools`

#### 3. Import Errors

**Problem**: `ModuleNotFoundError` for bot components

**Solutions**:
- Install in development mode: `pip install -e .`
- Check virtual environment activation
- Verify PYTHONPATH includes bot directory

#### 4. Performance Issues

**Problem**: Bot runs slowly or times out

**Solutions**:
- Disable debug mode in production
- Check system resource usage
- Reduce benchmark verbosity
- Update graphics drivers

#### 5. Map Loading Errors

**Problem**: Cannot load maps or missing map files

**Solutions**:
- Download ladder maps from Blizzard
- Place maps in StarCraft II Maps folder
- Verify map file integrity

### Debug Tools

#### Enable Verbose Logging

```python
import logging
from loguru import logger

logger.add("bot_debug.log", level="DEBUG", rotation="10 MB")
```

#### Performance Profiling

```python
import cProfile
import pstats

# Profile bot execution
cProfile.run('run_game(...)', 'bot_profile.prof')
stats = pstats.Stats('bot_profile.prof')
stats.sort_stats('cumulative').print_stats(20)
```

#### Memory Monitoring

```python
import psutil
import tracemalloc

# Monitor memory usage
tracemalloc.start()
# ... run bot ...
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
```

## Development Setup

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/FredNoonienSingh/HarstemsAunt-SC2-AI.git
cd HarstemsAunt-SC2-AI

# Create development environment
python -m venv dev_env
source dev_env/bin/activate  # or dev_env\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### IDE Configuration

#### VS Code Setup

Recommended `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"]
}
```

#### PyCharm Setup

1. Set Project Interpreter to virtual environment
2. Enable pylint and type checking
3. Configure run configurations for bot testing

## Testing the Installation

### Verification Script

Create and run this verification script:

```python
# verify_installation.py
import sys
print(f"Python version: {sys.version}")

try:
    import sc2
    print(f"BurnySC2 version: {sc2.__version__}")
except ImportError:
    print("ERROR: BurnySC2 not installed")

try:
    from bot.HarstemsAunt.main import HarstemsAunt
    print("✓ HarstemsAunt bot imported successfully")
except ImportError as e:
    print(f"ERROR: Cannot import HarstemsAunt: {e}")

try:
    import numpy, scipy, pillow
    print("✓ All required dependencies available")
except ImportError as e:
    print(f"ERROR: Missing dependencies: {e}")

print("Installation verification complete!")
```

### Quick Test Game

```python
# test_game.py
from bot.HarstemsAunt.main import HarstemsAunt
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

# Quick test game
result = run_game(
    maps.get("Simple64"),
    [
        Bot(Race.Protoss, HarstemsAunt(debug=True)),
        Computer(Race.Zerg, Difficulty.Easy)
    ],
    realtime=False,
    step_time_limit=2.0,
    game_time_limit=300  # 5 minutes
)

print(f"Game result: {result}")
```

If this test runs successfully, your installation is working correctly!
