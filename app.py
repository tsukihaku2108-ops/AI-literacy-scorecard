
import json
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
import pandas as pd
import gspread

st.set_page_config(
    page_title="AI Literacy Scorecard",
    page_icon="🧭",
    layout="wide"
)
# Phân nhóm lớp trong nghiên cứu
CLASS_GROUPS = {
    "11V": "Thực nghiệm",
    "11ĐS": "Thực nghiệm",
    "11L": "Thực nghiệm",
    "11T2": "Thực nghiệm",
    "11SiTi": "Đối chứng",
    "11H": "Đối chứng",
    "11T1": "Đối chứng",
    "11A": "Đối chứng",
}

CLASS_OPTIONS = list(CLASS_GROUPS.keys())
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

ADVICE = {
    DOMAINS[0]: [
        "Tập nêu mục tiêu, phần đã thử và chỗ chưa hiểu; yêu cầu AI giải thích từng bước thay vì chỉ xin đáp án.",
        "Bạn đã có một số cách hỏi phù hợp. Hãy yêu cầu AI nêu lý do, ví dụ tương tự và giải thích phần chưa hiểu.",
        "Tiếp tục viết prompt rõ mục tiêu, bối cảnh và tiêu chí đầu ra; yêu cầu AI nêu giới hạn và cách tự kiểm tra."
    ],
    DOMAINS[1]: [
        "Thử tự suy nghĩ/lập dàn ý trước khi mở AI. Dùng AI để phản biện hoặc kiểm tra một bước cụ thể.",
        "Giữ ý tưởng của mình trước khi hỏi AI; sau đó tự đánh giá xem gợi ý có hợp lý không.",
        "Duy trì thói quen tự làm trước, dùng AI để phản biện và giải thích lại kết quả bằng lời của mình."
    ],
    DOMAINS[2]: [
        "Đối chiếu câu trả lời với SGK, văn bản gốc, từ điển hoặc nguồn đáng tin. AI lặp lại câu trả lời không có nghĩa là câu đó đúng.",
        "Tạo thói quen xác minh dữ kiện quan trọng bằng ít nhất một nguồn độc lập.",
        "Tiếp tục kiểm tra nguồn gốc và ngữ cảnh; ưu tiên nguồn gốc/SGK với công thức và trích dẫn."
    ],
    DOMAINS[3]: [
        "Tránh nhập dữ liệu cá nhân không cần thiết; kiểm tra quy định của giáo viên và chịu trách nhiệm với bài nộp.",
        "Giảm thông tin nhận dạng khi nhập prompt, tôn trọng quyền riêng tư và kiểm tra quy định học tập.",
        "Duy trì nguyên tắc tối thiểu hóa dữ liệu, tôn trọng quyền riêng tư và tuân thủ quy định sử dụng AI."
    ]
}


def connect_sheet():
    config = st.secrets["google"]
    credentials = json.loads(config["service_account_json"])
    client = gspread.service_account_from_dict(credentials)
    spreadsheet = client.open_by_key(config["spreadsheet_id"])

    try:
        worksheet = spreadsheet.worksheet("results")
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title="results", rows=1000, cols=40
        )

    headers = [
        "Mã lượt làm", "Thời gian","Lớp",
    "Nhóm nghiên cứu",
        "Tổng điểm /36", "Điểm quy đổi /100"
    ]
    headers += [f"{domain} /9" for domain in DOMAINS]

    for i in range(1, 13):
        headers += [f"Câu {i} - lựa chọn", f"Câu {i} - điểm"]

    if not worksheet.row_values(1):
        worksheet.append_row(headers)

    return worksheet


def save_result(result):
    worksheet = connect_sheet()

    row = [
        result["attempt_id"],
        result["timestamp"],
        result["class_name"],
        result["group_name"],
        result["total"],
        round(result["total"] / 36 * 100, 1),
    ]

    row += [result["scores"][domain] for domain in DOMAINS]

    for item in result["detail"]:
        row += [item["Lựa chọn"], item["Điểm"]]

    worksheet.append_row(row, value_input_option="USER_ENTERED")


def show_stats():
    st.title("📊 Thống kê nghiên cứu")

    if "stats_authenticated" not in st.session_state:
        st.session_state["stats_authenticated"] = False

    if not st.session_state["stats_authenticated"]:
        with st.form("stats_login"):
            password = st.text_input("Mật khẩu quản trị", type="password")
            login = st.form_submit_button("Đăng nhập")

        if login:
            if password == st.secrets["admin"]["stats_password"]:
                st.session_state["stats_authenticated"] = True
                st.rerun()
            else:
                st.error("Mật khẩu chưa đúng.")

        return

    if st.button("Đăng xuất trang thống kê"):
        st.session_state["stats_authenticated"] = False
        st.rerun()

    try:
        worksheet = connect_sheet()
        records = worksheet.get_all_records()
        if not records:
            st.info("Chưa có lượt làm nào được lưu.")
            return

        df = pd.DataFrame(records)
        df["Tổng điểm /36"] = pd.to_numeric(
            df["Tổng điểm /36"], errors="coerce"
        )
        df["Điểm quy đổi /100"] = pd.to_numeric(
            df["Điểm quy đổi /100"], errors="coerce"
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Tổng lượt làm", len(df))
        c2.metric("Điểm trung bình /36",
                  f"{df['Tổng điểm /36'].mean():.2f}")
        c3.metric("Trung vị /36",
                  f"{df['Tổng điểm /36'].median():.2f}")

        st.subheader("Phân bố tổng điểm")
        st.bar_chart(df["Tổng điểm /36"].value_counts().sort_index())

        st.subheader("Điểm trung bình theo nhóm năng lực")
        domain_columns = [f"{domain} /9" for domain in DOMAINS]
        domain_means = df[domain_columns].apply(
            pd.to_numeric, errors="coerce"
        ).mean()
        domain_means.index = DOMAINS
        st.bar_chart(domain_means)

        st.subheader("Tần suất lựa chọn từng câu")
        for i in range(1, 13):
            column = f"Câu {i} - lựa chọn"
            st.write(f"**Câu {i}**")
            st.bar_chart(df[column].value_counts().reindex(
                ["A", "B", "C", "D"], fill_value=0
            ))

        st.subheader("Dữ liệu đã lưu")
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            "Tải dữ liệu CSV",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="ai_literacy_results.csv",
            mime="text/csv",
        )

        st.caption(
            "Đây là số lượt làm, không đồng nghĩa số học sinh duy nhất. "
            "Không thu thập họ tên, email hoặc số điện thoại."
        )

    except Exception:
        st.error(
            "Không đọc được dữ liệu. Hãy kiểm tra cấu hình Secrets, "
            "quyền Editor của service account và sheet results."
        )


