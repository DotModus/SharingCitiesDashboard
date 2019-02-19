import React from "react";
import PropTypes from 'prop-types';
import Typography from "@material-ui/core/Typography";
import Header from './../common/Header';
import GridLayout from './GridLayout';
import Button from '@material-ui/core/Button';

// material-ui
import { withStyles } from '@material-ui/core/styles';

import {saveLayout} from "./../../actions/dashboardActions";
import {initializeEditor} from "../../actions/widgetActions";
import {connect} from "react-redux";

const styles = (theme) => ({
  root: {
    display: 'flex',
  },
  content: {
    flexGrow: 1,
    //backgroundColor: theme.palette.background.default,
    paddingTop: theme.spacing.unit * 4,
    paddingBottom: theme.spacing.unit * 3,
    paddingLeft: theme.spacing.unit * 1,
    paddingRight: theme.spacing.unit * 1,
    height: '100vh',
    overflow: 'auto'
  },
  appBarSpacer: theme.mixins.toolbar,
  saveLayoutBar: {
    background: "#212121",
    width: "100%",
    position: "fixed",
    bottom: 0,
    padding: "15px",
    textAlign: "center"
  },
  saveLayoutButton: {
    backgroundColor: "#79e8cb"
  }
});

class DashboardPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      loginModalOpen: false
    }
  }

  showSaveLayout() {
    const { classes, dashboard } = this.props;

    if (dashboard.layoutChanged > 1) {
      return (
        <div className={classes.saveLayoutBar}>
          <Button variant="contained" color="primary" onClick={this.props.saveLayout}>
            Save New Layout
          </Button>
        </div>
      )
    } else {
      return null
    }
  }

  render() {
    const { classes, location } = this.props;

    return (
      <div className={classes.root}>
        <Header location={location} />
        <main className={classes.content}>
          <div className={classes.appBarSpacer} />
          <GridLayout />
        </main>
        {this.showSaveLayout()}
      </div>
    )
  }
}

DashboardPage.propTypes = {
  classes: PropTypes.object.isRequired,
};

const mapStateToProps = (state) => ({
  dashboard: state.dashboard,
});

const mapDispatchToProps = (dispatch) => ({
  initializeEditor: () => dispatch(initializeEditor()),
  saveLayout: () => dispatch(saveLayout()),
});

DashboardPage = withStyles(styles)(DashboardPage);
DashboardPage = connect(mapStateToProps, mapDispatchToProps)(DashboardPage);

export default DashboardPage
