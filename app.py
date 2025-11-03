import streamlit as st
import requests
import yaml
from datetime import date

# Cấu hình trang
st.set_page_config(page_title="Tạo mã Dịch vụ công (.VN)", layout="wide")

# Đọc cấu hình từ file config.yaml
with open("config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

st.title("📄 Yêu cầu tạo mã Dịch vụ công (.VN)")

# --- 1. Chọn nghiệp vụ ---
nghiep_vu = st.selectbox("Nghiệp vụ", ["Chuyển nhượng tên miền", "Đổi tên chủ thể"])

# --- 2. Nhập nhiều tên miền ---
st.subheader("Tên miền (.vn)")
st.caption("Nhập từng tên miền, sau đó nhấn ➕ để thêm tên miền khác")

# Dùng session_state để lưu danh sách tên miền
if "domains" not in st.session_state:
    st.session_state.domains = [""]

cols = st.columns([6, 1])
for i, domain in enumerate(st.session_state.domains):
    with cols[0]:
        st.session_state.domains[i] = st.text_input(
            f"Tên miền {i+1}", value=domain, key=f"domain_{i}"
        )
    with cols[1]:
        if st.button("🗑️", key=f"remove_{i}"):
            st.session_state.domains.pop(i)
            st.rerun()

if st.button("➕ Thêm tên miền"):
    st.session_state.domains.append("")
    st.rerun()

# --- 3. Chọn ngày tiếp nhận hồ sơ ---
st.subheader("Ngày tiếp nhận hồ sơ")
ngay_tiep_nhan = st.date_input("Chọn ngày:", value=date.today())

# --- 4. Gửi yêu cầu ---
if st.button("🚀 Gửi yêu cầu"):
    valid_domains = [d.strip() for d in st.session_state.domains if d.strip()]
    if not valid_domains:
        st.warning("Vui lòng nhập ít nhất một tên miền.")
    else:
        payload = {
            "api_key": cfg["api_key"],
            "nghiep_vu": nghiep_vu,
            "ten_mien": valid_domains,
            "ngay_tiep_nhan": str(ngay_tiep_nhan),
        }
        with st.spinner("Đang gửi yêu cầu tới hệ thống..."):
            try:
                resp = requests.post(cfg["api_url"], json=payload, timeout=60)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("status") == "success":
                        st.success(f"✅ Mã DVC: {data.get('ma_dvc')}")
                    else:
                        st.error(f"❌ Lỗi: {data.get('message')}")
                else:
                    st.error(f"⚠️ Lỗi kết nối tới Agent ({resp.status_code})")
            except Exception as e:
                st.error(f"Lỗi hệ thống: {e}")
