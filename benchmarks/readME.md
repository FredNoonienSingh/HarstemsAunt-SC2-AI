# SC2 Bot Benchmarker

**For [BurnySC2](https://github.com/BurnySc2/python-sc2?tab=readme-ov-file) and [sharpy-sc2](https://github.com/DrInfy/sharpy-sc2).**

**🚀 Fast and Repeatable Unit Micro Benchmarking 🚀**

This tool allows you to quickly and consistently evaluate the unit micro performance of your StarCraft II bots.

**Important Note:** This benchmarker assumes your bot class has `bot.name` and `bot.version` properties for result tracking.

## Installation

1.  **Clone the Repository:**

    ```bash
    cd YOUR_BOT_DIRECTORY
    git clone YOUR_BENCHMARKER_REPOSITORY_URL
    ```

2.  **Integrate into Your Bot:**

    * Import the `Benchmark` class in your `bot.py`:

        ```python
        from benchmarks.benchmark import Benchmark
        ```

    * Initialize and prepare the benchmarker in your `on_start()` method:

        ```python
        async def on_start(self) -> None:
            """Coroutine called on game start."""
            self.benchmarker: Benchmark = Benchmark(self)  # Or provide a custom config path

            if self.benchmark:  # Assuming you have a flag to enable benchmarking
                await self.benchmarker.prepare_benchmarks()
        ```

    * Run the benchmarker in your `on_step()` method:

        ```python
        async def on_step(self, iteration: int):
            """Coroutine running every game tick.

            Args:
                iteration (int): Current game tick.
            """
            if self.benchmark:
                await self.benchmarker()
        ```

## Configuration

The benchmarker's behavior is controlled by a JSON configuration file (default path: `benchmarks/configs/config.json`).

```json
{
    "endless": true,       // Run benchmarks continuously
    "save_data": true,      // Save results to CSV
    "verbose": true,        // Enable in-game overlay
    "blind": false,         // Not Currently used.
    "max_runtime": 30,      // Maximum runtime per scenario (seconds)
    "scenarios": "benchmarks/configs/short_test.json", // Path to scenario definitions
    "output_dir": "benchmarks/data/" // Output directory for CSV results
}
```

## Defining Benchmarks (Scenarios)

Benchmarks are defined in a separate JSON file (specified in the `scenarios` setting).

```json
{
    "benchmarks": [
        {
            "title": "Stalker_vs_STALKER",
            "positions": ["center", "enemy_spawn", "ramp_top", "ramp_bottom"],
            "enemy_units": [
                {
                    "unit_type": "UnitTypeId.STALKER",
                    "unit_count": 8
                }
            ],
            "own_units": [
                {
                    "unit_type": "UnitTypeId.STALKER",
                    "unit_count": 8
                }
            ],
            "options": {
                "has_creep": false,
                "enemy_behavior": "attack_closest"
            }
        }
    ]
}
```

* **`title`**: A descriptive name for the benchmark.
* **`positions`**: A list of map positions to run the benchmark at.
* **`enemy_units`**: A list of enemy unit types and counts.
* **`own_units`**: A list of your bot's unit types and counts.
* **`options`**: Scenario-specific settings:
    * **`has_creep`**: Whether to generate creep (for Zerg scenarios).
    * **`enemy_behavior`**: The AI behavior for enemy units.

### Possible Positions

* `center`
* `center_crossed`
* `spawn`
* `enemy_spawn`
* `ramp_top`
* `ramp_bottom`

### Possible Enemy Behaviors

* `attack_towards`
* `attack_weakest`
* `attack_closest`
* `attack_retreat`
* `attack_highest_dps`

## Future Features

* **Macro Benchmarks:**
    * Extend the benchmarking capabilities to evaluate macro strategies, such as economy management, build order execution, and expansion timing. This would involve simulating longer game segments with resource gathering and base building.
* **Performance Benchmarks:**
    * Measure the bot's performance in terms of frames per second (FPS), CPU usage, and memory consumption. This would help identify performance bottlenecks and optimize the bot's code.
* **Safe Average Build Data Collection:**
    * Implement a system to collect and analyze build order data from multiple benchmark runs, providing a "safe average" build order that minimizes risks and maximizes efficiency.
* **Build Comparison Tools:**
    * Develop tools to compare the performance of different build orders or bot versions, allowing users to identify the most effective strategies. This could involve visualizing data and providing statistical analysis.
* **Run Benchmarks for a Specified Number of Observations:**
    * Add the capability to run benchmarks for a specific number of game observations, ensuring consistent data collection and allowing for more precise statistical analysis. This can be used to gather data for machine learning applications.
