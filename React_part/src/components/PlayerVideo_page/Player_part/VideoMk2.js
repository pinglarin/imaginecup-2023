import React, { useState } from "react";

import { Player } from "./Player";
import "video.js/dist/video-js.min.css";

// My add function

// import Clip from "../../../../../sqlite3_videos/uploadedVideos/5d10ddea-111b-4fe7-b043-8777c6132014.mp4"
import Clip from "./uploadedVideos/bd13c986-f8e9-480f-80ec-9b284dfda3de.mp4"

export default function VideoMk2()  
{
  const Myplayer = {};  
  const [state, setstate] = useState({
    video: {     
      sources: [{
        //src: "http://vjs.zencdn.net/v/oceans.mp4",      
        src: Clip,
        type: 'video/mp4'
      }],
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
        src={state.video.sources}
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
