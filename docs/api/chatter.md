# Chatter System

The `Chatter` class handles all in-game communication, providing personality and strategic commentary during matches.

## Overview

The chatter system adds personality to the bot by:

- **Dynamic Commentary**: Responds to game events with contextual messages
- **Strategic Analysis**: Comments on opponent strategies and adaptations  
- **Personality Expression**: Maintains the "HarstemsAunt" character persona
- **Tactical Communication**: Provides information about bot decision-making

## Core Class

```python
class Chatter:
    """Handles all bot chatter and in-game communication"""
```

All methods are static, making the chatter system a utility class that can be called from anywhere in the bot.

## Communication Methods

### Greeting System

#### `greeting(bot)`
```python
@staticmethod
async def greeting(bot: BotAI):
    """Sends the initial greeting message"""
    await bot.chat_send(bot.greeting)
```

**Purpose:** Sends the bot's greeting message at game start  
**Timing:** Called once during `on_start()` event  
**Message:** Uses the bot's configured greeting property

### Strategic Commentary

#### `build_order_comments(bot)`
```python
@staticmethod
async def build_order_comments(bot: BotAI):
    """Comments on opponent build and adapts strategy"""
```

**Dynamic Responses:**

**Air Force Detection**
```python
if not bot.macro.build_order.opponent_builds_air:
    if [unit for unit in bot.seen_enemies if unit.is_flying and unit.can_attack]:
        bot.macro.build_order.opponent_builds_air = True
        await bot.chat_send("I see you got an AirForce, i can do that too")
```

**Detection Analysis**
```python
if not bot.macro.build_order.opponent_has_detection:
    if [unit for unit in bot.seen_enemies if unit.is_detector]:
        bot.macro.build_order.opponent_has_detection = True
```

**Cloaking Response**  
```python
if not bot.macro.build_order.opponent_uses_cloak:
    if [unit for unit in bot.seen_enemies if (unit.is_cloaked and unit.can_attack) 
        or (unit.is_burrowed and unit.can_attack)]:
        bot.macro.build_order.opponent_uses_cloak = True
        await bot.chat_send("Stop hiding and fight like a honorable ... ähm... Robot?\ndo computers have honor ?")
```

### End Game Communication

#### `end_game_message(bot)`
```python
@staticmethod
async def end_game_message(bot: BotAI) -> None:
    """Sends message before game ends"""
    await bot.chat_send(
        f"GG, you are probably a hackcheating smurf cheat hacker anyway also "
        f"{bot.enemy_race} is IMBA"
    )
```

**Purpose:** Provides humorous closing message  
**Timing:** Called during game end sequence  
**Content:** Playful accusation with race-specific commentary

### Special Event Responses

#### `nuke_message(bot)`
```python
@staticmethod
async def nuke_message(bot: BotAI) -> None:
    """Responds to enemy nuke detection"""
    await bot.chat_send("Nukes ?!? -> RUDE !!!")
```

**Trigger:** When enemy nuclear launch is detected  
**Response:** Expresses indignation at nuclear weapons use

#### `nydus_message(bot)`
```python
@staticmethod
async def nydus_message(bot: BotAI) -> None:  
    """Responds to nydus worm detection"""
    await bot.chat_send("You went into that thing ? DISGUSTING !!!")
```

**Trigger:** When nydus worm network is detected  
**Response:** Shows disgust at the biological transport method

## Integration Points

### Main Bot Integration

The chatter system integrates with the main bot through event handlers:

```python
class HarstemsAunt(BotAI):
    async def on_start(self):
        """Send greeting at game start"""
        await Chatter.greeting(self)
    
    async def on_step(self, iteration):
        """Continuous commentary during gameplay"""  
        await Chatter.build_order_comments(self)
        
    async def on_end(self, game_result):
        """End game message"""
        await Chatter.end_game_message(self)
```

### Strategic System Integration

The chatter system both reads and updates strategic information:

