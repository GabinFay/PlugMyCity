require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

// const PRIVATE_KEY = process.env.PRIVATE_KEY;

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.20",
  networks: {
    avalancheL1: {
      url: "https://upgraded-capybara-jqvrj5vxg9jcqxj7-9650.app.github.dev/ext/bc/finalblockchain/rpc",
      accounts: ["56289e99c94b6912bfc12adc093c9b51124f0dc54ac7a766b2bc5ccf558d8027"],
      chainId: 1234
    }
  }
};