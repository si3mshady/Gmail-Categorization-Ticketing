import os
import sqlite3
import base64
import openai
from flask import Flask, render_template, jsonify, request, redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure OpenAI API Key
openai.api_key = "sk-"

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

app = Flask(__name__)

# Initialize the database for tickets
def init_db():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            snippet TEXT,
            status TEXT DEFAULT 'Open',
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Authenticate and connect to Gmail API
def authenticate_gmail():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "cred.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

# Fetch and categorize emails, create tickets for security-related emails
def fetch_and_categorize_emails():
    service = authenticate_gmail()
    if not service:
        return []
    
    # Fetch the latest 10 messages
    results = service.users().messages().list(userId="me", maxResults=10).execute()
    messages = results.get("messages", [])
    categorized_emails = []

    for message in messages:
        msg = service.users().messages().get(userId="me", id=message["id"]).execute()
        headers = msg["payload"]["headers"]
        subject = next(header["value"] for header in headers if header["name"] == "Subject")
        snippet = msg["snippet"]

        # Use OpenAI to categorize the email
        category = categorize_email(subject, snippet)

        # Debug: Print out the category of each email
        print(f"Email Subject: {subject}")
        print(f"Categorized as: {category}")

        categorized_emails.append({
            "subject": subject,
            "snippet": snippet,
            "category": category
        })

        # If the email is categorized as "Security", create a ticket
        if category.strip().lower() == "security":
            print(f"Creating ticket for security email: {subject}")
            create_ticket(subject, snippet, category)

    return categorized_emails

# Function to categorize email content using OpenAI's ChatCompletion API
def categorize_email(subject, snippet):
    prompt = f"""
You are an AI assistant tasked with categorizing emails into the following categories:

Security: Related to security alerts, passwords, or account protection.
Work: Business or professional communications.
Personal: Related to personal matters, friends, or family.
Marketing: Promotional or marketing emails.
Spam: Unsolicited or irrelevant emails.
Other: Emails that don’t fit the above categories.
Email details:

Subject: {subject}
Content: {snippet}
Please return the most relevant category in a single word, such as 'Work' or 'Security'.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5 or GPT-4 model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that categorizes emails."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the category from the response
        category = response.choices[0].message.content.strip()
        return category
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Unknown"

# Function to create a ticket in the database
# Function to create a unique ticket in the database
def create_ticket(subject, snippet, category):
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    
    # Check if a ticket with the same subject and snippet already exists
    c.execute('SELECT * FROM tickets WHERE subject = ? AND snippet = ?', (subject, snippet))
    existing_ticket = c.fetchone()
    
    if existing_ticket:
        print(f"Ticket for {subject} already exists. Skipping ticket creation.")
    else:
        # Insert a new ticket if no existing ticket is found
        c.execute('INSERT INTO tickets (subject, snippet, category) VALUES (?, ?, ?)', (subject, snippet, category))
        conn.commit()
        print(f"Ticket created for {subject} in category {category}")  # Debug: Confirm ticket creation
    
    conn.close()

# Route to fetch categorized emails
@app.route('/emails')
def emails():
    categorized_emails = fetch_and_categorize_emails()

    # Calculate category counts for visualization
    category_counts = {}
    for email in categorized_emails:
        category = email["category"]
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    return jsonify({
        "emails": categorized_emails,
        "category_counts": category_counts
    })

@app.route('/tickets')
def view_tickets():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tickets')
    tickets = c.fetchall()
    conn.close()
    
    print(tickets)  # Debug: Check the retrieved tickets
    
    return render_template('tickets.html', tickets=tickets)


@app.route('/ticket/<int:ticket_id>')
def view_ticket(ticket_id):
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,))
    ticket = c.fetchone()  # Fetch the specific ticket
    conn.close()

    if ticket:
        return render_template('ticket_details.html', ticket=ticket)
    else:
        return "Ticket not found", 404







# Route to update ticket status
@app.route('/update_ticket', methods=['POST'])
def update_ticket():
    ticket_id = request.form.get('ticket_id')
    status = request.form.get('status')
    
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute('UPDATE tickets SET status = ? WHERE id = ?', (status, ticket_id))
    conn.commit()
    conn.close()
    return redirect('/tickets')

# Route to render the email dashboard
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
