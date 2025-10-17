# Production Buffer System

The `ProductionBuffer` system manages dynamic unit production requests from army groups and coordinates with the macro system for optimal unit production timing.

## Overview

The production buffer serves as a communication layer between army groups (which request units) and the macro system (which handles actual production). It ensures:

- **Dynamic Unit Composition**: Army groups can request specific unit types
- **Production Coordination**: Prevents overproduction and resource waste
- **Priority Management**: Handles competing production requests efficiently
- **Resource Awareness**: Considers available resources and production capacity

## Core Classes

### ProductionRequest

Represents a request for unit production from an army group.

```python
class ProductionRequest:
    """Represents a unit production request from an army group"""
    
    def __init__(self, requested_unit: UnitTypeId, 
                 army_group_id: int, 
                 build_structure_tag: int):
        self.requested_unit = requested_unit
        self.army_group_tag = army_group_id  
        self.build_structure_tag = build_structure_tag
```

#### Key Properties

**`handled`**
```python
@property
def handled(self) -> bool:
    """True if request has been fulfilled"""
```

Indicates whether the production request has been completed.

#### Methods

**`__repr__()`**
```python
def __repr__(self) -> str:
    return f"Unit: {self.requested_unit} requested by {self.army_group_tag}"
```

Provides clear string representation for debugging.

### ProductionBuffer

Main class managing all production requests and coordination.

```python
class ProductionBuffer:
    """Manages production requests from army groups"""
    
    def __init__(self, bot: BotAI):
        self.bot = bot
        self.requests: List[ProductionRequest] = []
        self.completed_requests: List[ProductionRequest] = []
```

## Request Management

### Adding Requests

Army groups add production requests through the buffer:

```python
def add_request(self, request: ProductionRequest):
    """Add a new production request"""
    if self.is_valid_request(request):
        self.requests.append(request)
        logger.info(f"Added production request: {request}")
```

**Validation Process:**
1. Checks if unit type is valid
2. Verifies requesting army group exists
3. Ensures production structure is available
4. Confirms resources will be available

### Request Processing

The buffer processes requests in priority order:

```python
def process_requests(self) -> List[ProductionRequest]:
    """Process pending requests and return actionable ones"""
    actionable_requests = []
    
    for request in self.prioritize_requests():
        if self.can_fulfill_request(request):
            actionable_requests.append(request)
            
    return actionable_requests
```

**Processing Steps:**
1. **Prioritization**: Orders requests by importance and urgency
2. **Resource Check**: Verifies sufficient resources available
3. **Production Capacity**: Checks if production structures are idle
4. **Queue Management**: Manages production queue efficiently

## Priority System

### Request Prioritization

Requests are prioritized based on multiple factors:

```python
def prioritize_requests(self) -> List[ProductionRequest]:
    """Sort requests by priority"""
    return sorted(self.requests, key=self.calculate_priority, reverse=True)

def calculate_priority(self, request: ProductionRequest) -> float:
    """Calculate priority score for request"""
    priority = 0.0
    
    # Army group urgency
    army_group = self.get_army_group(request.army_group_tag)
    priority += army_group.urgency_level * 10
    
    # Unit type priority  
    priority += self.get_unit_priority(request.requested_unit) * 5
    
    # Resource efficiency
    priority += self.get_resource_efficiency(request.requested_unit) * 2
    
    return priority
```

**Priority Factors:**

| Factor | Weight | Description |
|--------|--------|-------------|
| Army Urgency | 10x | How urgently army group needs reinforcement |
| Unit Priority | 5x | Strategic importance of unit type |
| Resource Efficiency | 2x | Cost-effectiveness of unit |
| Production Timing | 1x | How quickly unit can be produced |

### Unit Type Priority

Different unit types have different strategic priorities:

```python
UNIT_PRIORITIES = {
    UnitTypeId.STALKER: 8,      # High priority - versatile core unit
    UnitTypeId.ZEALOT: 6,       # Medium-high - strong ground unit
    UnitTypeId.IMMORTAL: 9,     # Very high - powerful but expensive
    UnitTypeId.PHOENIX: 7,      # High - air control essential
    UnitTypeId.PROBE: 5,        # Medium - economic support
    UnitTypeId.OBSERVER: 8,     # High - detection critical
}
```

## Integration with Macro System

### Production Coordination

The buffer coordinates with the macro system:

```python
class Macro:
    async def handle_production_requests(self):
        """Process production buffer requests"""
        requests = self.production_buffer.process_requests()
        
        for request in requests:
            if await self.can_produce_unit(request.requested_unit):
                await self.produce_unit(request)
                self.production_buffer.mark_completed(request)
```

### Resource Management

Coordinates with resource management:

