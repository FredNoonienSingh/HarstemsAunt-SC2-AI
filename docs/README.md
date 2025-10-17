# HarstemsAunt Documentation

Welcome to the comprehensive documentation for HarstemsAunt, a StarCraft II AI bot that plays as the Protoss race.

## Quick Navigation

- [Project Overview](overview.md) - High-level overview of the project
- [Architecture](architecture.md) - System architecture and design patterns
- [Installation & Setup](installation.md) - How to set up and run the bot
- [API Reference](api/) - Detailed API documentation for all modules
- [Bot Components](components/) - Documentation for individual bot components
- [Benchmarking System](benchmarking.md) - Performance testing framework
- [Configuration](configuration.md) - Configuration options and settings
- [Development Guide](development.md) - Guide for developers and contributors

## About HarstemsAunt

HarstemsAunt is a StarCraft II AI bot designed to play as the Protoss race. The bot was created by analyzing gameplay patterns and attempting to replicate strategic decision-making in an AI system. The name is a playful reference to the StarCraft II content creator Harstem.

### Key Features

- **Advanced Macro Management**: Automated resource management, build orders, and economy optimization
- **Intelligent Unit Control**: Sophisticated micro-management for individual units and army groups
- **Strategic Decision Making**: Dynamic strategy adaptation based on opponent analysis
- **Performance Benchmarking**: Built-in benchmarking system for testing and optimization
- **Map Analysis**: Advanced map reading and pathfinding capabilities
- **Modular Architecture**: Clean, maintainable code structure with well-defined components

### Current Version

**Version**: 1.1 (Development)  
**Race**: Protoss  
**Python Version**: 3.12.5  
**Primary Dependency**: BurnySC2 7.0.1

## Project Structure Overview

```text
HarstemsAunt/
├── bot/                    # Main bot implementation
│   ├── HarstemsAunt/      # Core bot logic
│   ├── map_analyzer/      # Map analysis tools
│   └── training_bots/     # Training opponents
├── benchmarks/            # Performance testing framework
├── data/                  # Game data and statistics
├── docs/                  # This documentation
├── dev_notebooks/         # Development notebooks
└── MapPlots/             # Map visualization
```

## Getting Started

For quick setup instructions, see the [Installation Guide](installation.md).

For understanding the bot's architecture, start with the [Architecture Overview](architecture.md).

To contribute to the project, check out the [Development Guide](development.md).

## Links

- **AI Arena Profile**: [HarstemsAunt on AI Arena](https://aiarena.net/bots/808/)
- **YouTube Channel**: [HarstemsAunt YouTube](https://www.youtube.com/channel/UCdnBJFMuxMgG0ZHOhxdIJmA)
- **GitHub Repository**: [StarCraftBot Repository](https://github.com/FredNoonienSingh/HarstemsAunt-SC2-AI)

## Support

If you encounter any issues or have questions about the bot, please:

1. Check the documentation in this folder
2. Review the [Development Guide](development.md) for troubleshooting
3. Create an issue on the GitHub repository
