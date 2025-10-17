# Target Allocation System

The target allocation system provides intelligent target selection and assignment for combat units, optimizing focus fire and combat effectiveness through mathematical analysis.

## Overview

The targeting system uses advanced algorithms to:

- **Calculate Target Priority**: Uses Target Allocation Score (TAS) for optimal target selection
- **Coordinate Focus Fire**: Ensures multiple units attack high-value targets
- **Minimize Overkill**: Prevents wasting firepower on already-dead targets
- **Adapt to Composition**: Adjusts targeting based on army composition

## Core Algorithm: Target Allocation Score (TAS)

### Mathematical Foundation

The TAS algorithm evaluates enemy units using a mathematical formula that considers:

```python
def target_allocation_score(bot: BotAI, unit: Unit) -> float:
    """Calculate Target Allocation Score for enemy unit"""
    
    # Army composition analysis
    fraction_ground = len(bot.units.filter(lambda u: not u.is_flying)) / len(bot.units)
    fraction_flying = len(bot.units.filter(lambda u: u.is_flying)) / len(bot.units)
    
    # DPS threat calculation
    dps_score = np.sqrt(pi * (
        (unit.air_range**2) * (fraction_flying * unit.air_dps) +
        (unit.ground_range**2) * (fraction_ground * unit.ground_dps)
    )) / 10
    
    # Health-based urgency
    health_score = 3/2 - Utils.sigmoid(unit.health / 10)
    
    # Final TAS calculation  
    return Utils.sigmoid(dps_score * health_score) * -1
```

### TAS Components

**DPS Threat Assessment**
- Considers unit's damage potential against current army composition
- Weights air and ground DPS based on friendly unit distribution
- Uses range-weighted calculation for positional advantage

**Health Urgency Factor**
- Prioritizes damaged units (easier to eliminate)
- Uses sigmoid function for smooth priority transitions
- Prevents overkill on near-dead targets

**Composition Adaptation**
- Dynamically adjusts based on friendly army makeup
- Emphasizes threats most relevant to current forces
- Accounts for range and positioning factors

## TargetAllocator Class

### Class Structure

```python
class TargetAllocator:
    """Coordinates target assignment for army groups"""
    
    def __init__(self, bot: BotAI, units: List[CombatUnit], targets: Set):
        self.bot = bot
        self.units = units
        self.targets = targets
        self.assignments = {}
        self.target_health_tracking = {}
```

### Core Methods

#### Target Assignment

```python
def assign_targets(self) -> Dict[Unit, Unit]:
    """Assign optimal targets to combat units"""
    assignments = {}
    
    # Calculate TAS for all enemies
    target_scores = {
        enemy: target_allocation_score(self.bot, enemy) 
        for enemy in self.targets
    }
    
    # Sort targets by priority (lowest TAS = highest priority)
    prioritized_targets = sorted(target_scores.items(), key=lambda x: x[1])
    
    # Assign targets to units
    for unit in self.units:
        best_target = self.find_optimal_target(unit, prioritized_targets)
        if best_target:
            assignments[unit] = best_target
            
    return assignments
```

#### Optimal Target Selection

```python
def find_optimal_target(self, unit: CombatUnit, prioritized_targets: List) -> Unit:
    """Find best target for specific unit"""
    
    for target, score in prioritized_targets:
        # Check if unit can attack target
        if not self.can_attack(unit, target):
            continue
            
        # Check if target needs more firepower
        if self.get_assigned_damage(target) >= target.health:
            continue  # Target already has enough firepower assigned
            
        # Check range and positioning
        if unit.distance_to(target) <= unit.effective_range:
            return target
            
    return None
```

## Focus Fire Coordination

### Damage Tracking

```python
def track_assigned_damage(self, target: Unit, attacking_unit: Unit):
    """Track damage assigned to prevent overkill"""
    
    if target not in self.assigned_damage:
        self.assigned_damage[target] = 0
        
    # Add expected damage from this unit
    expected_damage = self.calculate_expected_damage(attacking_unit, target)
    self.assigned_damage[target] += expected_damage
```

### Overkill Prevention

```python
def prevent_overkill(self, target: Unit) -> bool:
    """Check if target already has sufficient damage assigned"""
    
    current_health = target.health + target.shield
    assigned_damage = self.assigned_damage.get(target, 0)
    
    # Include damage from projectiles in flight
    incoming_damage = self.calculate_incoming_damage(target)
    
    total_incoming = assigned_damage + incoming_damage
    
    return total_incoming >= current_health
```

## Advanced Targeting Strategies

### Composition-Based Targeting

```python
def get_composition_priority(self, enemy: Unit) -> float:
    """Adjust priority based on army composition"""
    
    priority_modifier = 0.0
    
    # Anti-air priority
    if self.has_air_units() and enemy.can_attack_air:
        priority_modifier -= 2.0  # Higher priority (lower score)
    
    # Anti-ground priority  
    if self.has_ground_units() and enemy.can_attack_ground:
        priority_modifier -= 1.5
        
    # Detector priority
    if enemy.is_detector and self.has_cloaked_units():
        priority_modifier -= 3.0  # Very high priority
        
    return priority_modifier
```

