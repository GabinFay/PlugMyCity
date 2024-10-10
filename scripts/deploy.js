const hre = require("hardhat");

async function main() {
    // Deploy the contract
    const HouseCraftsmanPlatform = await hre.ethers.getContractFactory("HouseCraftsmanPlatform");
    const houseCraftsmanPlatform = await HouseCraftsmanPlatform.deploy();
    
    // Wait for the deployment to be confirmed
    await houseCraftsmanPlatform.waitForDeployment();

    console.log("HouseCraftsmanPlatform deployed to:", await houseCraftsmanPlatform.getAddress());
}

main()
    .catch((error) => {
        console.error(error);
        process.exitCode = 1;
    });