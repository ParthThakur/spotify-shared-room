import React, { Component } from "react";
import { Button, Grid, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";

export default class Room extends Component {
  constructor(props) {
    super(props);

    this.state = {
      votesToSkip: 2,
      guestsCanPause: false,
      isHost: false,
    };
    this.roomCode = this.props.match.params.roomCode;
    this.getRoomDetails();

    this.leaveRoom = this.leaveRoom.bind(this);
  }

  getRoomDetails() {
    fetch(`/api/getRoom?code=${this.roomCode}`)
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          votesToSkip: data.votes_to_skip,
          guestsCanPause: data.guest_can_pause,
          isHost: data.is_host,
        });
      });
  }

  leaveRoom() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code: this.state.roomCode,
      }),
    };
    fetch("/api/leaveRoom", requestOptions).then((response) => {
      console.log(response);
      this.props.history.push("/");
    });
  }

  render() {
    return (
      <Grid container spacing={1} align="center">
        <Grid item xs={12} align="left">
          <h1>Room details:</h1>
          <p>Room code: {this.roomCode}</p>
          <p>Votes: {this.state.votesToSkip}</p>
          <p>Guest can pause: {this.state.guestsCanPause.toString()}</p>
          <p>Host: {this.state.isHost.toString()}</p>
        </Grid>
        <Grid item xs={12}>
          <Button variant="contained" color="default" onClick={this.leaveRoom}>
            Leave Room
          </Button>
        </Grid>
      </Grid>
    );
  }
}
