import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

file_path = "test_data.csv"  
data = pd.read_csv(file_path)

st.title("Streamlit Visualization Dashboard นายอธิศ ฟองไข่มุกข์")

st.markdown(f"Test Data: [Here](https://drive.google.com/file/d/1A2sCTlefZFYVw9pydVmyYOXqynpocN10/view?usp=drive_link)")

if data is not None:
    # แปลงวันที่และคำนวณเวลาให้บริการ
    data['Date'] = pd.to_datetime(data['Date'])
    data['Order Time'] = pd.to_datetime(data['Order Time'])
    data['Serve Time'] = pd.to_datetime(data['Serve Time'])
    data['Service Time (Minutes)'] = (data['Serve Time'] - data['Order Time']).dt.total_seconds() / 60

    # Sidebar สำหรับกรอกข้อมูล
    st.sidebar.header("Filter Data")
    selected_category = st.sidebar.multiselect("Select Category", options=data['Category'].unique(), default=data['Category'].unique())
    start_date = st.sidebar.date_input("Select Start Date", value=pd.to_datetime('2023-06-01'))
    end_date = st.sidebar.date_input("Select End Date", value=pd.to_datetime('2023-12-31'))
    
    # ฟิลเตอร์ข้อมูลตามวันที่และประเภท
    filtered_data = data[(data['Category'].isin(selected_category)) & 
                         (data['Date'] >= pd.to_datetime(start_date)) & 
                         (data['Date'] <= pd.to_datetime(end_date))]

    # Header
    st.header(f"Sales Overview ({start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')})")
cols_price = st.columns(2)
with cols_price[0]:
    st.metric("Total Orders", len(filtered_data))

        # คำนวณยอดขายรวมทั้งหมด
    filtered_data['Total Sales'] = filtered_data['Price']
    total_sales = filtered_data['Total Sales'].sum()
    
    # คำนวณยอดขายแยกตามประเภท (Category)
    total_sales_food = filtered_data.groupby('Category')['Price'].sum()
    st.metric(label="Total Income", value=f"$ {total_sales:,.0f} ")

with cols_price[1]:
    filtered_sales = filtered_data[filtered_data['Category'].isin(['drink', 'food'])]
    category_size = filtered_sales.groupby('Category').size()
    category_size = category_size.rename("Order")
    st.write("Order By Category", category_size)


st.header("Sales Chart: Drink & Food")

cols_category = st.columns(2)
with cols_category[0]:
    filtered_sales = filtered_data[filtered_data['Category'].isin(['drink', 'food'])]
    category_size = filtered_sales.groupby('Category').size()

    fig, ax = plt.subplots()
    ax.pie(category_size, labels=category_size.index, autopct='%1.1f%%', startangle=90, colors=['#FF9999', '#66B2FF'])
    ax.axis('equal') 

    st.pyplot(fig)



with cols_category[1]:
    category_size_percent = (category_size / category_size.sum()) * 100
    category_size_percent = category_size_percent.rename(" % ")
    st.write("Percent by Category", category_size_percent.round(1))
    st.write("Price by Category (US dollar)", total_sales_food.round(0))



st.divider()

# Price popularity

st.header("Popularity Menu by Price")
price_vs_sales = filtered_data.groupby('Price')['Menu'].count()
st.bar_chart(price_vs_sales)

st.divider()

# # Average Price By Month

# st.header("Average Menu Price By Month")
# price_by_month = filtered_data.groupby(filtered_data['Date'].dt.month)['Price'].mean()
# price_by_month.index.name = "Month"
# st.line_chart(price_by_month)

# st.divider()

#  Popular Menu Graph

st.header("Popularity Menu")
top_menus = filtered_data['Menu'].value_counts().head(10)
st.bar_chart(top_menus)

# best seller

st.markdown(f"Popular Menu:  {top_menus.index[0]} - {top_menus[0]} Order ", unsafe_allow_html=True)

st.divider()

# Non Popular Menu Graph

st.header("Non-Popularity Menu")
least_sold_menus = filtered_data['Menu'].value_counts().tail(10)
st.bar_chart(least_sold_menus)

# Non-Popular

