import streamlit as st

from search import search_stocks
from stock_info import Stock
from backend import AI_report
from comments import (
    create_connection, 
    create_table, 
    insert_comment, 
    get_all_comments,
    )

@st.cache_data
def cache_AI_report(ticker):
    return AI_report(ticker)

class SearchResults:
    def __init__(self, item):
        self.item = item
    
    @property    
    def symbol(self):
        return self.item['Symbol']
    
    @property
    def name(self):
        return self.item['Name']
    
    def __str__(self):
        return f'{self.symbol} - {self.name}'

st.title('주식 정보 분석 대시보드')

search_query = st.text_input('검색창')
hits = search_stocks(search_query)['hits']
search_results = [SearchResults(hit) for hit in hits]

selected = st.selectbox('검색 결과 리스트', search_results)

tabs = ['회사 기본 정보', 'AI 분석 보고서', '종목 토론실']
tab1, tab2, tab3 = st.tabs(tabs)

with tab1:
    stock = Stock(selected.symbol)
    st.header(str(selected))

    st.subheader(f'거래량')
    stock_data = stock.financial_info()
    st.line_chart(stock_data['history']['Volume'])
    
    st.header(f'재무제표')
    
    st.header("재무제표")
    cols = st.columns(3)
    cols[0].subheader("매출액")
    cols[0].line_chart(stock_data['income_statement'].loc['Total Revenue'])
    cols[1].subheader("순이익")
    cols[1].line_chart(stock_data['income_statement'].loc['Net Income'])
    cols[2].subheader("영업이익")
    cols[2].line_chart(stock_data['income_statement'].loc['Operating Income'])

    cols = st.columns(3)
    cols[0].subheader("자산")
    cols[0].line_chart(stock_data['balance_sheet'].loc['Total Assets'])
    cols[1].subheader("부채")
    cols[1].line_chart(stock_data['balance_sheet'].loc['Total Liabilities Net Minority Interest'])
    cols[2].subheader("자본")
    cols[2].line_chart(stock_data['balance_sheet'].loc['Stockholders Equity'])

    cols = st.columns(4)
    cols[0].subheader("영업 현금흐름")
    cols[0].line_chart(stock_data['cash_flow'].loc['Operating Cash Flow'])
    cols[1].subheader("투자 현금흐름")
    cols[1].line_chart(stock_data['cash_flow'].loc['Investing Cash Flow'])
    cols[2].subheader("재무 현금흐름")
    cols[2].line_chart(stock_data['cash_flow'].loc['Financing Cash Flow'])
    cols[3].subheader("순 현금흐름")
    cols[3].line_chart(stock_data['cash_flow'].loc['Free Cash Flow'])

with tab2:
    st.header("AI 분석 보고서")
    if st.button("보고서 불러오기"):
        with st.spinner(text='In progress'):
            data = cache_AI_report(selected.symbol)
            st.success('Done')
        st.write(data)

with tab3:
    st.header('종목 토론실')
    conn = create_connection()
    create_table(conn)
    
    for comment in get_all_comments(conn):
        comment_time, comment_text = comment
        st.write(f'{comment_time}: {comment_text}')
        
    new_comment = st.text_area('댓글을 입력하세요')
    if st.button('댓글 작성'):
        insert_comment(conn, f'{selected.name} - {new_comment}')
        st.success('댓글이 작성되었습니다')
        st.rerun()
    