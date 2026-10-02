import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="DB증권 사업부문별 손익 및 지속가능 수익구조 분석",
    page_icon="📊",
    layout="wide"
)

# 단위: 억원
# DB증권 사업보고서 및 반기보고서 공개자료 기반
segment_df = pd.DataFrame({
    "기간": ["2024H1", "2025H1", "2026H1"],
    "WM": [-57.6, -62.2, 280.4],
    "기업금융": [206.6, 232.4, 14.1],
    "S&T": [264.6, 262.6, 217.9],
    "기타": [63.4, -5.5, 139.2],
    "전사 영업이익": [477.0, 427.2, 651.6]
})

revenue_df = pd.DataFrame({
    "기간": ["2024H1", "2025H1", "2026H1"],
    "수수료수익": [1271.54, 1225.10, 1776.21],
    "금융상품/파생상품 평가·처분이익": [3092.84, 5647.48, 18645.29],
    "이자수익": [2120.24, 2144.45, 2425.94],
    "배당금·분배금수익": [116.94, 79.95, 117.98]
})

fee_df = pd.DataFrame({
    "항목": [
        "수탁수수료",
        "인수·주선수수료",
        "집합투자증권 취급수수료",
        "자산관리수수료",
        "신탁보수",
        "기타 수입수수료"
    ],
    "2025H1": [301.57, 311.96, 72.74, 100.31, 15.69, 422.83],
    "2026H1": [845.91, 190.80, 125.40, 174.61, 19.38, 420.13]
})
fee_df["증감액"] = fee_df["2026H1"] - fee_df["2025H1"]
fee_df["증감률(%)"] = (fee_df["증감액"] / fee_df["2025H1"] * 100).round(1)

financial_product_df = pd.DataFrame({
    "구분": ["FVTPL 금융상품 관련 이익", "FVTPL 금융상품 관련 손실"],
    "2025H1": [2233.47, 1934.82],
    "2026H1": [6964.15, 5821.46]
})

derivative_df = pd.DataFrame({
    "구분": ["파생상품 평가·거래이익", "파생상품 평가·거래손실"],
    "2025H1": [3430.25, 3427.59],
    "2026H1": [11778.23, 12562.24]
})

capital_df = pd.DataFrame({
    "연도": ["2023", "2024", "2025"],
    "영업용순자본": [6844.38, 7376.48, 8163.87],
    "총위험액": [2701.68, 2829.11, 3523.52],
    "잉여자본": [4142.71, 4547.37, 4640.36],
    "순자본비율": [308.64, 338.79, 343.92]
})

def won(value):
    return f"{value:,.1f}억원"

def get_wm_conclusion():
    brokerage_growth = fee_df.loc[
        fee_df["항목"] == "수탁수수료", "증감액"
    ].iloc[0]
    asset_mgmt_growth = fee_df.loc[
        fee_df["항목"].isin(["집합투자증권 취급수수료", "자산관리수수료", "신탁보수"]),
        "증감액"
    ].sum()

    if brokerage_growth > asset_mgmt_growth:
        return {
            "title": "거래고객의 자산관리 고객 전환",
            "text": (
                "2026년 상반기 WM 회복 과정에서 수탁수수료 증가폭이 "
                "자산관리·금융상품 관련 수수료 증가폭보다 크게 나타났습니다. "
                "따라서 DB증권은 증시 유입으로 확대된 거래고객을 금융상품·자산관리 "
                "고객으로 전환하여 비위탁자산 기반 수익을 확대해야 합니다."
            ),
            "brokerage_growth": brokerage_growth,
            "asset_growth": asset_mgmt_growth
        }
    return {
        "title": "비위탁자산 기반 WM 성장 가속",
        "text": (
            "WM 실적 개선이 거래수수료뿐 아니라 자산관리·금융상품 관련 수수료 "
            "확대와 함께 나타나고 있습니다. DB증권은 비위탁자산 확대 흐름을 "
            "가속하기 위해 WM 고객기반에 자원을 지속적으로 배분해야 합니다."
        ),
        "brokerage_growth": brokerage_growth,
        "asset_growth": asset_mgmt_growth
    }

conclusion = get_wm_conclusion()

st.sidebar.title("DB증권 분석")
page = st.sidebar.radio(
    "분석 메뉴",
    [
        "1. 분석 개요",
        "2. 사업부문 손익",
        "3. WM 흑자전환 분석",
        "4. 금융상품·S&T 분석",
        "5. 리스크·자본적정성",
        "6. 최종 결론"
    ]
)
st.sidebar.divider()
st.sidebar.caption("생성형 AI를 활용해 구현한 DB증권 재무분석 프로그램")
st.sidebar.caption("자료: DB증권 사업보고서 및 반기보고서")

