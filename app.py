import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Literacy Scorecard", page_icon="🧭", layout="wide")

DOMAINS = [
    "Kỹ năng đặt câu hỏi và khai thác AI",
    "Tư duy độc lập",
    "Kiểm chứng thông tin",
    "Quyền riêng tư và trách nhiệm",
]
Q = [
("Bạn đang giải phương trình lượng giác nhưng chưa biết cách làm. Bạn muốn dùng AI để hiểu phương pháp.",
 [("A","Nhập đề và yêu cầu AI giải, không cần đọc lời giải.",1),("B","Hỏi AI đáp án của mình đúng không, không đưa cách làm.",2),("C","Yêu cầu đáp án cuối cùng để chép vào vở.",0),("D","Yêu cầu AI giải từng bước và giải thích cách làm.",3)],0),
("Trong bài viết tiếng Anh về Becoming Independent, AI sửa một câu nhưng bạn không hiểu vì sao cấu trúc thay đổi.",
 [("A","Chấp nhận câu sửa vì AI thường giỏi tiếng Anh.",1),("B","Sao chép câu mới và bỏ câu cũ.",0),("C","Yêu cầu AI chỉ rõ phần sửa, giải thích quy tắc và cho ví dụ tương tự.",3),("D","Yêu cầu AI viết lại toàn bộ đoạn văn.",2)],0),
("Bạn viết đoạn phân tích nhân vật, đã có nhận xét nhưng chưa biết triển khai luận điểm và dẫn chứng.",
 [("A","Yêu cầu AI viết hoàn chỉnh đoạn văn để dùng trực tiếp.",0),("B","Đưa tên tác phẩm rồi dùng toàn bộ phân tích AI cung cấp.",1),("C","Yêu cầu bài mẫu rồi thay vài từ.",2),("D","Nêu nhận xét của mình, nhờ AI gợi ý phát triển luận điểm rồi đối chiếu văn bản gốc.",3)],0),
("Bạn chưa nhớ công thức tính tổng n số hạng đầu của cấp số cộng.",
 [("A","Nhập đề vào AI rồi chép đáp số.",0),("B","Hỏi ba AI và chọn đáp án xuất hiện nhiều nhất.",1),("C","Nhờ AI giải hết rồi mới xem lại công thức.",2),("D","Xem lại SGK, tự thử làm trước và chỉ nhờ AI kiểm tra bước đang vướng.",3)],1),
("Bạn viết bài nghị luận, đã có quan điểm riêng nhưng chưa biết sắp xếp luận điểm.",
 [("A","Yêu cầu AI viết bài hoàn chỉnh.",0),("B","Tự lập dàn ý rồi nhờ AI phản biện logic và chỉ ra luận điểm thiếu.",3),("C","Dùng dàn ý AI tạo mà không so sánh với quan điểm của mình.",1),("D","Chỉ nhờ AI viết mở bài và kết bài.",2)],1),
("Bạn phân tích Tràng giang và đã có cách hiểu riêng về nỗi buồn nhân thế, tình yêu quê hương đất nước.",
 [("A","Bỏ ý tưởng riêng, nhờ AI viết theo văn mẫu.",0),("B","Nhờ AI viết mở bài và kết bài, mình chỉ viết thân bài.",1),("C","Lấy dàn ý AI tạo mà không đối chiếu góc nhìn của mình.",2),("D","Tự lập dàn ý rồi nhờ AI phản biện luận điểm và dẫn chứng thơ.",3)],1),
("AI đưa câu trích dẫn và nói là nguyên văn của tác giả, nhưng bạn không tìm thấy trong văn bản đang học.",
 [("A","Tra văn bản gốc/nguồn đáng tin; chưa xác minh thì không trích như nguyên văn.",3),("B","Dùng vì AI đã ghi tên tác giả.",1),("C","Giữ câu nhưng bỏ tên tác giả.",0),("D","Hỏi AI xác nhận lại rồi dùng nếu AI vẫn nói đúng.",2)],2),
("AI dịch sustainability là “sự chống chịu” trong bài đọc về Global Warming; bạn thấy chưa phù hợp.",
 [("A","Dùng luôn vì AI dịch nhanh.",0),("B","Đổi sang từ khác nghe xuôi tai.",1),("C","Dùng một công cụ dịch khác để so sánh.",2),("D","Tra từ điển đáng tin, xem định nghĩa và ngữ cảnh rồi chọn bản dịch phù hợp.",3)],2),
("AI đưa công thức biến đổi tổng thành tích có vẻ khác công thức trong vở.",
 [("A","Áp dụng ngay vì AI nhớ công thức chuẩn.",0),("B","Chép vào sổ để dùng sau.",1),("C","Hỏi AI xem công thức có đúng SGK lớp 11 không.",2),("D","Đối chiếu bảng công thức trong SGK và sửa nếu AI nhầm.",3)],2),
("Bạn muốn AI sửa đoạn tiếng Anh có họ tên, số điện thoại và địa chỉ của mình.",
 [("A","Gửi nguyên văn vì chỉ dùng cho học tập.",0),("B","Chỉ xóa số điện thoại.",2),("C","Gửi nguyên văn nhưng dặn AI giữ bí mật.",1),("D","Xóa/thay thông tin nhận dạng không cần thiết và xem xét cách dịch vụ xử lý dữ liệu.",3)],3),
("Bạn muốn dùng chuyện riêng tư của bạn cùng lớp làm chất liệu cho truyện hài do AI viết.",
 [("A","Dùng vì không ghi họ tên.",0),("B","Đưa vào AI rồi yêu cầu đổi tên.",2),("C","Không chia sẻ thông tin có thể nhận diện khi chưa có đồng ý phù hợp; dùng tình huống hư cấu.",3),("D","Chỉ kể trong nhóm lớp quen biết.",1)],3),
("Bạn dùng AI viết bài nghị luận và định nộp như bài hoàn toàn do mình tự viết.",
 [("A","Nộp nếu không bị phát hiện.",0),("B","Đổi vài từ để giống phong cách cá nhân.",1),("C","Chỉ kiểm tra chính tả trước khi nộp.",2),("D","Tự kiểm tra luận điểm/dẫn chứng, chỉnh sửa bằng hiểu biết, theo quy định giáo viên và chịu trách nhiệm.",3)],3),
]
EXPLANATIONS = [
"Yêu cầu AI giải thích từng bước giúp bạn hiểu phương pháp thay vì chỉ lấy đáp án.",
"Yêu cầu giải thích quy tắc và ví dụ giúp bạn hiểu lỗi để tự áp dụng.",
"Giữ nhận xét của mình và đối chiếu văn bản gốc giúp tránh phụ thuộc vào bài mẫu.",
"Tự thử trước và dùng AI kiểm tra điểm vướng giúp duy trì tư duy độc lập.",
"AI nên phản biện dàn ý của bạn, không thay thế quan điểm của bạn.",
"Bạn cần tự đánh giá lập luận và dẫn chứng, kể cả khi AI góp ý.",
"AI có thể tạo trích dẫn sai; cần kiểm chứng bằng nguồn độc lập.",
"Tra định nghĩa và ngữ cảnh giúp chọn nghĩa phù hợp hơn việc đoán hoặc chỉ so sánh máy dịch.",
"Đối chiếu SGK hoặc nguồn đáng tin cậy tốt hơn việc chỉ hỏi AI xác nhận.",
"Không nhập dữ liệu nhận dạng không cần thiết; yêu cầu giữ bí mật không bảo đảm an toàn tuyệt đối.",
"Đổi tên chưa chắc loại bỏ khả năng nhận diện; nên tôn trọng quyền riêng tư.",
"Người học cần chịu trách nhiệm về bài nộp và tuân thủ quy định sử dụng AI."
]
ADVICE = {
DOMAINS[0]: ["Tập nêu mục tiêu, phần đã thử và chỗ chưa hiểu; yêu cầu AI giải thích từng bước thay vì chỉ xin đáp án.",
"Bạn đã có một số cách hỏi phù hợp. Hãy yêu cầu AI nêu lý do, ví dụ tương tự và giải thích phần chưa hiểu.",
"Tiếp tục viết prompt rõ mục tiêu, bối cảnh và tiêu chí đầu ra; yêu cầu AI nêu giới hạn và cách tự kiểm tra."],
DOMAINS[1]: ["Thử tự suy nghĩ/lập dàn ý trước khi mở AI. Dùng AI để phản biện hoặc kiểm tra một bước cụ thể.",
"Giữ ý tưởng của mình trước khi hỏi AI; sau đó tự đánh giá xem gợi ý có hợp lý không.",
"Duy trì thói quen tự làm trước, dùng AI để phản biện và giải thích lại kết quả bằng lời của mình."],
DOMAINS[2]: ["Đối chiếu câu trả lời với SGK, văn bản gốc, từ điển hoặc nguồn đáng tin. AI lặp lại câu trả lời không có nghĩa là câu đó đúng.",
"Tạo thói quen xác minh dữ kiện quan trọng bằng ít nhất một nguồn độc lập.",
"Tiếp tục kiểm tra nguồn gốc và ngữ cảnh; ưu tiên nguồn gốc/SGK với công thức và trích dẫn."],
DOMAINS[3]: ["Tránh nhập dữ liệu cá nhân không cần thiết; kiểm tra quy định của giáo viên và chịu trách nhiệm với bài nộp.",
"Giảm thông tin nhận dạng khi nhập prompt, tôn trọng quyền riêng tư và kiểm tra quy định học tập.",
"Duy trì nguyên tắc tối thiểu hóa dữ liệu, tôn trọng quyền riêng tư và tuân thủ quy định sử dụng AI."]
}
st.set_page_config(page_title="AI Literacy Scorecard", page_icon="🧭", layout="wide")

