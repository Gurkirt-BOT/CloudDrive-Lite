import streamlit as st
import boto3
from botocore.exceptions import ClientError

# ---------------- CONFIG ----------------
BUCKET_NAME = "clouddrive-lite-gurkirt"
REGION = "ap-south-1"                      

s3 = boto3.client("s3", region_name=REGION)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CloudDrive Lite",
    page_icon="☁️",
    layout="wide"
)

st.title("☁️ CloudDrive Lite")
st.caption("Secure file storage using EC2 IAM Role + S3")

username = st.text_input("Enter your username")

if username:

    st.markdown("---")

    # ---------------- UPLOAD FORM (NO LOOP) ----------------
    st.subheader("📤 Upload File")

    with st.form("upload_form", clear_on_submit=True):
        uploaded_file = st.file_uploader(
            "Drag & Drop or Click to Upload"
        )
        upload_button = st.form_submit_button("Upload")

        if upload_button and uploaded_file:
            try:
                file_key = f"{username}/{uploaded_file.name}"
                s3.upload_fileobj(uploaded_file, BUCKET_NAME, file_key)
                st.success("✅ File uploaded successfully!")
            except ClientError as e:
                st.error(f"Upload failed: {e}")

    st.markdown("---")

    # ---------------- REFRESH BUTTON ----------------
    if st.button("🔄 Refresh Files"):
        st.rerun()

    # ---------------- FETCH FILES ----------------
    try:
        response = s3.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=f"{username}/"
        )
        files = response.get("Contents", [])
    except:
        files = []

    if files:

        sort_option = st.selectbox(
            "Sort by",
            ["Name", "Size", "Last Modified"]
        )

        if sort_option == "Name":
            files = sorted(files, key=lambda x: x["Key"])
        elif sort_option == "Size":
            files = sorted(files, key=lambda x: x["Size"], reverse=True)
        else:
            files = sorted(files, key=lambda x: x["LastModified"], reverse=True)

        st.subheader("📁 Your Files")

        cols = st.columns(4)

        for idx, file in enumerate(files):

            file_name = file["Key"].split("/")[-1]
            file_size = round(file["Size"] / 1024, 2)
            last_modified = file["LastModified"].strftime("%Y-%m-%d %H:%M")

            with cols[idx % 4]:
                st.write(f"📄 **{file_name}**")
                st.caption(f"Size: {file_size} KB")
                st.caption(f"Modified: {last_modified}")

                # Download
                file_obj = s3.get_object(
                    Bucket=BUCKET_NAME,
                    Key=file["Key"]
                )

                st.download_button(
                    "⬇ Download",
                    data=file_obj["Body"].read(),
                    file_name=file_name,
                    key=f"download-{idx}"
                )

                # Delete
                if st.button("🗑 Delete", key=f"delete-{idx}"):
                    s3.delete_object(
                        Bucket=BUCKET_NAME,
                        Key=file["Key"]
                    )
                    st.success("File deleted. Click refresh.")
                    
    else:
        st.info("No files uploaded yet.")

else:
    st.info("Enter username to continue.")
