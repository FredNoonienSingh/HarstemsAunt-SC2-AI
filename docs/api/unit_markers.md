# Unit Marker System

The unit marker system tracks enemy units that have left vision, maintaining strategic intelligence about their last known positions and capabilities. This system enables the bot to make informed decisions about areas it can no longer see directly.

## Overview

The marker system provides:

- **Memory Persistence**: Tracks units after they leave vision
- **Intelligence Gathering**: Maintains unit capability information
- **Threat Assessment**: Health and position tracking
- **Influence Mapping**: Integrates with map analysis systems

## Core Classes

### UnitMarker Class

```python
class UnitMarker:
    """
    A marker created whenever an enemy unit leaves vision.
    Remains at position until a certain age or position is in vision again.
    Adds influence to influence maps according to unit_type.
    """
    
    def __init__(self, unit: Unit, created_at_iteration: int):
        # Unit identification and capabilities
        self.type_id: UnitTypeId = unit.type_id
        self.unit_tag: int = unit.tag
        
        # Combat capabilities
        self.can_attack_ground: bool = unit.can_attack_ground
        self.can_attack_air: bool = unit.can_attack_air
        self.can_attack_both: bool = unit.can_attack_both
        self.ground_dps: float = unit.ground_dps
        self.ground_range: float = unit.ground_range
        self.air_dps: float = unit.air_dps
        self.air_range: float = unit.air_range
        self.is_detector: bool = unit.is_detector
        
        # Positional and temporal data
        self.position: Point2 = unit.position
        self.health: float = unit.health_percentage
        self.created_at: int = created_at_iteration
```

### StructureMarker Class

```python
class StructureMarker:
    """
    Marker for structures that have left vision.
    May not be necessary depending on implementation needs.
    """
    
    def __init__(self, structure: Unit, created_at_iteration: int):
        self.structure = structure
        self.type_id: UnitTypeId = structure.type_id
        self.position: Point2 = structure.position
        self.health: float = structure.health_percentage
        self.created_at: int = created_at_iteration
```

## Key Features

### Intelligence Preservation

#### Combat Capability Tracking

The marker system preserves essential combat information:

```python
# Offensive capabilities
self.ground_dps: float = unit.ground_dps      # Ground damage per second
self.ground_range: float = unit.ground_range  # Ground attack range
self.air_dps: float = unit.air_dps           # Air damage per second  
self.air_range: float = unit.air_range       # Air attack range

# Target capabilities
self.can_attack_ground: bool = unit.can_attack_ground
self.can_attack_air: bool = unit.can_attack_air
self.can_attack_both: bool = unit.can_attack_both

# Special abilities
self.is_detector: bool = unit.is_detector
```

**Use Cases:**
- Threat assessment for path planning
- Range calculation for positioning
- Detection awareness for cloaked units

#### Health Status Memory

```python
self.health: float = unit.health_percentage

@property
def color(self):
    """Visual representation based on health status"""
    if self.health < .25:
        return (0, 0, 255)      # Blue: Critically damaged
    elif self.health < .75:
        return (0, 155, 255)    # Light blue: Moderately damaged
    return (255, 255, 0)        # Yellow: Healthy
```

**Strategic Value:**
- **Damaged Units**: High-priority targets for elimination
- **Healthy Units**: Require more caution in engagement
- **Visual Feedback**: Quick health assessment through colors

### Temporal Tracking

#### Age Calculation

```python
def age_in_frames(self, iteration: int) -> int:
    """Returns the age of the marker in frames"""
    return iteration - self.created_at
```

**Aging Logic:**
- **Fresh Markers** (0-100 frames): High confidence in position
- **Aging Markers** (100-500 frames): Reduced confidence  
- **Stale Markers** (500+ frames): Low confidence, consider removal

#### Marker Lifecycle

```python
def should_expire(self, current_iteration: int, max_age: int = 500) -> bool:
    """Determine if marker should be removed"""
    return self.age_in_frames(current_iteration) > max_age

def update_if_visible(self, visible_units: Units) -> bool:
    """Update marker if unit is visible again"""
    for unit in visible_units:
        if unit.tag == self.unit_tag:
            # Unit is visible again, marker can be removed
            return True
    return False
```

## Integration with Bot Systems

### Vision Management

#### Marker Creation

