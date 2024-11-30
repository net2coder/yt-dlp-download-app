import express from 'express';
import ytDlp from 'yt-dlp-exec';  // Use yt-dlp-exec
import bodyParser from 'body-parser';
import fs from 'fs';
import path from 'path';
import os from 'os';

const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.json());
app.use(express.static('public')); // Serving files in 'public' folder

// Get the default Downloads directory based on the operating system
const getDownloadsFolder = () => {
  if (os.platform() === 'win32') {
    return path.join(os.homedir(), 'Downloads');
  } else if (os.platform() === 'darwin') {
    return path.join(os.homedir(), 'Downloads');
  } else if (os.platform() === 'linux') {
    return path.join(os.homedir(), 'Downloads');
  } else {
    return path.join(__dirname, 'downloads');
  }
};

// POST endpoint to download video
app.post('/download', (req, res) => {
  const { url, format } = req.body;

  if (!url) {
    return res.status(400).send('URL is required');
  }

  const downloadPath = getDownloadsFolder();

  if (!fs.existsSync(downloadPath)) {
    fs.mkdirSync(downloadPath, { recursive: true });
  }

  // Construct the command for yt-dlp
  const outputFilePath = path.join(downloadPath, '%(title)s.%(ext)s');
  const command = `yt-dlp -o "${outputFilePath}" ${url}`;

  // Execute yt-dlp command to download the video
  ytDlp(url, { output: outputFilePath })
    .then((output) => {
      console.log('Download complete:', output);

      // Extract the video filename (you may need to adjust based on yt-dlp output format)
      const videoFileName = output.match(/Destination: (.*\.mp4)/)[1]; // This regex assumes mp4, adjust for other formats

      // Send the response with the download link
      res.json({
        message: 'Download started successfully!',
        downloadLink: `http://localhost:3000/download/${path.basename(videoFileName)}`
      });
    })
    .catch((err) => {
      console.error('Download error:', err);
      res.status(500).send(`Download error: ${err.message}`);
    });
});

// Serve the video file for user download
app.get('/download/:filename', (req, res) => {
  const filename = req.params.filename;
  const filePath = path.join(getDownloadsFolder(), filename);

  // Check if the file exists and serve it
  if (fs.existsSync(filePath)) {
    res.download(filePath, filename, (err) => {
      if (err) {
        console.error('Error downloading the file:', err);
        res.status(500).send('Error downloading the file');
      }
    });
  } else {
    res.status(404).send('File not found');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