st.markdown(f"Non-Popular Menu: {least_sold_menus.index[-1]} - {least_sold_menus[-1]} Order", unsafe_allow_html=True)


st.divider()

# Best selling date

st.header("Best selling date")
orders_by_day = filtered_data.groupby('Day Of Week').size()
st.bar_chart(orders_by_day)

best_selling_day = orders_by_day.idxmax()
st.write(f"Best Selling Day:  {best_selling_day} - {orders_by_day[best_selling_day]} Order")


st.divider()

# Staff Analysis

st.header("Serve Time By Hour and Category")


filtered_data['Order Time'] = pd.to_datetime(filtered_data['Order Time'])
filtered_data['Serve Time'] = pd.to_datetime(filtered_data['Serve Time'])

# คำนวณเวลาการเสิร์ฟ (Service Time)
filtered_data['Service Time (Minutes)'] = (filtered_data['Serve Time'] - filtered_data['Order Time']).dt.total_seconds() / 60

# คำนวณค่าเฉลี่ยเวลาในการเสิร์ฟตามแต่ละชั่วโมงและหมวดหมู่
avg_service_time_by_hour_category = filtered_data.groupby(['Hour', 'Category'])['Service Time (Minutes)'].mean().unstack()

st.line_chart(avg_service_time_by_hour_category.round(1))


# # คำนวณค่าเฉลี่ยเวลาที่ใช้ในการเสิร์ฟ
# service_time = filtered_data.groupby(['Kitchen Staff', 'Drinks Staff'])['Service Time (Minutes)'].mean().reset_index()

# # คำนวณค่า mean max min
# avg_service_time = filtered_data['Service Time (Minutes)'].mean().round(2)
# max_service_time = service_time['Service Time (Minutes)'].max().round(2)
# min_service_time = service_time['Service Time (Minutes)'].min().round(2)

# st.metric(f"ค่าเฉลี่ยเวลาในการเสิร์ฟ (AVG): {start_date.strftime('%d-%m-%Y')} ถึง {end_date.strftime('%d-%m-%Y')}",f"{avg_service_time:.2f}", "Minute" )

# st.metric(f"ค่าเฉลี่ยเวลานานที่สุดในการเสิร์ฟ (MAX): {start_date.strftime('%d-%m-%Y')} ถึง {end_date.strftime('%d-%m-%Y')}",f"{max_service_time:.2f}", "Minute" )
# st.metric(f"ค่าเฉลี่ยเวลาน้อยที่สุดในการเสิร์ฟ (MIN): {start_date.strftime('%d-%m-%Y')} ถึง {end_date.strftime('%d-%m-%Y')}",f"{min_service_time:.2f}", "Minute" )

# Order Hour, Day, Month By Category

cols = st.columns(2)
with cols[0]:
  
    st.markdown("<h2 style='font-size: 20px;'>Order Per Hour By Category</h2>", unsafe_allow_html=True)

    order_by_hour_category = filtered_data.groupby([filtered_data['Order Time'].dt.hour, 'Category']).size().unstack(fill_value=0)
    order_by_hour_category.index.name = "Hour"
    order_by_hour_category.columns.name = "Category"
    st.line_chart(order_by_hour_category)

    st.divider()

    st.markdown("<h2 style='font-size: 20px;'>Order Per Day By Category</h2>", unsafe_allow_html=True)
    order_by_day_category = filtered_data.groupby([filtered_data['Order Time'].dt.day, 'Category']).size().unstack(fill_value=0)
    order_by_day_category.index.name = "Day"
    order_by_day_category.columns.name = "Category"
    st.line_chart(order_by_day_category)

    st.divider()

    st.markdown("<h2 style='font-size: 20px;'>Order Per Month By Category</h2>", unsafe_allow_html=True)
    order_by_monthly_category = filtered_data.groupby([filtered_data['Order Time'].dt.month, 'Category']).size().unstack(fill_value=0)
    order_by_monthly_category.index.name = "Month"
    order_by_monthly_category.columns.name = "Category"
    st.line_chart(order_by_monthly_category)

with cols[1]:
    st.write(order_by_hour_category)
    st.divider() 
    st.write(order_by_day_category)
    st.divider()
    st.write(order_by_monthly_category)







