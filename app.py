from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

CHARACTER_URL = "https://character.ai/chat/XrL_mFFjI9ERMND8CXocrQY1pxjB172gsV53x92z84Q"

def get_character_ai_response(user_input):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set to False for debugging
        page = browser.new_page()
        page.goto(CHARACTER_URL)

        # Wait for chatbox and send message
        page.fill("textarea", user_input)
        page.press("textarea", "Enter")

        # Wait for response
        page.wait_for_selector(".message-text")  # Adjust selector if needed
        bot_response = page.query_selector(".message-text").inner_text()

        browser.close()
        return bot_response

@app.route('/chat', methods=['GET'])
def chat():
    user_message = request.args.get('msg', '')
    if not user_message:
        return jsonify({'response': "Please provide a message."})

    response = get_character_ai_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
