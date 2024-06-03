import React, { useState } from 'react';
import { Document, Page } from 'react-pdf';
import { styled } from '@mui/material/styles';
import Header from '../../Components/Header/Header';
import './Json.css';
import localJsonData from './phi3_output2.json';
import samplePdf from './partnertest.pdf';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  backgroundColor: '#0B2CA3', // 배경색 설정
  color: 'white', // 글씨색 설정
  fontWeight: 'bold' // 글씨를 굵게
}));

function Json({ file }) {
  const [jsonData, setJsonData] = useState(Object.entries(localJsonData).map(([key, value]) => ({ id: key, ...value })));
  const [pdfFileUrl, setPdfFileUrl] = useState(samplePdf);

  useState(() => {
    if (file && file.type === 'application/pdf') {
      const pdfFileUrl = URL.createObjectURL(file);
      setPdfFileUrl(pdfFileUrl);
    } else {
      alert('Uploaded file is not a PDF.');
    }
  }, [file]);

  const renderTable = (data) => {
  return (
    <TableContainer component={Paper}>
      <Table>
        <TableBody>
          {data.map((section) => (
            Object.entries(section).map(([key, value], index) => {
              if (key === 'id') {
                return (
                  <TableRow key={index}>
                    <StyledTableCell align="left" colSpan={3}>Section {value}</StyledTableCell>
                  </TableRow>
                );
              } else {
                return (
                  <TableRow key={index}>
                    <TableCell align="left">{key}</TableCell>
                    <TableCell align="left">{value.toString()}</TableCell>
                  </TableRow>
                );
              }
            })
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

  return (
    <>
      <Header />
      <div className="json-page-container">
        <div className="json-split-container">
          <div className="json-pdf-container">
            <object data={pdfFileUrl} type="application/pdf" width="100%" height="100%">
              <p>Alternative text - include a link <a href="http://africau.edu/images/default/sample.pdf">to the PDF!</a></p>
            </object>
          </div>
          <div className="json-json-container">
            <h1>JSON Content</h1>
            {renderTable(jsonData)}
          </div>
        </div>
      </div>
    </>
  );
}

export default Json;