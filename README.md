# Make your own mad libs 
This application allows you to write their own mad lib and include the fill-in-the-blanks of their choice or use ChatGPT to generate
a mad lib based on your choice of a theme.

Finished mad libs can be saved as a word document with the filled text as well as the original text with the fill-in-the-blanks. These documents can be opened to re-load a mad lib and fill it out again and again! Finally, a user can set the background image of their choice as opposed to the default silly face image I made in paint. 

The inputs_file.py script contains the list of available fill-in-the-blank types and more can be added as desired. Add a new entry to the inputs dictionary where the key is the keyboard shortcut and the value is the fill-in-the-blank type (e.g., "i": "Instrument"). The custom fill-in-the-blank type allows you to enter any type you would like. 

ChatGPT uses only the original list of types to generate a mad lib. More types can be added within the ChatGPT function starting at line 310.

# Example


# Installation

1. Install Dependencies:
```
pip install docx
pip install pyqt6
pip install functional
pip install openai
```

2. Clone this repository (https://github.com/amhelmi/mad_libs_app.git).

3. Create your own OpenAI key (https://platform.openai.com/api-keys) and add it to your computer.

4. Run python script or use executable.

If the OpenAI key cannot be found automatically, enter the key manually into line 88 of the mad_libs.py file.

# Controls 
## Creating your own mad lib

1. Enter a theme of your choice in the theme text box.

2. Begin typing your own mad lib in the main text window.

3. Add any of the fill-in-the-blank types at any point in the text by clicking the button.
  - When a type is selected, it will be added to where the cursor is in the text.
  - A fill-in-the-blank may be deleted manually or by clicking undo to remove the most recent type from the text.

4. Custom fill-in-the-blank types can be created on the fly as needed.

5. Once the text is written and the fill-in-the-blanks have been generated, click Done.

6. A new window will open to allow for responses to be added.

7. The text will fully update after all the responses have been added.

8. After the mad lib is completed, it can be saved for future use.

9. Select the **Clear** button to start a new mad lib.


## Using ChatGPT to make a mad lib

1. Select **File** in the top left of the window.

2. Select **Generate a mad lib**.

3. A prompt will appear asking for a theme. Enter a theme of your choice and select ok.

  - The current default theme is Winter.

4. A new prompt will appear asking for how many fill-in-the-blanks ChatGPT should create within the text.
  - If no number is entered, it will choose a random number between 1 and 10.

5. Wait for ChatGPT to create the content.
 - ChatGPT will try a maximum of 3 times to generate the text with the correct number of responses before failing.

6. Once the content has been created, responses can be put in and the mad lib filled out.

7. ChatGPT does not check if the theme makes any sense for now and may make grammar errors in the text.

## Saving a mad lib

1. Select **File** in the top left of the window.

2. Select **Save File**.

3. Select a name for your document and click save.


## Opening a mad lib

1. Select **File** in the top left of the window.

2. Select **Open File**.

3. Choose the mad lib you wish to do again.

4. The mad lib text with the original fill-in-the-blanks will be loaded into the main text window.

5. All buttons are enabled to allow for adding of new fill-in-the-blanks or re-writing some of the text.


## Changing the background image

1. Select **File** in the top left of the window.

2. Select **Change Background**.

3. Select the image of your choice from your computer and it will be added as the background.


# Limitations
The application does not currently check if the fill-in-the-blank responses are expected input types (e.g., checking if a number is entered for a Number prompt). 

The application closes completely if a user clicks cancel in any window. This will be updated to only close the focused window.

Adding a custom prompt type does not allow you to save it as a future available button. This will be updated to include a button to save a custom prompt type for future use. 

The only way to change the default background image is within the python code. This will be updated to allow a user to use the most recent image as the default.
