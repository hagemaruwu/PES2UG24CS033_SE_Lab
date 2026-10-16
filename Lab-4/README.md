# Lab 4: VibeCoding - Donkey Kong Repair Lab

**Student Name:** Aditya Raj  
**SRN:** PES2UG24CS033  
**Course:** Software Engineering Lab  
**Assigned Repository:** [SETAPESU26/30_donkeykong](https://github.com/SETAPESU26/30_donkeykong)  
**Personal GitHub Account:** [hagemaruwu](https://github.com/hagemaruwu)

---

## 1. Overview & Objective

The objective of this lab is to utilize modern AI pair-programming / Vibe Coding tools to analyze, debug, and implement missing features in an object-oriented Python (Pygame) Donkey Kong clone under 3 to 4 prompt iterations.

The project contains:
- 1 Deliberate bug in barrel ladder descent physics.
- 3 Stubbed feature functions awaiting implementation:
  - `theme_color(score)`
  - `on_barrel_jumped(player, barrel)`
  - `score_multiplier(score)`

---

## 2. Tasks & Technical Implementations

### Task 1: Fix Ladder-Descent Probability Bug
- **Issue:** In the original build, `random.random() < 0.7` caused ~70% of barrels to immediately descend the first ladder encountered. This caused the top platform to drain rapidly and flooded lower platforms.
- **Fix:** Corrected the probability threshold in `Barrel.update(dt)`:
  ```python
  # Before:
  if random.random() < 0.7:
      self.ladder = index
      self.pos.x = lx

  # After:
  if random.random() < 0.3:
      self.ladder = index
      self.pos.x = lx
  ```
- **Verification:** Verified statistically across 100,000 simulated barrel updates that barrels descend approximately 29.7%–30.1% of the time.

---

### Task 2: Implement Dynamic Theme Color (`theme_color(score)`)
- **Objective:** Dynamically shift background coloration as player score increases, returning `None` for default navy `(15, 15, 25)`.
- **Implementation:**
  ```python
  def theme_color(score):
      if not score or score <= 0:
          return None
      progress = min(score / 1500.0, 1.0)
      r = int(15 + 40 * progress)
      g = int(15 + 3 * progress)
      b = max(10, int(25 - 10 * progress))
      return (r, g, b)
  ```
- **Visual Feedback:** Smooth transition from dark navy at 0 points to rich deep burgundy/crimson at 1500+ points, maintaining strong contrast against red platforms and golden ladders.

---

### Task 3: Implement Visual Feedback on Jump (`on_barrel_jumped(player, barrel)`)
- **Objective:** Spawn an airborne side effect whenever a player successfully leaps over a barrel.
- **Implementation:**
  ```python
  def on_barrel_jumped(player, barrel):
      pts = 100 * CURRENT_MULTIPLIER
      text = f"+{pts}" if CURRENT_MULTIPLIER == 1 else f"+{pts} (2X!)"
      FLOATING_LABELS.append({
          "pos": pygame.Vector2(barrel.pos.x, barrel.pos.y - 16),
          "text": text,
          "timer": 0.85
      })
  ```
- **Rendering:** Floating score labels render directly above jumped barrels and float upward smoothly before expiring.

---

### Task 4: Implement Late-Game Score Multiplier (`score_multiplier(score)`)
- **Objective:** Return a numeric multiplier for barrel jump rewards (or `None` for default 1x), rewarding late-game skill.
- **Implementation:**
  ```python
  def score_multiplier(score):
      global CURRENT_MULTIPLIER
      if score >= 300:
          CURRENT_MULTIPLIER = 2
          return 2
      CURRENT_MULTIPLIER = 1
      return None
  ```
- **Behavior:**
  - `score < 300`: Standard 100 points per cleared barrel.
  - `score >= 300`: 200 points per cleared barrel, with HUD badge `[2X ACTIVE]` and floating tag `+200 (2X!)`.

---

## 3. How to Run the Game

### Prerequisites
- Python 3.10+
- Pygame (`pip install pygame`)

### Launch Command
```bash
python3 game.py
```

### Controls
| Key | Action |
|---|---|
| **Left / Right Arrow** | Walk horizontally along sloped platforms |
| **Up / Down Arrow** | Climb up or down ladders when aligned |
| **Space** | Jump |
| **R** | Reset the game |

---

## 4. Deliverables Checklist

- [x] **`before.mov`**: 10-second gameplay recording of original unmodified code showing excessive ladder descent bug.
- [x] **`after.mov`**: 10-second gameplay recording showing bug fixed (barrels roll across, ~30% descend), floating `+100` jump bonuses, dynamic background warm hue, and `[2X ACTIVE]` multiplier.
- [x] **`game.py`**: Fully repaired and extended source code.
- [x] **`chat_history.pdf`**: Complete exported AI prompt conversation history documenting iterative prompting within 4 attempts.