st.title("DB증권 사업부문별 손익 및 지속가능 수익구조 분석")
st.caption(
    "사업활동 → 회계계정 → 사업부문 손익 → 전사 손익 → 리스크를 연결하여 "
    "DB증권의 이익 변화 원인을 분석합니다."
)

if page == "1. 분석 개요":
    st.header("1. 분석 목적")
    st.info("""
**핵심 질문**

2026년 DB증권의 실적 개선은 어느 사업부문에서 발생했으며,
그 성장을 지속하기 위해 어떤 수익기반을 강화해야 하는가?
""")
    st.markdown("""
이 프로그램은 단순히 영업이익이나 ROE의 증감을 보여주는 것이 아니라
**재무제표 숫자가 왜 변화했는지**를 사업활동과 연결하여 분석합니다.

**전사 실적 → 사업부문 → 세부 수익계정 → 금융상품 손익 → 위험 → 경영 제언**
""")
    st.subheader("DB증권이 제시한 경쟁우위 요소")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
**고객·사업 측면**
- 신채널을 통한 고객저변의 지속적 확대
- 고객 니즈에 대응하는 금융상품 개발 역량 제고
""")
    with c2:
        st.markdown("""
**재무·리스크 측면**
- 지속성장 가능한 리스크관리 능력 확보
- 신흥시장 거점 및 해외고객 등 글로벌 네트워크 확대
""")
    st.subheader("분석 구조")
    st.markdown("""
### 고객활동
↓
### 수수료수익 및 금융상품손익
↓
### WM · 기업금융 · S&T 영업이익
↓
### 전사 영업이익
↓
### 위험 및 자본적정성
↓
### 지속가능한 수익구조에 대한 제언
""")

elif page == "2. 사업부문 손익":
    st.header("2. 어떤 사업부문이 실적 변화를 만들었는가?")
    latest = segment_df.iloc[-1]
    previous = segment_df.iloc[-2]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("2026H1 WM 영업이익", won(latest["WM"]), f"{latest['WM']-previous['WM']:+.1f}억원")
    c2.metric("기업금융 영업이익", won(latest["기업금융"]), f"{latest['기업금융']-previous['기업금융']:+.1f}억원")
    c3.metric("S&T 영업이익", won(latest["S&T"]), f"{latest['S&T']-previous['S&T']:+.1f}억원")
    c4.metric("전사 영업이익", won(latest["전사 영업이익"]), f"{latest['전사 영업이익']-previous['전사 영업이익']:+.1f}억원")

    plot_df = segment_df.melt(
        id_vars="기간", value_vars=["WM", "기업금융", "S&T", "기타"],
        var_name="사업부문", value_name="영업이익"
    )
    fig = px.bar(plot_df, x="기간", y="영업이익", color="사업부문",
                 barmode="group", text_auto=".1f", title="사업부문별 영업이익 변화")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(segment_df, use_container_width=True, hide_index=True)

    wm_change = latest["WM"] - previous["WM"]
    total_change = latest["전사 영업이익"] - previous["전사 영업이익"]
    st.success(f"""
**자동 진단**

2025H1 → 2026H1 전사 영업이익은 **{total_change:+.1f}억원** 변화했습니다.
같은 기간 WM 영업이익은 **{previous['WM']:.1f}억원 → {latest['WM']:.1f}억원**으로
**{wm_change:+.1f}억원 개선**되었습니다.

반면 기업금융과 S&T의 영업이익은 감소했습니다.

→ **2026H1 실적구조 변화의 핵심 분석대상은 WM입니다.**
""")

elif page == "3. WM 흑자전환 분석":
    st.header("3. WM은 왜 흑자전환했는가?")
    c1, c2, c3 = st.columns(3)
    c1.metric("WM 영업이익", "280.4억원", "+342.6억원 YoY")
    c2.metric("수탁수수료", "845.9억원", "+544.3억원 YoY")
    c3.metric("자산관리수수료", "174.6억원", "+74.3억원 YoY")

    st.subheader("수수료 계정별 변화")
    fee_plot = fee_df.melt(
        id_vars="항목", value_vars=["2025H1", "2026H1"],
        var_name="기간", value_name="수수료수익"
    )
    fig = px.bar(fee_plot, x="항목", y="수수료수익", color="기간",
                 barmode="group", text_auto=".1f",
                 title="2025H1 vs 2026H1 수수료수익 비교")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(fee_df.round(1), use_container_width=True, hide_index=True)

    brokerage = conclusion["brokerage_growth"]
    asset = conclusion["asset_growth"]
    quality_df = pd.DataFrame({
        "구분": ["시장활동 기반 (수탁수수료)", "고객자산 기반 (집합투자+자산관리+신탁)"],
        "2025H1→2026H1 증가액": [brokerage, asset]
    })
    fig2 = px.bar(quality_df, x="구분", y="2025H1→2026H1 증가액",
                  text_auto=".1f", title="수익기반별 증가액")
    st.plotly_chart(fig2, use_container_width=True)

    st.warning("""
