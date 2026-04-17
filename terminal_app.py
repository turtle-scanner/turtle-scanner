import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os
import pytz
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# 1. 암호 보안 설정 (암호: 1353)
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # 암호 입력 화면 UI
    st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>🔐 Anti-Gravity Private Terminal</h1>", unsafe_allow_html=True)
    password = st.text_input("Access Code를 입력하십시오.", type="password")
    if st.button("Unlock"):
        if password == "1353":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Access Denied. 코드가 일치하지 않습니다.")
    return False

if check_password():
    # 사이드바 레이아웃 및 페이지 네비게이션
    st.sidebar.title("💎 Master Menu")

    # 실시간 시간 표시 (한국 & 미국)
    kst = pytz.timezone('Asia/Seoul')
    est = pytz.timezone('US/Eastern')
    now_kst = datetime.now(kst)
    now_est = datetime.now(est)

    st.sidebar.markdown(f"""
        <div style='background-color: #1e2129; padding: 15px; border-radius: 10px; border: 1px solid #3d4450; margin-bottom: 20px;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;'>
                <span style='font-size: 12px; color: #8a94a6;'>🇰🇷 KOREA (KST)</span>
                <span style='font-size: 10px; color: #4ade80;'>LIVE</span>
            </div>
            <div style='font-size: 18px; color: #FFFF00; font-family: monospace; font-weight: bold;'>{now_kst.strftime('%H:%M:%S')}</div>
            <div style='font-size: 12px; color: #FFFFFF;'>{now_kst.strftime('%Y-%m-%d')}</div>
            <hr style='margin: 10px 0; border: none; border-top: 1px solid #3d4450;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;'>
                <span style='font-size: 12px; color: #8a94a6;'>🇺🇸 USA (ET)</span>
                <span style='font-size: 10px; color: #4ade80;'>MARKET</span>
            </div>
            <div style='font-size: 18px; color: #FFFF00; font-family: monospace; font-weight: bold;'>{now_est.strftime('%H:%M:%S')}</div>
            <div style='font-size: 12px; color: #FFFFFF;'>{now_est.strftime('%Y-%m-%d')}</div>
        </div>
    """, unsafe_allow_html=True)

    page = st.sidebar.radio("Go to", ["🎯 주도주 타점 스캐너", "📈 실시간 분석 차트", "🧮 리스크 관리 계산기", "📰 실시간 뉴스 피드", "📊 본데 주식 50선", "💎 마스터 클래스"])

    # 공통 스타일 설정 (블랙 & 화이트 & 옐로우 포인트)
    st.markdown("""
        <style>
        /* 전체 배경 및 폰트 설정 */
        .main, .stApp, [data-testid="stSidebar"], [data-testid="stHeader"] { 
            background-color: #000000 !important; 
            background-image: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06)) !important;
            background-size: 100% 4px, 3px 100% !important;
        }
        
        /* 모바일 최적화: 여백 조정 */
        @media (max-width: 640px) {
            .main .block-container {
                padding: 1rem 0.5rem !important;
            }
            h1 { font-size: 1.8rem !important; }
            h2 { font-size: 1.5rem !important; }
            h3 { font-size: 1.2rem !important; }
            [data-testid="stMetricValue"] { font-size: 1.5rem !important; }
        }

        /* 터미널 스캔라인 효과 */
        .stApp::before {
            content: " ";
            display: block;
            position: absolute;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
            z-index: 2;
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
        }

        /* 기본 텍스트 흰색 */
        .stMarkdown:not(div[data-testid="stNotification"] *), .stText, p, span:not(div[data-testid="stNotification"] *), td, th, li { 
            color: #FFFFFF !important; 
            font-family: 'Courier New', Courier, monospace !important;
        }
        
        /* 헤더 노란색 + 빛남 효과 */
        h1, h2, h3, h4, h5, h6, [data-testid="stMetricLabel"] { 
            color: #FFFF00 !important; 
            font-weight: 900 !important;
            text-shadow: 0 0 5px rgba(255, 255, 0, 0.5), 0 0 10px rgba(255, 255, 0, 0.3) !important;
        }
        
        /* 버튼 스타일 */
        .stButton>button {
            width: 100% !important; /* 모바일에서 클릭하기 쉽게 너비 조정 */
            background-color: #111111 !important;
            color: #FFFF00 !important;
            border: 1px solid #FFFF00 !important;
            border-radius: 5px !important;
            padding: 10px !important;
        }
        .stButton>button:hover {
            background-color: #FFFF00 !important;
            color: #000000 !important;
            box-shadow: 0 0 15px rgba(255, 255, 0, 0.6);
        }

        /* 데이터프레임 모바일 가독성 */
        [data-testid="stTable"], [data-testid="stDataFrame"] {
            background-color: #000000 !important;
            border: 1px solid #333 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- 페이지 1: 주도주 타점 스캐너 ---
    if page == "🎯 주도주 타점 스캐너":
        st.markdown("<h1 style='white-space: nowrap;'>🎯 본데의 주식스캐너</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #FFFFFF; opacity: 0.8;'>✨ 실시간 시장 데이터 기반 주도주 포착</h3>", unsafe_allow_html=True)
        
        # --- 리얼타임 스캐너 엔진 로직 ---
        def get_scanner_data(tickers):
            results = []
            for ticker in tickers:
                try:
                    stock = yf.Ticker(ticker)
                    # 최신 1년치 데이터 (52주 고점 및 최신 변동성 계산용)
                    hist = stock.history(period="1y")
                    if len(hist) < 2: 
                        continue
                    
                    current_price = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    change_pct = ((current_price - prev_close) / prev_close) * 100
                    
                    # 거래량 비율 (오늘 거래량 / 10일 평균 거래량)
                    avg_volume = hist['Volume'].iloc[-11:-1].mean() if len(hist) > 10 else hist['Volume'].iloc[:-1].mean()
                    current_volume = hist['Volume'].iloc[-1]
                    vol_ratio = current_volume / avg_volume if avg_volume > 0 else 0
                    
                    # 52주 고점 정보 (history 데이터에서 직접 계산)
                    high_52w = hist['High'].max()
                    dist_from_high = ((current_price - high_52w) / high_52w) * 100
                    
                    results.append({
                        "Ticker": ticker,
                        "Name": ticker, # info 요청 생략으로 속도 향상
                        "Price": f"${current_price:.2f}" if any(c.isalpha() for c in ticker) else f"{int(current_price):,}원",
                        "Change": f"{change_pct:+.2f}%",
                        "Vol Ratio": f"{vol_ratio:.2f}x",
                        "Position": "신고가" if dist_from_high > -1 else f"{dist_from_high:.1f}%",
                        "_change_val": change_pct,
                        "_vol_val": vol_ratio
                    })
                except Exception as e:
                    print(f"Error fetching {ticker}: {e}")
                    continue
            return pd.DataFrame(results)

        us_tickers = ["NVDA", "TSLA", "AAPL", "MSFT", "AMD", "SMCI", "CELH", "PLTR", "HOOD", "CRWD"]
        kr_tickers = ["005930.KS", "000660.KS", "196170.KQ", "042700.KS", "007660.KS", "003230.KS", "015860.KS", "322000.KS"]

        col_scan1, col_scan2 = st.columns([2, 1])
        with col_scan1:
            if st.button("🔍 실시간 주식 스캔 시작"):
                with st.spinner("시장을 분석 중입니다 (yfinance 연동)..."):
                    all_tickers = us_tickers + kr_tickers
                    df_scan = get_scanner_data(all_tickers)
                    st.session_state['scanner_df'] = df_scan
                    if df_scan.empty:
                        st.warning("⚠️ 시장 데이터를 불러오지 못했습니다. 잠시 후 다시 시도하거나 네트워크 연결을 확인하세요.")
                    else:
                        st.success(f"✅ 분석 완료! {len(df_scan)}개의 주도주 데이터를 불러왔습니다.")
        with col_scan2:
            st.info("💡 종목명을 클릭하면 차트 분석(준비중)이 가능합니다.")

        # 시장 상황 필터 연동 (신호등) - 동적 계산
        st.markdown("---")
        
        market_score = 0
        if 'scanner_df' in st.session_state:
            # 시장 강도 계산 (52주 고점 근처 종목 비율)
            df = st.session_state['scanner_df']
            if not df.empty and 'Position' in df.columns:
                high_count = len(df[df['Position'] == "신고가"])
                total_count = len(df)
                market_score = (high_count / total_count) * 100 if total_count > 0 else 0
        
        signal_color = "🟢" if market_score > 30 else "🟡" if market_score > 10 else "🔴"
        signal_text = "위험 회피 해제 (공격적 매수)" if market_score > 30 else "관망 및 선별 매매" if market_score > 10 else "위험 관리 (현금 비중 확대)"
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<div style='text-align:center;'><h3 style='margin-bottom:0;'>🚦 신호</h3><div style='font-size:60px; margin-top:-10px;'>{signal_color}</div></div>", unsafe_allow_html=True)
        with col2:
            st.write(f"**현재 시장:** {signal_text}")
            st.write(f"신고가 비율: **{market_score:.1f}%**")
            if signal_color == "🟢":
                st.success("👉 **본데의 디렉션:** 돌파 매매(MB)와 에피소딕 피봇(EP)을 가장 공격적으로 노려야 할 시기입니다.")
            elif signal_color == "🟡":
                st.warning("👉 **본데의 디렉션:** 시장 주도주들만 선별적으로 매매하며 비중을 조절하십시오.")
            else:
                st.error("👉 **본데의 디렉션:** 무리한 진입보다는 현금을 확보하고 다음 기회를 기다리십시오.")
        st.markdown("---")

        # 탭 구성
        tab1, tab2, tab3, tab4 = st.tabs(["🔥 1. 모멘텀 버스트 (MB)", "🚀 2. 실적 홈런주 (EP)", "🤫 3. 조용한 눌림목 (Anticipation)", "📈 상세 기술적 분석"])

        selected_ticker = None

        with tab1:
            st.subheader("🔥 모멘텀 버스트 (Momentum Burst) 실시간")
            st.caption("조건: 당일 4% 이상 상승 | 거래량 폭증 | 추세 강화 종목")
            
            if 'scanner_df' in st.session_state:
                df = st.session_state['scanner_df']
                mb_df = df[df['_change_val'] >= 4].sort_values(by='_change_val', ascending=False)
                
                if not mb_df.empty:
                    display_df = mb_df.drop(columns=['_change_val', '_vol_val'])
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                    # 분석할 종목 선택
                    selected_ticker = st.selectbox("분석할 종목 선택 (MB)", mb_df['Ticker'].tolist())
                else:
                    st.warning("현재 조건(상승률 4% 이상)을 만족하는 종목이 없습니다.")
            else:
                st.write("위의 '스캔 시작' 버튼을 눌러 데이터를 불러오세요.")

        with tab2:
            st.subheader("🚀 실시간 에피소딕 피봇 (EP) 탐색")
            if 'scanner_df' in st.session_state:
                df = st.session_state['scanner_df']
                ep_df = df[df['_vol_val'] >= 2.5].sort_values(by='_vol_val', ascending=False)
                if not ep_df.empty:
                    st.dataframe(ep_df.drop(columns=['_change_val', '_vol_val']), use_container_width=True, hide_index=True)
                    if not selected_ticker:
                        selected_ticker = st.selectbox("분석할 종목 선택 (EP)", ep_df['Ticker'].tolist())
                else:
                    st.info("거래량이 평소보다 2.5배 이상 폭증한 종목이 아직 없습니다.")
            else:
                st.write("데이터를 먼저 스캔하세요.")

        with tab3:
            st.subheader("🤫 조용한 눌림목 (Anticipation)")
            st.write("준비 중인 기능입니다.")

        with tab4:
            st.subheader("📈 상세 기술적 분석 차트")
            
            if selected_ticker:
                st.write(f"### {selected_ticker} 분석 보고서")
                
                try:
                    with st.spinner("차트를 생성 중입니다..."):
                        # 데이터 로드 (6개월치)
                        data = yf.download(selected_ticker, period="6mo")
                        
                        # 지표 계산
                        data['MA50'] = data['Close'].rolling(window=50).mean()
                        data['MA200'] = data['Close'].rolling(window=200).mean()
                        
                        # RSI 계산
                        delta = data['Close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        data['RSI'] = 100 - (100 / (1+rs))
                        
                        # 차트 생성
                        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                           vertical_spacing=0.03, subplot_titles=(f'{selected_ticker} Candlestick', 'RSI'), 
                                           row_width=[0.3, 0.7])

                        # 캔들스틱
                        fig.add_trace(go.Candlestick(x=data.index,
                                        open=data['Open'],
                                        high=data['High'],
                                        low=data['Low'],
                                        close=data['Close'],
                                        name='Price'), row=1, col=1)

                        # 이동평균선
                        fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], line=dict(color='yellow', width=1), name='MA50'), row=1, col=1)
                        fig.add_trace(go.Scatter(x=data.index, y=data['MA200'], line=dict(color='orange', width=1.5), name='MA200'), row=1, col=1)

                        # RSI
                        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], line=dict(color='magenta', width=1), name='RSI'), row=2, col=1)
                        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

                        # 레이아웃 설정 (터미널 테마와 어울리게 다크하게)
                        fig.update_layout(
                            template='plotly_dark',
                            height=600,
                            showlegend=True,
                            xaxis_rangeslider_visible=False,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # 지표 요약
                        curr_rsi = data['RSI'].iloc[-1]
                        rsi_status = "과매수 (경계)" if curr_rsi > 70 else "과매도 (기회)" if curr_rsi < 30 else "중립"
                        
                        c1, c2, c3 = st.columns(3)
                        c1.metric("현재 RSI", f"{curr_rsi:.1f}", rsi_status)
                        c2.metric("50일 이평선", f"{data['MA50'].iloc[-1]:,.0f}")
                        c3.metric("200일 이평선", f"{data['MA200'].iloc[-1]:,.0f}")

                        # --- Phase 3: AI 뉴스 분석 & 백테스트 ---
                        st.markdown("---")
                        col_ai, col_bt = st.columns(2)
                        
                        with col_ai:
                            st.write("### 🤖 AI 뉴스 감성 분석")
                            news = yf.Ticker(selected_ticker).news
                            if news:
                                for item in news[:3]:
                                    title = item['title']
                                    # 간단한 감성 분석 시뮬레이션
                                    score = 0
                                    positive_words = ["high", "surge", "growth", "buy", "positive", "win", "beat", "profit", "신고가", "급등", "성장", "흑자"]
                                    if any(word in title.lower() for word in positive_words):
                                        sentiment = "Positive 🟢"
                                    else:
                                        sentiment = "Neutral ⚪"
                                    
                                    st.markdown(f"""
                                        <div style='background-color: #111111; padding: 10px; border-radius: 5px; border-left: 3px solid #FFFF00; margin-bottom: 5px;'>
                                            <span style='font-size: 10px; color: #8a94a6;'>{sentiment}</span>
                                            <div style='font-size: 14px;'>{title}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.write("최근 관련 뉴스가 없습니다.")

                        with col_bt:
                            st.write("### 📊 가상 백테스트 (6개월)")
                            # 6개월 전 대비 수익률 계산
                            start_price = data['Close'].iloc[0]
                            end_price = data['Close'].iloc[-1]
                            return_pct = ((end_price - start_price) / start_price) * 100
                            
                            st.write(f"**6개월 전 가격:** {start_price:,.2f}")
                            st.write(f"**현재 가격:** {end_price:,.2f}")
                            st.metric("수익률 (6mo)", f"{return_pct:+.2f}%")
                            
                            st.caption("※ 6개월 전 매수 후 보유 시의 가상 수익률입니다.")

                except Exception as e:
                    st.error(f"차트 생성 중 오류가 발생했습니다: {e}")
            else:
                st.info("먼저 스캔을 진행하고 종목을 선택해주세요.")

    # --- 페이지 3: 리스크 관리 계산기 ---
    elif page == "🧮 리스크 관리 계산기":
        st.header("🧮 리스크 관리 및 포지션 사이징")
        st.write("마크 미너비니의 리스크 관리 원칙을 적용한 계산기입니다.")
        
        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            capital = st.number_input("총 투자 자산 (원/$)", value=10000000)
            risk_percent = st.slider("1회 매매당 최대 리스크 (%)", 0.5, 5.0, 1.0)
            entry_price = st.number_input("매수 예정가", value=100000)
        
        with col_calc2:
            stop_loss = st.number_input("손절가 설정", value=95000)
            target_price = st.number_input("목표가 설정", value=120000)
        
        # 계산 로직
        total_risk_amount = capital * (risk_percent / 100)
        risk_per_share = entry_price - stop_loss
        
        if risk_per_share > 0:
            position_size = int(total_risk_amount / risk_per_share)
            total_investment = position_size * entry_price
            reward_per_share = target_price - entry_price
            rr_ratio = reward_per_share / risk_per_share
            
            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            c1.metric("권장 매수 수량", f"{position_size} 주")
            c2.metric("총 투입 금액", f"{total_investment:,} 원")
            c3.metric("손익비 (R/R)", f"{rr_ratio:.2f}")
            
            if rr_ratio < 2:
                st.warning("⚠️ 손익비가 2.0 미만입니다. 진입을 재검토하십시오.")
            else:
                st.success("✅ 손익비가 우수합니다. 진입하기 좋은 타점입니다.")
        else:
            st.error("손절가는 매수가보다 낮아야 합니다.")

    # --- 페이지 4: 실시간 뉴스 피드 ---
    elif page == "📰 실시간 뉴스 피드":
        st.header("📰 실시간 금융 뉴스 (Global News)")
        news_data = [
            {"title": "미 연준, 금리 동결 시사... 시장 반응은?", "source": "Reuters", "time": "10분 전"},
            {"title": "엔비디아(NVDA) 사상 최고가 경신, AI 열풍 지속", "source": "Bloomberg", "time": "30분 전"},
            {"title": "한국 반도체 수출 5개월 연속 상승세", "source": "연합뉴스", "time": "1시간 전"},
            {"title": "테슬라(TSLA), 중국 시장 점유율 확대 전략 발표", "source": "CNBC", "time": "2시간 전"}
        ]
        for news in news_data:
            st.markdown(f"""
                <div style='background-color: #111111; padding: 15px; border-radius: 10px; border-left: 5px solid #FFFF00; margin-bottom: 10px;'>
                    <span style='color: #8a94a6; font-size: 12px;'>{news['source']} | {news['time']}</span>
                    <h4 style='margin: 5px 0;'>{news['title']}</h4>
                </div>
            """, unsafe_allow_html=True)

    # --- 페이지 5: 본데 주식 50선 ---
    elif page == "📊 본데 주식 50선":
        st.header("📊 본데의 주식 50선 (Google Sheets 연동)")
        st.write("구글 스프레드시트에서 실시간으로 데이터를 불러옵니다.")
        sheet_id = "1xjbe9SF0HsxwY_Uy3NC2tT92BqK0nhArUaYU16Q0p9M"
        gid = "1499398020"
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        try:
            df = pd.read_csv(csv_url)
            st.dataframe(df, use_container_width=True)
            st.success("✅ 데이터를 성공적으로 불러왔습니다.")
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 엑셀(CSV) 파일로 저장", data=csv, file_name='bonde_top_50.csv', mime='text/csv')
        except Exception as e:
            st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")

    # --- 페이지 6: 마스터 클래스 ---
    elif page == "💎 마스터 클래스":
        tab_m1, tab_m2 = st.tabs(["💎 Pradeep Bonde", "🏆 Mark Minervini"])
        with tab_m1:
            st.header("💎 Master Class: Pradeep Bonde")
            st.write("프라딥 본데는 '안타'를 지속적으로 쳐서 복리를 극대화하는 전략의 대가입니다.")
            st.subheader("3대 핵심 철학")
            st.write("- 안타(Singles)를 쳐라\n- 절차적 기억(Procedural Memory)\n- 셀프 리더십(Self-Leadership)")
        with tab_m2:
            st.header("🏆 Master Class: Mark Minervini")
            st.write("마크 미너비니는 VCP(변동성 축소 패턴)의 창시자이자 미국 투자 챔피언입니다.")
            st.subheader("핵심 전략")
            st.write("- VCP 패턴: 변동성이 줄어드는 지점을 포착\n- SEPA 전략: 펀더멘털과 기술적 분석의 결합")

    # --- 페이지 2: 실시간 분석 차트 ---
    elif page == "📈 실시간 분석 차트":
        st.header("📈 실시간 개별 종목 분석 차트")
        ticker = st.text_input("분석할 티커를 입력하세요 (예: NVDA, 005930.KS)", "NVDA")
        if ticker:
            try:
                data = yf.download(ticker, period="1y")
                fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
                fig.update_layout(template='plotly_dark', title=f"{ticker} 실시간 차트", xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"차트를 불러올 수 없습니다: {e}")
    st.sidebar.markdown("---")
    st.sidebar.write("거북이투자전문가 전용 터미널")
    
    # 앰버서더 이미지 로드 시도
    if os.path.exists("bull_market_ambassador.png"):
        st.sidebar.image("bull_market_ambassador.png", width=150)
    else:
        st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzI5yZq00eP8vE8XG9-L_9u_vB_W_K7uB6A&s", width=150)
