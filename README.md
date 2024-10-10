# AI-Powered Hotel Marketing Automation

![Hotel Industry AI Marketing  Automation](https://saibaba9758140479.blob.core.windows.net/testimages/HOTEL_INDUSTRY1.PNG)

## Description

This project introduces an innovative, AI-driven marketing automation system for the hotel industry. It leverages generative AI to optimize occupancy rates through personalized, data-driven campaigns and content creation. The system monitors occupancy rates in real-time, automatically triggering targeted marketing initiatives when bookings fall below specified thresholds.

## Features

- Real-time occupancy rate monitoring and analysis
- Automated triggering of marketing campaigns based on occupancy thresholds
- Personalized email content generation using AI
- Social media content creation for platforms like Instagram and Twitter
- Integration of multiple data sources (reservations, weather, events, competitor analysis)
- Optimal campaign timing determination based on historical data
- Web-based interface for viewing analysis results and generated content
- Hotel reservation data entry system

## Technologies Used

- Python
- Pandas
- NumPy
- Flask
- Streamlit
- Google's Generative AI (Gemini model)
- PyODBC
- Dotenv
- SQL Server
- Markdown
- JSON
- HTML
- CSV

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hotel-marketing-automation.git
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. Set up your SQL Server connection in `hotel_entry.py`

## Usage

1. Run the Flask web application:
   ```
   python flask_app.py
   ```

2. Access the web interface at `http://localhost:5000`

3. To run the data entry system:
   ```
   streamlit run hotel_entry.py
   ```

## Contributing

Contributions to improve the project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.


Project Link: [https://github.com/yourusername/hotel-marketing-automation](https://github.com/yourusername/hotel-marketing-automation)