```python
class VisionManager:
    def __init__(self):
        self.unit_markers: List[UnitMarker] = []
        self.last_seen_enemies: Dict[int, Unit] = {}
    
    def update_markers(self, visible_enemies: Units, iteration: int):
        """Create markers for units that left vision"""
        current_tags = {unit.tag for unit in visible_enemies}
        
        # Find units that left vision
        for tag, unit in self.last_seen_enemies.items():
            if tag not in current_tags:
                # Unit left vision, create marker
                marker = UnitMarker(unit, iteration)
                self.unit_markers.append(marker)
        
        # Update current enemy tracking
        self.last_seen_enemies = {unit.tag: unit for unit in visible_enemies}
```

#### Marker Cleanup

```python
def cleanup_markers(self, iteration: int, visible_positions: Set[Point2]):
    """Remove expired or invalidated markers"""
    valid_markers = []
    
    for marker in self.unit_markers:
        # Remove if too old
        if marker.age_in_frames(iteration) > 500:
            continue
            
        # Remove if position is now visible and unit not there
        if marker.position in visible_positions:
            continue
            
        valid_markers.append(marker)
    
    self.unit_markers = valid_markers
```

### Influence Mapping Integration

#### Threat Projection

```python
class InfluenceMap:
    def add_marker_influence(self, marker: UnitMarker):
        """Add influence based on marker capabilities"""
        
        # Ground threat influence
        if marker.can_attack_ground:
            self.add_circular_influence(
                center=marker.position,
                radius=marker.ground_range,
                strength=marker.ground_dps * 0.5,  # Reduced for uncertainty
                influence_type='ground_threat'
            )
        
        # Air threat influence
        if marker.can_attack_air:
            self.add_circular_influence(
                center=marker.position,
                radius=marker.air_range,
                strength=marker.air_dps * 0.5,
                influence_type='air_threat'
            )
        
        # Detection influence
        if marker.is_detector:
            self.add_circular_influence(
                center=marker.position,
                radius=12,  # Standard detection range
                strength=1.0,
                influence_type='detection_threat'
            )
```

#### Positional Uncertainty

```python
def apply_uncertainty_decay(self, marker: UnitMarker, iteration: int):
    """Reduce influence strength based on marker age"""
    age = marker.age_in_frames(iteration)
    
    # Uncertainty increases over time
    if age < 100:
        confidence = 1.0      # High confidence
    elif age < 300:
        confidence = 0.7      # Medium confidence
    else:
        confidence = 0.3      # Low confidence
    
    return confidence
```

### Tactical Decision Making

#### Path Planning Integration

```python
class PathPlanner:
    def calculate_safe_path(self, start: Point2, end: Point2, unit_markers: List[UnitMarker]):
        """Plan path considering marked threats"""
        
        threat_zones = []
        for marker in unit_markers:
            if marker.can_attack_ground:
                threat_zones.append({
                    'center': marker.position,
                    'radius': marker.ground_range,
                    'strength': marker.ground_dps,
                    'confidence': self.get_marker_confidence(marker)
                })
        
        # Use threat zones in pathfinding algorithm
        return self.find_path_avoiding_threats(start, end, threat_zones)
```

#### Target Priority System

```python
class TargetPriority:
    def evaluate_marker_targets(self, markers: List[UnitMarker]):
        """Prioritize targets based on marker information"""
        
        priorities = []
        for marker in markers:
            priority = 0
            
            # High value targets
            if marker.is_detector:
                priority += 50
            
            # Damaged units (easier kills)
            if marker.health < 0.5:
                priority += 30
            
            # High DPS threats
            priority += marker.ground_dps + marker.air_dps
            
            # Reduce priority for old markers (uncertainty)
            age_penalty = min(marker.age_in_frames(self.iteration) / 10, 20)
            priority -= age_penalty
            
            priorities.append((marker, priority))
        
        return sorted(priorities, key=lambda x: x[1], reverse=True)
```

## Advanced Features

### Predictive Positioning

#### Movement Prediction

```python
def predict_unit_movement(self, marker: UnitMarker, iterations_ahead: int):
    """Estimate where unit might be now"""
    
    # Basic prediction based on unit type
    speed_estimates = {
        UnitTypeId.MARINE: 2.25,
        UnitTypeId.STALKER: 2.95,
        UnitTypeId.ZERGLING: 2.95,
        # ... other units
    }
    
    unit_speed = speed_estimates.get(marker.type_id, 2.0)
    max_distance = unit_speed * iterations_ahead / 22.4  # Convert to game units
    
    # Create uncertainty circle
    return {
        'center': marker.position,
        'radius': max_distance,
        'confidence': 0.3  # Low confidence for predictions
    }
```

