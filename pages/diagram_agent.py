import streamlit as st
import subprocess
import os
import re
from pathlib import Path
from openai import AzureOpenAI
import tempfile
from data import diagrams
import glob
import pandas as pd

# import the list of supported diagrams
df_diagrams = pd.DataFrame(diagrams)

# Directory for storing output diagrams
output_dir = Path('./diagrams')

# Path to the PlantUML .jar file
plantuml_jar_path = './plantuml.jar'

# Set up your OpenAI API key
api_key = st.secrets["AZURE_OPENAI_API_KEY"]
azure_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]

client = AzureOpenAI(
    api_key=api_key,  
    api_version="2024-02-01",
    azure_endpoint=azure_endpoint
)

# Initialize session state for PlantUML code
if 'plantuml_code' not in st.session_state:
    st.session_state['plantuml_code'] = ""

# Function to convert natural language instruction to PlantUML code using OpenAI
def nl_to_plantuml(nl_instruction, diagram_type, include_title, use_aws_orange_theme, use_note, use_illustration, error_details=None, failed_code=None):
    example = df_diagrams[df_diagrams['diagram_type'] == diagram_type]['example'].iloc[0]
    if diagram_type == "Let AI decide best Diagram":
        diagram_type = 'most appropriate diagram'
    # Construct the instruction message based on toggles
    instruction_message = f"You are a professional PlantUML coder."
    if include_title:
        instruction_message += " Include a title."
    if use_aws_orange_theme:
        instruction_message += " Use aws-orange theme. Syntax: !theme aws-orange"
    if use_note:
        instruction_message += " Use note if needed to explain more details."
    if use_illustration:
        instruction_message += " Use group or card if needed."
    instruction_message += f''' You MUST Output PlantUML code for a {diagram_type} only and explain nothing.
    For example the code will start with: {example}.
    '''

    if error_details and failed_code:
        # nl_instruction += f"\n\nPrevious error details: {error_details}\n\nPlantUML code from diagrams\output.puml:\n{failed_code}\n"
        # nl_instruction += " Why this PlantUML code doesn't run? Analyze the code for any syntax error and return a corrected PlantUML code."
        nl_instruction += " You must use Sequence Diagram for this request."

    try:
        # Use the OpenAI API to generate a response
        print("Instruction message:\n", instruction_message)
        print("NL Instruction:\n", nl_instruction)

        openai_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": instruction_message},
                {"role": "user", "content": nl_instruction}
            ],
            temperature=0.5,
            stream=False,
        )
        plantuml_code = openai_response.choices[0].message.content
        return plantuml_code
    except Exception as e:
        st.error(f"An error occurred with the OpenAI API: {e}")
        return None

# Function to generate UML diagram from PlantUML code
def generate_uml_diagram(plantuml_code, output_dir, plantuml_jar_path):
    retries = 2
    error_message = None

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

    # Define the path for the .puml file
    output_puml_file = output_dir / "output.puml"

    # Write the PlantUML code to the .puml file
    with open(output_puml_file, 'w') as file:
        file.write(plantuml_code)

    while retries >= 0:
        try:
            subprocess_result = subprocess.run(
                ['java',
                 '-jar', plantuml_jar_path,
                 str(output_puml_file)],
                capture_output=True, text=True
            )

            # Find the generated PNG file
            png_files = list(output_dir.glob('*.png'))
            if subprocess_result.returncode == 0 and png_files:
                # Assume the newest PNG file is the one we just created
                generated_png_file = max(png_files, key=os.path.getctime)
                output_png_file = output_dir / "output.png"
                # Rename the file to output.png
                generated_png_file.rename(output_png_file)
                return str(output_puml_file), str(output_png_file), None
            else:
                error_message = "Failed to create the output diagram or PlantUML error."
                if subprocess_result.stderr:
                    error_message = subprocess_result.stderr
                retries -= 1
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            retries -= 1

    return None, None, error_message

def extract_plantuml_code(full_code):
    """
    Extracts the PlantUML code between @startXXX and @endXXX tags.
    
    Args:
    - full_code (str): The full PlantUML code including unwanted text.
    
    Returns:
    - str: The extracted PlantUML code or None if no valid code block is found.
    """
    # Regular expression to find blocks starting with @start and ending with @end
    pattern = re.compile(r"@start\w+.*?@end\w+", re.DOTALL)
    match = pattern.search(full_code)
    
    if match:
        return match.group(0)  # Return the matched block, including start and end tags
    else:
        return None  # Return None if no valid block is found

# Function to create a download link for the image
def get_image_download_link(img_path):
    with open(img_path, "rb") as file:
        btn = st.download_button(
            label="Download diagram",
            data=file,
            file_name="diagram.png",
            mime="image/png",
            type="primary"
        )
    return btn

# Function to generate a plan using OpenAI
def generate_plan(nl_instruction):
    try:
        openai_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Generate a brief plan based on the user's description. This plan will be used to create a diagram. Keep the plan concise and relevant."},
                {"role": "user", "content": nl_instruction}
            ],
            temperature=0.5,
            stream=False,
        )
        return openai_response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred with the OpenAI API: {e}")
        return None
    
