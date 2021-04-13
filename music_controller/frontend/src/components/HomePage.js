import React, { Component } from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";
import {
  TextField,
  Button,
  Grid,
  Typography,
  ButtonGroup,
} from "@material-ui/core";

import JoinRoomPage from "./JoinRoomPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";

export default class HomePage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      room_code: false,
    };
  }

  async componentDidMount() {
    fetch("/api/userInRoom")
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          room_code: data.code,
        });
      });
  }

  joinCurrentRoom() {
    if (this.state.room_code) {
      return (
        <Button
          color="default"
          to={`/room/${this.state.room_code}`}
          component={Link}
        >
          Join previous room
        </Button>
      );
    }
    return null;
  }

  renderHomePage() {
    return (
      <Grid container spacing={3} align="center">
        <Grid item xs={12}>
          <Typography variant="h3" compact="h3">
            House Party
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <ButtonGroup disableElevation variant="contained" color="primary">
            <Button color="primary" to="/join" component={Link}>
              Join a Room
            </Button>
            <Button color="secondary" to="/create" component={Link}>
              Create a Room
            </Button>
          </ButtonGroup>
        </Grid>
        <Grid item xs={12}>
          {this.joinCurrentRoom()}
        </Grid>
      </Grid>
    );
  }

  render() {
    return (
      <Router>
        <Switch>
          <Route exact path="/">
            {this.renderHomePage()}
          </Route>
          <Route exact path="/join" component={JoinRoomPage} />
          <Route exact path="/create" component={CreateRoomPage} />
          <Route path="/room/:roomCode" component={Room} />
        </Switch>
      </Router>
    );
  }
}
