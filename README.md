# AI Recruitment System 🚀

## Project Description 📝

This project is an **AI Recruitment System** designed to accelerate the hiring process for HR and technical recruiters. The application allows recruiters to:

1. 📄 Upload candidate resumes, job descriptions, job roles, and additional evaluation instructions.
2. 🤖 Evaluate resumes using AI (SimpleAI, Ollama, OpenAI, Claude, or Mistral).
3. ✉️ Automatically send email notifications to candidates with feedback, indicating whether they are selected or rejected.
4. 📅 Schedule Zoom meetings for the next day as an initial round of interviews.

This system significantly streamlines the recruitment process by selecting the most suitable candidates and providing immediate feedback to candidates on areas for improvement.

---

## Prerequisites ⚙️

To configure this application, the following credentials and accounts are required:

### AI Model Options 🤖:
- **SimpleAI** (Recommended - FREE): Built-in AI model, no API key required
- **Ollama** (FREE): Local AI model, requires Ollama installation
- **OpenAI**: Requires API key from OpenAI
- **Claude**: Requires API key from Anthropic
- **Mistral**: Requires API key from Mistral

### Gmail Account for Email Notifications 📧:
1. Create or use an existing Gmail account for the recruiter.
2. Enable **2-Step Verification** and generate an **App Password**.
   - The app password is a 16-digit code generated through **[Google App Password](https://support.google.com/accounts/answer/185833)**.
   - Format: `afec wejf awoj fwrv` (use without spaces in the Streamlit app).

### Zoom API Credentials 🎥:
1. Create or use an existing Zoom account.
2. Navigate to the **[Zoom App Marketplace](https://marketplace.zoom.us/)** and create a new app with **Server-to-Server OAuth**.
3. Obtain the following credentials:
   - Client ID
   - Client Secret
   - Account ID
4. Add the following scopes to the app for Zoom meeting scheduling:
   - `meeting:write:invite_links:admin`
   - `meeting:write:meeting:admin`
   - `meeting:write:meeting:master`
   - `meeting:write:invite_links:master`
   - `meeting:write:open_app:admin`
   - `user:read:email:admin`
   - `user:read:list_users:admin`
   - `billing:read:user_entitlement:admin`

---

## Installation 🛠️

### Quick Start (Recommended) 🚀

1. Clone this repository:
   ```bash
   git clone https://github.com/ar-baazaja/Automated-Recruitment-System.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Automated-Recruitment-System
   ```

3. Install dependencies:
   ```bash
   pip install streamlit anthropic mistralai openai phidata pypdf2 streamlit-pdf-viewer huggingface_hub
   ```

4. Run the application:
   ```bash
   python -m streamlit run app.py
   ```

5. Open your browser and go to: `http://localhost:7860`

### Using Ollama (Free Local AI) 🆓

1. Install Ollama from [https://ollama.ai/](https://ollama.ai/)
2. Pull a model:
   ```bash
   ollama pull llama3.2:3b
   ```
3. Start Ollama service:
   ```bash
   ollama serve
   ```
4. Run the application and select "Ollama" as the model provider

### Run with Docker 🐳

1. Build the Docker image:
   ```bash
   docker build -t ai-recruitment-system .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 7860:7860 ai-recruitment-system
   ```

---

## Features ✨

- **Multiple AI Models**: Choose from SimpleAI (free), Ollama (free local), OpenAI, Claude, or Mistral
- **Automated Resume Analysis**: 📄 Evaluate candidate resumes based on the provided job description
- **Smart Candidate Selection**: AI-powered analysis with detailed feedback
- **Email Notifications**: ✉️ Notify candidates of their selection status with detailed feedback
- **Zoom Meeting Scheduler**: 📅 Automatically schedule interviews with selected candidates
- **Free Options Available**: Use SimpleAI or Ollama without any API costs

---

## How to Use 🎯

1. **Configure Settings**: In the sidebar, set up your AI model, Zoom credentials, and Gmail settings
2. **Upload Resume**: Upload a candidate's resume in PDF format
3. **Select Job Role**: Choose the position from available job descriptions
4. **Analyze Resume**: Click "Analyze Resume" to get AI-powered evaluation
5. **Review Results**: See detailed feedback and selection decision
6. **Proceed to Interview**: Schedule interviews and send emails to selected candidates

---

## Technologies Used 🛠️

- **Streamlit**: Web application framework
- **SimpleAI**: Built-in free AI model
- **Ollama**: Local AI model support
- **OpenAI/Claude/Mistral**: Cloud AI models
- **PyPDF2**: PDF processing
- **Python**: Backend logic

---

## Benefits 🌟

- ✅ **Completely FREE** with SimpleAI or Ollama
- ✅ **No API costs** for basic functionality
- ✅ **Privacy** - data stays on your computer with local models
- ✅ **Fast and reliable** resume analysis
- ✅ **Automated workflow** from resume to interview scheduling

---

## Contribution 🤝

Contributions are welcome! Please fork this repository and submit a pull request for any enhancements or bug fixes.

---

## License 📄

This project is open source and available under the MIT License.
