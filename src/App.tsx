import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Youtube, Instagram, Image, Linkedin, Twitter, Camera } from 'lucide-react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import DownloadCard from './components/DownloadCard';
import TelegramBot from './components/TelegramBot';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Contact from './pages/Contact';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/" element={
            <>
              {/* Hero Section */}
              <div className="pt-16 bg-gradient-to-br from-indigo-600 to-purple-600">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 text-center">
                  <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
                    Download Tree (VMGET)
                  </h1>
                  <p className="text-xl text-indigo-100 max-w-2xl mx-auto">
                    Your ultimate solution for downloading content from various social media platforms.
                  </p>
                </div>
              </div>

              {/* Main Content */}
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  <DownloadCard
                    title="YouTube Downloader"
                    description="Download videos and audio from YouTube in various qualities and formats."
                    icon={<Youtube className="h-6 w-6" />}
                    supportedFormats={['MP4 - 1080p', 'MP4 - 720p', 'MP4 - 480p', 'MP3 Audio']}
                    variant="youtube"
                  />
                  
                  <DownloadCard
                    title="Instagram Downloader"
                    description="Download stories, reels, highlights, and posts from Instagram."
                    icon={<Instagram className="h-6 w-6" />}
                    supportedFormats={['Video', 'Image', 'Story', 'Reel', 'Highlight']}
                    variant="instagram"
                  />
                  
                  <DownloadCard
                    title="Pinterest Downloader"
                    description="Download high-quality images and videos from Pinterest."
                    icon={<Image className="h-6 w-6" />}
                    supportedFormats={['Original Quality', 'High Quality', 'Medium Quality']}
                    variant="pinterest"
                  />

                  <DownloadCard
                    title="LinkedIn Downloader"
                    description="Download videos, images, and posts from LinkedIn."
                    icon={<Linkedin className="h-6 w-6" />}
                    supportedFormats={['Video', 'Image', 'Post']}
                    variant="linkedin"
                  />

                  <DownloadCard
                    title="Twitter Downloader"
                    description="Download videos and images from Twitter posts."
                    icon={<Twitter className="h-6 w-6" />}
                    supportedFormats={['High Quality', 'Medium Quality', 'Low Quality']}
                    variant="twitter"
                  />

                  <DownloadCard
                    title="Snapchat Downloader"
                    description="Download stories and spotlight content from Snapchat."
                    icon={<Camera className="h-6 w-6" />}
                    supportedFormats={['Story', 'Spotlight', 'Snap']}
                    variant="snapchat"
                  />
                </div>

                {/* Telegram Bot Section */}
                <div className="mt-16">
                  <TelegramBot />
                </div>
              </div>
            </>
          } />
        </Routes>

        <Footer />
      </div>
    </Router>
  );
}

export default App;