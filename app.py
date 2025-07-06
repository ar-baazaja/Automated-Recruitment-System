import json
import streamlit as st
from phi.utils.log import logger
from streamlit_pdf_viewer import pdf_viewer
from tasks import (
    init_session_state,
    schedule_interview_simple,
    extract_text_from_pdf,
    analyze_resume_simple,
    send_selection_email_simple,
    send_rejection_email,
    add_job_details,
)
from agents import (
    create_resume_analyzer_agent,
    create_scheduler_agent,
    create_email_agent,
)


def main() -> None:
    st.title("AI Recruitment System")

    init_session_state()
    with st.sidebar:
        st.header("Configuration")

        # API Configuration
        st.subheader("LLM Models")
        model_provider = st.selectbox("Model Provider", ["SimpleAI"])
        api_key = st.text_input(
            "API Key (Not needed for SimpleAI)",
            type="password",
            value=st.session_state.api_key,
            help="API key not needed for SimpleAI",
        )
        if model_provider:
            st.session_state.model_provider = model_provider
        if api_key:
            st.session_state.api_key = api_key

        st.subheader("Zoom Settings")
        zoom_account_id = st.text_input(
            "Zoom Account ID", type="password", value=st.session_state.zoom_account_id
        )
        zoom_client_id = st.text_input(
            "Zoom Client ID", type="password", value=st.session_state.zoom_client_id
        )
        zoom_client_secret = st.text_input(
            "Zoom Client Secret",
            type="password",
            value=st.session_state.zoom_client_secret,
        )

        st.subheader("Email Settings")
        email_sender = st.text_input(
            "Sender Email",
            value=st.session_state.email_sender,
            help="Email address to send from",
        )
        email_passkey = st.text_input(
            "Email App Password",
            type="password",
            value=st.session_state.email_passkey,
            help="App-specific password for email",
        )
        company_name = st.text_input(
            "Company Name",
            value=st.session_state.company_name,
            help="Name to use in email communications",
        )

        if zoom_account_id:
            st.session_state.zoom_account_id = zoom_account_id
        if zoom_client_id:
            st.session_state.zoom_client_id = zoom_client_id
        if zoom_client_secret:
            st.session_state.zoom_client_secret = zoom_client_secret
        if email_sender:
            st.session_state.email_sender = email_sender
        if email_passkey:
            st.session_state.email_passkey = email_passkey
        if company_name:
            st.session_state.company_name = company_name

        required_configs = {
            "Model Provider": st.session_state.model_provider,
            "Zoom Account ID": st.session_state.zoom_account_id,
            "Zoom Client ID": st.session_state.zoom_client_id,
            "Zoom Client Secret": st.session_state.zoom_client_secret,
            "Email Sender": st.session_state.email_sender,
            "Email Password": st.session_state.email_passkey,
            "Company Name": st.session_state.company_name,
        }

    # Only require API key for paid models (none in this case)
    if st.session_state.model_provider != "SimpleAI":
        st.warning("Please select SimpleAI as the model provider.")
        return

    missing_configs = [k for k, v in required_configs.items() if not v]
    if missing_configs:
        st.warning(
            f"Please configure the following in the sidebar: {', '.join(missing_configs)}"
        )
        return

    with st.expander("Add Job Role & Descriptions", expanded=False):
        job_role = st.text_input("Job Role")
        job_description = st.text_area("Job Description (Use Markdown)")
        additional_instructions = st.text_area(
            "Additional Instructions (Optional)",
            placeholder="Add additional instructions for candidate selection for this particular job role.",
        )
        button = st.button("Add details")
        if button:
            resonse = add_job_details(
                job_role, job_description, additional_instructions
            )
            if resonse:
                st.success("Data Saved Successfully.!!")
            else:
                st.error(
                    "Error occurred while storing the data. Make sure to provide Job Role and Job Description."
                )
    with open("data/job_descriptions.json", "r") as f:
        json_descriptions_data = json.load(f)

    role = st.selectbox(
        "Select the role you're applying for:",
        json_descriptions_data.keys(),
    )
    with st.expander("Job Description", expanded=True):
        text_markdown = """
        {job_descriptions}        
        """
        st.markdown(
            text_markdown.format(
                job_descriptions=json_descriptions_data[role]["job_description"],
            )
        )

    # Add a "New Application" button before the resume upload
    if st.button("📝 New Application"):
        # Clear only the application-related states
        keys_to_clear = [
            "resume_text",
            "analysis_complete",
            "is_selected",
            "candidate_email",
            "current_pdf",
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                st.session_state[key] = None if key == "current_pdf" else ""
        st.rerun()

    resume_file = st.file_uploader(
        "Upload your resume (PDF)", type=["pdf"], key="resume_uploader"
    )
    if resume_file is not None and resume_file != st.session_state.get("current_pdf"):
        st.session_state.current_pdf = resume_file
        st.session_state.resume_text = ""
        st.session_state.analysis_complete = False
        st.session_state.is_selected = False
        st.rerun()

    if resume_file:
        st.subheader("Uploaded Resume")
        col1, col2 = st.columns([4, 1])

        with col1:
            import tempfile, os

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(resume_file.read())
                tmp_file_path = tmp_file.name
            resume_file.seek(0)
            try:
                pdf_viewer(tmp_file_path)
            finally:
                os.unlink(tmp_file_path)

        with col2:
            st.download_button(
                label="📥 Download",
                data=resume_file,
                file_name=resume_file.name,
                mime="application/pdf",
            )
        # Process the resume text
        if not st.session_state.resume_text:
            with st.spinner("Processing your resume..."):
                resume_text = extract_text_from_pdf(resume_file)
                if resume_text:
                    st.session_state.resume_text = resume_text
                    st.success("Resume processed successfully!")
                else:
                    st.error("Could not process the PDF. Please try again.")

    # Email input with session state
    email = st.text_input(
        "Candidate's email address",
        value=st.session_state.candidate_email,
        key="email_input",
    )
    st.session_state.candidate_email = email

    # Analysis and next steps
    if (
        st.session_state.resume_text
        and email
        and not st.session_state.analysis_complete
    ):
        if st.button("Analyze Resume"):
            with st.spinner("Analyzing your resume..."):
                # Use SimpleAI analysis (no API key needed)
                print("DEBUG: Starting resume analysis with SimpleAI")
                is_selected, feedback = analyze_resume_simple(
                    resume_text=st.session_state.resume_text,
                    role_requirements=json_descriptions_data[role],
                    role=role,
                )
                print(
                    f"DEBUG: Analysis complete - Selected: {is_selected}, Feedback: {feedback}"
                )

                if is_selected:
                    st.success(
                        "Congratulations! Your skills match our requirements."
                    )
                    st.session_state.analysis_complete = True
                    st.session_state.is_selected = True
                    st.rerun()
                else:
                    st.warning(
                        "Your skills don't match our current requirements."
                    )
                    st.session_state.analysis_complete = True
                    st.session_state.is_selected = False
                    st.rerun()

    if st.session_state.get("analysis_complete") and st.session_state.get(
        "is_selected", False
    ):
        st.success("Congratulations! Your skills match our requirements.")
        st.info(
            "Click 'Proceed to Interview' to continue with the interview process."
        )

        if st.button("Proceed to Interview"):
            print("DEBUG: Proceed button clicked")
            
            # Use simple email sending instead of complex agent
            try:
                if st.session_state.get("email_sender") and st.session_state.get("email_passkey"):
                    # Send selection email using simple function
                    send_selection_email_simple(
                        to_email=st.session_state.get("candidate_email", ""),
                        role=role,
                        company_name=st.session_state.get("company_name", "Our Company")
                    )
                    st.success("Selection email sent successfully!")
                else:
                    st.warning("Email settings not configured. Please add Gmail settings in sidebar.")
                
                # Schedule interview using simple function
                if st.session_state.get("zoom_account_id"):
                    interview_link = schedule_interview_simple(
                        candidate_email=st.session_state.get("candidate_email", ""),
                        role=role,
                        company_name=st.session_state.get("company_name", "Our Company")
                    )
                    if interview_link:
                        st.success(f"Interview scheduled! Link: {interview_link}")
                    else:
                        st.warning("Could not schedule interview. Check Zoom settings.")
                else:
                    st.warning("Zoom settings not configured. Please add Zoom settings in sidebar.")
                
            except Exception as e:
                st.error(f"Error in interview process: {str(e)}")
                print(f"DEBUG: Error occurred: {str(e)}")

    # Reset button
    if st.sidebar.button("Reset Application"):
        for key in st.session_state.keys():
            if key != "api_key":
                del st.session_state[key]
        st.rerun()


if __name__ == "__main__":
    main()