def process_and_generate_diagrams(input_text):
    retry_count = 0
    error_message = None
    while retry_count < 3:
        with st.spinner(text="🤔 Thinking on how to draw this plan..."):
            generated_code = nl_to_plantuml(
                input_text,
                selected_diagram_type,
                include_title,
                use_aws_orange_theme,
                use_note,
                use_illustration,
                error_details=error_message,
                failed_code=st.session_state['plantuml_code'] if error_message else None
            )
        if generated_code:
            valid_plantuml_code = extract_plantuml_code(generated_code)
            if valid_plantuml_code:
                st.session_state['plantuml_code'] = valid_plantuml_code
                st.session_state['nl_instruction'] = input_text
                
                output_puml_file, output_png_file, error_message = generate_uml_diagram(
                    st.session_state['plantuml_code'], output_dir=output_dir, plantuml_jar_path=plantuml_jar_path
                )
                if output_png_file:
                    st.toast("Successfully generated your diagram", icon='✅')
                    # Display the generated diagram
                    st.image(str(output_png_file), caption='Diagram generated by Peter', use_column_width=False)
                    
                    # Provide a download button for the image
                    get_image_download_link(str(output_png_file))

                    if display_code:
                        st.text("🥳 Here's your PlantUML code if you need to generate this graph else where:")
                        plantuml_code = st.code(
                            body=st.session_state['plantuml_code'],
                            line_numbers=True
                        )
                        
                    break  # Exit loop on success
            else:
                st.error("No valid PlantUML code block found. Retrying...")
                retry_count += 1
        else:
            st.error("Failed to convert to PlantUML code.")
            break  # Exit loop on conversion failure

# Streamlit application layout
st.set_page_config(page_title="Diagram Generator", page_icon=":memo:", layout='wide', initial_sidebar_state='collapsed')
col1, col2, col3 = st.columns([1,2,1])
with col2:
    logo_path = "bavista_logo.png" 
    st.image(logo_path, use_column_width=True) 

st.title('Agent Peter - Diagram Generator')
st.markdown('**How to use Peter**', help='''1. Select the type of diagram you want to create.\n2. Describe your requirements in natural language.\n3. Click **Generate diagram** to generate code.\n4. You can **Edit** the PlantUML code if needed.\n5. You can **Download** the generated diagram.''')

# Sidebar content
with st.sidebar:
    st.header("Agent controls:")
    # Select box for choosing diagram type
    selected_diagram_type = st.selectbox("Choose diagram type:", df_diagrams['diagram_type'].to_list(), index=0)

    # Toggles for instruction message content
    use_planning = st.toggle("Enable Planning Mode", value=True)
    display_code = st.toggle("Display generated diagram code", value=False)
    include_title = st.checkbox("Include a title",value=True)
    use_aws_orange_theme = st.checkbox("Use aws-orange theme", value=True)
    use_illustration = st.checkbox("Use grouping", value=True)
    use_note = st.checkbox("Use notes", value=True)

# Text area for user to enter natural language instructions
nl_instruction = st.text_area(
    label="Describe your requirements in natural language:",
    height=150,
    value=st.session_state.get('nl_instruction', ''),
    placeholder="Explain how Bitcoin works"
)

# Button to convert natural language to PlantUML code
convert_button = st.button("Generate diagram", type="primary",use_container_width=True)

# When the button is clicked, convert the natural language to PlantUML code
if convert_button:
    if use_planning:
        # Generate plan and directly use it for conversion
        with st.spinner(text="🤔 Planning..."):
            plan = generate_plan(nl_instruction)
        if plan:
            st.session_state['plan'] = plan
            st.subheader('Done thinking ✅ Here is the plan:') 
            st.write(plan)
            process_and_generate_diagrams(plan)
        else:
            st.error("Failed to generate a plan.")
    else:
        # Proceed with direct conversion using the natural language instruction
        process_and_generate_diagrams(nl_instruction)

else:
    # Check if there is PlantUML code in the session state before creating the text_area
    if st.session_state['plantuml_code']:
        # Generate and display the diagram
        output_puml_file, output_png_file, error_message = generate_uml_diagram(
            st.session_state['plantuml_code'], output_dir=output_dir, plantuml_jar_path=plantuml_jar_path
        )
        if output_png_file:
            # Conditionally display the plan if it exists
            if 'plan' in st.session_state:
                st.subheader('Done thinking! Here is the plan:')
                st.write(st.session_state['plan'])

            # Display the generated diagram
            st.image(str(output_png_file), caption='Diagram generated by Peter', use_column_width=False)
            
            # Provide a download button for the image
            get_image_download_link(str(output_png_file))

            if display_code:
                st.text("🥳 Here's your PlantUML code if you need to generate this graph else where:")
                plantuml_code = st.code(
                    body=st.session_state['plantuml_code'],
                    line_numbers=True
                )
            