st.title("🧭 AI Literacy Scorecard")
st.write("Bộ 12 tình huống thực tế về cách sử dụng AI trong học tập.")
st.info("Đây là công cụ tự đánh giá thử nghiệm, chưa phải thang đo đã được kiểm định. Hãy chọn phương án gần với cách bạn thực sự sẽ làm.")

with st.form("quiz"):
    choices = []
    for i, (situation, options, domain_idx) in enumerate(Q):
        st.subheader(f"Câu {i + 1} · {DOMAINS[domain_idx]}")
        st.write(situation)
        choices.append(st.radio(
            "Chọn một phương án:",
            [f"{o[0]}. {o[1]}" for o in options],
            key=f"q{i}",
            index=None,
        ))
        st.divider()
    go = st.form_submit_button("Chấm điểm và xem lời khuyên", type="primary", use_container_width=True)

if go:
    if any(choice is None for choice in choices):
        st.error("Bạn cần trả lời đủ 12 tình huống trước khi chấm điểm.")
    else:
        scores = {domain: 0 for domain in DOMAINS}
        detail = []
        for i, ((situation, options, domain_idx), chosen) in enumerate(zip(Q, choices)):
            option = next(option for option in options if chosen.startswith(option[0] + "."))
            letter, label, score = option
            domain = DOMAINS[domain_idx]
            scores[domain] += score
            detail.append({"Câu": i + 1, "Nhóm năng lực": domain, "Lựa chọn": letter, "Điểm": score})
        st.session_state["result"] = {"scores": scores, "total": sum(scores.values()), "detail": detail}

