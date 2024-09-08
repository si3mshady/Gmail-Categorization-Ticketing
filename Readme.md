# Email Categorization and Security Ticketing App

This app fetches emails from Gmail, automatically classifies them into categories like **Security**, **Work**, **Personal**, **Spam**, etc., and generates tickets for security-related emails. The app also features an interactive dashboard for visualizing categorized emails and a basic ticketing system to track security alerts.

## Features
- **Email Categorization**: Automatically categorizes incoming emails into predefined categories using **OpenAI's GPT-3.5**.
- **Security Ticketing System**: Automatically generates tickets for emails classified under the **Security** category.
- **Interactive Dashboard**: Visualizes email categories with **Chart.js** and allows users to filter emails by category.
- **View & Manage Tickets**: Provides a list of security tickets with an option to update their status.
- **Prototyping with ChatGPT**: Utilizes ChatGPT to speed up prototyping and save development time.

## Technologies Used
- **Python**: Backend language used with Flask framework.
- **Flask**: Web framework for the backend server and routing.
- **OpenAI GPT-3.5**: Used for classifying email content.
- **Gmail API**: To fetch and process emails from Gmail.
- **Chart.js**: For rendering interactive charts in the frontend.
- **SQLite**: To store and manage security-related tickets.
- **HTML/CSS/Bootstrap**: Frontend for creating an interactive user interface.

## Installation

### Prerequisites
- Python 3.x
- Gmail API credentials
- OpenAI API key

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/email-security-ticketing-app.git
   cd email-security-ticketing-app
   ```

2. **Install Dependencies**
   Install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Gmail API Credentials**
   - Go to the [Google Developer Console](https://console.developers.google.com/), create a project, and enable the **Gmail API**.
   - Download your `credentials.json` file and place it in the root directory.

4. **Configure OpenAI API Key**
   Set up your **OpenAI API key** by adding it directly to the code or using environment variables:
   ```python
   openai.api_key = "your-openai-api-key"
   ```

5. **Initialize the Database**
   The SQLite database will store the security tickets. Run the app to automatically create the `tickets.db`:
   ```bash
   python app.py
   ```

6. **Run the App**
   Start the Flask server:
   ```bash
   flask run
   ```

7. **Access the Application**
   Open your browser and navigate to `http://127.0.0.1:5000/` to access the app.

## Usage

### 1. Fetch Emails
- Click the **"Fetch Emails"** button to retrieve your Gmail emails. The emails will be categorized into different groups (Security, Work, Spam, etc.).

### 2. View and Manage Tickets
- Navigate to the **Tickets** page by clicking the **"View Tickets"** button.
- View the list of security tickets generated based on incoming emails.
- Update ticket statuses (Open, In Progress, Resolved).

### 3. Ticket Details
- Click on a ticket subject to view detailed information about the ticket, including the subject, email snippet, category, and status.

## Project Structure

```bash
.
├── app.py                # Main Flask app
├── templates/            # HTML templates for the app
│   ├── index.html        # Dashboard page
│   ├── tickets.html      # List of tickets
│   └── ticket_details.html # Detailed view of a single ticket
├── static/               # Static files (CSS, JS)
│   ├── style.css         # Custom styles
│   └── chart.js          # Chart.js integration
├── tickets.db            # SQLite database for storing tickets
├── credentials.json      # Gmail API credentials
└── README.md             # This README file
```

## Future Enhancements
- **ServiceNow Integration**: Automatically create ServiceNow incidents for security-related emails.
- **Microsoft Outlook Support**: Extend the functionality to work with Outlook emails.
- **Advanced Categorization**: Add more customizable categories and refine the classification model.

## Contributing
Feel free to submit issues or pull requests to help improve the project!

## License
This project is licensed under the MIT License.

---

This README provides clear instructions on setup, usage, and features of the app. Let me know if you need further customization!# Gmail-Categorization-Ticketing
# Gmail-Categorization-Ticketing
