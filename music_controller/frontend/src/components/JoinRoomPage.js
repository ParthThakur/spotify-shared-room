import React, { Component } from "react";
import { TextField, Button, Grid, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";

export default class JoinRoomPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      roomCode: "",
      error: null,
    };
  }

  render() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Typography variant="h4" component={"h4"}>
            Join a room:
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <TextField
            error={this.state.error} // TODO: Mateiral-ui expects a boolean.
            label="Code"
            placeholder="Enter a room code"
            value={this.state.roomCode}
            helperText={this.state.error}
            variant="outlined"
          />
        </Grid>
        <Grid item xs={12} align="center">
          <Button variant="contained" color="primary">
            Enter
          </Button>
        </Grid>
        <Grid item xs={12} align="center">
          <Button variant="contained" color="secondary" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }
}
