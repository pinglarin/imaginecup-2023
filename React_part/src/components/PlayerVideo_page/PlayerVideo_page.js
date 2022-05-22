import React from 'react'

import VideoMk2 from "./Player_part/VideoMk2";
import Timeline from "./Timeline_part/Timeline";
import Doc from "./DocReader_part/Doc"
import samplePDF from './DocReader_part/Lec04 Image Matting.pdf';
import video from "./Player_part/OOP P01 CanteenICT Get-Started Session (Bi-Lingual)-20210310 0659-1.mp4";

import "./Playvideo.css";
function PlayerVideo_page() {
  
  return (
    <div className="PlayerVideo_page">
      <h1>This is PlayerVideo Area</h1>
      <br></br>
        <div className="PlayerVideo">
          <VideoMk2  src={video}/>
        </div>
      <br></br>
      <Timeline/>
      <br></br>
      <div className="Doc">
        <Doc pdf={samplePDF} />
      </div>

    </div>
  );
}

export default PlayerVideo_page;
