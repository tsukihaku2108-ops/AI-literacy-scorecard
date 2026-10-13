import streamlit as st

st.set_page_config(
    page_title="AI Literacy Scorecard",
    page_icon="🧠",
    layout="centered",
)

st.title("🧠 AI Literacy Scorecard")
st.subheader("Công cụ tự đánh giá năng lực sử dụng AI trong học tập")
st.warning(
    "Bản khảo sát phục vụ mục đích tham khảo. Cách tính điểm và ngưỡng phân loại "
    "chưa được kiểm định khoa học; kết quả không phải bài kiểm tra năng lực khách quan."
)

LIKERT = [
    "1 — Hoàn toàn không đồng ý",
    "2 — Không đồng ý",
    "3 — Trung lập/không có ý kiến",
    "4 — Đồng ý",
    "5 — Hoàn toàn đồng ý",
]

# Giữ nguyên câu chữ theo tài liệu khảo sát gốc; chỉ bỏ xuống dòng do dàn trang Word.
SECTIONS = [
    (
        "1. MỨC ĐỘ SỬ DỤNG CHATBOT AI",
        [
            "Bạn thường sử dụng chatbot AI để hỗ trợ việc học",
            "Bạn sử dụng chatbot AI nhiều lần trong một tuần",
            "Bạn dùng chatbot AI khi làm bài tập về nhà",
            "Bạn sử dụng chatbot AI trong nhiều môn học khác nhau",
            "Bạn sử dụng chatbot AI ngay cả khi chưa tự tìm cách giải quyết vấn đề",
            "Bạn chủ động tìm hiểu cách sử dụng chatbot AI",
        ],
        False,
    ),
    (
        "2. MỤC ĐÍCH SỬ DỤNG CHATBOT AI",
        [
            "Bạn dùng chatbot AI để giải bài tập",
            "Bạn dùng chatbot AI để tra cứu kiến thức",
            "Bạn dùng chatbot AI để tóm tắt tài liệu",
            "Bạn dùng chatbot AI để ôn tập, chuẩn bị cho kiểm tra",
            "Bạn dùng chatbot AI để dịch",
            "Bạn dùng chatbot AI để tìm ý tưởng, lập dàn ý hoặc cải thiện cách diễn đạt khi viết bài",
            "Bạn dùng chatbot AI để tìm ý tưởng học tập",
            "Bạn sử dụng chatbot Ai để kiểm tra hoặc đánh giá câu trả lời/ bài làm của mình",
        ],
        False,
    ),
    (
        "3. ẢNH HƯỞNG CỦA CHATBOT AI ĐẾN HỌC TẬP",
        [
            "Chatbot AI giúp hoàn thành nhiệm vụ học tập hiệu quả hơn",
            "Chatbot AI giúp tiết kiệm thời gian học tập",
            "Chatbot AI giúp hiểu bài nhanh hơn",
            "Chatbot AI giúp cải thiện kết quả học tập",
            "Chatbot AI giúp tôi chủ động tìm hiểu những kiến thức mà mình chưa hiểu",
            "Chatbot AI giúp tăng hứng thú học tập",
            "Việc lạm dụng chatbot AI có thể làm giảm khả năng tư duy",
        ],
        True,
    ),
    (
        "4. MỨC ĐỘ TIN TƯỞNG VÀ NGUY CƠ PHỤ THUỘC AI",
        [
            "Bạn thường tin tưởng câu trả lời của chatbot AI mà không cần kiểm tra thêm",
            "Bạn cảm thấy khó hoàn thành một số nhiệm vụ học tập nếu không có chatbot AI hỗ trợ",
            "Bạn ưu tiên hỏi chatbot AI hơn tự tìm tài liệu",
            "Bạn thường sao chép câu trả lời từ chatbot AI mà không chỉnh sửa hoặc kiểm tra thêm",
            "Bạn ít tự suy nghĩ khi có chatbot AI hỗ trợ",
            "Bạn sử dụng chatbot AI ngay cả khi có thể tự giải quyết vấn đề",
        ],
        True,
    ),
    (
        "5. KĨ NĂNG SỬ DỤNG AI",
        [
            "Bạn biết cách đặt câu hỏi rõ ràng để chatbot AI đưa ra câu trả lời phù hợp",
            "Bạn biết rằng chatbot AI có thể đưa ra thông tin sai, thiếu chính xác hoặc không phù hợp với một số vấn đề",
            "Bạn chú ý bảo mật thông tin cá nhân khi dùng chatbot AI",
            "Bạn yêu cầu chatbot AI giải thích hoặc làm rõ khi chưa hiểu câu trả lời.",
            "Bạn cố gắng tự giair quyết vấn đề trước khi nhờ chatbot AI hỗ trợ",
            "Bạn biết cách sử dụng chatbot AI phục vụ học tập hiệu quả",
        ],
        True,
    ),
    (
        "6.HÀNH VI KIỂM CHỨNG THÔNG TIN AI",
        [
            "Khi kiểm chứng thông tin do AI cung cấp, bạn ưu tiên đối chiếu với các nguồn đáng tin cậy (ví dụ: sách giáo khoa, tài liệu chính thống hoặc nguồn chuyên môn)",
            "Đối chiếu thông tin với Sách giáo khoa hoặc tài liệu học tập",
            "Đọc lại câu trả lời để tìm điểm bất thường",
            "Không sử dụng ngay thông tin AI nếu chưa kiểm chứng",
            "Nếu phát hiện thông tin đáng ngờ, bạn tìm nguồn khác để xác minh",
        ],
        True,
    ),
    (
        "7.QUYỀN DỮ LIỆU CÁ NHÂN VÀ NHẬN THỨC PHÁP LÍ",
        [
            "Bạn biết rằng việc chia sẻ thông tin cá nhân với chatbot AI có thể tạo ra rủi ro về quyền riêng tư",
            "Bạn hiểu rằng việc sử dụng dữ liệu hoặc hình ảnh của người khác trên AI cần tôn trọng quyền riêng tư và sự cho phép phù hợp",
            "Bạn biết rằng người sử dụng phải chịu trách nhiệm đối với nội dung do mình tạo ra hoặc chia sẻ bằng AI",
            "Bạn biết rằng việc dùng AI để tạo hoặc phát tán thông tin giả, xúc phạm hoặc gây hại cho người khác có thể dẫn đến hậu quả nghiêm trọng",
            "Bạn có thói quen kiểm tra nội dung do AI tạo ra trước khi chia sẻ cho người khác",
            "Chatbot AI có thể tạo ra thông tin giả hoặc sai lệch",
            "Bạn biết việc sử dụng một số nội dung do người khác tạo ra có thể liên quan đến vấn đề bản quyền",
            "Bạn biết rằng người dùng cần xin phép trước khi sử dụng dữ liệu của người khác trên AI",
            "Bạn biết rằng cần kiểm tra và cân nhắc tác động của nội dung do AI tạo ra trước khi chia sẻ cho người khác",
            "Bạn biết rằng việc sử dụng AI cần tuân thủ quy định pháp luật",
        ],
        True,
    ),
]

