import React, { useState } from "react";
import './Timeline.css';
export default function Timeline()
{       
    return(    
    <div class="container">
    <div class="row">
        <div class="col-md-12">
            <div class="card">
                <div class="card-body">
                    <h6 class="card-title">Topic Timeline in video</h6>
                    <div id="content">
                        <ul class="timeline">
                            <li class="event" data-date="10:00:00">
                                {/* Pass value Line */}
                                <a href="#Vid">Topic A</a>                                
                                <p>Get here on time, it's first come first serve. Be late, get turned away.</p>
                            </li>
                            <li class="event" data-date="20:00:00">
                                <a href="#Vid">Topic B</a>
                                <p>Get ready for an exciting event, this will kick off in amazing fashion with MOP &amp; Busta Rhymes as an opening show.</p>
                            </li>
                            <li class="event" data-date="30:00:00">
                                <a href="#Vid">Topic C</a>
                                <p>This is where it all goes down. You will compete head to head with your friends and rivals. Get ready!</p>
                            </li>
                            <li class="event" data-date="40:00:00">
                                <a href="#Vid">Topic D</a>
                                <p>See how is the victor and who are the losers. The big stage is where the winners bask in their own glory.</p>
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
  
