# Shorts-Factory

Shorts-Factory is an automated tool for generating, creating, and uploading YouTube Shorts. It leverages AI to produce engaging content, from text generation to video creation and upload.

## Features

- Generate facts, quotes, and book summaries
- Create voiceovers using OpenAI's text-to-speech API
- Fetch relevant images using Google Image Search
- Produce video shorts with subtitles and background music
- Upload generated shorts to YouTube

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- OpenAI API key
- Google Cloud Services API key
- YouTube Data API credentials
- Pexels API key

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/shorts-factory.git
   cd shorts-factory
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GCS_DEVELOPER_KEY=your_google_cloud_services_api_key
   GCS_CX=your_google_custom_search_engine_id
   PEXELS_API_KEY=your_pexels_api_key
   ```

## Usage

1. Configure your content in `item_list.py`:

   - Add topics for facts, quotes, books, and titles

2. Run the main script:

   ```
   python main.py
   ```

3. The script will generate shorts and save them in the `videos` directory

4. To upload videos to YouTube, uncomment the `main3()` function call in `main.py` and run the script again

## Project Structure

- `main.py`: Entry point of the application
- `short.py`: Defines the `Short` class for generating and managing individual shorts
- `video.py`: Contains functions for creating videos from generated content
- `item_list.py`: Lists of topics for content generation
- `secrets/client_secret.json`: YouTube API credentials (not included in repository)

## Customization

- Adjust video parameters in `short.py` (e.g., duration, caption height, voice model)
- Modify video creation process in `video.py`
- Add new content types by extending the `Short` class in `short.py`

## Contributing

Contributions to Shorts-Factory are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgements

- OpenAI for text generation and text-to-speech
- Google Cloud Services for image search
- YouTube Data API for video uploads
- Pexels for additional image resources
