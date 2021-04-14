import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Collapse from "@material-ui/core/Collapse";

export default class CreateRoomPage extends Component {
  static defaultProps = {
    votesToSkip: 2,
    guestCanPause: false,
    update: false,
    roomCode: null,
    updateCallback: () => {},
    goBack: () => {},
  };

  constructor(props) {
    super(props);
    this.state = {
      guestCanPause: this.props.guestCanPause,
      votesToSkip: this.props.votesToSkip,
      backButtonText: "Cancel",
      message: "",
      isError: false,
    };

    this.handleCreateRoomPressed = this.handleCreateRoomPressed.bind(this);
    this.handleUpdateRoomPressed = this.handleUpdateRoomPressed.bind(this);
    this.handleVotesChange = this.handleVotesChange.bind(this);
    this.handleGuestCanPauseChange = this.handleGuestCanPauseChange.bind(this);
    this.createButtons = this.createButtons.bind(this);
    this.updateButtons = this.updateButtons.bind(this);
  }

  handleVotesChange(e) {
    this.setState({
      votesToSkip: e.target.value,
    });
  }

  handleGuestCanPauseChange(e) {
    this.setState({
      guestCanPause: e.target.value === "true" ? true : false,
    });
  }

  handleCreateRoomPressed() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: this.state.votesToSkip,
        guest_can_pause: this.state.guestCanPause,
      }),
    };
    fetch("/api/createRoom", requestOptions)
      .then((response) => response.json())
      .then((data) => this.props.history.push(`/room/${data.code}`));
  }

  handleUpdateRoomPressed() {
    const requestOptions = {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: this.state.votesToSkip,
        guest_can_pause: this.state.guestCanPause,
        code: this.props.room_code,
      }),
    };
    fetch("/api/updateRoom", requestOptions)
      .then((response) => response.json())
      .then((response) => {
        if (response["Success"]) {
          this.props.updateCallback();
          this.setState({
            message: response["Success"],
            backButtonText: "Go back",
          });
        } else {
          this.setState({
            message: response["Error"],
            isError: true,
          });
        }
      });
  }

  createButtons() {
    return (
      <ButtonGroup>
        <Button
          color="primary"
          variant="contained"
          onClick={this.handleCreateRoomPressed}
        >
          Create A Room
        </Button>
        <Button color="secondary" variant="contained" to="/" component={Link}>
          Cancel
        </Button>
      </ButtonGroup>
    );
  }

  updateButtons() {
    return (
      <ButtonGroup>
        <Button
          color="primary"
          variant="contained"
          onClick={this.handleUpdateRoomPressed}
        >
          Save settings
        </Button>
        <Button
          color="secondary"
          variant="contained"
          onClick={this.props.goBack}
        >
          {this.state.backButtonText}
        </Button>
      </ButtonGroup>
    );
  }

  render() {
    let TITLE = "Create a Room";
    let BUTTONS = this.createButtons;
    let PLAY_PAUSE_DEFAULT = "false";
    let VOTES_TO_SKIP = 2;

    if (this.props.update) {
      TITLE = "Update Room";
      BUTTONS = this.updateButtons;
      PLAY_PAUSE_DEFAULT = this.props.guest_can_pause.toString();
      VOTES_TO_SKIP = this.props.votes_to_skip;
    }

    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Typography component={"h4"} variant="h4">
            {TITLE}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl component="fieldset">
            <FormHelperText>Guest Control of Playback State</FormHelperText>
            <RadioGroup
              row
              defaultValue={PLAY_PAUSE_DEFAULT}
              onChange={this.handleGuestCanPauseChange}
            >
              <FormControlLabel
                value="true"
                control={<Radio color="primary" />}
                label="Play/Pause"
                labelPlacement="bottom"
              />
              <FormControlLabel
                value="false"
                control={<Radio color="secondary" />}
                label="No Control"
                labelPlacement="bottom"
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl>
            <TextField
              required={true}
              type="number"
              onChange={this.handleVotesChange}
              defaultValue={VOTES_TO_SKIP}
              inputProps={{
                min: 1,
                style: { textAlign: "center" },
              }}
            />
            <FormHelperText>Votes Required To Skip Song</FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          {BUTTONS()}
        </Grid>
        <Grid item xs={12} align="center">
          <Collapse in={this.state.message != ""}>
            {this.state.message}
          </Collapse>
        </Grid>
      </Grid>
    );
  }
}
