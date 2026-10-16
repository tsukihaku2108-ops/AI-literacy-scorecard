import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Literacy Scorecard", page_icon="🧭", layout="centered")

QUESTIONS = [
    (1, "Kĩ năng đặt câu hỏi", "Bạn biết cách đặt câu hỏi rõ ràng để chatbot AI đưa ra câu trả lời phù hợp.", False),
    (2, "Kĩ năng đặt câu hỏi", "Bạn yêu cầu chatbot AI giải thích hoặc làm rõ khi chưa hiểu câu trả lời.", False),
    (3, "Kĩ năng đặt câu hỏi", "Bạn biết cách sử dụng chatbot AI phục vụ học tập hiệu quả.", False),
    (4, "Tư duy độc lập", "Bạn cố gắng tự giải quyết vấn đề trước khi nhờ chatbot AI hỗ trợ.", False),
    (5, "Tư duy độc lập", "Bạn sử dụng chatbot AI như công cụ hỗ trợ thay vì phụ thuộc hoàn toàn.", False),
    (6, "Tư duy độc lập", "Bạn thường sao chép câu trả lời từ chatbot AI mà không chỉnh sửa hoặc kiểm tra thêm.", True),
    (7, "Kiểm chứng thông tin", "Bạn biết chatbot AI có thể đưa ra thông tin sai.", False),
    (8, "Kiểm chứng thông tin", "Khi kiểm chứng thông tin do AI cung cấp, bạn ưu tiên đối chiếu với các nguồn đáng tin cậy như sách giáo khoa hoặc tài liệu chính thống.", False),
    (9, "Kiểm chứng thông tin", "Nếu phát hiện thông tin đáng ngờ, bạn tìm nguồn khác để xác minh.", False),
    (10, "Quyền riêng tư và trách nhiệm", "Bạn chú ý bảo mật thông tin cá nhân khi dùng chatbot AI.", False),
    (11, "Quyền riêng tư và trách nhiệm", "Bạn hiểu rằng việc sử dụng dữ liệu hoặc hình ảnh của người khác trên AI cần tôn trọng quyền riêng tư và có sự cho phép phù hợp.", False),
    (12, "Quyền riêng tư và trách nhiệm", "Bạn biết rằng người sử dụng phải chịu trách nhiệm đối với nội dung do mình tạo ra hoặc chia sẻ bằng AI.", False),
]
GROUPS = ["Kĩ năng đặt câu hỏi", "Tư duy độc lập", "Kiểm chứng thông tin", "Quyền riêng tư và trách nhiệm"]
LIKERT = {
    "1 — Hoàn toàn không đồng ý": 1,
    "2 — Không đồng ý": 2,
    "3 — Phân vân": 3,
    "4 — Đồng ý": 4,
    "5 — Hoàn toàn đồng ý": 5,
}

st.title("🧭 AI Literacy Scorecard")
st.caption("Công cụ tự đánh giá năng lực sử dụng chatbot AI trong học tập")
st.info("Hãy trả lời theo trải nghiệm thực tế. Kết quả chỉ mang tính tham khảo, không dùng để xếp hạng cá nhân.")

with st.expander("Hướng dẫn và cách tính điểm"):
    st.markdown("""
    - Có 12 câu hỏi thuộc 4 nhóm năng lực, mỗi nhóm 3 câu.
    - Chọn mức từ 1 (Hoàn toàn không đồng ý) đến 5 (Hoàn toàn đồng ý).
    - Câu 6 được đảo chiều vì mô tả hành vi sao chép mà không kiểm tra.
    - Đây là bộ câu hỏi rút gọn phục vụ Scorecard, chưa phải thang đo đã được kiểm định chính thức.
    """)

with st.form("scorecard_form"):
    answers = {}
    for group in GROUPS:
        st.subheader(group)
        for qid, qgroup, question, reverse in QUESTIONS:
            if qgroup == group:
                answers[qid] = st.radio(
                    f"{qid}. {question}",
                    list(LIKERT.keys()),
                    index=None,
                    key=f"q_{qid}",
                )
    submitted = st.form_submit_button("Xem kết quả", type="primary", use_container_width=True)

