# Gmail MCP Server & Client

A powerful Model Context Protocol (MCP) implementation for Gmail integration with AI agents, featuring email sending, fetching, and intelligent email management capabilities.

## 🌟 Features

### Email Server (MCP Server)
- **Send Emails**: Send emails with optional attachments via Gmail SMTP
- **Fetch Recent Emails**: Retrieve recent emails from any folder
- **Unread Email Detection**: Get unread emails from the last 2 days
- **Attachment Support**: 
  - Direct file attachments
  - Download attachments from URLs
  - Pre-staged attachment management
- **Health Monitoring**: Built-in health check endpoint
- **FastAPI Integration**: RESTful API with MCP protocol support

### Email Client (AI Agent)
- **Interactive Chat Interface**: Natural language email management
- **Groq LLM Integration**: Powered by Gemma2-9B-IT model
- **ReAct Agent**: Intelligent reasoning and action capabilities
- **Real-time Processing**: Async communication with MCP server

## 📋 Prerequisites

- Python 3.8+
- Gmail account with App Password enabled
- Groq API key
- Required Python packages (see requirements below)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone git clone https://github.com/NiazAhmed1/Email_MCP.git
cd Email_MCP
```

### 2. Install Dependencies

```bash
pip install -r requirements
```

### 3. Environment Setup

Create a `.env` file in the project root:

```env
# Gmail Configuration
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Groq API Configuration
GROQ_API_KEY=your-groq-api-key
```

### 4. Gmail Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password in `SMTP_PASSWORD`

### 5. Run the Application

#### Option A: Automatic (Recommended)
```bash
python Email_client.py
```
This automatically starts the server and connects the client.

#### Option B: Manual
```bash
# Terminal 1 - Start the server
python Email_client.py

# Terminal 2 - Start the client (if running separately)
python Email_client.py
```

## 🛠️ Usage Examples

### Sending Emails

```
🧮 Enter your question: Send an email to john@example.com with subject "Meeting Tomorrow" and body "Hi John, don't forget about our meeting tomorrow at 2 PM."
```

### Fetching Recent Emails

```
🧮 Enter your question: Show me my 5 most recent emails
```

### Checking Unread Emails

```
🧮 Enter your question: Check for unread emails from the last 2 days
```

### Sending with Attachments

```
🧮 Enter your question: Send an email to sarah@example.com with the quarterly report attached
```

## 📁 Project Structure

```
gmail-mcp/
├── Email_client.py          # MCP server implementation
├── Email_client.py          # AI agent client
├── .env                     # Environment variables
├── README.md               # This file
├── available_attachments/  # Pre-staged attachments folder
└── temp_attachments/       # Temporary downloads folder
```

## 🔧 Configuration

### Server Configuration

The MCP server runs on `localhost:8989` by default. You can modify these settings in `Email_client.py`:

```python
mcp = FastMCP(
    name="gmail-mcp",   
    port=8989,       
)
```

### Client Configuration

The client connects to the server and uses Groq's Gemma2-9B-IT model. You can change the model in `Email_client.py`:

```python
llm = ChatGroq(
    model="gemma2-9b-it",  # Change model here
    temperature=0,
    api_key=groq_api_key
)
```

## 🛡️ Security Considerations

- **App Passwords**: Use Gmail App Passwords instead of your main password
- **Environment Variables**: Never commit `.env` file to version control
- **API Keys**: Keep your Groq API key secure
- **Network Security**: Server runs on localhost by default

## 🧪 Available Tools

### `send_email_tool`
Send emails with optional attachments.

**Parameters:**
- `recipient`: Email address
- `subject`: Email subject
- `body`: Email content
- `attachment_path`: Direct file path (optional)
- `attachment_url`: URL to download attachment (optional)
- `attachment_name`: Filename for attachment (optional)

### `fetch_recent_emails`
Fetch recent emails from specified folder.

**Parameters:**
- `folder`: Email folder (default: "INBOX")
- `limit`: Maximum emails to fetch (default: 10)

### `fetch_unread_emails_last_2_days`
Get unread emails from the last 2 days.

**Parameters:**
- `folder`: Email folder (default: "INBOX")
- `limit`: Maximum emails to fetch (default: 10)

## 🚨 Troubleshooting

### Common Issues

1. **Authentication Error**
   ```
   Failed to send email: (535, 'Incorrect authentication data')
   ```
   - Ensure you're using an App Password, not your regular password
   - Verify the username and password in `.env`

2. **Connection Timeout**
   ```
   Failed to connect to MCP server
   ```
   - Ensure the server is running before starting the client
   - Check if port 8989 is available

3. **Missing Environment Variables**
   ```
   Error: GROQ_API_KEY environment variable not set!
   ```
   - Verify your `.env` file exists and contains all required variables

### Debug Mode

Enable debug logging by modifying the server startup:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server framework
- [LangChain](https://langchain.com/) for AI agent capabilities
- [Groq](https://groq.com/) for fast LLM inference
- Gmail API for email functionality

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-username/gmail-mcp/issues) page
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Error messages (if any)
   - Your environment details

---

**Made with ❤️ by [Your Name]**