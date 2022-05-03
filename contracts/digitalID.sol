// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

/// @title Digital ID
/// @author Nikhil Ghule
/// @notice Adds new document hashes to blockchain and maintains history of all documents
/// @dev Explain to a developer any extra details

contract digitalID {
    
    struct ID {
        string userName;
        mapping (string => string[]) documentsHash;
    }

    mapping (string => ID) public userInfo;

    function getDocumentHashHistory(string memory _userName, string memory _documentName) public view returns (string[] memory) {
        return userInfo[_userName].documentsHash[_documentName];
    }

    function addDocumentHash(string memory _userName, string memory _documentName, string memory _documentHash) public {
        userInfo[_userName].documentsHash[_documentName].push(_documentHash);
    }
}