**해석 시 주의**

수탁수수료·자산관리수수료 등은 회사 전체 수수료 계정입니다.
사업부문 WM 영업이익과 개별 수수료 계정 사이의 정확한 1:1 귀속은
공개자료만으로 확인할 수 없습니다.

따라서 본 프로그램은 **WM 흑자전환과 수수료 계정 변화가 동시에 나타난 구조**를
분석하며, 특정 수수료 증가액이 WM 영업이익 증가액을 직접 구성한다고 가정하지 않습니다.
""")
    st.success(f"""
**분석 결과**

수탁수수료 증가액: **{brokerage:.1f}억원**

집합투자증권·자산관리·신탁 관련 수수료 증가액: **{asset:.1f}억원**

거래활동 관련 수수료 증가폭이 더 크지만,
자산관리 및 금융상품 관련 수수료도 함께 증가했습니다.
""")

elif page == "4. 금융상품·S&T 분석":
    st.header("4. 금융상품 이익이 커졌다고 S&T 성과도 좋아졌을까?")
    st.markdown("""
증권사의 금융상품 관련 계정은 **총이익(Gross Profit)**만 보면
실제 성과를 과대평가할 수 있습니다. 따라서 관련 이익과 손실을 동시에 분석합니다.
""")
    current_profit = financial_product_df.loc[
        financial_product_df["구분"] == "FVTPL 금융상품 관련 이익", "2026H1"
    ].iloc[0]
    current_loss = financial_product_df.loc[
        financial_product_df["구분"] == "FVTPL 금융상품 관련 손실", "2026H1"
    ].iloc[0]
    current_net = current_profit - current_loss
    c1, c2, c3 = st.columns(3)
    c1.metric("FVTPL 관련 이익", won(current_profit))
    c2.metric("FVTPL 관련 손실", won(current_loss))
    c3.metric("FVTPL 단순 순액", won(current_net))

    fp_plot = financial_product_df.melt(
        id_vars="구분", value_vars=["2025H1", "2026H1"],
        var_name="기간", value_name="금액"
    )
    fig = px.bar(fp_plot, x="기간", y="금액", color="구분",
                 barmode="group", text_auto=".1f",
                 title="FVTPL 금융상품 관련 이익·손실")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("파생상품 평가·거래손익")
    derivative_plot = derivative_df.melt(
        id_vars="구분", value_vars=["2025H1", "2026H1"],
        var_name="기간", value_name="금액"
    )
    fig2 = px.bar(derivative_plot, x="기간", y="금액", color="구분",
                  barmode="group", text_auto=".1f",
                  title="파생상품 평가·거래 이익과 손실")
    st.plotly_chart(fig2, use_container_width=True)

    derivative_net_2025 = derivative_df.loc[
        derivative_df["구분"] == "파생상품 평가·거래이익", "2025H1"
    ].iloc[0] - derivative_df.loc[
        derivative_df["구분"] == "파생상품 평가·거래손실", "2025H1"
    ].iloc[0]
    derivative_net_2026 = derivative_df.loc[
        derivative_df["구분"] == "파생상품 평가·거래이익", "2026H1"
    ].iloc[0] - derivative_df.loc[
        derivative_df["구분"] == "파생상품 평가·거래손실", "2026H1"
    ].iloc[0]

    st.info(f"""
**Gross → Net 분석**

파생상품 평가·거래손익 단순 순액
- 2025H1: **{derivative_net_2025:,.1f}억원**
- 2026H1: **{derivative_net_2026:,.1f}억원**

따라서 금융상품/파생상품의 **총이익 증가만으로 S&T 수익성이 개선됐다고 판단할 수 없습니다.**
실제로 S&T 영업이익은 **262.6억원 → 217.9억원**으로 감소했습니다.
""")
    st.warning("""
