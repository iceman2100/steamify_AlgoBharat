# 🌐 Steamify: Decentralized Streaming Wage Payments on Algorand

## 🚀 Overview

**Steamify** is a Web3 decentralized application (dApp) that enables **real-time, continuous wage payments** using the **Algorand blockchain**.  
It transforms traditional payroll systems by streaming payments **as work happens**, ensuring instant settlement, transparency, and financial freedom for workers — powered by Algorand’s **scalable and low-cost** infrastructure.

---

## ⚙️ Core Features

- 💸 **Instant Wage Streaming** — Automates continuous payments based on verified work hours  
- 🔒 **Trustless & Secure** — Smart contracts manage funds with no intermediaries  
- 🪙 **Multi-Asset Support** — Works with ALGO and Algorand Standard Assets (ASAs)  
- 🧩 **Modular Smart Contracts** — Flexible PyTeal architecture for wage, royalty, or subscription models  
- 💻 **Developer-Ready APIs** — FastAPI-powered backend with clean REST endpoints  
- 🧠 **Cross-Chain Vision** — Solidity support for Ethereum/Polygon interoperability  

---

## ⚡ Powered by Algorand

Steamify leverages **Algorand’s Pure Proof-of-Stake (PPoS)** protocol to deliver **speed, security, and scalability** unmatched in traditional payment systems.

### 🚀 Scalability Advantages

| Feature | Description |
|----------|--------------|
| **High Throughput** | 6,000+ TPS with <3s block finality — ideal for thousands of wage streams |
| **Low Fees** | <0.001 ALGO per transaction (~$0.0002) — perfect for micro-payments |
| **Atomic Groups** | Combines multiple wage updates and transfers into single atomic actions |
| **ASA Flexibility** | Create unlimited company or department-specific tokens without chain changes |
| **Oracle Ready** | Supports real-time data feeds (e.g., stock-based wages or price oracles) |

> **Example:** A company with 10,000 employees can stream hourly wages in real-time with <\$50 total daily transaction cost.

---

## 🧮 Technical Implementation

### 🧠 Smart Contract Logic (PyTeal)

#### Phase 1: Deployment
- Employer deploys contract with `wage_rate`, `employer_addr`
- Creates a **WAGE ASA** token for payment
- Worker opts in to receive ASA

#### Phase 2: Hour Logging
- Employer triggers `update_hours(hours_worked)`
- Contract validates employer address
- Updates `total_hours` in global state

#### Phase 3: Streaming Payment
- Calculates `amount = wage_rate * total_hours`
- Performs **atomic transfer** to worker wallet
- Resets `total_hours` after successful disbursement

#### Phase 4: Verification
- Worker verifies balance on [AlgoExplorer TestNet](https://testnet.algoexplorer.io/)
- Continuous updates via backend polling and micro-payments

  <img width="1919" height="967" alt="image" src="https://github.com/user-attachments/assets/22de3c17-cb7a-472e-ae97-f2b2f6894deb" />

  <img width="1889" height="1079" alt="image" src="https://github.com/user-attachments/assets/cb6c2c9e-6ab0-4df2-bec7-a34ba229c099" />



#### Phase 5: Contract Termination
- Employer deletes contract, recovering remaining ALGO and ASA

---

## 🧩 Reusability & Extensibility

### 1. **Smart Contract Modularity**
- Parameterized **wage rate**, **asset type**, and **logic flow**
- Can easily adapt for:
  - Subscriptions
  - Royalty distributions
  - Milestone or performance-based bonuses

### 2. **Backend (FastAPI + Algorand SDK)**
- Core functions (`create_wage_asa`, `deploy_contract`, `stream_wages`)
- Reusable across different payment models (e.g., DeFi rewards, DAO salaries)

### 3. **Frontend (React / Next.js)**
- `WageStream.jsx` acts as a plug-and-play component
- Connects to **Pera Wallet** or **MyAlgo**
- Accepts dynamic backend API URLs for multi-project integration

### 4. **Multi-Chain Integration**
- Solidity contracts (`StreamFi.sol`) for cross-deployment on Ethereum or Polygon
- Enables hybrid Web3 systems using the same core model

---

## 🧰 Setup & Installation

### Prerequisites
- **Python** ≥ 3.9  
- **Node.js** ≥ 18  
- **Algorand Wallet** (Pera / MyAlgo)  
- **TestNet Account** (Get ALGO from [TestNet Faucet](https://dispenser.testnet.aws.algodev.network/))

### Steps

#### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/steamify.git
cd steamify


2️⃣ Backend Setup
python -m venv venv
source venv/bin/activate        # (Mac/Linux)
venv\Scripts\activate           # (Windows)
pip install -r requirements.txt
uvicorn backend.algorand_service:app --reload --port 8000

3️⃣ Smart Contract Compilation
python contracts/algorand/streaming_wage.py

4️⃣ Frontend Setup
cd frontend
npm install
npm install algosdk
npm run dev


Visit: http://localhost:3000

📊 Project Structure
steamify/
├── contracts/
│   ├── algorand/streaming_wage.py     # PyTeal smart contract
│   ├── StreamFi.sol                   # Solidity version
│   └── StreamFiToken.sol
├── backend/algorand_service.py        # FastAPI + Algorand SDK
├── frontend/components/WageStream.jsx # React component
├── scripts/                           # Helper scripts
├── requirements.txt
├── package.json
└── README.md

🧠 Why It Matters

🔍 Transparency — All payments are traceable on-chain

⚙️ Automation — Smart contract handles everything autonomously

🧾 Compliance — Immutable payroll data for audits and taxes

🛡️ Security — PPoS ensures no forks, double spends, or tampering

🌍 Adaptability — Expandable to royalty systems, DAOs, or freelancer platforms

🔧 Development Stack
Layer	Technology
Smart Contract	PyTeal (Algorand)
Backend	FastAPI + Algorand SDK
Frontend	React / Next.js
Wallets	Pera Wallet / MyAlgo
Blockchain	Algorand TestNet / MainNet
Multi-Chain	Solidity (Foundry / Truffle)
🚀 Deployment
TestNet (Default)

Network: Algorand TestNet

Explorer: AlgoExplorer TestNet

Faucet: Algorand Faucet

MainNet (Production)

Update API URL to MainNet

Fund with real ALGO

Audit contracts (Algorand Foundation recommended)

Deploy backend & frontend for production