### Range-Based Targeting

```python
def calculate_range_priority(self, attacker: Unit, target: Unit) -> float:
    """Adjust priority based on range considerations"""
    
    distance = attacker.distance_to(target)
    effective_range = attacker.effective_range
    
    if distance <= effective_range * 0.8:
        return -0.5  # Close targets get priority boost
    elif distance <= effective_range:
        return 0.0   # Normal priority
    else:
        return 1.0   # Distant targets get penalty
```

## Integration with Combat Units

### Unit-Level Integration

```python
class CombatUnit:
    def select_target(self) -> Unit:
        """Select target using target allocator"""
        
        if hasattr(self.army_group, 'target_allocator'):
            # Use coordinated targeting
            assigned_target = self.army_group.target_allocator.get_assignment(self)
            if assigned_target:
                return assigned_target
                
        # Fall back to individual targeting
        return self.select_individual_target()
        
    def select_individual_target(self) -> Unit:
        """Individual target selection when no coordinator available"""
        enemies_in_range = self.get_enemies_in_range()
        
        if not enemies_in_range:
            return None
            
        # Use TAS for individual selection
        best_score = float('inf')
        best_target = None
        
        for enemy in enemies_in_range:
            score = target_allocation_score(self.bot, enemy)
            if score < best_score:
                best_score = score
                best_target = enemy
                
        return best_target
```

### Army Group Coordination

```python
class ArmyGroup:
    def coordinate_targeting(self):
        """Coordinate targeting for all units in group"""
        
        # Initialize target allocator
        enemies_in_range = self.get_all_enemies_in_range()
        self.target_allocator = TargetAllocator(self.bot, self.units, enemies_in_range)
        
        # Get target assignments
        assignments = self.target_allocator.assign_targets()
        
        # Apply assignments to units
        for unit, target in assignments.items():
            unit.set_target(target)
```

## Performance Optimization

### Computational Complexity

- **TAS Calculation**: O(n) where n is number of enemy units
- **Target Assignment**: O(n × m) where n is units, m is enemies  
- **Overall Complexity**: O(n × m) per targeting update

### Optimization Strategies

```python
def optimize_targeting_performance(self):
    """Optimize targeting calculations for performance"""
    
    # Cache TAS calculations
    if not hasattr(self, 'tas_cache'):
        self.tas_cache = {}
        
    # Update cache only when enemy health changes significantly
    for enemy in self.targets:
        cache_key = (enemy.tag, int(enemy.health / 10))  # Quantize health
        if cache_key not in self.tas_cache:
            self.tas_cache[cache_key] = target_allocation_score(self.bot, enemy)
```

### Spatial Optimization

```python
def spatial_targeting_optimization(self):
    """Use spatial indexing for range queries"""
    
    # Group enemies by proximity
    enemy_clusters = self.cluster_enemies_by_position()
    
    # Assign cluster priorities
    for cluster in enemy_clusters:
        cluster_priority = self.calculate_cluster_priority(cluster)
        self.prioritize_cluster_targets(cluster, cluster_priority)
```

## Configuration and Tuning

### Targeting Parameters

```json
{
    "targeting": {
        "tas_weight_dps": 1.0,
        "tas_weight_health": 0.8,
        "tas_weight_range": 0.6,
        "overkill_threshold": 1.2,
        "focus_fire_minimum": 3
    }
}
```

### Priority Modifiers

```json
{
    "target_priorities": {
        "detector_bonus": -3.0,
        "air_threat_bonus": -2.0,
        "high_dps_bonus": -1.5,
        "low_health_bonus": -1.0
    }
}
```

## Usage Examples

### Basic Target Selection

```python
# Individual unit targeting
stalker = Stalker(stalker_unit, bot)
enemies = bot.enemy_units.closer_than(10, stalker_unit)

best_target = None
best_score = float('inf')

for enemy in enemies:
    score = target_allocation_score(bot, enemy)
    if score < best_score:
        best_score = score
        best_target = enemy

if best_target:
    await stalker.engage(best_target)
```

### Coordinated Army Targeting

```python
# Army group coordination
army_group = ArmyGroup(bot, stalker_units)
army_group.coordinate_targeting()

# Execute coordinated attack
for unit in army_group.units:
    assigned_target = unit.get_assigned_target()
    if assigned_target:
        await unit.engage(assigned_target)
```

### Custom Priority Targeting

```python
# Prioritize specific threats
def prioritize_air_threats(bot: BotAI, enemy: Unit) -> float:
    """Custom targeting for air threat priority"""
    
    base_score = target_allocation_score(bot, enemy)
    
    # Boost priority for air units attacking our ground forces
    if enemy.is_flying and enemy.can_attack_ground:
        base_score -= 2.0  # Higher priority
        
    return base_score
```

The target allocation system ensures optimal combat effectiveness by mathematically analyzing threats and coordinating focus fire across all combat units in the army.
