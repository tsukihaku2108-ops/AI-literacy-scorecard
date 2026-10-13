import streamlit as st

st.set_page_config(page_title="AI Literacy Scorecard", page_icon="🧭")
st.title("🧭 AI Literacy Scorecard")
st.subheader("Công cụ tự đánh giá năng lực sử dụng AI trong học tập")
st.warning("BẢN NGUYÊN MẪU SƠ CẤP. Thang câu hỏi và ngưỡng diễn giải chưa được kiểm định; kết quả chỉ mang tính tham khảo.")
st.write("Chọn mức độ phù hợp với bản thân. Không nhập tên, email hoặc thông tin cá nhân.")

sections = {
    "Nhận thức về AI": [
        "Tôi biết chatbot AI có thể đưa ra thông tin sai hoặc thiếu chính xác.",
        "Tôi hiểu câu trả lời của AI cần được đánh giá theo ngữ cảnh.",
        "Tôi nhận biết được một số giới hạn của chatbot AI."
    ],
    "Kỹ năng sử dụng AI": [
        "Tôi biết cách đặt câu hỏi rõ ràng để nhận được câu trả lời hữu ích.",
        "Tôi biết yêu cầu AI giải thích lại khi chưa hiểu.",
        "Tôi dùng AI như công cụ hỗ trợ, không thay thế hoàn toàn việc tự suy nghĩ."
    ],
    "Kiểm chứng thông tin": [
        "Tôi kiểm tra thông tin do AI cung cấp trước khi sử dụng.",
        "Tôi đối chiếu thông tin với sách giáo khoa hoặc nguồn chuyên môn đáng tin cậy.",
        "Tôi xem xét bằng chứng thay vì tin ngay câu trả lời nghe có vẻ thuyết phục."
    ],
    "An toàn và trách nhiệm": [
        "Tôi tránh nhập thông tin cá nhân hoặc dữ liệu nhạy cảm vào chatbot AI.",
        "Tôi cân nhắc độ chính xác và tác động của nội dung AI trước khi chia sẻ.",
        "Tôi chú ý đến quyền riêng tư, bản quyền và trách nhiệm khi sử dụng nội dung AI."
    ]
}
labels = {
    1: "1 — Hoàn toàn không đồng ý",
    2: "2 — Không đồng ý",
    3: "3 — Phân vân",
    4: "4 — Đồng ý",
    5: "5 — Hoàn toàn đồng ý"
}
responses = {}
with st.form("scorecard"):
    for section, questions in sections.items():
        st.markdown("### " + section)
        for i, question in enumerate(questions):
            responses[f"{section}_{i}"] = st.radio(
                question, [1, 2, 3, 4, 5],
                format_func=lambda x: labels[x], key=f"{section}_{i}"
            )
        st.divider()
    submitted = st.form_submit_button("Tính điểm tự đánh giá", type="primary")

if submitted:
    scores = {}
    for section, questions in sections.items():
        scores[section] = sum(responses[f"{section}_{i}"] for i in range(len(questions))) / len(questions)
    overall = sum(responses.values()) / len(responses)
    st.header("Kết quả tự đánh giá")
    st.metric("Điểm trung bình chung", f"{overall:.2f}/5")
    for section, score in scores.items():
        st.write(f"**{section}:** {score:.2f}/5")
        st.progress(score / 5)
    if overall < 2.5:
        advice = "Hãy bắt đầu bằng việc kiểm chứng câu trả lời AI, đặt câu hỏi rõ ràng và bảo vệ dữ liệu cá nhân."
    elif overall < 4:
        advice = "Hãy duy trì các thói quen tốt và tăng cường đối chiếu với nguồn đáng tin cậy."
    else:
        advice = "Hãy tiếp tục kiểm chứng thông tin và nhớ rằng điểm tự đánh giá không phải chứng nhận năng lực."
    st.subheader("Gợi ý cải thiện")
    st.write(advice)
    st.info("Các ngưỡng gợi ý trong bản mẫu chỉ để minh họa giao diện, chưa được xác thực bằng dữ liệu nghiên cứu.")
st.caption("Bản mẫu không lưu câu trả lời lên máy chủ.")
