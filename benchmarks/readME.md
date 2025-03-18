# SC2 Bot Bechmarker
#### for [BurnySC2](https://github.com/BurnySc2/python-sc2?tab=readme-ov-file) and [sharpy-sc2](https://github.com/DrInfy/sharpy-sc2).

### 🚀*For fast and repeatable testing and evaluating of __unit micro__* 🚀

Just clone into your bot:
```bash
cd YOUR_BOT
git clone ---
````

In your `bot.py`:

```py
from benchmarks.benchmark import Benchmark
````

In the `on_start()` method:
```py
   async def on_start(self) -> None:
        """ coroutine called on game_start """
        self.benchmarker:Benchmark = Benchmark(self, self.benchmark_message)

        if self.benchmark:
            await self.benchmarker.prepare_benchmarks()
```

In the `on_step()` method:
```py
    async def on_step(self, iteration:int):
        """ Coroutine running every game tick
        Args:
            iteration (_type_): current tick
        """
        await self.benchmarker()
```

In the `on_unit_took_damage` method:

```py
    async def on_unit_took_damage(self, unit:Unit, amount_damage_taken:float) -> None:
        """ Coroutine that gets called when unit takes damage
        Args:
            unit (Unit): Unit that took damage 
            amount_damage_taken (float): amount of damage taken
        """
        if unit in self.units:
            self.benchmarker.record_damage_taken(amount_damage_taken)
```

## Settings:
```json
{
    "endless":true,
    "save_data":true,
    "verbose": true,
    "blind":false,
    "scenarios":"benchmarks/configs/short_test.json",
    "output_dir":"benchmarks/data/"
}
```
## Defining Benchmarks:

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
      },
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
          "enemy_behavior": "attack_towards"
        }
      },

    ]
}
```


```bash
python bot/run.py -bench -bm "description"
```