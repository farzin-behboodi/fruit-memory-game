# Fruit Memory Deluxe in Python

## introduction
In this project we have a memory card game in Python using `pygame`. When you run `fruit-memory-game.py` it opens a 940x930 window. You do not need any image folders or audio files next to the code because all 16 fruits and sound effects are made directly inside the script.

At the start of the game you are in `self.state = "menu"` where you can pick between 4 board sizes: 4x4, 6x6, 8x8, and 10x10. Each board has its own time limit and saves your best score and stars. When a round begins, all cards flip open for a moment so you can memorize the fruits before the timer starts going down.

## Features

Card flip. Combo points: When you click two cards in `self.selected` and `c1.fruit == c2.fruit`, both cards get `matched = True`. Each match gives `100 * self.combo` points, spawns 28 `Particle` circles with `spawn_burst()`, and if `self.combo > 1` it adds `+2.0` seconds to `self.time_left`.

Clock button. Time boost: In `use_time_boost()` you have 2 boosts (`self.time_boosts = 2`). Clicking the green clock icon adds `+15.0` seconds to `self.time_left` and shows a `FloatingText` on the screen.

Eye button. Peek cards: In `use_peek()` you have 2 peeks (`self.peeks_left = 2`). Clicking the purple eye icon sets `self.preview_until` to `now + 1400` so all unmatched cards flip open for 1.4 seconds.

Bulb button. Hint pair: In `use_hint()` you have 3 hints (`self.hints_left = 3`). Clicking the orange bulb icon finds two matching cards in `unmatched` and sets `hint_timer = 95` to put a yellow border on them.

Stars and best score: When all cards in `self.cards` are matched, `self.won` becomes True and adds `int(self.time_left) * 15` to `self.score`. Then `calc_stars()` gives 1 to 3 stars based on `time_left / max_time` and saves them in `self.best_scores` and `self.best_stars`.

## How To Use

When we run this code it starts pygame using `pygame.init()`. It opens a game window with `pygame.display.set_mode((WIDTH, HEIGHT))`. First open your command prompt or terminal. If you do not have pygame installed on your computer you must install it using pip. Then run `fruit-memory-game.py` in the terminal.

```
pip install pygame

python fruit-memory-game.py
```

At first the window opens in the state `self.state = "menu"`. You can choose the board size using the mouse.

Pick board size: Click on the 4x4 (45s), 6x6 (100s), 8x8 (180s), or 10x10 (300s) card to start playing.

Left click on cards: In `self.state = "playing"` click on any card to flip it. If two cards do not match they close again by themselves.

Use power-up buttons: On the top right of the window you can click the Clock icon for extra time, the Eye icon to see all cards, or the Bulb icon to find a pair.

Press R or Reload button: To restart the current board size at any time press the R key on the keyboard or click the blue reload icon.

Press M or Home button: To return to `self.state = "menu"` and pick another grid size press the M key or click the red home icon.