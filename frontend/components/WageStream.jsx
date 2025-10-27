import algosdk from 'algosdk';
import { useState } from 'react';

const WageStream = () => {
  const [hours, setHours] = useState(0);
  const client = new algosdk.Algodv2('your_token', 'https://testnet-api.algonode.cloud', '');

  const streamWage = async () => {
    // Call backend API
    const response = await fetch('/disburse_wage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hours })
    });
    const result = await response.json();
    // Fetch worker balance
    const balance = await client.accountInformation('WORKER_ADDRESS').do();
    console.log('New balance:', balance.assets[0]?.amount);
    alert(`Wage streamed! TX: ${result.tx_id}`);
  };

  return (
    <div>
      <input type="number" onChange={(e) => setHours(e.target.value)} placeholder="Hours worked" />
      <button onClick={streamWage}>Stream Wage</button>
    </div>
  );
};

export default WageStream;
