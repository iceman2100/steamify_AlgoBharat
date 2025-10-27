const StreamFi = artifacts.require("StreamFi");
const StreamFiToken = artifacts.require("StreamFiToken");

module.exports = async function(deployer) {
  // Deploy StreamFiToken first
  await deployer.deploy(StreamFiToken);
  const tokenInstance = await StreamFiToken.deployed();
  
  // Deploy StreamFi with token address
  await deployer.deploy(StreamFi, tokenInstance.address);
  
  // Save contract addresses to a file
  const fs = require('fs');
  const contracts = {
    streamFi: StreamFi.address,
    streamFiToken: StreamFiToken.address
  };
  
  fs.writeFileSync(
    './frontend/contracts.json',
    JSON.stringify(contracts, null, 2)
  );
};