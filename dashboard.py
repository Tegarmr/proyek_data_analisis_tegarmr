import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('main_data.csv')

# Data Cleaning (pastikan sudah dilakukan sebelumnya)
data.dropna(inplace=True)

# Hitung penjualan per kategori
penjualan_per_kategori = data.groupby('product_category_name_english')['order_id'].nunique().reset_index()
penjualan_per_kategori.rename(columns={'order_id': 'Total Sales'}, inplace=True)

# Menghitung persentase penjualan
total_sales = penjualan_per_kategori['Total Sales'].sum()
penjualan_per_kategori['Percentage'] = (penjualan_per_kategori['Total Sales'] / total_sales) * 100

# Menggabungkan kategori dengan kontribusi di bawah 2.5% menjadi "Others"
penjualan_per_kategori['Product Category (English)'] = penjualan_per_kategori.apply(
    lambda row: 'Others' if row['Percentage'] < 2.5 else row['product_category_name_english'], axis=1
)

# Mengelompokkan ulang dan menghitung total sales untuk kategori "Others"
final_sales = penjualan_per_kategori.groupby('Product Category (English)')['Total Sales'].sum().reset_index()
final_sales['Percentage'] = (final_sales['Total Sales'] / final_sales['Total Sales'].sum()) * 100
final_sales = final_sales.sort_values(by='Total Sales', ascending=False)

# Streamlit App
st.title("Analisis E-commerce")

# Visualisasi Rerata Rating Ulasan per Kategori Produk
pivot_avg_rating_per_category_translated = data.groupby('product_category_name_english')['review_score'].mean().reset_index()
pivot_avg_rating_per_category_translated = pivot_avg_rating_per_category_translated.sort_values(by='review_score', ascending=False)

# Visualisasi 10 Kategori Produk Terpopuler di São Paulo dan Rio de Janeiro
top_10_kategori = data[data['customer_city'].isin(['sao paulo', 'rio de janeiro'])].groupby('product_category_name_english')['order_id'].nunique().reset_index()
top_10_kategori = top_10_kategori.sort_values(by='order_id', ascending=False).head(10)  # Ambil 10 teratas

# Visualisasi Rerata Rating Ulasan Tertinggi
st.subheader('Kategori Produk dengan Rerata Rating Ulasan Tertinggi')
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(data=pivot_avg_rating_per_category_translated.head(10), 
            x='review_score', 
            y='product_category_name_english', 
            palette='viridis', ax=ax1)
ax1.set_title('Kategori Produk dengan Rerata Rating Ulasan Tertinggi')
ax1.set_xlabel('Rerata Rating Ulasan')
ax1.set_ylabel('Kategori Produk')
st.pyplot(fig1)

# Visualisasi 10 Kategori Produk Terpopuler
st.subheader('10 Kategori Produk Terpopuler di São Paulo dan Rio de Janeiro')
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_10_kategori, 
            x='order_id', 
            y='product_category_name_english', 
            palette='rocket', ax=ax2)
ax2.set_title('10 Kategori Produk Terpopuler di São Paulo dan Rio de Janeiro')
ax2.set_xlabel('Jumlah Pesanan')
ax2.set_ylabel('Kategori Produk')
st.pyplot(fig2)

# Visualisasi Pie Chart
st.subheader('Persentase Penjualan Tiap Kategori Produk')
fig3, ax3 = plt.subplots(figsize=(10, 8))
ax3.pie(final_sales['Total Sales'], 
        labels=final_sales['Product Category (English)'], 
        autopct='%1.1f%%', 
        startangle=140)
ax3.set_title('Persentase Penjualan Tiap Kategori Produk di E-commerce')
ax3.axis('equal')  # Equal aspect ratio ensures that pie chart is a circle.
st.pyplot(fig3)

# Kesimpulan
st.subheader("Kesimpulan")
st.write("""
- Kategori produk yang paling laris di ecommerce dengan yang paling laris di kota Sao Paulo dan Rio de Janeiro memiliki kesamaan hanya houseware, 
  yang menandakan housewares itu sangat banyak dibeli di kota tersebut.
- Produk terlaris di ecommerce tidak mendapatkan review score top 10 teratas.
""")

st.write("""
Kesimpulan di atas berguna untuk pemasaran. Kita dapat memasarkan lebih masif lagi untuk produk-produk terlarisnya seperti bed_bath_table, health_beauty, 
sports_leisure ke Kota Sao Paulo dan Rio de Janeiro. Dan menjaga kualitas pelayanan dan barang agar review scorenya naik sehingga orang-orang lebih 
percaya lagi terhadap produk tersebut dan dapat menyebabkan peningkatan penjualan.
""")