**Reading Game State:**
- Analyzes enemy unit compositions
- Monitors strategic threats (air units, cloaking, detection)
- Tracks opponent build patterns

**Updating Strategy Flags:**
```python
# Sets strategic flags based on observations
bot.macro.build_order.opponent_builds_air = True
bot.macro.build_order.opponent_has_detection = True  
bot.macro.build_order.opponent_uses_cloak = True
```

**Note:** This dual responsibility (FIXME comment indicates) should be refactored to separate observation from communication.

## Personality and Character

### HarstemsAunt Persona

The chatter reflects the bot's personality:

- **Competitive**: Challenges opponents and claims superiority
- **Humorous**: Uses playful insults and exaggerated reactions
- **Observant**: Comments on strategic developments
- **Sarcastic**: Employs irony and wit in responses

### Message Tone Examples

**Confident:** "I see you got an AirForce, i can do that too"  
**Indignant:** "Nukes ?!? -> RUDE !!!"  
**Disgusted:** "You went into that thing ? DISGUSTING !!!"  
**Accusatory:** "you are probably a hackcheating smurf cheat hacker anyway"

## Configuration and Customization

### Message Customization

Messages can be customized through bot configuration:

```python
class HarstemsAunt:
    @property
    def greeting(self) -> str:
        """Customizable greeting message"""
        return "Hello! Prepare to face HarstemsAunt!"
```

### Conditional Messaging

Enable/disable chatter based on settings:

```python
def should_send_chatter(self) -> bool:
    """Check if chatter is enabled"""
    return self.config.get('enable_chatter', True) and not self.config.get('tournament_mode', False)
```

## Strategic Impact

### Opponent Analysis

The chatter system serves dual purposes:

**Entertainment Value:**
- Provides personality and engagement
- Creates memorable gameplay experience
- Reflects the bot creator's humor and style

**Strategic Intelligence:**
```python
# Strategic flag setting (needs refactoring)
if opponent_air_detected:
    self.macro.build_order.opponent_builds_air = True
    # This triggers anti-air production
```

## Usage Examples

### Basic Integration

```python
class CustomBot(HarstemsAunt):
    async def on_step(self, iteration):
        # Standard bot logic
        await super().on_step(iteration)
        
        # Custom chatter triggers
        if self.detect_special_condition():
            await Chatter.custom_message(self)
```

### Event-Driven Responses

```python
async def on_unit_destroyed(self, unit_tag):
    """React to unit losses"""
    unit = self.get_unit_by_tag(unit_tag)
    
    if unit and unit.is_mine:
        if unit.type_id == UnitTypeId.NEXUS:
            await bot.chat_send("Hey! That was expensive!")
    else:
        await bot.chat_send("One down, more to go!")
```

### Strategic Commentary

```python
def analyze_and_comment(self):
    """Provide ongoing strategic commentary"""
    
    # Economy comparison
    if self.supply_used > self.enemy_supply * 1.5:
        await bot.chat_send("I'm ahead, might as well end this quickly")
    
    # Technology analysis  
    if self.enemy_has_superior_tech():
        await bot.chat_send("Fancy tech won't save you!")
```

## Best Practices

### Timing Considerations

- **Rate Limiting**: Don't spam chat with too many messages
- **Context Awareness**: Ensure messages are relevant to current game state
- **Performance Impact**: Keep chatter system lightweight

### Message Quality

- **Personality Consistency**: Maintain character voice
- **Strategic Relevance**: Connect messages to actual game events
- **Respectful Humor**: Keep messages playful rather than offensive

### Code Organization

```python
# Separate observation from communication (recommended refactor)
class GameStateObserver:
    def analyze_enemy_composition(self):
        """Pure observation without side effects"""
        pass

class Chatter:
    def respond_to_observations(self, observations):
        """Pure communication based on observations"""
        pass
```

The chatter system adds character and engagement to the bot while providing strategic commentary, though it would benefit from refactoring to separate its observation and communication responsibilities.
