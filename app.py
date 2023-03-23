import pandas as pd
import streamlit as st
from itertools import chain

W_SHEET, B_SHEET = "data/whitelist.csv", "data/blacklist.csv"

def setup_streamlit():
    st.set_page_config(layout="wide")
    st.title('Whitelist Assist')
    st.write("Alejandro Alonso UChicago '26")

def add_lists():
    whitelists = st.file_uploader("Add Whitelist(s)", 
                                  type=["csv"],
                                  accept_multiple_files=True)
    blacklists = st.file_uploader("Add Blacklist(s)",
                                  type=["csv"],
                                  accept_multiple_files=True)

@st.cache_data
def get_lists(wsheets, b_sheet):
    res = []
    for wsheet in wsheets:
        raw = pd.read_csv(wsheet, sep=",")
        lst = raw.drop(raw.columns[0], axis=1).values.tolist()
        lst = [x.lower() for x in list(chain.from_iterable(lst)) if isinstance(x, str)]
        res += lst
    
    raw_b = pd.read_csv(b_sheet, sep=",")
    b = [x.lower() for x in raw_b.Name.values.tolist() if type(x) == str]
    return raw, res, raw_b, b

def check_name(name, whitelist, blacklist):
    if " ".join(name) in blacklist:
        st.error("Blacklisted")
    elif " ".join(name) in whitelist:
        st.success("Whitelisted")
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
    add_lists()
    raw_w, whitelist, raw_b, blacklist = get_lists([W_SHEET], B_SHEET)

    st.header("Check Name")
    name = st.text_input("First Name Last Name: ", "Joe Smith").split(" ")
    if len(name) < 2:
        name += "None"
    elif len(name) > 2:
        name = [name[0], name[-1]]
    
    check_name(list(map(str.lower, name)), whitelist, blacklist)
    st.text("")

    #st.header("Full Blacklist")
    #st.table(raw_b)