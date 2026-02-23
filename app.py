import streamlit as st
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
BUCKET = "clouddrive-lite-gurkirt"

st.set_page_config(page_title="CloudDrive Lite", page_icon="☁️")
st.title("☁️ CloudDrive Lite")

username = st.text_input("Enter your username")

if not username:
    st.warning("Username is required.")
    st.stop()

username = username.strip()

st.success(f"Welcome {username}")

# ---------------- Upload Section ----------------
st.subheader("Upload File")

uploaded_file = st.file_uploader("Choose file")

if uploaded_file:
    file_key = f"{username}/{uploaded_file.name}"

    try:
        s3.upload_fileobj(uploaded_file, BUCKET, file_key)
        st.success("File uploaded successfully!")
    except ClientError as e:
        st.error(f"Upload failed: {e}")

# ---------------- List Section ----------------
st.subheader("Your Files")

try:
    response = s3.list_objects_v2(Bucket=BUCKET)

    user_files = []

    if "Contents" in response:
        for obj in response["Contents"]:
            key = obj["Key"]

            # STRICT CHECK
            if key.startswith(f"{username}/") and not key.endswith("/"):
                user_files.append(key)

    if user_files:
        for file_key in user_files:
            file_name = file_key.split("/")[-1]

            col1, col2 = st.columns([3, 1])
            col1.write(file_name)

            file_obj = s3.get_object(Bucket=BUCKET, Key=file_key)
            file_data = file_obj["Body"].read()

            col2.download_button(
                label="Download",
                data=file_data,
                file_name=file_name,
                mime="application/octet-stream",
                key=file_key
            )
    else:
        st.info("No files uploaded yet.")

except ClientError as e:
    st.error(f"Error fetching files: {e}")
