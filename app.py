import pandas as pd
import streamlit as st
from itertools import chain
from math import nan

SHEET = "data/whitelist.csv"

def get_df(spreadsheet):
    return pd.read_csv(spreadsheet, sep=",")

def get_lists(raw):
    raw = raw.drop(raw.columns[0], axis=1).values.tolist()

    w = [x.lower() for x in list(chain.from_iterable(raw)) if type(x) == str]
    b = ["daniel labrador"]

    return w, b

def setup_streamlit():
    st.set_page_config(layout="wide")
    st.title('ΣΧ Door Assist')

def check_name(name, whitelist, blacklist):
    if " ".join(name) in whitelist:
        st.success("Whitelisted")
    elif " ".join(name) in blacklist:
        st.error("Blacklisted")
    else:
        wfirsts = [x for x in whitelist if name[0] in x.split()]
        wlasts = [x for x in whitelist if name[1] in x.split()]
        bfirsts = [x for x in blacklist if name[0] in x.split()]
        blasts = [x for x in blacklist if name[1] in x.split()]
        
        st.warning("Not listed. Potential Whitelist Matches:")
        for match in set(wlasts + wfirsts):
            st.write(match.title())
        st.warning("Not listed. Potential Blacklist Matches:")
        for match in set(blasts + bfirsts):
            st.write(match.title())

if __name__ == "__main__":
    raw = get_df(SHEET)
    whitelist, blacklist = get_lists(raw)
    setup_streamlit()

    st.header("Check Name")
    name = st.text_input("First Name Last Name: ", "Joe Smith").split(" ")
    if len(name) < 2:
        name += "None"
    elif len(name) > 2:
        name = [name[0], name[-1]]
    
    check_name(list(map(str.lower, name)), whitelist, blacklist)
    st.text("")
    
    st.header("Full Whitelist")
    raw