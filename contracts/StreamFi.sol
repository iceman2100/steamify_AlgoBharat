// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract StreamFi {
    struct Stream {
        address sender;
        address recipient;
        uint256 startTime;
        uint256 ratePerSecond;
        uint256 lastClaimTime;
        bool isActive;
    }

    mapping(address => Stream) public streams;

    function startStream(address _recipient, uint256 _ratePerSecond) external {
        require(streams[_recipient].isActive == false, "Stream already active");
        streams[_recipient] = Stream({
            sender: msg.sender,
            recipient: _recipient,
            startTime: block.timestamp,
            ratePerSecond: _ratePerSecond,
            lastClaimTime: block.timestamp,
            isActive: true
        });
    }

    function claimStream() external {
        Stream storage stream = streams[msg.sender];
        require(stream.isActive, "No active stream");

        uint256 elapsed = block.timestamp - stream.lastClaimTime;
        uint256 amount = elapsed * stream.ratePerSecond;
        stream.lastClaimTime = block.timestamp;

        payable(msg.sender).transfer(amount);
    }

    function pauseStream(address _recipient) external {
        Stream storage stream = streams[_recipient];
        require(stream.sender == msg.sender, "Only sender can pause");
        stream.isActive = false;
    }

    receive() external payable {}
}
