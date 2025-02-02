import streamlit as st
from streamlit.runtime.state import SessionStateProxy
from typing import cast
from common import PRODUCT_TITLE
from settings import Settings
from chat import ChatPage


st.set_page_config(page_title=PRODUCT_TITLE, initial_sidebar_state="expanded")
Settings(widget=st.sidebar, store=cast(SessionStateProxy, st.session_state)).render()
ChatPage().render()
