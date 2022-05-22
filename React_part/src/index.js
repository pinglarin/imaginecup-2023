import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css'
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";


import Header from './components/Navbar'
// import Login_page from './components/Login_part/Login'
import Search_page from './components/Search_part/Search_page'
import Search_page_ShowID from './components/Search_part/Show'
import UploadVideo_page from './components/Uploader_part/Uploader_page'
import LearningUI_page from './components/PlayerVideo_page/PlayerVideo_page'

ReactDOM.render(
  <React.StrictMode>
      <Router>
        <Header/>
      <Switch>
        
        <Route exact path="/" component={App} />
        {/* <Route path="/login" component={Login_page} /> */}
        <Route path="/Search_page" component={Search_page} />
        <Route path="/UploadVideo" component={UploadVideo_page} />
        <Route path="/LearningUI" component={LearningUI_page} />
        
      </Switch>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);


