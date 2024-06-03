import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import AuthPage from './Pages/AuthPage/Authpage';
import FileUpload from './Pages/Fileupload/Fileupload';
import Json from './Pages/Json/Json';
import './App.css';

function App() {
  const [uploadedFile, setUploadedFile] = useState(null); 

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* <Route path="/" element={<AuthPage />} /> */}
          <Route path="/" element={<FileUpload onFileUpload={setUploadedFile} />} />
          <Route path="json" element={<Json file={uploadedFile} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
