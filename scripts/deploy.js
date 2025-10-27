const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  // Deploy StreamFiToken
  console.log("Deploying StreamFiToken...");
  const StreamFiToken = await hre.ethers.getContractFactory("StreamFiToken");
  const streamFiToken = await StreamFiToken.deploy();
  await streamFiToken.waitForDeployment();
  const tokenAddress = await streamFiToken.getAddress();
  console.log("StreamFiToken deployed to:", tokenAddress);

  // Deploy StreamFi
  console.log("Deploying StreamFi...");
  const StreamFi = await hre.ethers.getContractFactory("StreamFi");
  const streamFi = await StreamFi.deploy();
  await streamFi.waitForDeployment();
  const streamFiAddress = await streamFi.getAddress();
  console.log("StreamFi deployed to:", streamFiAddress);

  // Fund the StreamFi contract with tokens
  const mintAmount = hre.ethers.parseUnits("1000000", 18); // 1 million tokens
  console.log("Minting tokens to StreamFi contract...");
  await streamFiToken.mint(streamFiAddress, mintAmount);
  console.log("StreamFi contract funded with 1,000,000 SFT");

  // Save contract addresses
  const addresses = {
    streamFiToken: tokenAddress,
    streamFi: streamFiAddress
  };

  // Create frontend directory if it doesn't exist
  const frontendDir = path.join(__dirname, "..", "frontend");
  if (!fs.existsSync(frontendDir)) {
    fs.mkdirSync(frontendDir, { recursive: true });
  }

  // Write addresses to frontend/contracts.json
  const addressesPath = path.join(frontendDir, "contracts.json");
  fs.writeFileSync(
    addressesPath,
    JSON.stringify(addresses, null, 2)
  );
  console.log("Contract addresses saved to frontend/contracts.json");

  // Update the frontend index.html with contract addresses
  const indexPath = path.join(frontendDir, "index.html");
  if (fs.existsSync(indexPath)) {
    let indexHtml = fs.readFileSync(indexPath, "utf8");
    indexHtml = indexHtml.replace(
      "const streamFiAddress = '';",
      `const streamFiAddress = '${streamFiAddress}';`
    );
    indexHtml = indexHtml.replace(
      "const streamFiTokenAddress = '';",
      `const streamFiTokenAddress = '${tokenAddress}';`
    );
    fs.writeFileSync(indexPath, indexHtml);
    console.log("Updated contract addresses in frontend/index.html");
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });