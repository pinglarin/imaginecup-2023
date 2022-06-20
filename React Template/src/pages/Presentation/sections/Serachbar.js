// Normal import
import React, { useState } from "react";
// import axios from "axios";

// @mui material components
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import InputAdornment from "@mui/material/InputAdornment";

// @mui icons
import SearchIcon from "@mui/icons-material/Search";

// Material Kit 2 React components
import MKBox from "components/MKBox";
import MKInput from "components/MKInput";
import MKTypography from "components/MKTypography";
import MKButton from "components/MKButton";

function Search() {
  const [UserKeyword, setKeyword] = useState();

  const SendKeysearach = () => {
    const formData = new FormData();
    formData.append("Keyword", UserKeyword);

    if (UserKeyword) {
      console.log(`Ready to send ${UserKeyword}`);
      console.log(formData.get("Keyword"));
    } else {
      // eslint-disable-next-line
      alert("Please Inform your Keyword!");
    }
    // for debugging
    console.log("uploading");
  };

  return (
    <MKBox component="section" py={12}>
      <Container>
        <Grid container item justifyContent="center" xs={10} lg={7} mx="auto" textAlign="center">
          <MKTypography variant="h3" mb={1}>
            Search bar
          </MKTypography>
        </Grid>
        <Grid container item xs={12} lg={4} py={1} mx="auto">
          <MKInput
            variant="standard"
            label="Search bar"
            fontSize="large"
            placeholder="input course name, etc."
            fullWidth
            onChange={(e) => setKeyword(e.target.value)}
            InputProps={{
              endAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="medium" />
                </InputAdornment>
              ),
            }}
          />
        </Grid>
        <br />
        <Grid container item xs={12} lg={2} py={1} mx="auto">
          <MKButton variant="gradient" color="info" onClick={SendKeysearach} fullWidth>
            Search
          </MKButton>
        </Grid>
      </Container>
    </MKBox>
  );
}

export default Search;
