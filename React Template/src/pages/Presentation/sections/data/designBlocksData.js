/*
=========================================================
* Material Kit 2 React - v2.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-kit-react
* Copyright 2021 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/
import axios from "axios";

const imagesPrefix = "https://cdn.discordapp.com/attachments/917582730982723625";
// https://cdn.discordapp.com/attachments/917582730982723625/983667848545202206/FB_IMG_1558676210120.jpgconst

const ExportData = [
  {
    title: "Example Course",
    description: "Just for test all video in fastapi",
    items: [
      {
        image: `${imagesPrefix}/983667449650114611/IMG_20181130_234218.jpg`,
        name: "LockVideoExample",
        count: 691140,
        pro: true,
      },
    ],
  },
  {
    title: "Navigation",
    description: "30+ components that will help go through the pages",
    items: [
      {
        image: `${imagesPrefix}/983667848545202206/FB_IMG_1558676210120.jpg`,
        name: "Navbars",
        count: 4,
        route: "/sections/navigation/navbars",
      },
      {
        image: `${imagesPrefix}/983667848545202206/FB_IMG_1558676210120.jpg`,
        name: "Nav Tabs",
        count: 2,
        route: "/sections/navigation/nav-tabs",
      },
      {
        image: `${imagesPrefix}/983667848545202206/FB_IMG_1558676210120.jpg`,
        name: "Pagination",
        count: 3,
        route: "/sections/navigation/pagination",
      },
    ],
  },
];

function RefreshData() {
  let i = 0;
  axios
    .get("http://localhost:8000/getallvideos")
    .then((response) => {
      console.log(response);
      console.log(ExportData);
      console.log(ExportData[0].items);
      console.log(response.data[0].LectureName);
      for (i = 0; i < response.data.length; i += 1) {
        ExportData[0].items.push({
          image: `${imagesPrefix}/983667449650114611/IMG_20181130_234218.jpg`,
          name: response.data[i].LectureName,
          count: response.data[i].uuid,
          route: `VideoPlayer/${response.data[i].uuid}`,
        });
      }
      // ExportData[0].items.push({
      //   image: `${imagesPrefix}/983667449650114611/IMG_20181130_234218.jpg`,
      //   name: response.data[0].LectureName,
      //   count: 10,
      //   route: `/pages/landing-pages/UploadPage/${response.data[0].uuid}`,
      // });
      console.log("==============");
      console.log(ExportData);
    })
    .catch((error) => console.log(error));
}

RefreshData();

export default ExportData;
