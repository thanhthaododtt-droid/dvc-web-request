import streamlit as st
import requests
import yaml

st.set_page_config(page_title="Tạo mã DVC", layout="wide")

# cấu hình: bạn có thể upload config.yaml lên repo hoặc set trong UI
with open("config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

st.title("Yêu cầu tạo mã Dịch vụ công (.VN)")

nghiep_vu = st.selectbox("Nghiệp vụ", cfg["nghiep_vu"])
ten_mien = st.text_input("Tên miền (.vn)")
chu_the = st.text_input("Chủ thể (nếu có)")

if st.button("Gửi yêu cầu"):
    payload = {
        "api_key": cfg["api_key"],
        "nghiep_vu": nghiep_vu,
        "ten_mien": ten_mien,
        "chu_the": chu_the
    }
    try:
        resp = requests.post(cfg["api_url"], json=payload, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                st.success(f"Mã DVC: {data.get('ma_dvc')}")
            else:
                st.error(f"Lỗi: {data.get('message')}")
        else:
            st.error(f"Lỗi kết nối: {resp.status_code}")
    except Exception as e:
        st.error(f"Exception: {e}")
