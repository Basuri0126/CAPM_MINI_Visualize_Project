import pandas as pd
import streamlit as st
import yfinance as yf
import datetime
import pandas_datareader.data as wb
import FUNC

st.set_page_config(page_title='CAPM', page_icon='money.png', layout='wide')
st.title('Capital Asset Pricing Model')


col1, col2 = st.columns([1, 1])
with col1:
    stock_list = st.multiselect('Select four Stock', ('AAPL', 'MSFT', 'NFLX', 'MGM', 'AMZN', 'NVDA', 'TSLA', 'GOOGL'), ['GOOGL', 'TSLA', 'MSFT', 'AMZN'])
with col2:
    year = st.number_input('Number of Years', 1, 10)

try:
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)

    SP500 = wb.DataReader(['sp500'], 'fred', start, end)
    stock_df = pd.DataFrame()
    for stock in stock_list:
        data = yf.download(stock, period=f'{year}y')
        stock_df[f'{stock}'] = data['Close']

    stock_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)

    SP500.columns = ['Date', 'sp500']
    stock_df['Date'] = stock_df['Date'].astype('datetime64[ns]')
    stock_df['Date'] = stock_df['Date'].apply(lambda x: str(x)[:10])
    stock_df['Date'] = pd.to_datetime(stock_df['Date'])
    stock_df = pd.merge(stock_df, SP500, on='Date', how='inner')
    print(stock_df)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('#### **Dataframe head**')
        st.dataframe(stock_df.head(), use_container_width=True)

    with col2:
        st.markdown("**Dataframe Tail**")
        st.dataframe(stock_df.tail(), use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('### Price Of all Stocks')
        st.plotly_chart(FUNC.beautiful_plot(stock_df))

    with col2:
        st.markdown('### Price Of all Stocks after normalizing')
        st.plotly_chart(FUNC.beautiful_plot(FUNC.normalize(stock_df)))

    stock_daily_return = FUNC.daily_return(stock_df)
    print(stock_daily_return)

    beta = {}
    alpha = {}

    for i in stock_daily_return.columns:
        if i != 'Date' and i != 'sp500':
            b, a = FUNC.calculate_beta(stock_daily_return, i)
            beta[i] = b
            alpha[i] = a
    print(beta, alpha)

    beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
    beta_df['Stock'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

    with col1:
        st.markdown("### Calculated Beta Value")
        st.dataframe(beta_df, use_container_width=True)

    rf = 0
    rm = stock_daily_return['sp500'].mean()*252

    return_df = pd.DataFrame()
    return_value = []

    for stock, value in beta.items():
        return_value.append(str(round(rf+(value*(rm-rf)), 2)))

    return_df['Stock'] = stock_list

    return_df['Return Value'] = return_value

    with col2:
        st.markdown('### Calculated return using CAPM')
        st.dataframe(return_df, use_container_width=True)
except:
    st.write('Please Select Valid Input')