if "result" in st.session_state:
    result = st.session_state["result"]
    st.header("Kết quả của bạn")
    col1, col2 = st.columns(2)
    col1.metric("Tổng điểm", f"{result['total']}/36")
    col2.metric("Điểm quy đổi", f"{result['total'] / 36 * 100:.1f}/100")
    st.caption("Điểm quy đổi = tổng điểm / 36 × 100. Chỉ số này mô tả kết quả trong bộ tình huống, không phải đánh giá năng lực đã được kiểm định.")

    domain_df = pd.DataFrame([
        {"Nhóm năng lực": domain, "Điểm": score, "Tối đa": 9, "Quy đổi (%)": round(score / 9 * 100, 1)}
        for domain, score in result["scores"].items()
    ])
    st.subheader("Điểm theo nhóm năng lực")
    st.bar_chart(domain_df.set_index("Nhóm năng lực")["Quy đổi (%)"])
    st.dataframe(domain_df, use_container_width=True, hide_index=True)

    st.subheader("Lời khuyên dựa trên điểm từng nhóm")
    for domain, score in result["scores"].items():
        band = 0 if score <= 3 else (1 if score <= 6 else 2)
        with st.expander(f"{domain}: {score}/9", expanded=(score <= 3)):
            st.write(ADVICE[domain][band])

    st.subheader("Điểm từng câu")
    st.dataframe(pd.DataFrame(result["detail"]), use_container_width=True, hide_index=True)
    if st.button("Làm lại bài đánh giá"):
        st.session_state.pop("result", None)
        st.rerun()

st.caption("Lưu ý: cần giáo viên Toán, Ngữ văn và Tiếng Anh rà soát các tình huống trước khi triển khai chính thức. Bài làm không được lưu vào cơ sở dữ liệu hay gửi đi đâu; kết quả chỉ giữ tạm trong phiên ứng dụng để hiển thị.")