※ 금융상품 및 파생상품 계정은 여러 사업활동과 연결될 수 있으므로
위 순액을 S&T 영업이익과 동일한 값으로 해석하지 않습니다.
""")

elif page == "5. 리스크·자본적정성":
    st.header("5. 위험 증가를 감당할 자본은 충분한가?")
    latest_capital = capital_df.iloc[-1]
    previous_capital = capital_df.iloc[-2]
    c1, c2, c3 = st.columns(3)
    c1.metric("2025 영업용순자본", won(latest_capital["영업용순자본"]),
              f"{latest_capital['영업용순자본']-previous_capital['영업용순자본']:+.1f}억원")
    c2.metric("2025 총위험액", won(latest_capital["총위험액"]),
              f"{latest_capital['총위험액']-previous_capital['총위험액']:+.1f}억원")
    c3.metric("2025 순자본비율", f"{latest_capital['순자본비율']:.2f}%",
              f"{latest_capital['순자본비율']-previous_capital['순자본비율']:+.2f}%p")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=capital_df["연도"], y=capital_df["영업용순자본"], name="영업용순자본"))
    fig.add_trace(go.Bar(x=capital_df["연도"], y=capital_df["총위험액"], name="총위험액"))
    fig.update_layout(title="영업용순자본과 총위험액 변화", barmode="group", yaxis_title="억원")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.line(capital_df, x="연도", y="순자본비율",
                   markers=True, text="순자본비율", title="순자본비율 추이")
    fig2.update_traces(texttemplate="%{text:.2f}%", textposition="top center")
    st.plotly_chart(fig2, use_container_width=True)

    st.success("""
**분석 결과**

총위험액은 2023년 **2,702억원**에서 2025년 **3,524억원**으로 증가했습니다.
그러나 같은 기간 영업용순자본도 **6,844억원 → 8,164억원**으로 증가했고,
순자본비율은 **308.64% → 343.92%**로 개선됐습니다.

따라서 공개자료만으로 **'위험 증가로 자본적정성이 악화됐다'고 판단할 근거는 없습니다.**
""")

elif page == "6. 최종 결론":
    st.header("6. 최종 결론")
    st.subheader("① 무엇이 변했는가?")
    st.markdown("""
- WM 영업이익: **-62.2억원 → +280.4억원**
- 기업금융 영업이익: **232.4억원 → 14.1억원**
- S&T 영업이익: **262.6억원 → 217.9억원**
""")
    st.subheader("② WM 변화와 함께 어떤 계정이 움직였는가?")
    st.markdown("""
- 수탁수수료: **301.6억원 → 845.9억원**
- 자산관리수수료: **100.3억원 → 174.6억원**
- 집합투자증권 취급수수료: **72.7억원 → 125.4억원**
- 신탁보수: **15.7억원 → 19.4억원**
""")
    st.subheader("③ 금융상품 운용은 어떻게 봐야 하는가?")
    st.markdown("""
금융상품 및 파생상품의 Gross 이익은 크게 증가했지만 관련 손실도 동시에 크게 발생했습니다.
따라서 **총이익 증가 = 안정적인 수익성 개선**으로 해석할 수 없습니다.
실제 S&T 영업이익은 전년 동기보다 감소했습니다.
""")
    st.subheader("④ 리스크는 감당 가능한가?")
    st.markdown("""
총위험액은 증가했지만 영업용순자본 역시 확대되면서
순자본비율은 **2023년 308.64% → 2025년 343.92%**로 개선됐습니다.
""")
    st.divider()
    st.subheader("최종 경영 제언")
    st.success(f"""
### {conclusion['title']}

{conclusion['text']}
""")
    st.markdown("""
**왜 이 결론인가?**

2026년 상반기에는 증시 거래 활성화와 함께 수탁수수료가 크게 증가했고,
동시에 자산관리·집합투자증권 관련 수수료도 증가했습니다.

따라서 단기적인 거래활동 증가를 일회성 수탁수수료에 그치게 하기보다,
**유입된 거래고객의 자산을 금융상품·자산관리 영역으로 연결하여
고객당 수익원을 다변화하는 것**이 WM 수익구조의 지속가능성을 높이는 방향입니다.
""")
    st.info("""
**회계 직무 관점의 의미**

사업부문별 영업이익에서 출발해 수수료수익을 세부 계정으로 분해하고,
금융상품 관련 이익과 손실을 함께 확인한 뒤 자본적정성까지 연결했습니다.

즉 **사업활동이 어떤 회계계정을 거쳐 재무성과로 나타나는지 추적하고,
숫자의 증감보다 그 원인을 파악하는 것**이 프로그램의 핵심입니다.
""")
    st.caption("""
※ 본 분석은 DB증권 공개 사업보고서·반기보고서를 기반으로 한 외부 분석이며,
공개되지 않은 고객별 자산·수익성 및 내부 관리회계 데이터는 사용하지 않았습니다.
""")
