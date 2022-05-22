import React, {useMemo} from 'react';
import {useDropzone} from 'react-dropzone';
import { useState } from "react";
import Button from 'react-bootstrap/Button'
//CSS
const baseStyle = {
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: '20px',
  borderWidth: 2,
  borderRadius: 2,
  borderColor: '#eeeeee',
  borderStyle: 'dashed',
  backgroundColor: '#fafafa',
  color: '#bdbdbd',
  outline: 'none',
  transition: 'border .24s ease-in-out'
};
  
const focusedStyle = {
  borderColor: '#2196f3'
};

const acceptStyle = {
  borderColor: '#00e676'
};

const rejectStyle = {
  borderColor: '#ff1744'
};



function Drag_Uploader(props) {
  const {
    acceptedFiles,
    fileRejections,
    getRootProps,
    getInputProps,
    isFocused,
    isDragAccept,
    isDragReject
  } = useDropzone({
    accept: {
      'video/*': ['.mp4', '.mp3']
    },
    maxFiles:1
  });

  const acceptedFileItems = acceptedFiles.map(file => (
    <li key={file.path}>
      {file.path} - {file.size} bytes
    </li>
  ));

  const fileRejectionItems = fileRejections.map(({ file, errors }) => (
    <li key={file.path}>
      {file.path} - {file.size} bytes
      <ul>
        {errors.map(e => (
          <li key={e.code}>{e.message}</li>
        ))}
      </ul>
    </li>
  ));

  const style = useMemo(() => ({
    ...baseStyle,
    ...(isFocused ? focusedStyle : {}),
    ...(isDragAccept ? acceptStyle : {}),
    ...(isDragReject ? rejectStyle : {})
  }), [
    isFocused,
    isDragAccept,
    isDragReject
  ]);

  const Uploadvideo = (event) => 
  {
    var Datavideo = {acceptedFileItems};
    // fetch('http://localhost:3001/AllData/:id', 
    // {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //         "accept": "application/json"
    //     },
    //     "body": JSON.stringify({                     
    //         Select_ID_Data: {
    //             p_id: Product_ID                           
    //         }
    //     })
    // })
    //     .then(response => response.json())
    //     .then(response => {
    //         console.log(response);
    //         setSelctedID_Data(response);
    //         console.log(SelctedID_Data);
    //     })
    //     .catch((error) => {
    //         console.error(error);
    //   });  
    console.log("Test Upload");
    console.log({acceptedFileItems});
    console.log(Datavideo.acceptedFileItems[0]._source.fileName);
  }


    

  return (
    <section className="container">
      <div {...getRootProps({style})}>
        <input {...getInputProps()}/>
        <p>Drag 'n' drop some files here, or click to select files</p>
        <em>(Only *.mp3 or *.mp4 video will be accepted)</em>
      </div>
      <aside>
        <h4>Accepted files</h4>
        <ul>{acceptedFileItems}</ul>
        <h4>Rejected files</h4>
        <ul>{fileRejectionItems}</ul>
      </aside>
      <Button onClick={Uploadvideo}>Submit</Button>
    </section>
  );
}

export default Drag_Uploader;