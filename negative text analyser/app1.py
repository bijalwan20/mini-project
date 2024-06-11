import streamlit as st
import pandas as pd

import numpy as np
from prediction import xgb_predict, lr_predict, xgb_suicide

import nltk
from nltk import sent_tokenize, word_tokenize

import pdfplumber
import danger_words
from fpdf import FPDF

nltk.download('punkt')

#convert ke leye string to PDF 
def StringToPDF(string):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)
    pdf.set_font('DejaVu', size=14)
    pdf.multi_cell(190, 10, txt=string)
    return bytes(pdf.output(dest='S').encode('latin1'))



def WriteToFile(flaglist, title):
    string = "\n*" + title + "*\n"
    for i, flag in enumerate(flaglist, start=1):
        string += str(i) + ". " + flag.replace("\n", " ") + "\n"
    if not flaglist:
        string += "No red flags found!"
    string += "\n"
    return string



#ye wala flag analyze or display karne ke leye 
def ShowFlags(flaglist):
    count = 0
    flagcount = len(flaglist)
    if flagcount == 0:
        st.write("No red flags found!")
    else:
        with st.expander("Found " + str(flagcount) + " red flag/s:", True):
            for flag in flaglist:
                count += 1
                st.write(str(count) + ". " + flag)
            st.write("\n")



#ye analyze text for flags
def Display(essay, progress=None, filename=None):
    if essay:
        sentences = sent_tokenize(essay)
        xgflags = []
        lrflags = []
        xgsflags = []
        wrflags = []

        concerning_words = danger_words.GetDangerWords()

        loading = st.progress(0, text="Loading...")
        for i, sentence in enumerate(sentences, start=1):
            loading.progress(i / len(sentences), text=f"Analyzing sentence {i}/{len(sentences)}...")
            if xgb_predict(sentence) == 1:
                xgflags.append(sentence)
            if lr_predict(sentence) == 1:
                lrflags.append(sentence)
            if xgb_suicide(sentence) == 1:
                xgsflags.append(sentence)
            if any(word in concerning_words for word in word_tokenize(sentence.lower())):
                wrflags.append(sentence)
                
        loading.progress(1, text="Complete!")
        
        with col1:
            st.write("### Concerning Words Test")
            ShowFlags(wrflags)
        with col2:
            st.write("### Potential Struggles Test")
            ShowFlags(lrflags)
        with col3:
            st.write("### Depressive Thoughts Test")
            ShowFlags(xgflags)
        with col4:
            st.write("###  Destructive Thoughts Test")
            ShowFlags(xgsflags)
        
        if filename:
            string = ("Results for " + filename + ":\n").upper()
        else:
            string = "Results:\n"
        string += WriteToFile(xgsflags, "Destructive Thoughts")
        string += WriteToFile(xgflags, "Depressive Thoughts")
        string += WriteToFile(lrflags, "Potential Struggles")
        string += WriteToFile(wrflags, "Concerning Words")
        return string



# extract text from PDF 
def GetPDFText(uploaded_file):
    data = ""
    try:
        with pdfplumber.open(uploaded_file) as current_pdf:
            for page in current_pdf.pages:
                data += page.extract_text()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
    return data






# Function to refresh the app
def Refresh():
    st.stop()



st.title("Welcome to :red[Mental Stress Predictor]")
st.subheader("Text-based Early Distress Detector for Youth", anchor="welcome-to-Mental-Stress-Predictor")
st.caption("In the sidebar, enter :red[TEXT] that is reflective of a person's thoughts: essays, reflections, and chat conversations work best.\n Mental Stress Predictor will use ML Train Model to display sentences that may be a cause for concern.")
st.write("\n")

col1, col2, col3, col4 = st.columns(4)

with st.sidebar:
    st.title("Enter your text to analyze your thoughts:")
    essay = st.text_area("Enter your text :")
    if st.button("Submit Text"):
        string = Display(essay)
        st.download_button("Download Report", StringToPDF(string), file_name="Report.pdf")
    uploaded_file = st.file_uploader('Upload a PDF file:', type="pdf")
    if uploaded_file and st.button("Submit File"):
        string = Display(GetPDFText(uploaded_file), "1/1", uploaded_file.name)
        st.download_button("Download Report", StringToPDF(string), file_name="Report.pdf")
