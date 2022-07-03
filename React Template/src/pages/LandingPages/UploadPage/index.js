// import Grid from "@mui/material/Grid";

// Material Kit 2 React components
import MKBox from "components/MKBox";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import MKTypography from "components/MKTypography";
import MKButton from "components/MKButton";
import HorizontalTeamCard from "examples/Cards/TeamCards/HorizontalTeamCard";
// import MKInput from "components/MKInput";
import Card from "@mui/material/Card";

// Material Kit 2 React examples
import DefaultNavbar from "examples/Navbars/DefaultNavbar";
// import DefaultFooter from "examples/Footers/DefaultFooter";

// Routes
import routes from "routes";
// import footerRoutes from "footer.routes";

// Image
// import bgImage from "assets/images/illustrations/illustration-reset.jpg";

import Timeline from "./PlayerVideo_page/Timeline_part/Timeline";
import Doc from "./PlayerVideo_page/DocReader_part/Doc";
import samplePDF from "./PlayerVideo_page/DocReader_part/Lec04 Image Matting.pdf";
import VideoPlayer from "./PlayerVideo_page/Player_part/VideoMk2";
import "./PlayerVideo_page/Playvideo.css";

function Upload() {
  const Splitpart = window.location.pathname.split("/");
  const UUID = Splitpart[2];
  console.log(UUID);
  console.log(`http://127.0.0.1:8000/get/lecturename?vuuid=${UUID}`);

  // I DUNNO WUT TO DO
  // const [state /* , setstate */] = useState({
  //   video: {
  //     sources: [
  //       {
  //         src: `http://127.0.0.1:8000/vid?uuid=${UUID}`,
  //         type: "video/mp4",
  //       },
  //     ],
  //     poster:
  //       "https://cdn.discordapp.com/attachments/595430234736689173/923864093511798814/167a9d14e5017ffa2d39ac5567f37d30-db6wtbu.jpg",
  //   },
  // });

  return (
    <>
      {/* <MKBox position="fixed" top="0.5rem" width="100%"> */}
      <DefaultNavbar
        routes={routes}
        action={{
          type: "external",
          route: "https://www.creative-tim.com/product/material-kit-react",
          label: "free download",
          color: "default",
        }}
        // sticky
        transparent
        light
      />
      {/* </MKBox> */}
      {/* Header */}
      <MKBox
        minHeight="75vh"
        width="100%"
        sx={{
          backgroundImage: ({ functions: { linearGradient, rgba }, palette: { gradients } }) =>
            `${linearGradient(
              rgba(gradients.dark.main, 0.6),
              rgba(gradients.dark.state, 0.6)
            )}, url(https://media.discordapp.net/attachments/917582730982723625/936967309866704916/yihao-ren-bai.jpg?width=1440&height=333)`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          display: "grid",
          placeItems: "center",
        }}
      >
        <Container>
          <Grid
            container
            item
            xs={12}
            lg={6}
            justifyContent="center"
            alignItems="center"
            flexDirection="column"
            sx={{ mx: "auto", textAlign: "center" }}
          >
            <MKTypography
              variant="h1"
              color="white"
              sx={({ breakpoints, typography: { size } }) => ({
                [breakpoints.down("md")]: {
                  fontSize: size["3xl"],
                },
              })}
            >
              <br />
              <br />
              Uploader Page
            </MKTypography>
            <MKTypography variant="body1" color="white" opacity={0.8} mt={1} mb={3}>
              We&apos;re constantly trying to express ourselves and actualize our dreams. If you
              have the opportunity to play this game
            </MKTypography>
            <MKButton color="default" sx={{ color: ({ palette: { dark } }) => dark.main }}>
              Buy course
            </MKButton>
            <br />
            <HorizontalTeamCard
              image="https://cdn.discordapp.com/attachments/917582730982723625/990506757220630598/FB_IMG_1560130403592.png"
              name="Created by"
              position={{ label: "Teacher A" }}
              description=" "
            />
            <br />
            <br />
            <br />
          </Grid>
        </Container>
      </MKBox>
      <Card
        sx={{
          p: 2,
          mx: { xs: 2, lg: 3 },
          mt: -8,
          mb: 4,
          boxShadow: ({ boxShadows: { xxl } }) => xxl,
        }}
      >
        <br />
        {/* <br />
        <br />
        <br /> */}
        {/* <div className="PlayerVideo_page">
          <p> Test Video </p>
          <div className="PlayerVideo">
            <VideoPlayer />
          </div>
          <p>Test Timeline</p>
          <Timeline />
          <p>Test Doc Reader</p>
          <div className="Doc">
            <Doc pdf={samplePDF} />
          </div>
        </div> */}
        <Grid container spacing={6}>
          <Grid item xs={6} justifyContent="center" sx={{ mx: "auto", textAlign: "center" }}>
            <MKTypography
              variant="h5"
              color="dark"
              sx={({ breakpoints, typography: { size } }) => ({
                [breakpoints.down("md")]: {
                  fontSize: size["2xl"],
                },
              })}
            >
              Test Video
            </MKTypography>
            <div className="PlayerVideo">
              <VideoPlayer />
            </div>
            <br />
            <MKTypography
              variant="h5"
              color="dark"
              sx={({ breakpoints, typography: { size } }) => ({
                [breakpoints.down("md")]: {
                  fontSize: size["2xl"],
                },
              })}
            >
              <br />
              Test Doc Reader
            </MKTypography>
            <div className="Doc">
              <Grid item xs={14} justifyContent="left" sx={{ mx: "auto", textAlign: "center" }}>
                <Doc pdf={samplePDF} />
              </Grid>
            </div>
          </Grid>
          <Grid item xs={12} lg={6} justifyContent="right" sx={{ mx: "auto", textAlign: "center" }}>
            <MKTypography
              variant="h5"
              color="dark"
              sx={({ breakpoints, typography: { size } }) => ({
                [breakpoints.down("md")]: {
                  fontSize: size["2xl"],
                },
              })}
            >
              Test Timeline
            </MKTypography>
            <Timeline />
          </Grid>
        </Grid>
        {/* <br />
        <br />
        <br />
        <br /> */}
      </Card>
    </>
  );
}

export default Upload;
