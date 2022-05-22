import React, { useState } from "react";
import { Player } from "./Player";
import "video.js/dist/video-js.min.css";
// My add function
import Clip from "./OOP P01 CanteenICT Get-Started Session (Bi-Lingual)-20210310 0659-1.mp4";

export default function VideoMk2()  
{
  const Myplayer = {};
  const videoSrc = Clip;
  
  const [state, setstate] = useState({
    video: {
      src: "http://vjs.zencdn.net/v/oceans.mp4",
      //src: require("./OOP P01 CanteenICT Get-Started Session (Bi-Lingual)-20210310 0659-1.mp4"),  
      //src: require(videoSrc),            
      poster:
      "https://cdn.discordapp.com/attachments/595430234736689173/923864093511798814/167a9d14e5017ffa2d39ac5567f37d30-db6wtbu.jpg"
    }
  });

  function onPlayerReady(player) {
    console.log("Player is ready: ", player);
    player = Myplayer;
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
        controls={true}
        src={state.video.src}
        poster={state.video.poster}
        width="650"
        height="420"
        // onReady={onPlayerReady}
        // onPlay={onVideoPlay}
        // onPause={onVideoPause}
        // onTimeUpdate={onVideoTimeUpdate}
        onSeeking={onVideoSeeking}
        onSeeked={onVideoSeeked}
        onEnd={onVideoEnd}        
      />      
    </div>    
  );
};
