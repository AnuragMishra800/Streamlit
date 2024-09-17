import streamlit as st 
import pandas as pd 
import time 
import matplotlib.pyplot as plt 

# st.title('Startup Dashboard')
# st.subheader('Hello Sir!')
# st.header('Hi Bhidu!')

# st.write("I am learning.")

# st.markdown("""
# ## My favourite movies
# - MCU
# - DC 
# """)

# st.code("""
# def foo(input):
#         return foo**2

# x= foo(2) 
# """) 

# st.latex('x^2 + y^2 + 2xy = 0')

# df = pd.DataFrame({
#     'Name': ['Anurag', 'Ansh', 'Shanu'],
#     'Marks': [50, 60, 75],
#     'Package': [9, 10, 10] 
# }) 

# st.dataframe(df) 

# st.metric('Revenue', 'Rs. 3L', '-2%')
# st.metric('Race Cars', 'Rs. 21L', '6%') 

# st.json({
#     'Name': ['Anurag', 'Ansh', 'Shanu'],
#     'Marks': [50, 60, 75],
#     'Package': [9, 10, 10] 
# })

# st.image('red.jpg') 
# # st.video('')

# st.sidebar.image('anime.jpg') 

# col1, col2 = st.columns(2) 

# with col1:
#     st.image('anime.jpg')
# with col2:
#     st.image('red.jpg') 

# st.error('Login Failed') 
# st.warning('First Sign Up and Then Login') 
# st.info('Login Pending') 
# st.success('Login Successfully') 

# bar = st.progress(0)

# for i in range(0, 101):
#     # time.sleep(0.1)
#     bar.progress(i)

# email = st.text_input('Enter Your E-mail :') 
# age = st.number_input('Enter Your Age :') 
# st.date_input('Enter Date:')  

# email = st.text_input('Enter Your Email :')
# password = st.text_input('Enter Your Password :') 
# gender = st.selectbox('Select Gender', ['Male', 'Female', 'Rather Not To Say']) 

# btn = st.button('Login') 

# if btn:
#     if email == 'Bohot Khaas Log' and password == 'BKL':
#         st.success('Login Successful')
#         st.write(gender)   
#         st.balloons()  
#     else:
#         st.error('Login Failed.') 

# file = st.file_uploader('Upload a CSV File') 

# if file is not None:
#     df = pd.read_csv(file) 
#     st.dataframe(df.describe())  

# Our Website using Stramlit 

st.set_page_config(layout='wide',page_title='Stratup Analysis') 

st.title('Indian Stratup Funding Analysis') 

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce') 
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis') 
    
    col1, col2, col3, col4 = st.columns(4) 

    # total invested amount 
    total = round(df['amount'].sum()) 
 
    # maximum funding in startup 
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0] 

    # average funding in startup 
    average = df.groupby('startup')['amount'].sum().mean()

    # total funded startups 
    funded = df['startup'].nunique() 

    with col1:
        st.metric('Total', str(total) + 'cr')
    with col2: 
        st.metric('Max Funding', str(max_funding) + 'cr')  
    with col3: 
        st.metric('Average Funding', str(round(average)) + 'cr')  
    with col4: 
        st.metric('Total Funded Startups', str(funded)) 

    st.header('MOM Graph')

    selected_options = st.selectbox('Select Type', ['Total', 'Count']) 
    if(selected_options=='Total'):
       temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index() 
    else:
       temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index() 

    temp_df['x_axis'] = df['month'].astype('str') + '-' + df['year'].astype('str') 

    fig4, ax4 = plt.subplots()
    ax4.hist(temp_df['x_axis'], bins=20)   
    st.pyplot(fig4)
    

def load_investor_details(investor):
    st.title(investor)  
    # load the recent 5 investments of investor 
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']] 
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)
    
    col1, col2 = st.columns(2)
    with col1: 
        # biggest investments 
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head() 
        st.subheader('Biggest Investments')
        st.dataframe(big_series)
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig) 
    
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested In')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")  
        st.pyplot(fig1)
    
    col3, col4 = st.columns(2)

    # stage wise 
    with col3:
        stage_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum() 
        st.subheader('Equity In Investments')
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_series, labels=stage_series.index, autopct="%0.01f%%")  
        st.pyplot(fig2) 

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum() 
        st.subheader('City Wise Investment')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index)
        st.pyplot(fig3) 
    
    col5, col6 = st.columns(2) 

    with col5:
        df['year'] = df['date'].dt.year  
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('YOY Investments')
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values)
        st.pyplot(fig4) 

def load_gen_info(startup):
    st.title(startup) 
    investor_name = df[df['startup'] == selected_startup]['investors'].values[0] 
    st.subheader(f"Investor: {investor_name}")
    
    df['date'] = pd.to_datetime(df['date']).dt.date 
    details = df[df['startup'] == selected_startup][['date', 'vertical', 'subvertical', 'city', 'round', 'amount']].values[0] 
    st.subheader(f"Date: {details[0]}")
    st.subheader(f"Vertical: {details[1]}")
    st.subheader(f"Subvertical: {details[2]}")
    st.subheader(f"City: {details[3]}")
    st.subheader(f"Equity: {details[4]}")
    st.subheader(f"Amount: {details[5]}cr") 


st.sidebar.title('Startup Funding Analysis') 

option = st.sidebar.selectbox('Select One',['Overall Analysis', 'Startup', 'Investor'])
if option == 'Overall Analysis':
    btn0 = st.sidebar.button('Show Overall Analysis') 
    if btn0:
        load_overall_analysis()   

elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))  
    btn1 = st.sidebar.button('Find Startup Details') 
    if btn1:
        load_gen_info(selected_startup) 
else:
    selected_investor = st.sidebar.selectbox('Select Startup', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details') 
    if btn2:
        load_investor_details(selected_investor) 