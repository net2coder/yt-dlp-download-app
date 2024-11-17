import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
import os
from dotenv import load_dotenv
from downloaders.youtube import YouTubeDownloader
from downloaders.instagram import InstagramDownloader
from downloaders.pinterest import PinterestDownloader
from downloaders.linkedin import LinkedInDownloader
from downloaders.twitter import TwitterDownloader
from downloaders.snapchat import SnapchatDownloader

load_dotenv()

# Conversation states
PLATFORM = 0
URL = 1
QUALITY = 2

# Platform options
PLATFORMS = {
    'youtube': ('YouTube', YouTubeDownloader, ['MP4 - 1080p', 'MP4 - 720p', 'MP4 - 480p', 'MP3 Audio']),
    'instagram': ('Instagram', InstagramDownloader, ['Video', 'Image', 'Story', 'Reel', 'Highlight']),
    'pinterest': ('Pinterest', PinterestDownloader, ['Original Quality', 'High Quality', 'Medium Quality']),
    'linkedin': ('LinkedIn', LinkedInDownloader, ['Video', 'Image', 'Post']),
    'twitter': ('Twitter', TwitterDownloader, ['High Quality', 'Medium Quality', 'Low Quality']),
    'snapchat': ('Snapchat', SnapchatDownloader, ['Story', 'Spotlight', 'Snap'])
}

class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.user_data = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton(name, callback_data=platform)]
            for platform, (name, _, _) in PLATFORMS.items()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            'Welcome to VMGET Download Bot! 🚀\n'
            'Please select a platform to download from:',
            reply_markup=reply_markup
        )
        return PLATFORM

    async def platform_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        platform = query.data
        context.user_data['platform'] = platform
        platform_name = PLATFORMS[platform][0]
        
        await query.edit_message_text(
            f'You selected {platform_name}.\n'
            'Please send me the URL you want to download from:'
        )
        return URL

    async def url_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        url = update.message.text
        context.user_data['url'] = url
        platform = context.user_data['platform']
        
        # Show quality options
        _, _, qualities = PLATFORMS[platform]
        keyboard = [
            [InlineKeyboardButton(quality, callback_data=quality)]
            for quality in qualities
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            'Please select the quality/format:',
            reply_markup=reply_markup
        )
        return QUALITY

    async def quality_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        quality = query.data
        platform = context.user_data['platform']
        url = context.user_data['url']
        
        await query.edit_message_text('⏳ Processing your download...')
        
        try:
            # Initialize the appropriate downloader
            _, downloader_class, _ = PLATFORMS[platform]
            downloader = downloader_class()
            
            # Download the content
            result = downloader.download(url, quality)
            
            if os.path.exists(result['filename']):
                # Send the file
                await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=open(result['filename'], 'rb'),
                    caption='✅ Here is your downloaded content!'
                )
            else:
                await query.edit_message_text('❌ Download failed. Please try again.')
        except Exception as e:
            await query.edit_message_text(f'❌ Error: {str(e)}')
        
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Operation cancelled.')
        return ConversationHandler.END

    def run(self):
        # Set up the event loop in the current thread
        loop = asyncio.new_event_loop()  # Create a new event loop
        asyncio.set_event_loop(loop)  # Set it as the current event loop

        application = Application.builder().token(self.token).build()

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                PLATFORM: [CallbackQueryHandler(self.platform_callback)],
                URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.url_handler)],
                QUALITY: [CallbackQueryHandler(self.quality_callback)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

        application.add_handler(conv_handler)

        # Run the bot using the event loop
        loop.run_until_complete(application.run_polling())

