import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime

st.title('Costco Wholesale: Stock Analysis')

# import CSV and jpeg files and prepare data into dataframes
data = pd.read_csv("Costco1.csv")
data1 = pd.read_csv("Financials.csv")
data2 = pd.read_csv("5_Year_Stock_Data.csv")
data3 = pd.read_csv("Retail_Beta_PE.csv")
data4 = pd.read_csv("Quarterly_Costco.csv")
image1 = Image.open('costco.jpeg')
image2 = Image.open('overvalued.jpg')
df1= pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
df4 = pd.DataFrame(data4)

df1['Fiscal Year'] = pd.to_datetime(df1['Fiscal Year'], format='%Y').dt.year

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Introduction', 'Overview', '5 Year Share Price Trend', 
'Risk vs Reward', 'Qtly Performance & Volume', 'Conclusion'])

with tab1:
    st.header('''Introduction''')
    st.image(image1, caption=None, width=650)
    st.markdown('''This presentation serves to analyze the investment prospects of equity securities 
    in Costco Wholesale (Costco). We will examine key financial metrics and historical share prices in 
    comparison with other big-box retail stores, including Wal-Mart, Home Depot, and Target, as well as the 
    retail industry and the overall stock market. For the purposes of comparison, the retail industry 
    will be represented by SPDR S&P Retail ETF and the overall stock market will be represented by SPDR 
    S&P 500 ETF. At the end of the presentation, a conclusion on whether the shares are undervalued, 
    fairly valued or overvalued will be made, as well as a recommendation to buy or sell the shares.''')

with tab2:
    st.header('''Overview''')
    st.markdown('''Costco Wholesale is a chain of membership-only big-box retail stores headquartered in 
    Issaquah, Washington. Founded in 1983, Costco is the third largest retailer in the world, behind only 
    Wal-Mart and Amazon, with 578 locations in the US and 261 international locations.''')
    st.markdown('''Below is a map of all 578 US locations:''')
    st.map(data)

with tab3:
    st.header('''5 Year Share Price Trend''')
    st.markdown('''Below shows the five-year trend of closing share prices for Costco, compared with retail 
    competitors Home Depot (HD), Target (TGT) and Wal-Mart (WMT). Additionally, share price trends for the 
    retail sector, which is represented by SPDR S&P Retail ETF (XRT), and the entire stock market, which is 
    represented by SPDR S&P 500 ETF (SPY), are presented alongside the other shares.''')
    st.markdown('''Over the five years from October 2017 through October 2022, Costco has outperformed its 
    peers in the retail sector and the entire market. A box plot summarizing 5 years of closing share prices
    is shown below. Use the double slider scale below to choose a range of dates of closing stock prices information''')

    Date = df2["Date"].unique().tolist()

    min_value = datetime.strptime(min(Date), '%Y-%m-%d')  # str to datetime
    max_value = datetime.strptime(max(Date), '%Y-%m-%d')
    value = (min_value, max_value)

    Model = st.slider(
        'Date:',
        min_value=min_value,
        max_value=max_value,
        value=value)

    selmin, selmax = Model
    selmind = selmin.strftime('%Y-%m-%d')  # datetime to str
    selmaxd = selmax.strftime('%Y-%m-%d')

    dfres = df2.loc[(df2['Date'] >= selmind) & (df2['Date'] <= selmaxd)]
    
    Price_Chart = alt.Chart(dfres).mark_line().encode(
        x=alt.X('Date:T'),
        y=alt.Y('Close:Q', axis=alt.Axis(format='$.0f', title='Dollar Amount')),
        color='Ticker:N',
        tooltip=('Ticker:N', 'Date:T', 
            alt.Tooltip('Open:Q', format='$.2f'),
            alt.Tooltip('High:Q', format='$.2f'),
            alt.Tooltip('Low:Q', format='$.2f'),
            alt.Tooltip('Close',format='$.2f'))
        ).properties(
            width = 600,
            height = 550
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=16
        ).configure_legend(
                titleFontSize=16,
                labelFontSize=16
        ).interactive()
    st.write(Price_Chart)

    Box_Plot = alt.Chart(dfres).mark_boxplot(size=20).encode(
        x=alt.X('Ticker:N'),
        y=alt.Y('Close:Q', 
        axis=alt.Axis(format='$.0f', title='Dollar Amount'))
        ).properties(
            width = 525,
            height = 525
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=16
        )  
    st.write(Box_Plot)

