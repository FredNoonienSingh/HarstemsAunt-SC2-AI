# Configuration Guide

The HarstemsAunt bot uses a flexible configuration system that allows for extensive customization of bot behavior, performance tuning, and debugging options.

## Configuration Architecture

### Configuration Hierarchy

The bot supports multiple levels of configuration:

1. **Default Configuration**: Built-in default values
2. **Global Configuration**: Bot-wide settings
3. **Component Configuration**: Module-specific settings  
4. **Runtime Configuration**: Dynamic adjustments during gameplay
5. **Environment Variables**: System-level overrides

### Configuration Format

All configuration files use JSON format for human readability and easy parsing:

```json
{
    "bot_settings": {
        "name": "HarstemsAunt",
        "version": "1.1_dev",
        "debug": false
    },
    "performance": {
        "max_units_tracked": 200,
        "pathfinding_resolution": 1.0
    }
}
```

## Main Configuration Files

### Bot Configuration (`bot/configs/debug_config.json`)

Primary bot configuration file:

```json
{
    "debug": {
        "enabled": false,
        "show_unit_info": true,
        "show_army_groups": true,
        "show_build_order": true,
        "font_size": 18,
        "unit_label_font_size": 12
    },
    "performance": {
        "benchmark_enabled": false,
        "verbose_logging": false,
        "save_match_data": true
    },
    "gameplay": {
        "race": "Protoss",
        "difficulty_scaling": 1.0,
        "aggressive_expansion": false
    }
}
```

### Benchmark Configuration (`benchmarks/configs/config.json`)

Benchmarking system configuration:

```json
{
    "benchmark_settings": {
        "endless": false,
        "save_data": true,
        "verbose": true,
        "blind": false
    },
    "scenarios": [
        {
            "name": "stalker_micro_test",
            "enabled": true,
            "repetitions": 10,
            "friendly_units": {"stalker": 5},
            "enemy_units": {"stalker": 5}
        }
    ],
    "data_output": {
        "format": "csv",
        "include_detailed_stats": true,
        "auto_analysis": true
    }
}
```

### Map-Specific Configuration

Different settings can be applied per map:

```json
{
    "map_configs": {
        "Acropolis AIE": {
            "expansion_strategy": "defensive",
            "early_army_positioning": "natural_ramp"
        },
        "Automaton AIE": {
            "expansion_strategy": "aggressive", 
            "early_scouting": "extended"
        }
    }
}
```

## Component Configuration

### Macro System Configuration

```json
{
    "macro": {
        "workers_per_base": 22,
        "supply_buffer": 8,
        "max_supply_blocks": 2,
        "probe_production": {
            "early_game_ratio": 0.6,
            "mid_game_ratio": 0.4,
            "late_game_ratio": 0.2
        },
        "build_order": {
            "adaptive_timing": true,
            "economic_priority": 0.7,
            "military_priority": 0.3
        }
    }
}
```

**Configuration Options:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `workers_per_base` | int | 22 | Target workers per resource base |
| `supply_buffer` | int | 8 | Supply cushion before building pylons |
| `adaptive_timing` | bool | true | Adjust build timing based on game state |

### Army Management Configuration

```json
{
    "army_management": {
        "group_settings": {
            "max_group_size": 30,
            "min_group_size": 5,
            "formation_spacing": 2.0,
            "engagement_range": 15.0
        },
        "unit_composition": {
            "stalker_ratio": 0.6,
            "zealot_ratio": 0.3,
            "immortal_ratio": 0.1
        },
        "combat_behavior": {
            "aggression_level": 0.7,
            "retreat_threshold": 0.3,
            "kiting_enabled": true,
            "focus_fire": true
        }
    }
}
```

**Army Configuration Parameters:**

| Parameter | Range | Description |
|-----------|-------|-------------|
| `aggression_level` | 0.0-1.0 | How aggressively to engage enemies |
| `retreat_threshold` | 0.0-1.0 | Army strength ratio to trigger retreat |
| `formation_spacing` | 1.0-5.0 | Distance between units in formation |

### Unit-Specific Configuration

#### Stalker Configuration

```json
{
    "stalker": {
        "blink_settings": {
            "enabled": true,
            "health_threshold": 0.3,
            "energy_threshold": 75,
            "cooldown_awareness": true
        },
        "kiting": {
            "enabled": true,
            "range_buffer": 2.5,
            "retreat_distance": 4.0
        },
        "targeting": {
            "priority_air": true,
            "focus_weak_targets": false
        }
    }
}
```

#### Zealot Configuration

```json
{
    "zealot": {
        "charge_settings": {
            "enabled": true,
            "range_threshold": 8.0,
            "target_priority": "closest"
        },
        "engagement": {
            "flanking_enabled": true,
            "surround_attempts": true,
            "retreat_when_low": true
        }
    }
}
```

## Environment Variables