st.title("🧭 AI Literacy Scorecard")
st.write("Bộ 12 tình huống thực tế về cách sử dụng AI trong học tập.")
st.info(
    "Đây là công cụ tự đánh giá thử nghiệm, chưa phải thang đo đã được "
    "kiểm định. Hãy chọn phương án gần với cách bạn thực sự sẽ làm."
)

page = st.sidebar.radio(
    "Chọn trang",
    ["Làm bài đánh giá", "Thống kê nghiên cứu"]
)

if page == "Thống kê nghiên cứu":
    show_stats()
else:
    with st.form("quiz"):
        selected_class = st.selectbox(
            "Bạn đang học lớp nào?",
            options=CLASS_OPTIONS,
            index=None,
            placeholder="Chọn lớp của bạn"
        )

        selected_group = (
            CLASS_GROUPS[selected_class] if selected_class else None
        )

        choices = []

        for i, (situation, options, domain_idx) in enumerate(Q):
            st.subheader(f"Câu {i + 1} · {DOMAINS[domain_idx]}")
            st.write(situation)

            choices.append(
                st.radio(
                    "Chọn một phương án:",
                    [f"{o[0]}. {o[1]}" for o in options],
                    key=f"q{i}",
                    index=None,
                )
            )
            st.divider()

        go = st.form_submit_button(
            "Chấm điểm và xem lời khuyên",
            type="primary",
            use_container_width=True,
        )

    
    if go:
        if selected_class is None:
            st.error("Bạn hãy chọn lớp trước khi nộp bài.")
        elif any(choice is None for choice in choices):
            st.error("Bạn hãy trả lời đầy đủ 12 câu hỏi.")
        else:
            scores = {domain: 0 for domain in DOMAINS}
            detail = []

            for i, ((situation, options, domain_idx), chosen) in enumerate(
                zip(Q, choices)
            ):
                option = next(
                    option for option in options
                    if chosen.startswith(option[0] + ".")
                )
                letter, label, score = option
                domain = DOMAINS[domain_idx]
                scores[domain] += score

                detail.append({
                    "Câu": i + 1,
                    "Nhóm năng lực": domain,
                    "Lựa chọn": letter,
                    "Điểm": score,
                })

            result = {
                "attempt_id": str(uuid.uuid4()),
                "timestamp": datetime.now(
                    ZoneInfo("Asia/Ho_Chi_Minh")
                ).isoformat(timespec="seconds"),
                "class_name": selected_class,
                "group_name": selected_group,
                "scores": scores,
                "total": sum(scores.values()),
                "detail": detail,
            }

            st.session_state["result"] = result

            try:
                save_result(result)
                st.session_state["saved_attempt_id"] = result["attempt_id"]
                st.success("Kết quả đã được lưu vào hệ thống.")
            except Exception:
                st.error(
                    "Chưa lưu được kết quả. Hãy báo người quản trị kiểm tra "
                    "Secrets và quyền truy cập Google Sheets."
                )

    if "result" in st.session_state:
        result = st.session_state["result"]

        col1, col2 = st.columns(2)
        col1.metric("Tổng điểm", f"{result['total']}/36")
        col2.metric(
            "Điểm quy đổi",
            f"{result['total'] / 36 * 100:.1f}/100"
        )

        st.caption(
            "Điểm quy đổi = tổng điểm / 36 × 100. "
            "Đây không phải đánh giá năng lực đã được kiểm định."
        )

        domain_df = pd.DataFrame([
            {
                "Nhóm năng lực": domain,
                "Điểm": score,
                "Tối đa": 9,
                "Quy đổi (%)": round(score / 9 * 100, 1),
            }
            for domain, score in result["scores"].items()
        ])

        st.subheader("Điểm theo nhóm năng lực")
        st.bar_chart(
            domain_df.set_index("Nhóm năng lực")["Quy đổi (%)"]
        )
        st.dataframe(domain_df, use_container_width=True, hide_index=True)

        st.subheader("Lời khuyên dựa trên điểm từng nhóm")
        for domain, score in result["scores"].items():
            band = 0 if score <= 3 else (1 if score <= 6 else 2)
            with st.expander(f"{domain}: {score}/9", expanded=(score <= 3)):
                st.write(ADVICE[domain][band])

        st.subheader("Điểm từng câu")
        st.dataframe(
            pd.DataFrame(result["detail"]),
            use_container_width=True,
            hide_index=True,
        )

        if st.button("Làm lại bài đánh giá"):
            st.session_state.pop("result", None)
            st.rerun()

st.caption(
    "Kết quả được lưu vào Google Sheets để phục vụ thống kê nghiên cứu. "
    "Không nhập thông tin nhận dạng cá nhân vào bài đánh giá."
)
