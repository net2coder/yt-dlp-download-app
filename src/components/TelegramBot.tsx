import React from 'react';
import { MessageCircle, ExternalLink } from 'lucide-react';

const TelegramBot = () => {
  return (
    <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-8 text-white text-center transform transition-all hover:scale-105">
      <MessageCircle className="h-16 w-16 mx-auto mb-6" />
      <h3 className="text-2xl font-bold mb-4">Use Our Telegram Bot</h3>
      <p className="mb-6">
        Download content directly through our Telegram bot. Fast, convenient, and always available!
      </p>
      <a
        href="https://t.me/Vmget_bot"
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center px-6 py-3 bg-white text-blue-600 rounded-full font-semibold hover:bg-blue-50 transition-colors"
      >
        Open in Telegram
        <ExternalLink className="ml-2 h-5 w-5" />
      </a>
      <div className="mt-6 text-sm">
        <p className="text-blue-100">
          1. Click "Open in Telegram"<br />
          2. Start the bot with /start<br />
          3. Select your platform<br />
          4. Send the URL<br />
          5. Choose quality and download!
        </p>
      </div>
    </div>
  );
};

export default TelegramBot;