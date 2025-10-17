# Benchmarking System

The HarstemsAunt bot includes a comprehensive benchmarking system designed to measure and analyze combat performance, strategic decision-making, and overall bot effectiveness.

## Overview

The benchmarking framework allows for:

- **Unit Micro Performance**: Measuring individual unit control effectiveness
- **Combat Scenario Testing**: Testing specific combat situations repeatedly  
- **Strategy Evaluation**: Analyzing the effectiveness of different strategies
- **Regression Testing**: Ensuring new changes don't degrade performance
- **Competitive Analysis**: Comparing performance against different opponents

## Core Components

### Benchmark Class

The main `Benchmark` class orchestrates the benchmarking process:

```python
class Benchmark:
    def __init__(self, bot: BotAI, path_to_config: str = "benchmarks/configs/config.json"):
        self.bot = bot
        self.path_to_config = path_to_config
        self.current_index = 0
        self.scenario_running = False
        self.scenarios = []
```

**Key Features:**
- Configuration-driven test scenarios
- Automatic scenario progression
- Data collection and analysis
- Performance metrics tracking

### Scenario System

Test scenarios define specific situations to benchmark:

```python
class Scenario:
    def __init__(self, name: str, friendly_units: Dict, enemy_units: Dict):
        self.name = name
        self.friendly_units = friendly_units
        self.enemy_units = enemy_units
        self.victory_conditions = []
        self.duration_limit = 300  # 5 minutes
```

**Scenario Types:**
- **Unit vs Unit**: Direct combat comparisons (e.g., Stalker vs Marine)
- **Micro Challenges**: Complex micro situations (e.g., Phoenix vs Mutalisk)
- **Army Compositions**: Large-scale battle testing
- **Economic Challenges**: Resource management optimization

### Result Analysis

The `Result` class captures and analyzes benchmark outcomes:

```python
class Result:
    def __init__(self, scenario_name: str):
        self.scenario_name = scenario_name
        self.start_time = 0
        self.end_time = 0
        self.units_lost = {}
        self.units_killed = {}
        self.damage_dealt = 0
        self.damage_taken = 0
        self.victory = False
```

## Configuration

### Benchmark Configuration

Benchmarks are configured through JSON files:

```json
{
    "endless": false,
    "save_data": true,
    "verbose": true,
    "blind": false,
    "scenarios": [
        {
            "name": "stalker_vs_stalker",
            "friendly_units": {"stalker": 5},
            "enemy_units": {"stalker": 5},
            "repetitions": 10
        },
        {
            "name": "phoenix_vs_mutalisk", 
            "friendly_units": {"phoenix": 8},
            "enemy_units": {"mutalisk": 8},
            "repetitions": 5
        }
    ]
}
```

**Configuration Options:**
- **endless**: Run scenarios indefinitely for continuous testing
- **save_data**: Save detailed results to CSV files
- **verbose**: Enable detailed logging during benchmarks
- **blind**: Hide enemy units from bot vision (fog of war testing)

### Predefined Scenarios

#### Combat Scenarios

**Stalker Micro**
- Tests blink usage timing and effectiveness
- Evaluates kiting behavior against different unit types
- Measures micro efficiency in various terrain conditions

**Phoenix Control**
- Air superiority combat scenarios
- Graviton beam usage optimization
- Multi-target engagement coordination

**Immortal Positioning**
- Hardened shield optimization
- Range and positioning effectiveness
- Focus fire coordination

#### Economic Scenarios

**Worker Efficiency**
- Speedmining implementation testing
- Resource gathering optimization
- Worker allocation strategies

**Build Order Execution**
- Build timing accuracy measurement
- Resource efficiency analysis
- Supply management effectiveness

## Usage

### Basic Usage

```python
from bot.HarstemsAunt.main import HarstemsAunt
from benchmarks.benchmark import Benchmark

# Create bot with benchmarking enabled
bot = HarstemsAunt(benchmark=True, benchmark_message="v1.1 stalker micro test")

# Benchmark will automatically run during gameplay
# Results saved to data/benchmark_HarstemsAunt_v1.1_dev.csv
```

### Custom Benchmarking

```python
# Create custom benchmark configuration
custom_config = {
    "scenarios": [
        {
            "name": "custom_test",
            "friendly_units": {"stalker": 3, "zealot": 2},
            "enemy_units": {"marine": 8},
            "repetitions": 20
        }
    ]
}

# Save to config file and run
with open("benchmarks/configs/custom.json", "w") as f:
    json.dump(custom_config, f)

bot = HarstemsAunt(benchmark=True)
benchmark = Benchmark(bot, "benchmarks/configs/custom.json")
```

### Analyzing Results

```python
import pandas as pd

# Load benchmark results
results = pd.read_csv("data/benchmark_HarstemsAunt_v1.1_dev.csv")

# Analyze stalker performance
stalker_results = results[results['scenario'] == 'stalker_vs_stalker']
win_rate = stalker_results['victory'].mean()
avg_efficiency = stalker_results['damage_dealt'] / stalker_results['damage_taken']

print(f"Stalker win rate: {win_rate:.2%}")
print(f"Average damage efficiency: {avg_efficiency:.2f}")
```

