# Project Overview

## Introduction

HarstemsAunt is a sophisticated StarCraft II AI bot developed to compete on the AI Arena platform. The bot specializes in playing the Protoss race and implements advanced strategies including macro management, micro control, and strategic decision-making.

## Design Philosophy

The bot is designed with the following principles in mind:

### Modularity
The codebase is organized into distinct, loosely-coupled modules that handle specific aspects of gameplay:
- **Macro Management**: Resource management and build orders
- **Army Control**: Unit micro-management and combat tactics  
- **Map Analysis**: Terrain analysis and pathfinding
- **Strategy**: High-level decision making and adaptation

### Performance
The bot emphasizes computational efficiency to ensure real-time performance during matches:
- Optimized algorithms for unit selection and pathfinding
- Efficient data structures for game state management
- Built-in benchmarking system for performance monitoring

### Maintainability  
Code quality and maintainability are prioritized through:
- Comprehensive documentation and type hints
- Clean architecture with clear separation of concerns
- Extensive logging and debugging capabilities
- Unit testing framework

## Core Features

### 1. Advanced Macro Management
- **Build Order System**: Predefined and adaptive build orders
- **Resource Management**: Optimal worker allocation and resource spending
- **Supply Management**: Automated supply building to prevent blocks
- **Expansion Timing**: Strategic base expansion decisions

### 2. Intelligent Unit Control
- **Combat Units**: Specialized micro for Stalkers, Zealots, Immortals
- **Flying Units**: Phoenix and Void Ray control with advanced positioning
- **Support Units**: Warp Prism micro and strategic usage
- **Formation Control**: Coordinated army movement and positioning

### 3. Strategic Decision Making
- **Opponent Analysis**: Enemy unit composition and strategy detection
- **Counter Strategies**: Dynamic unit composition adjustments  
- **Timing Attacks**: Coordinated multi-pronged offensives
- **Defensive Positioning**: Optimal defensive structure placement

### 4. Map Analysis
- **Terrain Analysis**: Height advantage and choke point identification
- **Pathfinding**: Efficient unit movement across complex terrain
- **Vision Control**: Strategic observer and pylon placement
- **Expansion Analysis**: Safe expansion identification and timing

### 5. Performance Monitoring
- **Real-time Benchmarking**: Performance metrics during gameplay
- **Unit Efficiency Tracking**: Combat effectiveness measurements
- **Resource Efficiency**: Economic performance analysis
- **Match Statistics**: Comprehensive game data collection

## Technology Stack

### Core Dependencies
- **BurnySC2 7.0.1**: Primary StarCraft II API framework
- **Python 3.12.5**: Programming language
- **NumPy**: Numerical computations for positioning and analysis
- **Loguru**: Advanced logging system

### Development Tools
- **Jupyter Notebooks**: Analysis and development environment
- **Pillow**: Image processing for map analysis
- **PyYAML**: Configuration file management
- **Pytest**: Unit testing framework

## Bot Behavior Overview

### Early Game (0-5 minutes)
1. **Build Order Execution**: Follows predefined build order for economic foundation
2. **Scout Management**: Initial scouting for enemy location and early strategy detection
3. **Wall Construction**: Defensive structures at natural expansion ramp
4. **Worker Production**: Continuous probe production for economic growth

### Mid Game (5-10 minutes)
1. **Tech Tree Progression**: Research key upgrades (Warp Gate, Blink)
2. **Army Composition**: Build core army units based on enemy composition
3. **Expansion**: Secure natural expansion and begin third base preparation
4. **Map Control**: Establish key defensive and offensive positions

### Late Game (10+ minutes)  
1. **Army Coordination**: Large-scale army movements and multi-pronged attacks
2. **Economic Optimization**: Advanced economic management with multiple bases
3. **Tech Switches**: Adapt unit composition based on opponent strategy
4. **Victory Conditions**: Push for decisive battles or economic advantages

## Version History

### Version 1.0 Series
- **1.0.0**: Initial release with basic Stalker/Zealot composition
- **1.0.1-1.0.2**: Stability improvements and upgrade system
- **1.0.3**: Warp Gate research and improved Stalker behavior
- **1.0.4**: Critical crash fixes for misplaced town halls
- **1.0.5**: Zealot behavior improvements and production fixes
- **1.0.6**: Reworked army movement system

### Version 1.1 Series (Current Development)
- **1.1.0**: Complete architecture overhaul
  - Redesigned build order system
  - Enhanced unit movement and targeting
  - Comprehensive bug fixes and stability improvements
  - New benchmarking framework integration

## Performance Metrics

The bot tracks various performance indicators:

### Combat Metrics
- Unit kill/death ratios
- Damage dealt vs. damage taken
- Army efficiency ratings
- Micro-management effectiveness scores

### Economic Metrics  
- Resource collection rates
- Worker efficiency measurements
- Supply block frequency
- Build order execution accuracy

### Strategic Metrics
- Map control percentages
- Expansion timing efficiency
- Technology progression speed
- Opponent adaptation success rate

## Future Development

### Planned Features
- **Machine Learning Integration**: Neural networks for strategic decision making
- **Advanced Scouting**: Improved enemy strategy recognition
- **Dynamic Build Orders**: Adaptive build order generation
- **Multi-Race Support**: Expansion beyond Protoss gameplay

### Research Areas
- **Reinforcement Learning**: Game state evaluation and action selection
- **Computer Vision**: Enhanced map and unit analysis
- **Genetic Algorithms**: Build order and strategy optimization
- **Multi-Agent Systems**: Coordinated unit group behaviors
