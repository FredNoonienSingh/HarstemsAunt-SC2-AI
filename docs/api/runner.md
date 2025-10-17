# Bot Runner and Command Line Interface

The `run.py` script serves as the main entry point for running the HarstemsAunt bot with various configurations and modes.

## Overview

This script provides a comprehensive command-line interface for:
- Running local games against AI opponents
- Executing benchmarking suites  
- Ladder game integration for AI Arena
- Full benchmark testing for bot evaluation

## Usage

### Basic Usage

```bash
# Run with default settings
python bot/run.py

# Run in debug mode
python bot/run.py --debug

# Run with benchmarking enabled
python bot/run.py --benchmark --benchmark_message "Testing v1.1"
```

### Advanced Usage

```bash
# Run against specific opponent
python bot/run.py --race zerg --difficulty veryhard --map "Acropolis AIE"

# Run full benchmark suite
python bot/run.py --full_benchmark

# Run in real-time mode (warning: may cause issues)
python bot/run.py --realtime
```

## Command Line Arguments

### Benchmark Settings

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `--benchmark` | `-bench` | flag | False | Enable benchmarking mode |
| `--benchmark_message` | `-bm` | string | None | Custom message for benchmark data |
| `--benchmark_max_iterations` | `-bmax_iter` | int | None | Maximum benchmark iterations |
| `--full_benchmark` | `-fb` | flag | False | Run comprehensive benchmark suite |

### Debug Settings

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `--debug` | `-d` | flag | False | Enable debug mode |
| `--debug_config` | `-dc` | string | `bot/configs/debug_config.json` | Path to debug configuration |

### Bot Settings  

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `--race` | `-r` | string | `terran` | Enemy race (terran/zerg/protoss) |
| `--difficulty` | `-di` | string | `hard` | Enemy AI difficulty |
| `--ai_build` | `-aiB` | string | None | Enemy AI build strategy |
| `--map` | `-m` | string | Random | Map name to play on |
| `--realtime` | `-t` | flag | False | Enable real-time mode |
| `--sc2_version` | `-v` | string | `5.0.10` | StarCraft II client version |

## Core Functions

### Ladder Integration

```python
if "--LadderServer" in sys.argv:
    bot = Bot(Race.Protoss, HarstemsAunt())
    result, opponentid = run_ladder_game(bot)
```

**Purpose:** Handles AI Arena ladder integration
**Behavior:** Automatically detected when launched by ladder manager

### Full Benchmark Suite

```python
def run_full_benchmark(arguments: dict) -> None:
    """Execute comprehensive benchmark testing"""
```

**Test Categories:**
1. **AI Opponent Testing**: Tests against all races and difficulties
2. **Scenario Testing**: Runs predefined micro scenarios  
3. **Performance Analysis**: Measures bot performance metrics

**Benchmark Process:**
1. Tests against AI opponents of varying difficulties
2. Runs on multiple maps for terrain variety
3. Executes micro benchmarks for unit control testing
4. Saves results to CSV files for analysis

### Local Game Execution

The main execution path for local games:

```python
# Bot initialization
bot = Bot(Race.Protoss, HarstemsAunt(
    debug=args.debug,
    benchmark=args.benchmark
))

# Enemy selection
enemy_bot = Computer(enemy_race, enemy_strength)

# Map selection  
arena = maps.get(args.map or choice(MAP_LIST))

# Game execution
run_game(arena, [bot, enemy_bot], 
         realtime=args.realtime, 
         sc2_version=args.sc2_version)
```

## Configuration Integration

### Debug Configuration Loading

```python
debug_params: dict = Utils.read_json(args.debug_config)
```

Loads debug configuration from JSON file to customize:
- Visual debug output settings
- Logging verbosity levels  
- Performance monitoring options

### Dynamic Configuration

The runner supports runtime configuration through:
- Command line argument overrides
- Environment variable integration
- Configuration file selection

## Error Handling

### Map Loading

```python
if args.map:
    try:
        arena = maps.get(args.map)
    except Exception as e:
        logger.warning("Map can't be found... loading random map...")
        arena = maps.get(choice(MAP_LIST))
```

**Graceful Degradation:** Falls back to random map if specified map not found

### Real-time Mode Warning

```python
if args.realtime:
    logger.warning("running in realtime may lead to unexpected behavior and crashes")
```

**Safety Check:** Warns users about potential issues with real-time mode

## Usage Examples

### Development Testing

```bash
# Quick test game
python bot/run.py -d -r zerg -di easy -m "Simple64"

# Performance testing
python bot/run.py -bench -bm "stalker micro improvements" -r protoss -di veryhard
```

### Benchmark Execution

```bash
# Run specific benchmark scenarios
python bot/run.py --benchmark --benchmark_message "Version 1.1 testing"

# Full evaluation suite  
python bot/run.py --full_benchmark
```

### Production Testing

```bash
# Test against challenging opponents
python bot/run.py -r random -di cheatinsane

# Multi-game testing
for i in {1..10}; do
    python bot/run.py -r zerg -di veryhard -m random
done
```

## Integration Points

### AI Arena Ladder

The script automatically detects ladder environment:
- Responds to `--LadderServer` argument
- Uses standard ladder game interface
- Reports results back to ladder system

### Benchmarking System

Seamlessly integrates with benchmark framework:
- Passes configuration to benchmark system
- Enables detailed performance tracking  
- Saves results for analysis

### Logging Integration  

Uses the bot's logging system:
- Consistent log formatting
- Configurable verbosity levels
- Performance timing information

## Environment Variables

The runner respects environment variables:

```bash
export SC2PATH="/custom/starcraft2/path"
export HARSTEM_DEBUG=1
export HARSTEM_LOG_LEVEL="DEBUG"
```

## Best Practices

### Development Workflow

```bash
# 1. Quick functionality test
python bot/run.py -d

# 2. Performance verification  
python bot/run.py -bench

# 3. Stress testing
python bot/run.py -fb
```

### Debugging Process

```bash
# Enable all debug features
python bot/run.py -d -dc custom_debug_config.json -t

# Test specific scenarios
python bot/run.py -d -r terran -di hard -m "Acropolis AIE"
```

This runner script provides a flexible and comprehensive interface for all bot testing and deployment needs, from quick development tests to comprehensive evaluation suites.
