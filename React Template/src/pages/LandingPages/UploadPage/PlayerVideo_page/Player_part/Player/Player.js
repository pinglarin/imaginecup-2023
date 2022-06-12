import React, { useEffect } from "react";
import PropTypes, { string } from "prop-types";
import videoJs from "video.js";
import "videojs-markers";
import "videojs-markers/dist/videojs.markers.css";

import Controls from "./Controls";

const markers = [
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
  },
];

const EditableMarkers = ({ text }) => <div>{text}</div>;
EditableMarkers.defaultProps = {
  text: "",
};

EditableMarkers.propTypes = {
  text: string,
};

const Player = (props) => {
  // generate uniq identifier
  const playerId = `video-player-${new Date() * 1}`;
  let player = {};

  // set visibility for controls options
  const setControlsVisibility = (Player_, hiddenControls) => {
    // eslint-disable-next-line array-callback-return
    Object.keys(Controls).map((x) => {
      Player_.controlBar[Controls[x]].show();
    });
    if (hiddenControls) {
      // eslint-disable-next-line array-callback-return
      hiddenControls.map((x) => {
        Player_.controlBar[Controls[x]].hide();
      });
    }
  };
  // generate player options from props
  const generatePlayerOptions = (props_) => {
    const playerOptions = {};
    playerOptions.controls = props_.controls;
    playerOptions.autoplay = props_.autoplay;
    playerOptions.preload = props_.preload;
    playerOptions.width = props_.width;
    playerOptions.height = props_.height;
    playerOptions.bigPlayButton = props_.bigPlayButton;
    const hidePlaybackRates =
      props_.hidePlaybackRates !== null || props_.hideControls.includes("playbackrates");
    if (!hidePlaybackRates) playerOptions.playbackRates = props_.playbackRates;
    return playerOptions;
  };

  // init Player
  const initPlayer = () => {
    const playerOptions = generatePlayerOptions(props);
    player = videoJs(document.querySelector(`#${playerId}`), playerOptions);
    player.src(props.src);
    player.poster(props.poster);
    setControlsVisibility(player, props.hideControls);
  };

  const initPlayerEvents = (Props) => {
    let currentTime = 0;
    let previousTime = 0;
    let position = 0;

    player.ready(() => {
      Props.onReady(player);
      window.player = player;
    });
    player.on("play", () => {
      Props.onPlay(player.currentTime());
    });
    player.on("pause", () => {
      Props.onPause(player.currentTime());
    });
    // eslint-disable-next-line no-unused-vars
    player.on("timeupdate", (e) => {
      Props.onTimeUpdate(player.currentTime());
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
      Props.onSeeking(player.currentTime());
      console.log(player.currentTime());
    });

    player.on("seeked", () => {
      const completeTime = Math.floor(player.currentTime());
      Props.onSeeked(position, completeTime);
    });
    player.on("ended", () => {
      Props.onEnd();
    });
  };

  useEffect(() => {
    initPlayer(props);
    initPlayerEvents(props);

    // add markers
    const video = videoJs(`${playerId}`);
    video.markers({
      markerStyle: {
        width: "8px",
        "background-color": "red",
      },
      markerTip: {
        display: true,
        html(marker) {
          const { text } = marker;
          return <EditableMarkers text={text} />;
        },
      },
      breakOverlay: {
        display: true,
        displayTime: 3,
        text(marker) {
          return marker.text;
        },
      },
      onMarkerReached(marker) {
        console.log(marker);
      },
      markers,
    });

    return () => player.dispose();
  }, []);

  Player.propTypes = {
    src: PropTypes.string,
    poster: PropTypes.string,
    // controls: PropTypes.bool,
    // autoplay: PropTypes.bool,
    // preload: PropTypes.oneOf(["auto", "none", "metadata"]),
    // width: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    // height: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    hideControls: PropTypes.arrayOf(PropTypes.string),
    // bigPlayButton: PropTypes.bool,
    bigPlayButtonCentered: PropTypes.bool,
    // onReady: PropTypes.func,
    // onPlay: PropTypes.func,
    // onPause: PropTypes.func,
    // onTimeUpdate: PropTypes.func,
    // onSeeking: PropTypes.func,
    // onSeeked: PropTypes.func,
    // onEnd: PropTypes.func,
    // playbackRates: PropTypes.arrayOf(PropTypes.number),
    // hidePlaybackRates: PropTypes.bool,
    className: PropTypes.string,
  };

  Player.defaultProps = {
    src: "",
    poster: "",
    // controls: true,
    // autoplay: false,
    // preload: "auto",
    // playbackRates: [0.5, 1, 1.5, 2],
    // hidePlaybackRates: false,
    className: "",
    hideControls: [],
    // bigPlayButton: true,
    bigPlayButtonCentered: true,
    // onReady: () => {},
    // onPlay: () => {},
    // onPause: () => {},
    // onTimeUpdate: () => {},
    // onSeeking: () => {},
    // onSeeked: () => {},
    // onEnd: () => {},
  };

  const { hideControls, src, bigPlayButtonCentered, className } = props;
  useEffect(() => {
    setControlsVisibility(player, hideControls);
    initPlayer(props);
  }, [src]);

  return (
    // eslint-disable-next-line jsx-a11y/media-has-caption
    <video
      id={playerId}
      className={`video-js ${bigPlayButtonCentered ? "vjs-big-play-centered" : ""}
        ${className}
      `}
    />
  );
};

export default Player;
