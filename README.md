# Pictionary Bot

## Description
Pictionary Bot is a project aimed at developing an Optical Character Recognition (OCR) and word lookup tool to assist with guessing words from images and obfuscated prompts. 
This project is a work in progress, with separate functionalities for OCR and word lookup currently in place.

## Examples:

### Obfuscation taken from [Skribbl.io](https://skribbl.io/):
Performing an OCR on the following image would result in ```_a_t```.\
<img src="https://github.com/user-attachments/assets/0ac5a1c3-9eda-4385-aa89-d848545d5fa0" alt="Example Obfuscation 1 OCR" width="400">\
Upon pasting the OCR text into the lookup field, the search would yield 9 potential matches.\
<img src="https://github.com/user-attachments/assets/7e8c2f39-7a46-4b9c-ac38-37f1fca0d900" alt="Example Obfuscation 1 Lookup" width="400">

*NOTE TO SELF: INACCURATE OBFUSCATION EXAMPLE. 
THE OCR WOULD ACTUALLY YIELD* `_a_ta` *AS IT BELIEVES THE 4 TO BE A LOWERCASE A*

### Obfuscation taken from [DrawIt](https://www.roblox.com/games/3173458677/Draw-It):
Performing an OCR on the following image would result in ```d___i__```.\
<img src="https://github.com/user-attachments/assets/a0b44254-5e92-48b6-99c8-c56d57d483c6" alt="Example Obfuscation 2 OCR" width="400">\
Upon pasting the OCR text into the lookup field, the search would yield 1 potential match.\
<img src="https://github.com/user-attachments/assets/274f7fc3-c593-4d4e-99c1-b2853fafe56c" alt="Example Obfuscation 2 Lookup" width="400">

Currently, the OCR can only handle images that solely contain a string of underscores spliced with sparse characters (limited to the alphabet, periods and hyphens). Any other text or characters that deviate from this format will throw off the OCR. The wordlists that the lookup app references are also not up to date with the pictionary games they represent, nor are there a wide selection of wordlists to choose from. 

## Usage for OCR Testing
1. **Browse for an Image**: Use the `↑` button to select an image file for OCR processing.
2. **Paste from Clipboard**: Use the `📋` button or `Ctrl + V` to paste an image from the clipboard.
3. **Run OCR**: Click the `Run OCR` button to process the image and display the results.
4. **Clear Annotations**: Use the `Clear Annotations` button to remove annotations and start fresh.
5. **Reload Script**: Click the `⟳` button to restart the script.

<img src="https://github.com/user-attachments/assets/dd51353e-25e5-437c-83a4-450d2b5e3990" alt="OCR Testing 1" width="400">

## Usage for Word Lookup Testing
1. **Adding/Removing Words**: Click the `+` or `-` buttons to add or remove words from the user-added words list.
2. **Select Word Lists**: Select the wordlist(s) to read from. Currently only capable of writing to the user-added-words list.
3. **Recent Changes**: Views the 10 most recently added/removed words from the user-added-words list.  
4. **Always On Top**: Check or uncheck the `Always On Top` button to make this program stay on top of other applications.
5. **Up/Down Arrows**: When the cursor is not selected on the input field, use the up or down arrow keys to scroll through the potential word matches.

<img src="https://github.com/user-attachments/assets/45920fc2-332e-43d2-8864-cd583d83f0d9" alt="Word Lookup 1" width="400">

## Installation
Currently not meant for installation, but the OCR and word lookup functionalities can be explored by doing the following:
1. Clone the repository:
   ```bash
   git clone https://github.com/MilesMoosavi/pictionary-bot.git
   cd pictionary-bot
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

## Contributing
Currently posting for version control. While contribution is not expected, it is not unwelcome. Feel free to open issues or submit pull requests.
 
## License
This project is licensed under the MIT License.
