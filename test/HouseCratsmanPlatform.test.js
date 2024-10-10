const { expect } = require("chai");

describe("HouseCraftsmanPlatform", function () {
  let HouseCraftsmanPlatform, houseCraftsmanPlatform, owner, addr1, addr2;

  beforeEach(async function () {
    HouseCraftsmanPlatform = await ethers.getContractFactory("HouseCraftsmanPlatform");
    [owner, addr1, addr2] = await ethers.getSigners();
    houseCraftsmanPlatform = await HouseCraftsmanPlatform.deploy();
    await houseCraftsmanPlatform.deployed();
  });

  it("Should create a house and emit event", async function () {
    await expect(houseCraftsmanPlatform.createHouse("Test House"))
      .to.emit(houseCraftsmanPlatform, "HouseCreated")
      .withArgs(1, owner.address);
  });

  // Add more tests for other functions
});