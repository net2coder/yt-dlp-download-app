import React, { useState } from 'react';
import { Menu, X, Download, User, UserPlus } from 'lucide-react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <nav className="bg-gradient-to-r from-purple-600 to-indigo-600 fixed w-full z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <Download className="h-8 w-8 text-white" />
              <span className="ml-2 text-xl font-bold text-white">VMGET</span>
            </Link>
          </div>

          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <Link to="/" className="text-white hover:bg-indigo-500 px-3 py-2 rounded-md">Home</Link>
              <button
                onClick={() => setIsModalOpen(true)}
                className="text-white hover:bg-indigo-500 px-3 py-2 rounded-md"
              >
                Tools
              </button>
              <Link to="/contact" className="text-white hover:bg-indigo-500 px-3 py-2 rounded-md">Contact</Link>
              <Link to="/login" className="bg-white text-indigo-600 px-4 py-2 rounded-md font-medium hover:bg-indigo-50 transition-colors">
                <User className="inline-block w-4 h-4 mr-2" />
                Login
              </Link>
              <Link to="/signup" className="bg-indigo-800 text-white px-4 py-2 rounded-md font-medium hover:bg-indigo-700 transition-colors">
                <UserPlus className="inline-block w-4 h-4 mr-2" />
                Sign Up
              </Link>
            </div>
          </div>

          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-white hover:text-gray-200"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden bg-indigo-700">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <Link to="/" className="text-white block px-3 py-2 rounded-md">Home</Link>
            <button
              onClick={() => setIsModalOpen(true)}
              className="text-white block px-3 py-2 rounded-md w-full text-left"
            >
              Tools
            </button>
            <Link to="/contact" className="text-white block px-3 py-2 rounded-md">Contact</Link>
            <Link to="/login" className="block w-full text-left bg-white text-indigo-600 px-3 py-2 rounded-md font-medium">
              <User className="inline-block w-4 h-4 mr-2" />
              Login
            </Link>
            <Link to="/signup" className="block w-full text-left bg-indigo-800 text-white px-3 py-2 rounded-md font-medium">
              <UserPlus className="inline-block w-4 h-4 mr-2" />
              Sign Up
            </Link>
          </div>
        </div>
      )}

      {/* Tools Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold text-gray-900">Available Tools</h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-gray-400 hover:text-gray-500"
              >
                <X className="h-6 w-6" />
              </button>
            </div>
            <div className="space-y-3">
              <a href="#youtube" className="block p-3 rounded-lg hover:bg-gray-50 transition-colors">
                YouTube Downloader
              </a>
              <a href="#instagram" className="block p-3 rounded-lg hover:bg-gray-50 transition-colors">
                Instagram Downloader
              </a>
              <a href="#pinterest" className="block p-3 rounded-lg hover:bg-gray-50 transition-colors">
                Pinterest Downloader
              </a>
              <a href="#telegram" className="block p-3 rounded-lg hover:bg-gray-50 transition-colors">
                Telegram Bot
              </a>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;