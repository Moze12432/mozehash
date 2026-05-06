import streamlit as st
import hashlib
import os

st.set_page_config(page_title="Hashing Security System", layout="centered")

st.title("🔐 Secure Hashing System")
st.subheader("Password Storage & Data Integrity Verification")

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

def generate_salt():
    return os.urandom(16).hex()

def hash_file(file_data):
    return hashlib.sha256(file_data).hexdigest()

# -----------------------------
# SESSION STORAGE
# -----------------------------
if "stored_hash" not in st.session_state:
    st.session_state.stored_hash = None
    st.session_state.salt = None

# -----------------------------
# MODE SELECT
# -----------------------------
mode = st.radio("Select Mode:", ["Register", "Login", "File Integrity Check"])

# -----------------------------
# REGISTER
# -----------------------------
if mode == "Register":
    st.markdown("### 📝 Register Password")

    password = st.text_input("Enter password:", type="password")

    if st.button("Store Securely"):
        salt = generate_salt()
        hashed = hash_password(password, salt)

        st.session_state.stored_hash = hashed
        st.session_state.salt = salt

        st.success("✅ Password stored securely!")

        st.code(f"Salt: {salt}")
        st.code(f"Hash: {hashed}")

# -----------------------------
# LOGIN
# -----------------------------
elif mode == "Login":
    st.markdown("### 🔑 Verify Password")

    password = st.text_input("Enter password:", type="password")

    if st.button("Verify"):
        if st.session_state.stored_hash is None:
            st.warning("⚠️ No password stored. Register first.")
        else:
            hashed = hash_password(password, st.session_state.salt)

            if hashed == st.session_state.stored_hash:
                st.success("✅ Access Granted")
            else:
                st.error("❌ Access Denied")

# -----------------------------
# FILE INTEGRITY CHECK
# -----------------------------
elif mode == "File Integrity Check":
    st.markdown("### 📁 Verify File Integrity")

    uploaded_file = st.file_uploader("Upload a file")

    if uploaded_file:
        file_data = uploaded_file.read()
        file_hash = hash_file(file_data)

        st.code(f"File Hash: {file_hash}")

        reference_hash = st.text_input("Enter original hash to compare:")

        if st.button("Verify File"):
            if reference_hash == file_hash:
                st.success("✅ File is intact (no changes)")
            else:
                st.error("❌ File has been modified!")