with tab4:
    st.header('''Risk vs Reward''')
    Scatter_plot1 = alt.Chart(df3).mark_circle(size=75, color='#e21414').encode(
        x='P/E',
        y='Beta',
        tooltip=['Retailer','P/E','Beta']
        ).properties(
            width = 500,
            height = 500
        )   
    
    # 2nd layer to put Costco image on scatter plot
    points = pd.DataFrame([{
    "P/E": 36.39, "Beta": 0.72, "img": "https://raw.githubusercontent.com/awill321/costco_stock_analysis/main/costco.jpeg"
    }])

    Scatter_plot2 = alt.Chart(points).mark_image(
        width=65,
        height=65).encode(
        x='P/E',
        y='Beta',
        url='img',
        tooltip=['P/E', 'Beta']
        ).properties(
            width = 10,
            height = 10
        )   

    st.write(Scatter_plot1+Scatter_plot2)
    st.markdown('''The plot above shows the relationship between the Beta on the X-axis and P/E on the Y-axis. 
    Beta measures the volatility of a stock prices for an individual company relative to volatility of the overall market. 
    The Beta of Costco is 0.72, which can be interpreted as if S&P 500 index rises or falls 10%, Costco is expected to rise or 
    fall 7.2%, indicating that Costco is considered less risky than the overall market.''')
    st.markdown('''The P/E ratio of Costco is 36.4x, which is calculated by dividing the price of the share by 
    the earnings per share of the company. Amongst the 26 retailers included in the plot above, Costco has the 
    2nd highest P/E ratio, which implies it is overpriced, all else equal.''')
    
    st.subheader('''Profitability''')
    Line_Item = [' ', 'Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income']
    Profitability = st.selectbox("Select a Profitability Metric:",Line_Item)

    df_income = df1[df1['Line Item']== Profitability]

    if Profitability != ' ':
        bar = alt.Chart(df_income).mark_bar(color='#e21414').encode(
            alt.X('Fiscal Year:N',title = "Fiscal Year"),
            alt.Y('sum(Amount)',title="$ (in millions)",
                axis=alt.Axis(format='$,.0f'))
        ).properties(
            width = 500,
            height = 500
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=16
        )
        st.altair_chart(bar)
        st.markdown('''Over the past 5 years, revenue, gross profit and net profit have steadily improved. 
        In 2022, revenue, gross profit and net profit increased 59.9%, 49.7% and 46.4%, respectively, from 2018. 
        The growth is impressive, especially considering online retailers have taken market share from brick-and-mortar 
        stores and growth has been modest for traditional big-box retailers in recent years.''')

with tab5:
    st.header('''Qtly Performance & Volume''')
    st.markdown('''For a more granular view of the daily volatility and volume of Costco shares, refer to the graphs below. The top
    graph shows the prices of the shares when the stock market opened and closed each trading day and the highest and lowest 
    prices of the shares during that trading day. The bottom graph shows the daily number of shares sold, also known as the daily volume.''')        
    
    Line_Item1 = [' ', '2022 Q4', '2022 Q3', '2022 Q2', '2022 Q1', '2021 Q4', '2021 Q3', '2021 Q2', '2021 Q1',
                  '2020 Q4', '2020 Q3', '2020 Q2', '2020 Q1', '2019 Q4', '2019 Q3', '2019 Q2', '2019 Q1', '2018 Q4',
                  '2018 Q3', '2018 Q2', '2018 Q1', '2017 Q4']
    quarter_select = st.selectbox("Select a Quarter",Line_Item1)

    quarter_data = df4[df4['Quarter']== quarter_select]

    if quarter_select != ' ':
        Quarterly_Chart = alt.Chart(quarter_data).mark_line(size=5).encode(
            x=alt.X('Date:T'),
            y=alt.Y('Close:Q',axis=alt.Axis(format='$.0f', title='Dollar Amount')),
            tooltip=['Date:T',
                alt.Tooltip('Open:Q', format='$.2f'),
                alt.Tooltip('High:Q', format='$.2f'),
                alt.Tooltip('Low:Q', format='$.2f'),
                alt.Tooltip('Close',format='$.2f')]         
        ).properties(
                width=500,
                height=500
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=16
        )
        
        st.write(Quarterly_Chart)

        Area_Chart = alt.Chart(quarter_data).mark_area().encode(
            x=alt.X('Date:T'),
            y=alt.Y('Volume:Q'),
            tooltip=['Date:T',
                alt.Tooltip('Volume:Q',format=',.0f')]
            ).properties(
                width = 500,
                height = 500
            ).configure_axis(
                labelFontSize=16,
                titleFontSize=16
            )
        st.write(Area_Chart)

with tab6:
    st.header('''Conclusion''')
    st.image(image2, caption=None, width=600)
    st.markdown('''As demonstrated before, Costco has seen impressive growth over the 
    past five years. During that span, revenue, gross profit and net profit steadily 
    improved by 59.9%, 49.7% and 46.4%, respectively. As inflation spirals worldwide, 
    consumers look to save money. Costco sells an annual membership costing $60 but the 
    company’s policy is to markup merchandise by only 10-15% above cost, which is 
    substantially lower than most other grocery chains and retailers.''')
    st.markdown('''Costco has performed exceptionally well over the past five years and 
    investors have taken notice. Over the past five years, the price of Costco shares 
    have increased by approximately 200%. The P/E ratio as of the date of the project 
    is 36.4x, which was the 2nd highest P/E ratio of the 26 retailers that were previously 
    analyzed. As a probable recession looms, investors have turned to investing in 
    cost-leader retailers. The top 5 highest P/E ratios of the analyzed retailers were 
    Burlington Stores, Costco, Walmart, TJX Companies (parent company of TJ Maxx and 
    Marshalls) and Dollar General, respectively, which all target price conscience consumers.''')
    st.markdown('''Although the performance of Costco is expected to continue over the 
    next few years as a recession occurs, the price of Costco shares has more than 
    reflected the expectations.''')
    st.subheader('''In this analyst’s opinion, Costco shares are overpriced and would recommend selling.''')
