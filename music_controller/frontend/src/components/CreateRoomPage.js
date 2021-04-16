import React, { Component } from "react";
import {
  Button,
  ButtonGroup,
  Collapse,
  FormControl,
  FormHelperText,
  FormControlLabel,
  Grid,
  Radio,
  RadioGroup,
  TextField,
  Typography,
} from "@material-ui/core";
import { Link } from "react-router-dom";
import Alert from "@material-ui/lab/Alert";

export default class CreateRoomPage extends Component {
  static defaultProps = {
    votesToSkip: 2,
    guestCanPause: false,
    hostNickName: "Anon",
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
      hostNickName: this.props.hostNickName,
      hostName: "Anonymous",
      isHostNickNameValid: true,
      backButtonText: "Cancel",
      message: "",
      isError: false,
    };

    this.handleCreateRoomPressed = this.handleCreateRoomPressed.bind(this);
    this.handleUpdateRoomPressed = this.handleUpdateRoomPressed.bind(this);
    this.handleVotesChange = this.handleVotesChange.bind(this);
    this.handleGuestCanPauseChange = this.handleGuestCanPauseChange.bind(this);
    this.handleHostNickNameChange = this.handleHostNickNameChange.bind(this);
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

  handleHostNickNameChange(e) {
    if (e.target.value.length <= 32) {
      this.setState({
        isHostNickNameValid: true,
        hostNickName: e.target.value === "" ? "Anon" : e.target.value,
      });
    } else {
      this.setState({
        isHostNickNameValid: false,
      });
    }
  }

  handleCreateRoomPressed() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: this.state.votesToSkip,
        guest_can_pause: this.state.guestCanPause,
        nick_name: this.state.hostNickName,
        name: this.state.hostName,
        update: false,
      }),
    };
    console.log(requestOptions);
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
        nick_name: this.state.hostNickName,
        name: "Anonymous",
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
    let HOST_NICK_NAME = "Anon";
    let HOST_NAME = "Anonymous";

    if (this.props.update) {
      TITLE = "Update Room";
      BUTTONS = this.updateButtons;
      PLAY_PAUSE_DEFAULT = this.props.guest_can_pause.toString();
      VOTES_TO_SKIP = this.props.votes_to_skip;
      HOST_NICK_NAME = this.props.hostNickName;
    }

    return (
      <Grid container spacing={1} align="center">
        <Grid item xs={12}>
          <Typography component={"h4"} variant="h4">
            {TITLE}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <FormControl>
            <FormHelperText>Guest control of playback:</FormHelperText>
            <RadioGroup
              defaultValue={PLAY_PAUSE_DEFAULT}
              onChange={this.handleGuestCanPauseChange}
            >
              <FormControlLabel
                value="true"
                control={<Radio color="primary" />}
                label="Play/Pause"
              />
              <FormControlLabel
                value="false"
                control={<Radio color="secondary" />}
                label="No Control"
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12}>
          <FormControl>
            <FormHelperText>Votes required to skip song:</FormHelperText>
            <TextField
              required={true}
              type="number"
              onChange={this.handleVotesChange}
              defaultValue={VOTES_TO_SKIP}
              inputProps={{
                min: 0,
              }}
            />
          </FormControl>
        </Grid>
        <Grid item xs={12}>
          <FormControl>
            <FormHelperText>Choose a nick name</FormHelperText>
            <TextField
              required={false}
              type="text"
              onChange={this.handleHostNickNameChange}
              placeholder={HOST_NICK_NAME}
              inputProps={{ maxLength: 32 }}
            />
          </FormControl>
        </Grid>
        <Grid item xs={12}>
          <FormControl>
            <FormHelperText>Full Name</FormHelperText>
            <TextField
              required={false}
              type="text"
              onChange={() => {}}
              placeholder={HOST_NAME}
              inputProps={{ maxLength: 32 }}
            />
          </FormControl>
        </Grid>
        <Grid item xs={12}>
          {BUTTONS()}
        </Grid>
        <Grid item xs={12}>
          <Collapse in={this.state.message != ""}>
            <Alert
              severity={this.state.isError ? "error" : "success"}
              onClose={() => {
                this.setState({ message: "" });
              }}
            >
              {this.state.message}
            </Alert>
          </Collapse>
        </Grid>
      </Grid>
    );
  }
}
