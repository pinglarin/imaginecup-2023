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

function InputIcon() {
  return (
    <MKBox component="section" py={12}>
      <Container>
        <Grid container item justifyContent="center" xs={10} lg={7} mx="auto" textAlign="center">
          <MKTypography variant="h3" mb={1}>
            Search
          </MKTypography>
        </Grid>
        <Grid container item xs={12} lg={4} py={1} mx="auto">
          <MKInput
            variant="standard"
            label="Search"
            fontSize="large"
            placeholder="input course name, etc."
            fullWidth
            InputProps={{
              endAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="medium" />
                </InputAdornment>
              ),
            }}
          />
        </Grid>
      </Container>
    </MKBox>
  );
}

export default InputIcon;
