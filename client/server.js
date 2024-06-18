const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 5000;
const storage = multer.diskStorage({
  destination: function(req, file, cb) {
    cb(null, 'uploads/')
  },
  filename: function(req, file, cb) {
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname))
  }
});

const upload = multer({ storage: storage });
app.use(cors());
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
app.post('/upload', upload.single('file'), (req, res) => {
  console.log(req.file); // Uploaded file information
  
  // Run Python script
  exec('python your_script.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  });
  res.json({ message: 'File uploaded successfully.' });
});

app.get('/get-json', (req, res) => {
  const jsonFilePath = path.join(__dirname, 'uploads', 'your-json-file.json'); // Replace 'your-json-file.json' with your actual JSON file name
  fs.readFile(jsonFilePath, 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      res.status(500).json({ message: 'Failed to read JSON file.' });
      return;
    }

    try {
      const jsonData = JSON.parse(data);
      res.json(jsonData);
    } catch (err) {
      console.error(err);
      res.status(500).json({ message: 'Failed to parse JSON file.' });
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});