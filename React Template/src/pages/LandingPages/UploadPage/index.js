// import Grid from "@mui/material/Grid";

// Material Kit 2 React components
import MKBox from "components/MKBox";
// import MKInput from "components/MKInput";
// import MKButton from "components/MKButton";
// import MKTypography from "components/MKTypography";

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

function Upload() {
  return (
    <>
      <MKBox position="fixed" top="0.5rem" width="100%">
        <DefaultNavbar
          routes={routes}
          action={{
            type: "external",
            route: "https://www.creative-tim.com/product/material-kit-react",
            label: "free download",
            color: "default",
          }}
          sticky
        />
      </MKBox>
      <p> Test Video </p>
      <VideoPlayer />
      <p>Test Timeline</p>
      <Timeline />
      <p>Test Doc Reader</p>
      <Doc pdf={samplePDF} />
    </>
  );
}

export default Upload;
