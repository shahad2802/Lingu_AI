from transformers import pipeline
import google.generativeai as genai
import streamlit as st

key = "AIzaSyBUQhOgsMRwJNttWusGdRD7CyAFt4_PhXw"

genai.configure(
    api_key= key
)

# Initialize the generative model for chat
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Load the saved models
translator = pipeline("translation", model="shahad-alh/translateAR_EN", tokenizer="shahad-alh/translateAR_EN")

translator2 = pipeline("translation", model="shahad-alh/translateEN_AR", tokenizer="shahad-alh/translateEN_AR")
def translate_AR_EN(text, source_lang="ar", target_lang="en"):
    translated_text = translator(text, src_lang=source_lang, tgt_lang=target_lang)
    return translated_text[0]["translation_text"]

def translate_EN_AR(text, source_lang="en", target_lang="ar"):
    translated_text = translator2(text, src_lang=source_lang, tgt_lang=target_lang)
    return translated_text[0]["translation_text"]



def Gemini_respon(text):
    ai_response = chat.send_message(text).text
    return ai_response

def translate_and_learn(text):
  excluded_keywords = ["ترجم", "هل يمكنك ترجمة", "هل يمكن أن تترجم"]
  if text.lower().startswith(tuple(excluded_keywords)):
    for keyword in excluded_keywords:
      if keyword.lower() in text.lower():
        # Extract the text to be translated after the keyword
        text_to_translate = text.split(keyword, 1)[-1].strip()
        # Perform translation only for the extracted text
        translated_text = translate_AR_EN(text_to_translate, source_lang="ar", target_lang="en")
        return text_to_translate, translated_text
  else:
    excluded_keywords = ["translate", "can you translate"]
    if text.lower().startswith(tuple(excluded_keywords)):
      for keyword in excluded_keywords:
        if keyword.lower() in text.lower():
          # Extract the text to be translated after the keyword
          text_to_translate = text.split(keyword, 1)[-1].strip()
          # Perform translation only for the extracted text
          translated_text = translate_EN_AR(text_to_translate, source_lang="en", target_lang="ar")
          return text_to_translate, translated_text
      else:
        return None

def main():
    st.markdown(
        """
        <style>
        .stTitle {
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            background-color: white;
            z-index: 1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("lingu AI")

    # Add some content to create space at the bottom of the page
    st.write(" " * 50)

    # Apply CSS to position the text input at the bottom
    st.markdown(
        """
        <style>
        .stTextInput {
            position: fixed;
            bottom: 10px;
            width: 50%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    user_input = st.text_input("You:", "")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    chat_history = st.session_state.chat_history
    if user_input:
        chat_history.append(f"You: {user_input}")
        if user_input.lower().startswith(("goodbye", "bye", "see you")):
            ai_response = "AI: Goodbye!"
        elif user_input.lower().startswith(("ترجم", "هل يمكن أن تترجم", "هل يمكنك ترجمة")):
             original, translated_text = translate_and_learn(user_input)
             if original and translated_text:
                    st.write(f"AI: {translated_text}{original} بالعربية، تُترجم إلى  ")
             else:
                    st.write("AI: Sorry, I couldn't process the translation request.")

        elif user_input.lower().startswith(("can you translate", "translate")):
                original, translated_text = translate_and_learn(user_input)
                if original and translated_text:
                    st.write(f"AI: Sure! In English, '{original}' translates to '{translated_text}'")
                else:
                    st.write("AI: Sorry, I couldn't process the translation request.")

        else:
            ai_response = Gemini_respon(user_input)
        chat_history.append(f"AI: {ai_response}")
        st.write("\n\n".join(chat_history))

    # Add a sidebar button icon for the game
    if st.button("Play Game"):
       # Add your game logic here
      st.write("AI: Let's play a game!")if __name__ == "__main__":
if __name__ == "__main__":
    main()
