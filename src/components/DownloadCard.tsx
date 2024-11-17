import React, { useState } from 'react';
import { Download, Link as LinkIcon, Loader2 } from 'lucide-react';
import Swal from 'sweetalert2';

interface DownloadCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  supportedFormats: string[];
  variant: 'youtube' | 'instagram' | 'pinterest' | 'linkedin' | 'twitter' | 'snapchat';
}

const DownloadCard: React.FC<DownloadCardProps> = ({
  title,
  description,
  icon,
  supportedFormats,
  variant,
}) => {
  const [url, setUrl] = useState('');
  const [selectedFormat, setSelectedFormat] = useState(supportedFormats[0]);
  const [loading, setLoading] = useState(false);

  // Handle file download logic
  const handleDownload = async (response: Response) => {
    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    // Use the correct file extension based on format
    link.download = `download.${variant === 'youtube' && selectedFormat.includes('MP3') ? 'mp3' : 'mp4'}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // URL validation
    if (!url.trim()) {
      Swal.fire({
        icon: 'error',
        title: 'Invalid URL',
        text: 'Please enter a valid URL',
        confirmButtonColor: '#4F46E5',
      });
      return;
    }

    setLoading(true);

    try {
      // Make the request to backend
      const response = await fetch(`http://localhost:5000/api/download/${variant}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url.trim(),
          format: selectedFormat, // Sent format as selected format
          type: selectedFormat,   // Ensure this matches what backend expects
          quality: selectedFormat, // Same as above
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        // Handle JSON response (error or success message from backend)
        const data = await response.json();
        if (data.error) {
          throw new Error(data.error);
        }
        Swal.fire({
          icon: 'success',
          title: 'Success!',
          text: 'Content downloaded successfully',
          confirmButtonColor: '#4F46E5',
        });
      } else {
        // Handle file download if the response is not JSON
        await handleDownload(response);
        Swal.fire({
          icon: 'success',
          title: 'Download Complete!',
          text: 'Your content has been downloaded successfully.',
          confirmButtonColor: '#4F46E5',
        });
      }
    } catch (error) {
      console.error('Download error:', error);
      Swal.fire({
        icon: 'error',
        title: 'Download Failed',
        text: error instanceof Error ? error.message : 'An unexpected error occurred',
        confirmButtonColor: '#DC2626',
      });
    } finally {
      setLoading(false);
    }
  };

  const variants = {
    youtube: {
      gradient: 'from-red-500 to-red-700',
      iconColor: 'text-red-600',
      buttonBg: 'bg-red-600 hover:bg-red-700',
      ringColor: 'focus:ring-red-600 focus:border-red-600',
    },
    instagram: {
      gradient: 'from-pink-500 via-purple-500 to-indigo-500',
      iconColor: 'text-pink-600',
      buttonBg: 'bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500 hover:from-pink-600 hover:via-purple-600 hover:to-indigo-600',
      ringColor: 'focus:ring-purple-600 focus:border-purple-600',
    },
    pinterest: {
      gradient: 'from-red-600 to-red-800',
      iconColor: 'text-red-700',
      buttonBg: 'bg-red-700 hover:bg-red-800',
      ringColor: 'focus:ring-red-700 focus:border-red-700',
    },
    linkedin: {
      gradient: 'from-blue-600 to-blue-800',
      iconColor: 'text-blue-700',
      buttonBg: 'bg-blue-700 hover:bg-blue-800',
      ringColor: 'focus:ring-blue-700 focus:border-blue-700',
    },
    twitter: {
      gradient: 'from-sky-400 to-sky-600',
      iconColor: 'text-sky-500',
      buttonBg: 'bg-sky-500 hover:bg-sky-600',
      ringColor: 'focus:ring-sky-500 focus:border-sky-500',
    },
    snapchat: {
      gradient: 'from-yellow-400 to-yellow-600',
      iconColor: 'text-yellow-500',
      buttonBg: 'bg-yellow-500 hover:bg-yellow-600',
      ringColor: 'focus:ring-yellow-500 focus:border-yellow-500',
    },
  };

  const currentVariant = variants[variant];

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden transform transition-all hover:scale-105">
      <div className={`h-2 bg-gradient-to-r ${currentVariant.gradient}`} />
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold text-gray-900">{title}</h3>
          <div className={currentVariant.iconColor}>{icon}</div>
        </div>
        
        <p className="text-gray-600 mb-6">{description}</p>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <LinkIcon className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste URL here"
              className={`block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-2 ${currentVariant.ringColor}`}
              required
              disabled={loading}
            />
          </div>
          
          <select
            value={selectedFormat}
            onChange={(e) => setSelectedFormat(e.target.value)}
            className={`block w-full px-3 py-2 border border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-2 ${currentVariant.ringColor}`}
            disabled={loading}
          >
            {supportedFormats.map((format) => (
              <option key={format} value={format}>
                {format}
              </option>
            ))}
          </select>
          
          <button
            type="submit"
            disabled={loading}
            className={`w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-white ${currentVariant.buttonBg} focus:outline-none focus:ring-2 focus:ring-offset-2 ${currentVariant.ringColor} disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            {loading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <>
                <Download className="h-5 w-5 mr-2" />
                Download
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default DownloadCard;