st.markdown(
    "Hãy chọn một mức độ đồng ý cho từng phát biểu. Vui lòng trả lời theo trải nghiệm "
    "của bạn; không có câu trả lời đúng hay sai."
)

with st.form("ai_literacy_survey"):
    st.markdown("### Thông tin chung (không bắt buộc)")
    respondent_code = st.text_input(
        "Mã người tham gia (nếu có; không nhập họ tên hoặc thông tin định danh)",
        value="",
    )

    answers = {}
    for section_index, (section_title, questions, scored) in enumerate(SECTIONS):
        st.markdown("---")
        st.markdown(f"### {section_title}")
        if not scored:
            st.caption("Nhóm câu hỏi mô tả thực trạng sử dụng AI; không cộng vào điểm năng lực.")
        for question_index, question in enumerate(questions):
            key = f"q_{section_index}_{question_index}"
            answers[key] = st.radio(
                question,
                options=LIKERT,
                index=None,
                key=key,
                horizontal=False,
            )

    submitted = st.form_submit_button("Tính điểm và xem kết quả", type="primary")

if submitted:
    unanswered = [
        question
        for section_index, (_, questions, _) in enumerate(SECTIONS)
        for question_index, question in enumerate(questions)
        if answers.get(f"q_{section_index}_{question_index}") is None
    ]

    if unanswered:
        st.error(f"Bạn còn {len(unanswered)} câu chưa trả lời. Hãy hoàn thành trước khi tính điểm.")
    else:
        scored_values = []
        section_scores = []

        for section_index, (section_title, questions, scored) in enumerate(SECTIONS):
            if not scored:
                continue

            values = []
            for question_index, _ in enumerate(questions):
                selected = answers[f"q_{section_index}_{question_index}"]
                raw_score = int(selected[0])

                # Nhóm 4 là nhóm nguy cơ phụ thuộc: điểm được đảo chiều.
                if section_index == 3:
                    raw_score = 6 - raw_score

                values.append(raw_score)

            scored_values.extend(values)
            section_score = ((sum(values) / len(values) - 1) / 4) * 100
            section_scores.append((section_title, section_score))

        total_score = ((sum(scored_values) / len(scored_values) - 1) / 4) * 100

        if total_score <= 40:
            level = "AI Rookie"
            interpretation = "Điểm tự đánh giá hiện ở mức thấp theo ngưỡng phân loại dự kiến."
        elif total_score <= 70:
            level = "AI User"
            interpretation = "Điểm tự đánh giá hiện ở mức trung bình theo ngưỡng phân loại dự kiến."
        else:
            level = "AI Master"
            interpretation = "Điểm tự đánh giá hiện ở mức cao theo ngưỡng phân loại dự kiến."

        st.markdown("---")
        st.header("Kết quả tự đánh giá")
        st.metric("Điểm AI Literacy dự kiến", f"{total_score:.1f}/100")
        st.subheader(level)
        st.write(interpretation)
        st.progress(int(round(total_score)))

        st.markdown("### Điểm theo từng nhóm được tính")
        for section_title, section_score in section_scores:
            st.write(f"**{section_title}** — {section_score:.1f}/100")
            st.progress(int(round(section_score)))

        st.info(
            "Cách tính hiện tại: nhóm 1–2 không cộng điểm; nhóm 3, 5, 6, 7 chấm thuận; "
            "nhóm 4 đảo chiều. Điểm tổng được chuẩn hóa về thang 0–100. "
            "Đây là quy tắc vận hành dự kiến đã bàn, chưa phải thang đo được kiểm định."
        )

        with st.expander("Xem lại câu trả lời của bạn"):
            for section_index, (section_title, questions, _) in enumerate(SECTIONS):
                st.markdown(f"**{section_title}**")
                for question_index, question in enumerate(questions):
                    st.write(f"- {question}: {answers[f'q_{section_index}_{question_index}']}")

        st.caption("Cảm ơn bạn đã thực hiện khảo sát!")

st.markdown("---")
st.caption(
    "Lưu ý quyền riêng tư: ứng dụng này không yêu cầu họ tên, email hoặc thông tin cá nhân. "
    "Không nhập thông tin định danh vào phần mã người tham gia."
)
