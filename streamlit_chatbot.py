import streamlit as st
import google.generativeai as genai

# Configure Gemini API (replace with your API key)
genai.configure(api_key='Your_api_key')

model = genai.GenerativeModel('gemini-pro')

st.title("Chatbot")
st.caption("A Streamlit chatbot powered by Gemini")

if "messages" not in st.session_state:
  st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat history
for msg in st.session_state.messages:
  st.chat_message(msg["role"]).write(msg["content"])

if prompt_msg := st.chat_input():
  # Add user message to history
  st.session_state.messages.append({"role": "user", "content": prompt_msg})
  st.chat_message("user").write(prompt_msg)

  def generate_response_with_gemini(prompt):

    # Build prompt considering conversation history
    history = " ".join([msg["content"] for msg in st.session_state["messages"] if msg["role"] != "assistant"])
    prompt = f"  Context: {history}. User query: for the message: {prompt_msg}, if it is health, medicine or disease related, generate required response which must include what disease the symptoms indicate, home remedies if possible and other courses of action. Otherwise generate response prompting user to enter health related query. Essentailly act like a health assistant"

    try:
      response = model.generate_content(prompt)

    except ValueError as e:
      # Handle safety errors
      if "safety_ratings" in str(e):
        st.error("The topic you entered might be sensitive. Please choose a different topic.")
        return None  # Indicate error by returning None
      else:
        raise e  # Re-raise other ValueErrors

    # Return the generated text
    return response.text  # Access the first generated text

  response = generate_response_with_gemini(prompt_msg)
  if response:
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
  else:
    st.warning("I am unable to answer that question at this time.")