System-level configuration through environment variables:

### Core Environment Variables

```bash
# StarCraft II installation path
export SC2PATH="/Applications/StarCraft II"

# Bot data directory  
export HARSTEM_DATA_PATH="/path/to/data"

# Debug mode override
export HARSTEM_DEBUG=1

# Benchmark mode override
export HARSTEM_BENCHMARK=1

# Log level (DEBUG, INFO, WARNING, ERROR)
export HARSTEM_LOG_LEVEL="INFO"

# Performance profiling
export HARSTEM_PROFILE=1
```

### Advanced Environment Variables

```bash
# Custom configuration file path
export HARSTEM_CONFIG_PATH="/path/to/custom/config.json"

# Override specific settings
export HARSTEM_MAX_WORKERS=24
export HARSTEM_SUPPLY_BUFFER=10

# Testing overrides
export HARSTEM_TEST_MODE=1
export HARSTEM_DISABLE_CHAT=1
```

## Runtime Configuration

### Dynamic Configuration Updates

Some settings can be modified during gameplay:

```python
class HarstemsAunt(BotAI):
    def update_configuration(self, new_config: Dict):
        """Update configuration during runtime"""
        if 'aggression_level' in new_config:
            for army_group in self.army_groups:
                army_group.set_aggression(new_config['aggression_level'])
        
        if 'supply_buffer' in new_config:
            self.macro.set_supply_buffer(new_config['supply_buffer'])
```

### Adaptive Configuration

The bot can automatically adjust settings based on game conditions:

```python
def adapt_configuration_to_enemy(self, enemy_race: Race):
    """Adapt configuration based on enemy race"""
    if enemy_race == Race.Terran:
        self.config['unit_composition']['stalker_ratio'] = 0.8
        self.config['combat_behavior']['kiting_enabled'] = True
    
    elif enemy_race == Race.Zerg:
        self.config['unit_composition']['zealot_ratio'] = 0.5  
        self.config['macro']['early_expansion'] = True
```

## Configuration Validation

### Schema Validation

Configuration files are validated against JSON schemas:

```python
def validate_config(config: Dict) -> bool:
    """Validate configuration against schema"""
    schema = {
        "type": "object",
        "properties": {
            "macro": {
                "type": "object", 
                "properties": {
                    "workers_per_base": {"type": "integer", "minimum": 10, "maximum": 30}
                }
            }
        },
        "required": ["macro"]
    }
    
    return jsonschema.validate(config, schema)
```

### Runtime Checks

Configuration values are checked for validity:

```python
def validate_army_config(config: Dict):
    """Validate army configuration values"""
    assert 0.0 <= config['aggression_level'] <= 1.0
    assert config['max_group_size'] > config['min_group_size'] 
    assert sum(config['unit_composition'].values()) == 1.0
```

## Configuration Examples

### Development Configuration

Optimized for development and debugging:

```json
{
    "debug": {
        "enabled": true,
        "show_all_info": true,
        "verbose_logging": true
    },
    "performance": {
        "benchmark_enabled": true,
        "save_detailed_stats": true
    },
    "gameplay": {
        "slower_gameplay": true,
        "extended_analysis": true
    }
}
```

### Production Configuration

Optimized for competitive play:

```json
{
    "debug": {
        "enabled": false,
        "minimal_logging": true
    },
    "performance": {
        "max_performance": true,
        "reduced_calculations": false
    },
    "gameplay": {
        "aggressive_optimization": true,
        "risk_taking": 0.8
    }
}
```

### Testing Configuration

For automated testing and benchmarking:

```json
{
    "testing": {
        "deterministic_behavior": true,
        "fixed_random_seed": 12345,
        "accelerated_gameplay": true
    },
    "benchmark": {
        "comprehensive_metrics": true,
        "detailed_logging": true,
        "save_all_data": true
    }
}
```

## Configuration Management Best Practices

### Version Control

- Keep configuration files in version control
- Use separate configs for development/production/testing
- Document configuration changes in commit messages
- Tag configuration versions with bot releases

### Configuration Inheritance

```python
def load_configuration(base_config: str, override_config: str = None):
    """Load configuration with optional overrides"""
    config = load_json(base_config)
    
    if override_config and os.path.exists(override_config):
        overrides = load_json(override_config)
        config = deep_merge(config, overrides)
    
    return config
```

### Configuration Profiles

Support different configuration profiles:

```bash
# Development profile
python run_bot.py --config-profile=development

# Competition profile  
python run_bot.py --config-profile=competition

# Testing profile
python run_bot.py --config-profile=testing
```

### Security Considerations

- Don't commit sensitive information (API keys, passwords)
- Use environment variables for sensitive data
- Validate all external configuration input
- Set reasonable limits on all numeric parameters

This configuration system provides the flexibility needed to optimize bot performance across different scenarios while maintaining ease of use and reliability.
