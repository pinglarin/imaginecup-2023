import React, {useMemo} from 'react';
import {useDropzone} from 'react-dropzone';
import Button from 'react-bootstrap/Button';
import axios from 'axios';
import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';
import { useState } from "react";
import { v4 as uuidv4 } from 'uuid';


// //CSS
// const baseStyle = {
//   flex: 1,
//   display: 'flex',
//   flexDirection: 'column',
//   alignItems: 'center',
//   padding: '20px',
//   borderWidth: 2,
//   borderRadius: 2,
//   borderColor: '#eeeeee',
//   borderStyle: 'dashed',
//   backgroundColor: '#fafafa',
//   color: '#bdbdbd',
//   outline: 'none',
//   transition: 'border .24s ease-in-out'
// };
  
// const focusedStyle = {
//   borderColor: '#2196f3'
// };

// const acceptStyle = {
//   borderColor: '#00e676'
// };

// const rejectStyle = {
//   borderColor: '#ff1744'
// };

// function Drag_Uploader(props) {
//   const {
//     acceptedFiles,
//     fileRejections,
//     getRootProps,
//     getInputProps,
//     isFocused,
//     isDragAccept,
//     isDragReject
//   } = useDropzone({
//     accept: {
//       'video/*': ['.mp4', '.mp3']
//     },
//     maxFiles:1
//   });

//   const acceptedFileItems = acceptedFiles.map(file => (
//     <li key={file.path}>
//       {file.path} - {file.size} bytes
//     </li>
//   ));

//   const fileRejectionItems = fileRejections.map(({ file, errors }) => (
//     <li key={file.path}>
//       {file.path} - {file.size} bytes
//       <ul>
//         {errors.map(e => (
//           <li key={e.code}>{e.message}</li>
//         ))}
//       </ul>
//     </li>
//   ));

//   const style = useMemo(() => ({
//     ...baseStyle,
//     ...(isFocused ? focusedStyle : {}),
//     ...(isDragAccept ? acceptStyle : {}),
//     ...(isDragReject ? rejectStyle : {})
//   }), [
//     isFocused,
//     isDragAccept,
//     isDragReject
//   ]);

//   const [Data,setData] = useState([]); 

//   const Uploadvideo = (event) => 
//   {
//     // var Datavideo = {acceptedFileItems};
//     // fetch('http://localhost:3001/AllData/:id', 
//     // {
//     //     method: 'POST',
//     //     headers: {
//     //         'Content-Type': 'application/json',
//     //         "accept": "application/json"
//     //     },
//     //     "body": JSON.stringify({                     
//     //         Select_ID_Data: {
//     //             p_id: Product_ID                           
//     //         }
//     //     })
//     // })
//     //     .then(response => response.json())
//     //     .then(response => {
//     //         console.log(response);
//     //         setSelctedID_Data(response);
//     //         console.log(SelctedID_Data);
//     //     })
//     //     .catch((error) => {
//     //         console.error(error);
//     //   });  
//     // console.log("Test Upload");
//     // console.log({acceptedFileItems});
//     // console.log(Datavideo.acceptedFileItems[0]._source.fileName);
//     axios.post('upload_file', Data, {
//       headers: {
//         'Content-Type': 'multipart/form-data'
//       }
//   })
//     console.log(Data);
//   }


    

//   return (
//     <section className="container">
//       {/* <div {...getRootProps({style})}>
//         <input {...getInputProps()}/>
//         <p>Drag 'n' drop some files here, or click to select files</p>
//         <em>(Only *.mp3 or *.mp4 video will be accepted)</em>
//       </div>
//       <aside>
//         <h4>Accepted files</h4>
//         <ul>{acceptedFileItems}</ul>
//         <h4>Rejected files</h4>
//         <ul>{fileRejectionItems}</ul>
//       </aside>
//       <Button onClick={Uploadvideo}>Submit</Button> */}
//       <input type="file" onChange={(e) => setData(e.target.value)}></input>
//       <Button onClick={Uploadvideo}>Submit</Button>
//     </section>
//   );
// }

function Drag_Uploader(props) {  

  const [Lecture_name,setLecture_name] = useState(""); 
  const [Lecturer_ID,setLecturer_ID] = useState(""); 
  const [Student_ID,setStudent_ID] = useState(""); 
  const Uploadvideo = (event) => 
  {
    var formData = new FormData();
    var uploadfile = document.querySelector('#file');    
    formData.append("file", uploadfile.files[0]); 
    formData.append("uuid", uuidv4());   
    formData.append("lecture_name", Lecture_name);
    formData.append("lecturer_ID", Lecturer_ID);
    formData.append("student_ID",Student_ID);

    


    if(uploadfile.files[0]&&Lecture_name&&Lecturer_ID&&Student_ID)
    {
      axios.post('http://localhost:8000/uploadvideo', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.error(error);
      });    

    }
    else
    {
      alert("Please Inform your data!")
    }  



    // Display the values
    for (var value of formData.values()) {
      console.log(value);
    }
  
  }   
  return (
    <section className="container">      

      <Form>
        <Form.Group className="mb-3">
          <Form.Label>Lecture name</Form.Label>
          <Form.Control placeholder="Enter lecture_name" onChange={(e) => setLecture_name(e.target.value)}/>         
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Lecturer ID</Form.Label>
          <Form.Control type="number" placeholder="Enter Lecturer ID" onChange={(e) => setLecturer_ID(e.target.value)} />
        </Form.Group>  

         <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Student ID</Form.Label>
          <Form.Control type="number" placeholder="Student ID" onChange={(e) => setStudent_ID(e.target.value)} />
        </Form.Group>  

        <p>Test UUID V4 : {uuidv4()}</p>   

      </Form>      

      <input type="file" id="file" name="file"></input>
      <br></br>
      <br></br>
      <Button onClick={Uploadvideo}>Submit</Button>
      
    </section>
  );
}

export default Drag_Uploader;
