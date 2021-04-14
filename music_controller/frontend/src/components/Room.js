import React, { Component } from "react";
import { Button, ButtonGroup, Grid, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";

import CreateRoomPage from "./CreateRoomPage";

export default class Room extends Component {
  constructor(props) {
    super(props);

    this.state = {
      votesToSkip: 2,
      guestsCanPause: false,
      isHost: false,
      showSettings: false,
    };
    this.roomCode = this.props.match.params.roomCode;
    this.getRoomDetails();

    this.leaveRoom = this.leaveRoom.bind(this);
    this.toggleSettings = this.toggleSettings.bind(this);
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
      this.props.history.push("/");
    });
  }

  toggleSettings() {
    this.setState((prevState) => ({
      showSettings: !prevState.showSettings,
    }));
  }

  showSettingsButton() {
    return (
      <Button variant="contained" color="default" onClick={this.toggleSettings}>
        Settings
      </Button>
    );
  }

  renderSettings() {
    return (
      <Grid container spacing={1} align="center">
        <Grid item xs={12}>
          <CreateRoomPage
            update={true}
            votes_to_skip={this.state.votesToSkip}
            guest_can_pause={this.state.guestsCanPause}
            room_code={this.roomCode}
            updateCallback={() => {}}
          />
        </Grid>
      </Grid>
    );
  }

  render() {
    if (this.state.showSettings) {
      return this.renderSettings();
    } else {
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
            <ButtonGroup>
              <Button
                variant="contained"
                color="default"
                onClick={this.leaveRoom}
              >
                Leave Room
              </Button>
              {this.state.isHost ? this.showSettingsButton() : null}
            </ButtonGroup>
          </Grid>
        </Grid>
      );
    }
  }
}
