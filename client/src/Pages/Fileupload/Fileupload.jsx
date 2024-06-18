import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../Components/Header/Header';
import './Fileupload.css';

function FileUpload({ onFileUpload }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState('No file chosen');
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setFileName(file.name);
    }
  };

  const handleButtonClick = () => {
    document.getElementById('fileInput').click();
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    alert('Please wait for the system to process the file. Close this box to continue. This may take a while.');
    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Upload successful:', data);
        alert('File uploaded successfully!');
        onFileUpload(selectedFile);
        navigate('/json');
      } else {
        const errorText = await response.text();
        throw new Error(errorText || 'Upload failed');
      }
    } catch (error) {
      console.error('Error during upload:', error);
      alert('An error occurred during file upload: ' + error.message);
    }
  };

  return (
    <>
      <Header />
      <div className="file-upload-container">
        <h1>PDF Uploader</h1>
        <div className="upload-area">
          <p>Select PDF to upload</p>
          <input
            type="file"
            id="fileInput"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
          <button onClick={handleButtonClick}>Choose Files</button>
          <span>{fileName}</span>
        </div>
        <button className="generate-btn" onClick={handleUpload}>Generate JSON</button>
      </div>
    </>
  );
}

export default FileUpload;