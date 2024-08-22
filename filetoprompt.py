import streamlit as st
import PIL.Image as Image
import io
import requests
import asyncio
import time
import google.generativeai as genai
import bunny_file
import speech_recognition as sr

def speak():
    rec=sr.Recognizer()
    with sr.Microphone() as mic:
        sound=rec.listen(mic)
        text_rec=rec.recognize_google(sound)
        return text_rec
    
def fileAnalysis():
    flag = 0
    api = 'AIzaSyCBHTmgKXbiputUhfU9PlFUufQYVGqsMHs'
    genai.configure(api_key=api)
    img_model = genai.GenerativeModel('gemini-1.5-flash')
    
    with st.sidebar:
        img__ = st.select_slider("Choose an option:", ["Camera", "Device", "URL"], value="Device")
    
    if img__ == "Device":
        img_name = st.file_uploader("Upload the file from the computer:", type=['pdf', 'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'mp4', 'avi', 'mov','mp3','wav'])
        if img_name:
            content, file_type = bunny_file.process_file(img_name)
            if content:
                flag = 1
    
    elif img__ == "Camera":
        img = st.camera_input("Enter the camera input:")
        if img:
            img = Image.open(img)
            flag = 1
    
    elif img__ == 'URL':
        st.markdown("### :rainbow[Make sure that you are providing the correct URL]")
        input_url = st.text_input("Enter the URL:")
        if input_url:
            try:
                req = requests.get(input_url)
                byte = io.BytesIO(req.content)
                img = Image.open(byte)
                flag = 1
            except Exception as e:
                st.warning("Provide the correct URL - Hint: check whether the link ends with jpg or png and starts with http:// or https://")

    if flag:
        if file_type == 'image':
            col, _ = st.columns(2)
            with col:
                st.image(content, use_column_width=True)
        elif file_type == 'video':
            col, _ = st.columns(2)
            with col:
                st.video(img_name)
            content="Ellobrate the audio text,what is the audio described"
        elif file_type == 'audio':
            st.audio(img_name)
        else:
            st.markdown("### Document Uploaded Sucessfully")
            #st.text(content)
        
        if st.button("New attempt"):
            st.rerun()
        if file_type!='video':
            chat_c = st.radio("", ("Text📄", "Speak🎤"))
            st.session_state.img_input = ""
            
            if chat_c == "Text📄":
                st.session_state.img_input = st.text_input('**🤖**', placeholder='Enter the prompt...', disabled=False)
            
            elif chat_c == 'Speak🎤':
                st.markdown("### :violet[Speak now:] 🗣️ ")
                st.session_state.img_input = st.text_input('**🤖**', value=speak(), disabled=False)
        
        if st.button("Genrate"):
          for i in '1':
            if st.button("cancel"):
                break
            async def genmsg():
                return img_model.generate_content([st.session_state.img_input, content])
            
            async def spin():
                with st.spinner("Generating..."):
                    await asyncio.sleep(3)
            
            async def main():
                result, _ = await asyncio.gather(genmsg(), spin())
                return result
            
            result = asyncio.run(main())
            
            def generate():
                for i in result.text:
                    yield i
                    time.sleep(0.02)
            
            st.write_stream(generate)

fileAnalysis()