## Metrics Collected

### Combat Metrics

**Unit Performance**
- Kill/death ratios by unit type
- Damage dealt vs damage taken
- Ability usage effectiveness (blink, charge, etc.)
- Micro-management response times

**Army Performance**  
- Formation maintenance during combat
- Target prioritization accuracy
- Retreat timing effectiveness
- Coordination between unit types

### Economic Metrics

**Resource Management**
- Resource collection rates
- Spending efficiency (resources banked vs spent)
- Supply block frequency and duration
- Build order execution accuracy

**Strategic Metrics**
- Map control percentages over time
- Expansion timing optimization
- Technology progression speed
- Adaptation to enemy strategies

### Behavioral Metrics

**Decision Making**
- Response time to enemy actions
- Strategic decision accuracy
- Risk assessment effectiveness
- Learning and adaptation rates

## Data Storage

### CSV Format

Results are automatically saved in CSV format for easy analysis:

```csv
timestamp,scenario,bot_version,duration,victory,units_lost,units_killed,damage_dealt,damage_taken,efficiency_score
2024-01-15_14:30:25,stalker_vs_stalker,v1.1_dev,45.2,True,2,4,1250,800,1.56
2024-01-15_14:31:10,stalker_vs_stalker,v1.1_dev,52.1,False,3,3,980,1100,0.89
```

### Data Fields

| Field | Description | Type |
|-------|-------------|------|
| `timestamp` | When the test was run | string |
| `scenario` | Scenario name | string |
| `bot_version` | Bot version tested | string |
| `duration` | Test duration in seconds | float |
| `victory` | Whether bot won the scenario | boolean |
| `units_lost` | Number of units lost | integer |
| `units_killed` | Number of enemy units killed | integer |
| `damage_dealt` | Total damage dealt | integer |
| `damage_taken` | Total damage received | integer |
| `efficiency_score` | Calculated efficiency metric | float |

## Performance Analysis

### Statistical Analysis

The benchmarking system provides statistical analysis tools:

```python
from benchmarks.result import Result

# Analyze scenario performance
results = Result.load_from_csv("data/benchmark_results.csv")
scenario_stats = results.analyze_scenario("stalker_vs_stalker")

print(f"Mean win rate: {scenario_stats.win_rate:.2%}")
print(f"Standard deviation: {scenario_stats.win_rate_std:.3f}")
print(f"95% Confidence interval: {scenario_stats.confidence_interval_95}")
```

### Trend Analysis

Track performance changes over time:

```python
# Compare versions
v1_0_results = results.filter_by_version("v1.0")
v1_1_results = results.filter_by_version("v1.1")

improvement = v1_1_results.win_rate - v1_0_results.win_rate
print(f"Performance improvement: {improvement:.2%}")
```

### Regression Detection

Automatically detect performance regressions:

```python
def detect_regression(baseline_results, current_results, threshold=0.05):
    """Detect if current results show significant regression"""
    baseline_winrate = baseline_results.win_rate
    current_winrate = current_results.win_rate
    
    regression = baseline_winrate - current_winrate
    return regression > threshold, regression
```

## Integration with Development

### Continuous Integration

Integrate benchmarking with CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Run Benchmarks
  run: |
    python -m pytest benchmarks/test_performance.py
    python analyze_regression.py --baseline=v1.0 --current=HEAD
```

### Development Workflow

1. **Before Changes**: Run baseline benchmarks
2. **Development**: Make code changes
3. **Testing**: Run targeted benchmarks for affected areas
4. **Analysis**: Compare results with baseline
5. **Optimization**: Iterate based on benchmark feedback
6. **Validation**: Final comprehensive benchmark suite

### Automated Alerts

Set up alerts for significant performance changes:

```python
def check_performance_alert(results, baseline, alert_threshold=0.10):
    """Send alert if performance drops significantly"""
    if results.win_rate < baseline.win_rate - alert_threshold:
        send_alert(f"Performance regression detected: {results.win_rate:.2%} vs {baseline.win_rate:.2%}")
```

## Best Practices

### Benchmark Design

- **Isolate Variables**: Test one aspect at a time
- **Sufficient Repetitions**: Run enough tests for statistical significance
- **Controlled Conditions**: Ensure consistent test environments
- **Realistic Scenarios**: Use scenarios that mirror actual gameplay

### Data Collection

- **Comprehensive Metrics**: Collect multiple performance indicators
- **Consistent Format**: Standardize data storage and analysis
- **Historical Tracking**: Maintain long-term performance history
- **Automated Analysis**: Use scripts for consistent analysis

### Performance Optimization

- **Profile Bottlenecks**: Identify performance bottlenecks through benchmarks
- **Iterative Improvement**: Make small, measurable improvements
- **Regression Prevention**: Catch performance regressions early
- **Balance Trade-offs**: Consider accuracy vs performance trade-offs

This benchmarking system provides a comprehensive framework for measuring and improving bot performance across all aspects of StarCraft II gameplay.
