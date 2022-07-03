import React from "react";

import "./Timeline.css";

export default function Timeline() {
  return (
    <div className="container">
      <div className="row">
        <div className="col-md-12">
          <div className="card">
            <div className="card-body">
              <h6 className="card-title">Topic Timeline in video</h6>
              <div id="content">
                <ul className="timeline">
                  <li className="event" data-date="10:00:00">
                    {/* Pass value Line */}
                    <a href="#Vid">Topic A</a>
                    <p>Get here on time, its first come first serve. Be late, get turned away.</p>
                  </li>
                  <li className="event" data-date="20:00:00">
                    <a href="#Vid">Topic B</a>
                    <p>abcd</p>
                  </li>
                  <li className="event" data-date="30:00:00">
                    <a href="#Vid">Topic C</a>
                    <p>abcd</p>
                  </li>
                  <li className="event" data-date="40:00:00">
                    <a href="#Vid">Topic D</a>
                    <p>A12</p>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