if submitted:
    missing = [qid for qid, _, _, _ in QUESTIONS if not answers.get(qid)]
    if missing:
        st.error("Bạn hãy trả lời đủ 12 câu. Còn thiếu câu: " + ", ".join(map(str, missing)))
    else:
        raw = {qid: LIKERT[value] for qid, value in answers.items()}
        scored = {}
        for qid, _, _, reverse in QUESTIONS:
            scored[qid] = 6 - raw[qid] if reverse else raw[qid]

        total = sum(scored.values())
        overall = (total - 12) / 48 * 100
        group_scores = {}
        for group in GROUPS:
            ids = [qid for qid, qgroup, _, _ in QUESTIONS if qgroup == group]
            group_total = sum(scored[qid] for qid in ids)
            group_scores[group] = round((group_total - 3) / 12 * 100, 1)

        st.divider()
        st.subheader("Kết quả tự đánh giá")
        c1, c2 = st.columns(2)
        c1.metric("Điểm tổng hợp", f"{overall:.1f}/100")
        c2.metric("Tổng điểm sau quy đổi", f"{total}/60")
        st.progress(int(round(overall)))

        if overall < 40:
            st.write("**Nhận xét tổng quan:** Kết quả cho thấy bạn có thể bắt đầu từ những thói quen cơ bản khi học cùng AI. Hãy chọn một hoặc hai hành động nhỏ để luyện trước, thay vì cố thay đổi tất cả cùng lúc.")
        elif overall < 70:
            st.write("**Nhận xét tổng quan:** Bạn đã có một số thói quen hữu ích. Hãy xem các nhóm và câu trả lời cụ thể bên dưới để chọn kĩ năng cần luyện tiếp theo.")
        else:
            st.write("**Nhận xét tổng quan:** Bạn tự đánh giá khá tích cực về các thói quen sử dụng AI. Hãy tiếp tục duy trì chúng và chú ý những hành vi cụ thể vẫn còn cần cải thiện.")

        st.subheader("Điểm theo nhóm năng lực")
        chart_df = pd.DataFrame({"Nhóm năng lực": list(group_scores.keys()), "Điểm (0–100)": list(group_scores.values())})
        st.bar_chart(chart_df.set_index("Nhóm năng lực"))

        # Advice is generated from the user's actual item-level responses and group scores.
        group_advice = {
            "Kĩ năng đặt câu hỏi": {
                "focus": "Làm cho yêu cầu gửi đến AI rõ ràng và dễ trả lời hơn.",
                "actions": [
                    "Nêu rõ mục tiêu, bối cảnh và dạng câu trả lời mong muốn khi đặt câu hỏi.",
                    "Nếu chưa hiểu, yêu cầu AI giải thích bằng ngôn ngữ đơn giản hơn hoặc đưa ví dụ.",
                    "Sau câu trả lời đầu tiên, hãy hỏi tiếp để làm rõ điểm còn thiếu thay vì chấp nhận ngay."
                ],
                "challenge": "Chọn một nội dung đang học và viết lại câu hỏi theo cấu trúc: mục tiêu + bối cảnh + yêu cầu đầu ra."
            },
            "Tư duy độc lập": {
                "focus": "Giữ vai trò chủ động của bản thân khi sử dụng AI.",
                "actions": [
                    "Tự thử giải bài hoặc ghi ra ý tưởng ban đầu trước khi mở chatbot.",
                    "Yêu cầu AI đưa gợi ý từng bước hoặc phản biện cách làm, thay vì chỉ xin đáp án.",
                    "Đóng chatbot và tự trình bày lại kết quả bằng lời của mình để kiểm tra xem bạn đã hiểu chưa."
                ],
                "challenge": "Làm một bài tập theo cách của bạn trước, sau đó nhờ AI chỉ ra điểm cần xem lại và tự sửa bài."
            },
            "Kiểm chứng thông tin": {
                "focus": "Không xem câu trả lời của AI là đúng chỉ vì câu trả lời nghe có vẻ thuyết phục.",
                "actions": [
                    "Đối chiếu thông tin quan trọng với sách giáo khoa, tài liệu chính thống hoặc nguồn chuyên môn đáng tin cậy.",
                    "Kiểm tra riêng tên riêng, số liệu, công thức, trích dẫn và các khẳng định bất thường.",
                    "Nếu hai nguồn không thống nhất, ghi lại điểm khác biệt và hỏi giáo viên hoặc tìm thêm nguồn đáng tin cậy."
                ],
                "challenge": "Chọn một câu trả lời AI về bài học và xác minh ít nhất hai khẳng định bằng nguồn đáng tin cậy."
            },
            "Quyền riêng tư và trách nhiệm": {
                "focus": "Bảo vệ dữ liệu cá nhân và chịu trách nhiệm với nội dung được tạo hoặc chia sẻ bằng AI.",
                "actions": [
                    "Không nhập mật khẩu, địa chỉ nhà, số điện thoại, dữ liệu học bạ hoặc thông tin riêng tư vào chatbot khi không cần thiết.",
                    "Xin phép phù hợp trước khi đưa dữ liệu hoặc hình ảnh của người khác vào công cụ AI.",
                    "Đọc lại, kiểm tra độ chính xác và chỉnh sửa nội dung AI tạo ra trước khi nộp bài hoặc chia sẻ."
                ],
                "challenge": "Trước lần dùng AI tiếp theo, kiểm tra xem yêu cầu của bạn có chứa dữ liệu cá nhân hoặc thông tin của người khác không."
            },
        }
        lowest = min(group_scores, key=group_scores.get)
        st.markdown("### Lời khuyên dành cho bạn")
        st.write(f"Nhóm có điểm thấp nhất trong lần tự đánh giá này là **{lowest}** ({group_scores[lowest]:.1f}/100). Đây là gợi ý để ưu tiên luyện tập, không phải kết luận chắc chắn về năng lực của bạn.")
        st.write("**Trọng tâm:** " + group_advice[lowest]["focus"])
        st.write("**Các bước bạn có thể thử:**")
        for action in group_advice[lowest]["actions"]:
            st.markdown(f"- {action}")
        st.info("**Thử thách nhỏ:** " + group_advice[lowest]["challenge"])

        # Item-specific advice can flag a concrete habit even if the overall score is high.
        item_advice = {
            1: ("Bạn có thể luyện cách đặt yêu cầu rõ ràng hơn.", "Khi hỏi AI, thêm mục tiêu, bối cảnh và dạng câu trả lời bạn mong muốn."),
            2: ("Bạn có thể chủ động hỏi lại khi chưa hiểu.", "Thử yêu cầu AI giải thích theo từng bước hoặc đưa một ví dụ tương tự."),
            3: ("Bạn có thể xác định mục tiêu học tập rõ hơn trước khi dùng AI.", "Trước khi mở chatbot, viết một câu nêu rõ mình muốn hiểu, luyện tập hay kiểm tra điều gì."),
            4: ("Bạn nên dành thời gian tự suy nghĩ trước khi nhờ AI.", "Tự thử ít nhất một cách làm hoặc ghi ra điều mình đã biết trước khi hỏi chatbot."),
            5: ("Bạn có thể củng cố vai trò chủ động của mình khi học cùng AI.", "Dùng AI để nhận gợi ý hoặc phản biện, sau đó tự quyết định và tự diễn đạt câu trả lời."),
            6: ("Câu trả lời cho thấy bạn có thể đang sao chép nội dung AI mà chưa kiểm tra đủ.", "Đừng dùng nguyên văn ngay: kiểm chứng nội dung, sửa bằng lời của mình và bảo đảm bạn hiểu điều mình nộp."),
            7: ("Bạn nên ghi nhớ rằng chatbot AI đôi khi tạo ra thông tin sai hoặc không cập nhật.", "Với thông tin quan trọng, hãy kiểm tra nguồn trước khi tin hoặc sử dụng."),
            8: ("Bạn có thể hình thành thói quen ưu tiên nguồn đáng tin cậy hơn.", "Đối chiếu với sách giáo khoa, tài liệu của cơ quan chính thống hoặc nguồn chuyên môn phù hợp."),
            9: ("Bạn có thể chủ động xác minh khi gặp thông tin đáng ngờ.", "Tìm nguồn độc lập thứ hai và kiểm tra xem nguồn đó có thực sự hỗ trợ khẳng định của AI không."),
            10: ("Bạn nên chú ý hơn đến dữ liệu cá nhân khi dùng chatbot.", "Tránh nhập thông tin định danh hoặc riêng tư; chỉ chia sẻ dữ liệu cần thiết và phù hợp."),
            11: ("Bạn có thể cần cân nhắc kĩ hơn quyền riêng tư của người khác.", "Không tải lên hình ảnh hoặc dữ liệu riêng tư của người khác nếu chưa có sự cho phép phù hợp."),
            12: ("Bạn nên xem lại nội dung AI tạo ra trước khi sử dụng hoặc chia sẻ.", "Bạn vẫn chịu trách nhiệm kiểm tra độ chính xác, tính phù hợp và quyền sử dụng của nội dung mình chia sẻ."),
        }
        flagged = []
        for qid, group, question, reverse in QUESTIONS:
            # For reverse-scored Q6, a high raw answer indicates the risk behavior.
            concern = raw[qid] >= 4 if qid == 6 else scored[qid] <= 2
            if concern:
                flagged.append((qid, item_advice[qid]))
        if flagged:
            with st.expander("Lời khuyên theo câu trả lời cụ thể của bạn"):
                st.caption("Các gợi ý dưới đây được kích hoạt từ một số câu trả lời cụ thể; chúng không phải chẩn đoán hay đánh giá chính thức.")
                for qid, (heading, action) in flagged:
                    st.markdown(f"**Câu {qid}. {heading}**")
                    st.write(action)
        else:
            st.success("Trong các câu trả lời của bạn chưa có dấu hiệu nổi bật thuộc ngưỡng cần nhắc riêng. Bạn vẫn có thể chọn nhóm điểm thấp nhất để luyện tập tiếp.")
        st.caption("Điểm số phản ánh câu trả lời tự báo cáo tại thời điểm làm bài; không phải chứng nhận năng lực. Lời khuyên được tạo theo quy tắc cố định, không phải tư vấn chuyên môn cá nhân.")

        rows = []
        for qid, group, question, reverse in QUESTIONS:
            rows.append({
                "Câu": qid, "Nhóm năng lực": group, "Phát biểu": question,
                "Câu trả lời": answers[qid], "Điểm gốc": raw[qid],
                "Đảo chiều": "Có" if reverse else "Không", "Điểm tính": scored[qid],
            })
        csv_data = pd.DataFrame(rows).to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "Tải kết quả của bạn (CSV)", data=csv_data,
            file_name="ai_literacy_scorecard_ket_qua.csv", mime="text/csv",
            use_container_width=True,
        )

st.divider()
st.caption("AI Literacy Scorecard • Bản rút gọn 12 câu • Dành cho mục đích học tập và nghiên cứu")
