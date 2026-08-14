import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="ai data assistant", layout="wide")

st.title("🪩 AI DATA ASSISTANT")
st.write("Upload your Excel or CSV file to query, filter, or plot charts!")

st.divider()

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully 🧿.")

    st.subheader("👾 Data Preview (First 5 Rows)")
    st.dataframe(df.head())

    st.divider()

    st.subheader("🧸 Ask a question or request an operation on your data")
    user_query = st.text_input("E.g., Create a bar chart of sales by category, Get records where city is Istanbul...")

    if user_query:
        if not api_key:
            st.error("⚠️ API Key not found! Please check your .env file")
        else:
            with st.spinner("AI is processing your data..."):
                client = genai.Client(api_key=api_key)

                max_deneme = 3
                hata_gecmisi = ""
                basarili = False
                clean_code = ""
                son_hata = None

                for deneme in range(max_deneme):
                    try:
                        prompt = f"""
                        Elimizde 'df' adında bir pandas Dataframe var.
                        Sütunları şunlardır: {list(df.columns)}

                        Kullanıcının isteği: "{user_query}"

                        ÖNEMLİ KURALLAR:
                        1. SADECE ve SADECE çalıştırılabilir Python kodu yaz.
                        2. Gereksiz hiçbir metin, açıklama veya markdown bloğu (```python gibi) ekleme.
                        3. Bütün tabloya işlem yaparken güncel Pandas kullandığımız için sakın 'applymap' kullanma! Onun yerine 'map' veya sütun bazlı dönüştürme kullan.
                        4. Eğer kullanıcı GRAFİK / ÇİZİM istiyorsa:
                           - `matplotlib.pyplot` kullan.
                           - `fig, ax = plt.subplots()` ile başlat ve grafiği `ax` üzerine çiz.
                           - `plt.show()` YAZMA!
                           - Sonuç değişkeni `result = fig` olmalı.
                        5. Eğer kullanıcı TABLO / FİLTRE istiyorsa:
                           - 'result' değişkeni bir DataFrame olmalı.
                        6. Eğer TEK BİR CEVAP / ÖZET ise:
                           - 'result' değişkenine metin veya sayı ata.
                        {hata_gecmisi}
                        """

                        # --- YENİ SDK: generate_content artık client.models üzerinden çağrılıyor ---
                        response = client.models.generate_content(
                            model='gemini-3.5-flash-lite',
                            contents=prompt
                        )
                        clean_code = response.text.replace("```python", "").replace("```", "").strip()

                        local_vars = {"df": df, "pd": pd, "plt": plt}
                        exec(clean_code, {}, local_vars)

                        result = local_vars.get("result", "Process completed, but no results were generated.")
                        basarili = True
                        break  

                    except Exception as e:
                        son_hata = e
                        hata_gecmisi = f"""
                        NOT: Bir önceki denemende şu kodu ürettin:
                        ---
                        {clean_code if clean_code else '(kod üretilemedi)'}
                        ---
                        Bu kod çalıştırılınca şu hatayı verdi: "{e}"
                        Lütfen bu hatayı dikkate alarak kodu düzelt ve tekrar SADECE kod olarak yaz.
                        """
                        continue 

                if basarili:
                    st.markdown("💥 Result:")
                    if isinstance(result, pd.DataFrame):
                        st.dataframe(result)
                    elif isinstance(result, plt.Figure):
                        st.pyplot(result)
                    else:
                        st.write(result)
                else:
                   st.error(f"Could not resolve the issue after {max_deneme} attempts. Last error: {son_hata}")
