// copied version >> all the ' ' are replaced with " "
import React, { useState } from "react";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import { useModal } from "react-hooks-use-modal";
// import ReactDOM from "react-dom"

// @mui material components
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";

// Material Kit 2 React components
import MKBox from "components/MKBox";
import MKInput from "components/MKInput";
import MKButton from "components/MKButton";
import MKTypography from "components/MKTypography";
import HorizontalTeamCard from "examples/Cards/TeamCards/HorizontalTeamCard";

// Toasts
// import Toast from "react-bootstrap/Toast";
//  const Splitpart = window.location.pathname.split("/");
// const UUID = Splitpart[2];

function DragUploader() {
  // removed props because of 'props' is defined but never used

  const [LectureName, setLectureName] = useState("");
  const [LecturerID, setLecturerID] = useState("");
  const [CourseName, setCourseName] = useState(""); // removed event because error: 'event' is defined but never used

  const [ModalSuccess, openSuccess, closeSuccess] = useModal("root", {
    preventScroll: true,
    closeOnOverlayClick: false,
  });

  const [ModalFail, openFail, closeFail] = useModal("root", {
    preventScroll: true,
    closeOnOverlayClick: false,
  });

  const Uploadvideo = () => {
    const formData = new FormData();
    const uploadfile = document.querySelector("#file");
    formData.append("file", uploadfile.files[0]);
    formData.append("uuid", uuidv4());
    formData.append("LectureName", LectureName); // formData.append("lecture_name", Lecture_name);
    formData.append("LecturerID", LecturerID); // formData.append("lecturer_ID", Lecturer_ID);
    formData.append("CourseName", CourseName); // formData.append("student_ID",Student_ID);
    if (uploadfile.files[0] && LectureName && LecturerID && CourseName) {
      axios
        .post(`http://localhost:8000/uploadvideo/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          // eslint-disable-next-line
          console.log(response);
          openSuccess(true);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          openFail(true);
        });
    } else {
      // eslint-disable-next-line
      alert("Please Inform your data!");
    }
    // for debugging
    console.log("uploading");
    console.log(formData.get("file"));
    console.log(formData.get("uuid"));
    console.log(formData.get("LectureName"));
    console.log(formData.get("LecturerID"));
    console.log(formData.get("CourseName"));
  };
  return (
    <MKBox component="section" py={12}>
      <Container>
        <Grid container item justifyContent="center" xs={10} lg={7} mx="auto" textAlign="center">
          <MKTypography variant="h3" mb={1}>
            Upload page Video Information
          </MKTypography>
        </Grid>
        <Grid container item xs={12} lg={7} sx={{ mx: "auto" }}>
          <MKBox width="100%" component="form" method="post" autocomplete="off">
            <MKBox p={3}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <MKTypography component="a" fontWeight="regular" color="dark">
                    <input type="file" id="file" name="file" />
                  </MKTypography>
                  {/* can I decorate this? */}
                </Grid>
                <Grid item xs={12} md={12}>
                  <MKInput
                    variant="standard"
                    label="Lecture name"
                    placeholder="Enter Lecture name"
                    onChange={(e) => setLectureName(e.target.value)}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <MKInput
                    variant="standard"
                    label="Course Name"
                    placeholder="Enter CourseName"
                    onChange={(e) => setCourseName(e.target.value)}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <MKInput
                    variant="standard"
                    type="number"
                    label="Lecturer ID"
                    placeholder="Enter Lecturer ID"
                    onChange={(e) => setLecturerID(e.target.value)}
                    fullWidth
                  />
                </Grid>
              </Grid>
              <Grid container item justifyContent="center" xs={12} my={2}>
                <MKButton
                  onClick={Uploadvideo}
                  type="submit"
                  href="#"
                  variant="gradient"
                  color="dark"
                  fullWidth
                >
                  Submit
                </MKButton>
              </Grid>
            </MKBox>
          </MKBox>
        </Grid>
      </Container>
      <ModalSuccess>
        <HorizontalTeamCard
          image="https://c.tenor.com/xVfFIHxAzW4AAAAC/success.gif"
          name="Notification"
          position={{ color: "success", label: "Upload Success!" }}
          description=" "
        />
        <MKButton
          onClick={closeSuccess}
          type="submit"
          href="#"
          variant="gradient"
          color="dark"
          fullWidth
        >
          Close
        </MKButton>
      </ModalSuccess>
      <ModalFail>
        <HorizontalTeamCard
          image="https://c.tenor.com/_EOg1bM-P-AAAAAC/fail.gif"
          name="Notification"
          position={{ color: "error", label: "Upload Fail!" }}
          description="Please try agian"
        />
        <MKButton
          onClick={closeFail}
          type="submit"
          href="#"
          variant="gradient"
          color="dark"
          fullWidth
        >
          Close
        </MKButton>
      </ModalFail>
    </MKBox>
  );
}

export default DragUploader;
