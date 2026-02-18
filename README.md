# catan-ai (Raspberry Pi)

Train and evaluate bots for a simulated Settlers of Catan environment on a Raspberry Pi using `catanatron`.

This repo currently contains:
- baseline simulation scripts (random vs random)
- tournament scripts (SimplePlayer vs RandomPlayer, with fair seat rotation)
- run logging to CSV (so results are reproducible/comparable)

---

## Requirements

- Raspberry Pi OS (or any Linux)
- Python 3.11+ recommended
- Git

---

## Setup (first time)

### 1) Clone the repo
```
git clone https://github.com/pycoder08/catan-ai.git
cd catan-ai
```

### 2) Create + activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```
