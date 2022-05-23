import React, { useEffect } from "react";
import PropTypes from "prop-types";
import videoJs from "video.js";
import "videojs-markers";
import "videojs-markers/dist/videojs.markers.css";

import Controls from "./Controls";

var markers = [
  {
    time: 600,
    text: "Testing topic A", 
  },
  {
    time: 1200,
    text: "Testing topic B", 
  },
  {
    time: 2400,
    text: "Testing topic C", 
  },
  {
    time: 3600,
    text: "Testing topic D", 
  }  
 
];

const EditableMarkers = ({ text }) => {
  return <div>{text}</div>;
};

const Player = (props) => {
  // generate uniq identifier
  const playerId = `video-player-${new Date() * 1}`;
  let player = {};

  // set visibility for controls options
  const set_controls_visibility = (player, hidden_controls) => {
    // eslint-disable-next-line array-callback-return
    Object.keys(Controls).map((x) => {
      player.controlBar[Controls[x]].show();
    });
    if (hidden_controls) {
      // eslint-disable-next-line array-callback-return
      hidden_controls.map((x) => {
        player.controlBar[Controls[x]].hide();
      });
    }
  };
  // generate player options from props
  const generate_player_options = (props) => {
    const playerOptions = {};
    playerOptions.controls = props.controls;
    playerOptions.autoplay = props.autoplay;
    playerOptions.preload = props.preload;
    playerOptions.width = props.width;
    playerOptions.height = props.height;
    playerOptions.bigPlayButton = props.bigPlayButton;
    const hidePlaybackRates =
      props.hidePlaybackRates !== null ||
      props.hideControls.includes("playbackrates");
    if (!hidePlaybackRates) playerOptions.playbackRates = props.playbackRates;
    return playerOptions;
  };

  // init Player
  const init_player = () => {
    const playerOptions = generate_player_options(props);
    player = videoJs(document.querySelector(`#${playerId}`), playerOptions);
    player.src(props.src);
    player.poster(props.poster);
    set_controls_visibility(player, props.hideControls);
  };

  const init_player_events = (props) => {
    let currentTime = 0;
    let previousTime = 0;
    let position = 0;

    player.ready(() => {
      props.onReady(player);
      window.player = player;
    });
    player.on("play", () => {
      props.onPlay(player.currentTime());
    });
    player.on("pause", () => {
      props.onPause(player.currentTime());
    });
    // eslint-disable-next-line no-unused-vars
    player.on("timeupdate", (e) => {
      props.onTimeUpdate(player.currentTime());
      previousTime = currentTime;
      currentTime = player.currentTime();
      if (previousTime < currentTime) {
        position = previousTime;
        previousTime = currentTime;
      }
    });
    player.on("seeking", () => {
      player.off("timeupdate", () => {});
      player.one("seeked", () => {});
      props.onSeeking(player.currentTime());
      console.log(player.currentTime())
    });

    player.on("seeked", () => {
      const completeTime = Math.floor(player.currentTime());
      props.onSeeked(position, completeTime);
    });
    player.on("ended", () => {
      props.onEnd();
    });
  };

  useEffect(() => {
    init_player(props);
    init_player_events(props);

    // add markers
    let video = videoJs(`${playerId}`);
    video.markers({
      markerStyle: {
        width: "8px",
        "background-color": "red",
      },
      markerTip: {
        display: true,
        html: function (marker) {
          return <EditableMarkers text={marker.text} />;
        },
      },
      breakOverlay: {
        display: true,
        displayTime: 3,
        text: function (marker) {
          return marker.text;
        },
      },
      onMarkerReached: function (marker) {
        console.log(marker);
      },
      markers: markers,
    });

    return () => player.dispose();
  }, []);

  useEffect(() => {
    set_controls_visibility(player, props.hideControls);

    init_player(props);
  }, [props.src]);

  return (
    // eslint-disable-next-line jsx-a11y/media-has-caption
    <video
      id={playerId}
      className={`video-js ${
        props.bigPlayButtonCentered ? "vjs-big-play-centered" : ""
      } ${props.className}`}
    />
  );
};

Player.propTypes = {
  src: PropTypes.string,
  poster: PropTypes.string,
  controls: PropTypes.bool,
  autoplay: PropTypes.bool,
  preload: PropTypes.oneOf(["auto", "none", "metadata"]),
  width: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  height: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  hideControls: PropTypes.arrayOf(PropTypes.string),
  bigPlayButton: PropTypes.bool,
  bigPlayButtonCentered: PropTypes.bool,
  onReady: PropTypes.func,
  onPlay: PropTypes.func,
  onPause: PropTypes.func,
  onTimeUpdate: PropTypes.func,
  onSeeking: PropTypes.func,
  onSeeked: PropTypes.func,
  onEnd: PropTypes.func,
  playbackRates: PropTypes.arrayOf(PropTypes.number),
  hidePlaybackRates: PropTypes.bool,
  className: PropTypes.string,
};

Player.defaultProps = {
  src: "",
  poster: "",
  controls: true,
  autoplay: false,
  preload: "auto",
  playbackRates: [0.5, 1, 1.5, 2],
  hidePlaybackRates: false,
  className: "",
  hideControls: [],
  bigPlayButton: true,
  bigPlayButtonCentered: true,
  onReady: () => {},
  onPlay: () => {},
  onPause: () => {},
  onTimeUpdate: () => {},
  onSeeking: () => {},
  onSeeked: () => {},
  onEnd: () => {},
};

export default Player;
