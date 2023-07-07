import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def beautiful_plot(df):
    data = []
    for i in df.columns[1:]:
        trace = go.Scatter(x=df['Date'], y=df[i], name=i)
        data.append(trace)
    layout = go.Layout(title="Stock Price", xaxis={'title': 'Date'}, yaxis={'title': 'Price'}, width=550,
                       margin=dict(l=20, r=20, t=40, b=40), legend=dict(borderwidth=1, bgcolor='lightgray'
                       , bordercolor='black', font=dict(color='red')))
    fig = go.Figure(data=data, layout=layout)
    return fig


def normalize(df2):
    df = df2.copy()
    for i in df.columns[1:]:
        df[i] = df[i]/df[i][0]
    return df


def daily_return(df):
    df_daily = df.copy()
    for i in df_daily.columns[1:]:
        for j in range(1, len(df)):
            df_daily[i][j] = ((df[i][j] - df[i][j-1])/df[i][j-1]) * 100
        df_daily[i][0] = 0
    return df_daily


def calculate_beta(stocks_daily, stock):
    x = stocks_daily['sp500'].mean()*252

    b, a = np.polyfit(stocks_daily['sp500'], stocks_daily[stock], 1)
    return b, a