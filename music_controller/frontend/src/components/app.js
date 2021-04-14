import React, { Component } from "react";
import { render } from "react-dom";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";

import HomePage from "./HomePage";
import JoinRoomPage from "./JoinRoomPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="center">
        <Router>
          <Switch>
            <Route exact path="/" component={HomePage} />
            <Route exact path="/join" component={JoinRoomPage} />
            <Route exact path="/create" component={CreateRoomPage} />
            <Route path="/room/:roomCode" component={Room} />
          </Switch>
        </Router>
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