### Marker Validation

#### Position Verification

```python
def verify_marker_position(self, marker: UnitMarker, current_vision: Set[Point2]):
    """Check if marker position is still valid"""
    
    # If position is in current vision but unit not seen, likely moved
    if marker.position in current_vision:
        return False
    
    # Check if similar units are nearby (might be same unit)
    nearby_units = self.get_units_near_position(marker.position, 3.0)
    for unit in nearby_units:
        if unit.type_id == marker.type_id:
            # Potentially the same unit, update marker
            return self.update_marker_from_unit(marker, unit)
    
    return True
```

### Debug Integration

#### Marker Visualization

```python
def render_markers(self, debug_tools: DebugTools):
    """Render markers for debugging"""
    for marker in self.unit_markers:
        # Draw marker position with health-based color
        debug_tools.draw_unit_marker(marker)
        
        # Show threat ranges
        if marker.can_attack_ground:
            debug_tools.debug_pos(
                marker.position, 
                marker.ground_range, 
                color=(255, 0, 0)
            )
        
        # Show detection range
        if marker.is_detector:
            debug_tools.debug_pos(
                marker.position,
                12,  # Detection range
                color=(255, 255, 0)
            )
```

## Performance Considerations

### Memory Management

```python
class MarkerManager:
    def __init__(self, max_markers: int = 200):
        self.max_markers = max_markers
        self.unit_markers: List[UnitMarker] = []
    
    def add_marker(self, marker: UnitMarker):
        """Add marker with memory limits"""
        self.unit_markers.append(marker)
        
        # Remove oldest markers if limit exceeded
        if len(self.unit_markers) > self.max_markers:
            # Sort by age and remove oldest
            self.unit_markers.sort(key=lambda m: m.created_at)
            self.unit_markers = self.unit_markers[-self.max_markers:]
```

### Update Optimization

```python
def efficient_marker_update(self, visible_enemies: Units, iteration: int):
    """Optimized marker update process"""
    
    # Use sets for O(1) lookups
    visible_tags = {unit.tag for unit in visible_enemies}
    visible_positions = {unit.position for unit in visible_enemies}
    
    # Batch operations
    new_markers = []
    valid_markers = []
    
    # Process existing markers
    for marker in self.unit_markers:
        if (marker.age_in_frames(iteration) < 500 and 
            marker.position not in visible_positions):
            valid_markers.append(marker)
    
    # Find new units that left vision
    for tag, unit in self.last_seen_enemies.items():
        if tag not in visible_tags:
            new_markers.append(UnitMarker(unit, iteration))
    
    self.unit_markers = valid_markers + new_markers
```

## Usage Examples

### Basic Implementation

```python
class HarstemsAunt(BotAI):
    def __init__(self):
        self.marker_system = UnitMarkerSystem()
    
    async def on_step(self, iteration):
        # Update markers based on current vision
        self.marker_system.update_markers(
            self.enemy_units, 
            iteration
        )
        
        # Use markers in decision making
        threat_markers = [m for m in self.marker_system.unit_markers 
                         if m.can_attack_ground and m.ground_dps > 10]
        
        # Adjust army positioning based on remembered threats
        self.adjust_army_positioning(threat_markers)
```

### Integration with Army Groups

```python
class ArmyGroup:
    def evaluate_area_safety(self, target_position: Point2, markers: List[UnitMarker]):
        """Assess safety of area considering markers"""
        
        threat_level = 0
        for marker in markers:
            distance = marker.position.distance_to(target_position)
            
            if marker.can_attack_ground and distance < marker.ground_range:
                # Apply age-based confidence reduction
                confidence = max(0.1, 1.0 - marker.age_in_frames(self.bot.iteration) / 500)
                threat_level += marker.ground_dps * confidence
        
        return threat_level < self.acceptable_threat_threshold
```

The unit marker system provides essential intelligence persistence, enabling the bot to maintain tactical awareness of enemy positions and capabilities even when units are no longer visible, significantly improving strategic decision-making and positioning.
