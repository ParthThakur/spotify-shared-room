import React, { Component } from "react";

export default class Room extends Component {
  constructor(props) {
    super(props);

    this.state = {
      votesToSkip: 2,
      guestsCanPause: false,
      isHost: false,
    };
    this.roomCode = this.props.match.params.roomCode;
  }

  render() {
    return (
      <div>
        <h1>Room details:</h1>
        <p>Room code: {this.roomCode}</p>
        <p>Votes: {this.state.votesToSkip}</p>
        <p>Guest can pause: {this.state.guestsCanPause}</p>
        <p>Host: {this.state.isHost}</p>
      </div>
    );
  }
}
