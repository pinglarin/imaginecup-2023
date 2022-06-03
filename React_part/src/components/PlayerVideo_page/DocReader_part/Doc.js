// import React from 'react';
// import { Document, Page } from 'react-pdf';

// import samplePDF from './Doc/assignment1.pdf';

// const Doc = () => 
// {   return (
//     <Document file={samplePDF}>
//       <Page pageNumber={0} />
//     </Document>
//   );
// };
// export default Doc

//=========================================
import React, { useState } from "react";
import { Document, Page } from "react-pdf";
import { pdfjs } from 'react-pdf';pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

export default function SinglePage(props) {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1); //setting 1 to show fisrt page

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
    setPageNumber(1);
  }

  //For Change Auto in page
  // function SetpagebyBookmark ({ numPages }) {
  //   setNumPages(numPages);
  //   setPageNumber(numPages);
  // }

  function changePage(offset) {
    setPageNumber(prevPageNumber => prevPageNumber + offset);
  }

  // Change page by button
  function previousPage() {
    changePage(-1);
  }
  
  function nextPage() {
    changePage(1);
  }

  const { pdf } = props;
  //console.log("Test")

  return (
    <>
      <Document
        file={pdf}
        // options={{ workerSrc: "/pdf.worker.js" }}
        //options = {{ workerSrc: "../../public/pdf.worker.js"}}
        onLoadSuccess={onDocumentLoadSuccess}
      >
        <Page pageNumber={pageNumber} />
      </Document>
      <div>
        <p>
          Page {pageNumber || (numPages ? 1 : "--")} of {numPages || "--"}
        </p>
        <button type="button" disabled={pageNumber <= 1} onClick={previousPage}>
          Previous
        </button>
        <button
          type="button"
          disabled={pageNumber >= numPages}
          onClick={nextPage}
        >
          Next
        </button>
      </div>
    </>
  );
}
