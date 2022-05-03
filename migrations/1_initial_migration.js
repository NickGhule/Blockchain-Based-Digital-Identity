const Migrations = artifacts.require("Migrations");
const digitalID = artifacts.require("digitalID");

module.exports = function (deployer) {
  deployer.deploy(Migrations);
  deployer.deploy(digitalID);
};
