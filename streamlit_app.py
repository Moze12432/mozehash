import streamlit as st
import hashlib
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Secure Login System", layout="centered")

# -----------------------------
# CUSTOM CSS (REAL LOGIN UI)
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.card {
    background-color: #1c1f26;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
}
.title {
    text-align: center;
    color: white;
}
.subtitle {
    text-align: center;
    color: #9ca3af;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HASH FUNCTIONS
# -----------------------------
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

def generate_salt():
    return os.urandom(16).hex()

def hash_file(file_data):
    return hashlib.sha256(file_data).hexdigest()

# -----------------------------
# SESSION STATE
# -----------------------------
if "stored_hash" not in st.session_state:
    st.session_state.stored_hash = None
    st.session_state.salt = None

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<h1 class='title'>🔐 Secure Login System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Hashing-based Password Security & Data Integrity</p>", unsafe_allow_html=True)

mode = st.radio("", ["Login", "Register", "File Integrity"], horizontal=True)

# -----------------------------
# LOGIN CARD
# -----------------------------
if mode == "Login":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Login")

    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if st.session_state.stored_hash is None:
            st.warning("⚠️ No account found. Please register first.")
        else:
            hashed = hash_password(password, st.session_state.salt)

            if hashed == st.session_state.stored_hash:
                st.success("✅ Login Successful")
            else:
                st.error("❌ Incorrect Password")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# REGISTER CARD
# -----------------------------
elif mode == "Register":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Create Account")

    password = st.text_input("Create Password", type="password")

    if st.button("Register"):
        salt = generate_salt()
        hashed = hash_password(password, salt)

        st.session_state.stored_hash = hashed
        st.session_state.salt = salt

        st.success("✅ Account Created Securely")

        with st.expander("🔍 View Security Details"):
            st.write("Salt:")
            st.code(salt)
            st.write("Hashed Password:")
            st.code(hashed)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# FILE INTEGRITY CARD
# -----------------------------
elif mode == "File Integrity":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("File Integrity Check")

    uploaded_file = st.file_uploader("Upload File")

    if uploaded_file:
        file_data = uploaded_file.read()
        file_hash = hash_file(file_data)

        st.write("Generated File Hash:")
        st.code(file_hash)

        reference_hash = st.text_input("Enter Original Hash")

        if st.button("Verify File"):
            if reference_hash == file_hash:
                st.success("✅ File is Authentic (Not Modified)")
            else:
                st.error("❌ File Integrity Compromised")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# EXPLANATION PANEL
# -----------------------------
st.markdown("---")
st.markdown("###  How This System Works")

st.info("""
1. Password is NEVER stored directly  
2. A random salt is generated  
3. Password + salt → hashed using SHA-256  
4. During login, hash is recomputed  
5. If hashes match → access granted  

This ensures security even if stored data is exposed.
""")
