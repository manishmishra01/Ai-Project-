import os
from dotenv import load_dotenv
from groq import Groq
from langchain.prompts import PromptTemplate
import streamlit as st
# Load environment variables
load_dotenv()
# Initialize Groq client
api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key=api_key)
def generate_linkedin_post(project_name, project_description, key_features, tech_stack):
    # Create prompt template
    prompt_template = PromptTemplate(
        input_variables=["project_name", "project_description", "key_features", "tech_stack"],
        template="""You are a professional LinkedIn content writer specializing in tech project announcements.
Create an engaging LinkedIn post announcing my project with the following details:
Project Name: {project_name}
Project Description: {project_description}
Key Features: {key_features}
Technologies Used: {tech_stack}
Guidelines for the post:
1. Start with an exciting hook about the project launch
2. Briefly explain what problem the project solves
3. Highlight 2-3 key features or capabilities
4. Mention the tech stack naturally
5. Include a clear call-to-action (like checking out the project, providing feedback, or connecting)
6. Add 3-4 relevant hashtags
7. Use appropriate emojis to make the post engaging
8. Keep it under 1300 characters
9. Use line breaks for better readability
Generate a professional yet enthusiastic LinkedIn post following these guidelines."""
    )
    # Format the prompt
    post = prompt_template.format(
        project_name=project_name,
        project_description=project_description,
        key_features=key_features,
        tech_stack=tech_stack
    )
    # Generate completion
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": post
                }
            ],
            model="llama3-8b-8192"
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating caption: {str(e)}"
def main():
    st.set_page_config(page_title="LinkedIn Caption Generator", page_icon="📝")
    
    # Add custom CSS
    st.markdown("""
        <style>
        .stTextArea textarea {min-height: 100px}
        .main .block-container {padding-top: 2rem}
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown(
           """
         <h1 style='color: white;'>Projexbuzz</h1>
          """,
         unsafe_allow_html=True
          )
     
    st.markdown(
    """
    <div style="
        background-color: #f4f4f8; 
        border-radius: 10px; 
        padding: 20px; 
        border: 1px solid #ddd; 
        text-align: center;">
        <h2 style="
            color: #4A90E2; 
            font-family: Arial, sans-serif; 
            font-weight: bold;">
            ✨ Generate Professional LinkedIn Posts for Your Tech Projects ✨
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)
    
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["Generate Post", "About"])
    
    with tab1:
        # Input form
        
        
        with st.form("post_form"):
            
            st.subheader("Project Details")
            
            project_name = st.text_input("Project Name", 
                placeholder="Enter your project name")
            
            project_description = st.text_area("Project Description",
                placeholder="Briefly describe what your project does and its main purpose")
            
            key_features = st.text_area("Key Features",
                placeholder="List the main features of your project (comma-separated)")
            
            tech_stack = st.text_area("Technologies Used",
                placeholder="List the technologies used in your project (comma-separated)")
            
            submit_button = st.form_submit_button("Generate Post")
        
        # Move the generated post and action buttons outside the form
        if submit_button:
            if not all([project_name, project_description, key_features, tech_stack]):
                st.error("Please fill in all fields")
            else:
                with st.spinner("Generating your LinkedIn post..."):
                    generated_post = generate_linkedin_post(
                        project_name,
                        project_description,
                        key_features,
                        tech_stack
                    )
                    
                    # Display generated post
                    st.subheader("Generated LinkedIn Post")
                    st.text_area("Copy your post:", generated_post, height=300)
                    
                    # Add action buttons outside the form
                    st.markdown("### Quick Actions")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📋 Copy to Clipboard"):
                            st.code(generated_post)  # This makes it easy to copy
                            st.success("Post copied! Click the copy button in the code block above.")
                    with col2:
                        if st.button("🔄 Generate New Version"):
                            st.experimental_rerun()
        
        
    with tab2:
        st.markdown("""
        ### About This Tool
        
        This LinkedIn post generator helps you create professional announcements for your tech projects. It follows best practices for LinkedIn content and ensures your posts are engaging and well-structured.
        
        #### Features:
        - Professional post structure
        - Emoji integration
        - Automatic hashtag generation
        - Character limit compliance
        - Natural tech stack integration
        
        #### Tips for Best Results:
        1. Provide clear, concise project descriptions
        2. List specific, notable features
        3. Include all relevant technologies
        4. Review and personalize the generated post
        """)
if __name__ == "__main__":
    main()
    
