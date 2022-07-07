import React, { useState } from "react";
import axios from "axios";
import Player from "./Player/Player";
import "video.js/dist/video-js.min.css";
import "videojs-youtube";
import "./Player/Controls";
import "./Player/index";

// My add function
// import Clip from "./VideoExample/OOP P01 CanteenICT Get-Started Session (Bi-Lingual)-20210310 0659-1.mp4";

// const Splitpart = window.location.href.split("/");
// console.log("split");
// console.log(Splitpart);
// const UUID = Splitpart[4];
// console.log(UUID);

export default function VideoMk2() {
  const Splitpart = window.location.pathname.split("/");
  const UUID = Splitpart[2];
  console.log(UUID);
  console.log(`http://127.0.0.1:8000/vid?uuid=${UUID}`);
  // const Myplayer = {};
  // let i = 0;
  let link = "";
  console.log("smth");
  axios
    .get(`http://127.0.0.1:8000/youtube?uuid=${UUID}`)
    .then((response) => {
      console.log("res");
      link = response.data;
      console.log(response);
      console.log(link);
    })
    .catch((error) => console.log(error));
  console.log("link");
  console.log(link);
  const [state /* , setstate */] = useState({
    video: {
      techOrder: "youtube",
      sources: [
        {
          // src: "http://vjs.zencdn.net/v/oceans.mp4",
          // src: Clip,
          // src: "http://127.0.0.1:8000/stream?uuid=8ab5d6e3-16a7-4205-a47a-152151bed883",
          // src: "https://sto010.akamai-cdn-cntent.com/tysxeebv4w66j6cdaa6brqcbgrshewemx7c2pvq7kpmqzvx4lo3vwrj2ptkq/sugar-sugar-rune-episode-1.mp4",

          // for mp4 videos
          // src: `http://127.0.0.1:8000/vid?uuid=${UUID}`,
          // type: "video/mp4",

          // for youtube videos
          // src: "https://www.youtube.com/watch?v=KVybZvrIbOM&list=RDMMKVybZvrIbOM&start_radio=1", from search bar
          // src: "https://youtu.be/UHAcmded2rA",
          src: link, // from sharing
          type: "video/youtube",
        },
      ],
      poster:
        "https://cdn.discordapp.com/attachments/595430234736689173/923864093511798814/167a9d14e5017ffa2d39ac5567f37d30-db6wtbu.jpg",
    },
  });
  console.log("after");

  function onPlayerReady(player) {
    console.log(UUID);
    console.log("Player is ready: ", player);
    // Myplayer = player;
  }

  function onVideoPlay(duration) {
    console.log("Video played at: ", duration);
  }

  function onVideoPause(duration) {
    console.log("Video paused at: ", duration);
  }

  function onVideoTimeUpdate(duration) {
    console.log("Time updated: ", duration);
  }

  function onVideoSeeking(duration) {
    console.log("Video seeking: ", duration);
  }

  function onVideoSeeked(from, to) {
    console.log(`Video seeked from ${from} to ${to}`);
  }

  function onVideoEnd() {
    console.log("Video ended");
  }

  return (
    <div className="App">
      <Player
        controls
        preload="auto"
        src={state.video.sources}
        poster={state.video.poster}
        width="650"
        height="420"
        onReady={onPlayerReady}
        onPlay={onVideoPlay}
        onPause={onVideoPause}
        onTimeUpdate={onVideoTimeUpdate}
        onSeeking={onVideoSeeking}
        onSeeked={onVideoSeeked}
        onEnd={onVideoEnd}
      />
    </div>
  );
}
