import pandas as pd
import streamlit as st
from itertools import chain
from math import nan

SHEET = "data/whitelist.csv"
st.set_page_config(layout="wide")

@st.cache_data
def get_lists(sheet):
    raw = pd.read_csv(sheet, sep=",")
    raw = raw.drop(raw.columns[0], axis=1).values.tolist()

    w = [x.lower() for x in list(chain.from_iterable(raw)) if type(x) == str]
    b = ["daniel labrador"]

    return raw, w, b

def setup_streamlit():
    st.title('ΣΧ Door Assist')
    st.write("Alejandro Alonso, Alpha Alpha, Sig '26")

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
        w, b = set(wlasts + wfirsts), set(blasts + bfirsts)
        if not w and not b:
            st.warning("Not listed. No Potential Matches.")
        elif w:
            st.warning("Not listed. Potential Whitelist Matches:")
            for match in w:
                st.write(match.title())
        elif b:
            st.warning("Not listed. Potential Blacklist Matches:")
            for match in b:
                st.write(match.title())

if __name__ == "__main__":
    setup_streamlit()
    raw, whitelist, blacklist = get_lists(SHEET)

    st.header("Check Name")
    name = st.text_input("First Name Last Name: ", "Joe Smith").split(" ")
    if len(name) < 2:
        name += "None"
    elif len(name) > 2:
        name = [name[0], name[-1]]
    
    check_name(list(map(str.lower, name)), whitelist, blacklist)
    st.text("")
    
    st.header("Full Whitelist")
    st.table(raw)