```python
def check_resource_availability(self, request: ProductionRequest) -> bool:
    """Check if resources are available for request"""
    unit_cost = self.bot.calculate_cost(request.requested_unit)
    
    # Current resources
    available_minerals = self.bot.minerals
    available_gas = self.bot.vespene
    
    # Pending commitments
    committed_resources = self.calculate_committed_resources()
    
    # Check availability
    return (available_minerals - committed_resources.minerals >= unit_cost.minerals and
            available_gas - committed_resources.gas >= unit_cost.gas)
```

## Army Group Integration

### Request Creation

Army groups create requests based on their needs:

```python
class ArmyGroup:
    def request_reinforcements(self):
        """Request additional units based on army composition"""
        needed_units = self.analyze_composition_needs()
        
        for unit_type, count in needed_units.items():
            for _ in range(count):
                request = ProductionRequest(
                    requested_unit=unit_type,
                    army_group_id=self.group_id,
                    build_structure_tag=self.get_production_structure(unit_type)
                )
                self.bot.macro.production_buffer.add_request(request)
```

### Dynamic Adaptation

Army groups adapt their requests based on battlefield conditions:

```python
def update_unit_requests(self):
    """Update unit requests based on current situation"""
    enemy_composition = self.analyze_enemy_composition()
    
    # Counter enemy air units
    if enemy_composition.air_threat > 0.5:
        self.request_unit(UnitTypeId.STALKER, priority=HIGH)
        self.request_unit(UnitTypeId.PHOENIX, priority=HIGH)
    
    # Counter enemy armor
    if enemy_composition.armored_threat > 0.7:
        self.request_unit(UnitTypeId.IMMORTAL, priority=VERY_HIGH)
```

## Performance Optimization

### Request Batching

Batches similar requests for efficiency:

```python
def batch_requests(self) -> Dict[UnitTypeId, int]:
    """Batch requests by unit type"""
    batched = {}
    for request in self.requests:
        unit_type = request.requested_unit
        batched[unit_type] = batched.get(unit_type, 0) + 1
    return batched
```

### Resource Prediction

Predicts resource availability for better planning:

```python
def predict_resource_availability(self, time_horizon: float) -> Dict[str, int]:
    """Predict available resources in future"""
    current_income = self.bot.state.score.collection_rate_minerals
    
    predicted_minerals = self.bot.minerals + (current_income * time_horizon)
    predicted_gas = self.bot.vespene + (self.bot.state.score.collection_rate_vespene * time_horizon)
    
    return {
        'minerals': predicted_minerals,
        'gas': predicted_gas
    }
```

## Monitoring and Analytics

### Request Tracking

Tracks request fulfillment metrics:

```python
def calculate_fulfillment_rate(self) -> float:
    """Calculate percentage of requests fulfilled"""
    total_requests = len(self.requests) + len(self.completed_requests)
    if total_requests == 0:
        return 1.0
    
    return len(self.completed_requests) / total_requests
```

### Performance Metrics

Monitors system performance:

```python
class BufferMetrics:
    def __init__(self):
        self.average_fulfillment_time = 0.0
        self.request_queue_length = 0
        self.resource_utilization = 0.0
        self.production_efficiency = 0.0
```

## Configuration

### Buffer Settings

```json
{
    "production_buffer": {
        "max_queue_size": 20,
        "priority_threshold": 5.0,
        "batch_processing": true,
        "resource_prediction_window": 30.0
    }
}
```

### Unit Production Limits

```json
{
    "production_limits": {
        "stalker_max_queue": 5,
        "zealot_max_queue": 8,
        "immortal_max_queue": 2,
        "phoenix_max_queue": 4
    }
}
```

## Usage Examples

### Basic Request Creation

```python
# Army group requests stalkers
request = ProductionRequest(
    requested_unit=UnitTypeId.STALKER,
    army_group_id=army_group.group_id,
    build_structure_tag=gateway.tag
)
production_buffer.add_request(request)
```

### Priority Request

```python
# High priority immortal request
urgent_request = ProductionRequest(
    requested_unit=UnitTypeId.IMMORTAL,
    army_group_id=army_group.group_id,
    build_structure_tag=robotics_facility.tag
)
urgent_request.priority = HIGH_PRIORITY
production_buffer.add_request(urgent_request)
```

### Batch Processing

```python
# Process all pending requests
actionable_requests = production_buffer.process_requests()

for request in actionable_requests:
    if macro_system.can_produce(request.requested_unit):
        await macro_system.produce_unit(request)
        production_buffer.mark_completed(request)
```

The Production Buffer system ensures efficient and strategic unit production by serving as an intelligent intermediary between army groups' tactical needs and the macro system's production capabilities.
