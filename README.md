# 🍯 SSH Honeypot — Cloud-Ready MITM Proxy

A high-interaction SSH honeypot built from scratch in Python. Instead of emulating a fake shell, this honeypot acts as a **Man-in-the-Middle proxy** between the attacker and a real decoy VM — making it nearly impossible to detect while logging everything.

Built as a portfolio project to understand real-world attacker behavior, offensive SSH techniques, and defensive infrastructure.

---

## How It Works

```
Attacker ──→ Honeypot (Paramiko SSH Server) ──→ Decoy VM (Real Linux Shell)
                        ↓
              Logs credentials + commands
              to SQLite DB and .log file
```

1. Attacker connects to port 22 and sees a real SSH server
2. Honeypot uses **randomized authentication delay** — accepts login after a random number of attempts (2–5) to mimic a real server
3. Once authenticated, honeypot connects to the real decoy VM and proxies everything bidirectionally
4. Every credential attempt and command gets logged to both SQLite and a rotating log file

---

## Features

- **MITM Proxy Architecture** — attacker gets a real Linux shell, not a fake emulated one
- **Randomized Auth Delay** — accepts login after random number of attempts per attacker, defeating automated honeypot detection
- **Credential Memory** — once credentials are accepted, they're stored in memory so repeat logins are consistent
- **Dual Logging** — real-time `.log` file for live monitoring + SQLite database for structured analysis
- **Multi-threaded** — each attacker gets their own isolated thread, handles concurrent connections
- **Thread-safe Database Writes** — uses `threading.Lock()` to prevent race conditions
- **Environment-based Config** — no hardcoded credentials, fully portable across machines

---

## Project Structure

```
Honey_Pot_Cloud/
├── honeypot.py              ← main entry point
├── requirements.txt
├── .gitignore
├── README.md
├── Server/
│   ├── __init__.py
│   ├── server.py            ← Paramiko SSH server + MITM proxy logic
│   ├── config.py            ← loads environment variables
│   └── .env.example         ← template for setup of VM Credentials
├── Database/
│   ├── __init__.py
│   └── log_database.py      ← SQLite setup and logging functions
└── Logs/
    └── honeypot.log         ← generated at runtime
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Paramiko | SSH protocol implementation (server + client mode) |
| Socket | Raw TCP connection handling |
| Threading | Concurrent attacker sessions |
| SQLite3 | Structured credential and command storage |
| Logging | Real-time file and terminal output |
| python-dotenv | Environment-based configuration |

---

## Database Schema

```sql
CREATE TABLE attempts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp   TEXT,
    ip          TEXT,
    username    TEXT,
    password    TEXT,
    accepted    INTEGER    -- 0 = rejected, 1 = accepted
);
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/Honey_Pot_Cloud.git
cd Honey_Pot_Cloud
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file inside `Server/`
```bash
cp Server/.env.example Server/.env
```

Edit `Server/.env` with your actual values:
```
Decoy_ip=your_decoy_vm_ip
Decoy_port=22
Decoy_username=your_decoy_username
Decoy_password=your_decoy_password
Honeypot_Port=2222
```

### 4. Make sure SSH is running on your decoy VM
```bash
sudo systemctl enable ssh && sudo systemctl start ssh
```

### 5. Run the honeypot
```bash
python honeypot.py
```

---

## Monitoring

**Watch live in terminal:**
```bash
tail -f Logs/honeypot.log
```

**Query the database:**
```bash
python -c "import sqlite3; conn = sqlite3.connect('./Database/Honeypot_logs.db'); cursor = conn.cursor(); cursor.execute('SELECT * FROM attempts'); print(cursor.fetchall())"
```

---

## Architecture Decisions

**Why a real decoy VM instead of emulation?**
Emulated shells are detectable — attackers run commands that behave slightly differently than a real OS. A real VM gives authentic responses, making the honeypot impossible to fingerprint through behavior.

**Why randomized auth delay?**
A honeypot that accepts every password immediately is trivially detected. Randomizing the number of attempts required per attacker makes it behave like a real server with a strong password.

**Why both SQLite and log files?**
Log files allow live monitoring with `tail -f`. SQLite enables structured queries — most common usernames, attack frequency by IP, time-based patterns — which is what turns raw data into actual threat intelligence.

---

## What This Captures

Once deployed on a public IP, this honeypot collects:
- Attacker IP addresses and geolocation data
- Credential stuffing lists (real passwords attackers use)
- Post-exploitation commands (what attackers do after getting in)
- Attack timing patterns and botnet behavior

---

## Planned Improvements

- [ ] Oracle Cloud deployment for real-world data collection
- [ ] GeoIP enrichment on attacker IPs
- [ ] Dashboard for visualizing attack data
- [ ] Automated alerts on high-frequency attackers

---

## Author

**Yaseen Rather**
Cybersecurity Engineering Student 
Focus: SOC Analyst
