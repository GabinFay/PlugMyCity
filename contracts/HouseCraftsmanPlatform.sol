// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract HouseCraftsmanPlatform is ERC721 {
    uint256 private _nextTokenId;

    struct House {
        address owner;
        string details;
        bool needsCraftsman;
        string craftmanField;
    }

    struct WorkOrder {
        uint256 houseId;
        address craftsman;
        uint256 quotation;
        bool accepted;
        bool completed;
    }

    mapping(uint256 => House) public houses;
    mapping(uint256 => WorkOrder) public workOrders;
    mapping(uint256 => uint256) public escrows;

    event HouseCreated(uint256 tokenId, address owner);
    event CraftsmanNeeded(uint256 tokenId, string field);
    event QuotationMade(uint256 tokenId, address craftsman, uint256 amount);
    event WorkOrderAccepted(uint256 tokenId, address craftsman);
    event WorkCompleted(uint256 tokenId);
    event PaymentReleased(uint256 tokenId, address craftsman, uint256 amount);

    constructor() ERC721("HouseNFT", "HNFT") {
        _nextTokenId = 1;
    }

    function createHouse(string memory _details) public {
        uint256 newTokenId = _nextTokenId;
        _nextTokenId++;
        _safeMint(msg.sender, newTokenId);

        houses[newTokenId] = House(msg.sender, _details, false, "");
        emit HouseCreated(newTokenId, msg.sender);
    }

    function requestCraftsman(uint256 _tokenId, string memory _field) public {
        require(ownerOf(_tokenId) == msg.sender, "Not the house owner");
        houses[_tokenId].needsCraftsman = true;
        houses[_tokenId].craftmanField = _field;
        emit CraftsmanNeeded(_tokenId, _field);
    }

    function makeQuotation(uint256 _tokenId, uint256 _amount) public {
        require(houses[_tokenId].needsCraftsman, "No craftsman needed");
        workOrders[_tokenId] = WorkOrder(_tokenId, msg.sender, _amount, false, false);
        emit QuotationMade(_tokenId, msg.sender, _amount);
    }

    function acceptQuotation(uint256 _tokenId) public payable {
        require(ownerOf(_tokenId) == msg.sender, "Not the house owner");
        require(msg.value == workOrders[_tokenId].quotation, "Incorrect payment amount");

        workOrders[_tokenId].accepted = true;
        escrows[_tokenId] = msg.value;
        emit WorkOrderAccepted(_tokenId, workOrders[_tokenId].craftsman);
    }

    function completeWork(uint256 _tokenId) public {
        require(workOrders[_tokenId].craftsman == msg.sender, "Not the assigned craftsman");
        workOrders[_tokenId].completed = true;
        emit WorkCompleted(_tokenId);
    }

    function releasePayment(uint256 _tokenId) public {
        require(ownerOf(_tokenId) == msg.sender, "Not the house owner");
        require(workOrders[_tokenId].completed, "Work not completed");

        address payable craftsman = payable(workOrders[_tokenId].craftsman);
        uint256 payment = escrows[_tokenId];
        escrows[_tokenId] = 0;
        craftsman.transfer(payment);

        emit PaymentReleased(_tokenId, craftsman, payment);
    }
}
