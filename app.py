import streamlit as st
import datetime
import yfinance as yf
import pandas as pd
import base64
import io

# Sembol girişini kontrol etmek için bir fonksiyon
def validate_symbol(symbol):
    if not symbol:
        st.error("Lütfen bir hisse senedi sembolü girin.")
        return False
    return True

symbol = st.sidebar.text_input("Hisse Senedi Sembolü", value="GOOGL")

if validate_symbol(symbol):
    st.title(symbol + " Hisse Senedi Grafiği")

    start_date = st.sidebar.date_input("Başlangıç Tarihi", value=datetime.datetime(2020, 1, 1))
    end_date = st.sidebar.date_input("Bitiş Tarihi", value=datetime.datetime.now())

    df = yf.download(symbol, start=start_date, end=end_date)
    if not df.empty:
        st.subheader("Hisse Senedi Bilgileri")
        info = yf.Ticker(symbol).info
        if info:
            st.write("Şirket Adı:", info.get('longName', 'Bilgi Yok'))
            st.write("Sektör:", info.get('sector', 'Bilgi Yok'))
            st.write("İşletme Alanı:", info.get('industry', 'Bilgi Yok'))
            # İhtiyaç duyulan diğer bilgileri ekleyebilirsiniz.
        else:
            st.error("Hisse senedi bilgileri alınamadı.")

        # Hisse Senedi Trend Grafiği
        st.subheader("Hisse Senedi Trend Grafiği")
        st.line_chart(df["Close"], use_container_width=True)

        # Hacim Grafiği
        st.subheader("Hisse Senedi Hacmi")
        st.line_chart(df["Volume"], use_container_width=True)

        # Hisse Senedi Fiyatları
        st.subheader("Hisse Senedi Fiyatları")
        st.write(df)

        # Temel İstatistikler
        st.subheader("Hisse Senedi İstatistikleri")
        st.write(df.describe())

        # Hisse Senedi Fiyatlarını İndirme Bağlantısı
        formats = ["CSV", "Excel"]
        selected_format = st.radio("İndirme Formatı:", formats)

        if selected_format == "CSV":
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{symbol}_hisse_fiyatlari.csv">Hisse Fiyatlarını İndir (CSV)</a>'
        elif selected_format == "Excel":
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)
            b64 = base64.b64encode(excel_buffer.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{symbol}_hisse_fiyatlari.xlsx">Hisse Fiyatlarını İndir (Excel)</a>'

        st.markdown(href, unsafe_allow_html=True)
    else:
        st.error("Belirtilen tarih aralığında veri bulunamadı. Lütfen başka bir tarih aralığı seçin.")

    st.sidebar.info("Borsa İstanbul için bilgi almak isterseniz .IS ekleyiniz. Örneğin ASELS.IS")
    st.sidebar.info("Bu bilgiler yahoo finance üzerinden çekilmiştir.")
    st.sidebar.info("Sadece bilgi amaçlı tasarlanmıştır.")
