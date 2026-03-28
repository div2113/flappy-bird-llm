# 🐦 Flappy Bird — Cute Edition

A modern Flappy Bird clone built with Python + Pygame, featuring cute cartoon visuals, AI commentary, dynamic difficulty, and a Django-powered backend.

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| 🎮 Game Frontend | Python + Pygame |
| ⚙️ Backend | Python + Django |
| 🤖 LLM Integration | Claude / OpenAI API |
| 🗄️ Database | SQLite → PostgreSQL |

---

## 🎮 Features

### ✅ Done
- 🐦 Animated cartoon bird with gravity + jump
- 🧱 Scrolling pipes with random gaps
- 💥 Collision detection
- 🎯 Score system
- 🎬 Game states — Start / Playing / Game Over
- 🎨 Cute cartoon UI with animated screens
- ☁️ Clouds, sun, parallax background
- 💀 Death explosion + screen shake
- 🏅 Medal system (Bronze / Silver / Gold / Platinum)
- 🔊 Procedurally generated sound effects
- ✨ Confetti + particle effects

### ⏳ Coming Soon
- 🌅 Day / Night theme
- ⚡ Dynamic difficulty scaling
- ⚙️ Django backend + High score API
- 🤖 LLM AI Commentator (roasts & hypes you)
- 💡 Smart hint system (tips based on how you die)
- 🏆 Online leaderboard

---

## 📁 Project Structure

```
flappy_bird/
│
├── main.py           # Game loop + states
├── bird.py           # Bird logic + animation
├── pipes.py          # Pipe spawning + movement
├── background.py     # Clouds, sun, sky
├── sounds.py         # Procedural sound generation
├── game_state.py     # State constants
├── settings.py       # All game constants
│
├── backend/          # Django (Phase 5)
│   ├── manage.py
│   ├── api/
│   │   ├── views.py
│   │   ├── models.py
│   │   └── llm.py
│   └── settings.py
│
└── assets/
    └── sounds/       # Reserved for future audio files
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- pip

### Install dependencies
```bash
pip install pygame numpy
```

### Run the game
```bash
cd flappy_bird
python main.py
```

---

## 🕹️ Controls

| Key | Action |
|---|---|
| `SPACE` | Flap / Jump |
| `SPACE` (Start screen) | Start game |
| `SPACE` (Game Over) | Restart |
| `ESC` | Quit |

---

## 🏅 Medal System

| Medal | Score Required |
|---|---|
| 🥉 Bronze | 5+ |
| 🥈 Silver | 10+ |
| 🥇 Gold | 20+ |
| 🏆 Platinum | 40+ |

---

## 🤖 LLM Integration (Phase 6)

The game will use an LLM API for:

- **AI Commentator** — roasts or hypes you based on performance
- **Dynamic Difficulty** — LLM adjusts pipe speed and gap based on your play style
- **Smart Hints** — personalized tips shown on Game Over based on how you died

### Flow
```
Pygame → Django API → LLM API → Response → Display in game
```

---

## 🗺️ Roadmap

| Phase | Status |
|---|---|
| Phase 1 — Window + Game Loop | ✅ Complete |
| Phase 2 — Bird + Physics | ✅ Complete |
| Phase 3 — Pipes + Collision + Score | ✅ Complete |
| Phase 4 — Game States + UI | ✅ Complete |
| Phase 5 — Django Backend | 🔜 Next |
| Phase 6 — LLM Integration | 🔜 Planned |

---

## 👨‍💻 Development Approach

Built iteratively using LLM-assisted development:
- Small focused modules
- Test after every phase
- Git commit after every step
- Clean separation of concerns

---

## 📜 License

MIT License — free to use, modify and share.

---

> Built with ❤️ using Python, Pygame, Django and AI
