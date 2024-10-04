```markdown
# DocGenie: Automated Code Documentation Generator

DocGenie is an intelligent application designed to automate the generation of code documentation. Utilizing AI capabilities, it creates clear, comprehensive, and engaging documentation tailored for both technical and non-technical audiences. Users can either input their code directly or upload a code file in various formats.

## Features

- **Multi-Format Support**: Upload code files in formats such as PDF, Python, Java, C, C++, JavaScript, HTML, CSS, and more.
- **Text Area Input**: Directly enter your code in the app for instant documentation generation.
- **Smart Code Analysis**: The app analyzes the code and generates detailed documentation.
- **Customizable Documentation**: Tailor the documentation style and focus with customizable prompts.
- **Downloadable Output**: Download the generated documentation as a Markdown file.

## Installation

To run this application locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/ankit-kk/docgenie.git
   cd docgenie
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key in `secrets.toml`:
   ```toml
   [openai]
   api_key = "your_openai_api_key"
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. You can either:
   - Enter your code directly into the text area provided.
   - Upload a code file using the file uploader.

4. Adjust the **Max tokens** slider to control the length of the generated documentation.

5. Click on **Generate Documentation** to create the documentation. 

6. The generated documentation will be displayed, and you will have the option to download it as a Markdown file.

## Example

1. Enter or upload your code.
2. Set the desired token limit.
3. Click on the **Generate Documentation** button.
4. View and download the generated documentation.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or features you'd like to add.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for building interactive web applications easily.
- [OpenAI](https://openai.com/) for providing the AI model that powers this app.
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) for PDF handling.
- [python-magic](https://github.com/ahupp/python-magic) for file type detection.

## Contact

For any questions or suggestions, feel free to reach out to me at ankitashuk20@gmail.com.

---

**Created with ❤️ by Ankit**
```

