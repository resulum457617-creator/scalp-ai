import streamlit as st
import re

# --- EKRAN AYARLARI (Mobil Görünüm) ---
st.set_page_config(page_title="ScalpAI - Kepek & INCI Analizi", page_icon="🧬", layout="centered")

# Custom CSS ile mobil uygulama hissi veriyoruz
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main-card { background-color: #FFFFFF; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .score-badge { font-size: 24px; font-weight: bold; color: #10B981; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- INCI VERİ TABANI ---
INCI_DATABASE = {
    "salicylic acid": {"type": "Keratolytic", "action": "Ölü deriyi ve yağı eritir", "score": 5},
    "piroctone olamine": {"type": "Antifungal", "action": "Malassezia mantarını engeller", "score": 5},
    "niacinamide": {"type": "Sebum Dengeleyici", "action": "Yağ üretimini düzenler", "score": 4},
    "menthol": {"type": "Ferahlatıcı", "action": "Kaşıntıyı anında baskılar", "score": 3},
    "glycerin": {"type": "Nemlendirici", "action": "Derinin nem dengesini korur", "score": 4},
    "sodium lauryl sulfate": {"type": "Sert Sürfaktan", "action": "Aşırı kurutma riski taşıtır", "score": -2}
}

st.title("🧬 ScalpAI® Mobile")
st.caption("Yapay Zeka Destekli Kepek & Şampuan Etiket Taraması")

# --- TAB'LAR (EKRANLAR) ---
tab1, tab2 = st.tabs(["📸 Şampuan Etiketi Tara", "📋 Kafa Derisi Teşhisi"])

with tab1:
    st.subheader("🔍 Şampuan INCI Taraması")
    st.write("Şampuanının arka yüzündeki **'İçindekiler / Ingredients'** bölümünün fotoğrafını çek.")
    
    # Telefon kamerasını açan bileşen
    camera_image = st.camera_input("Etiketi Hizala ve Çek")
    
    if camera_image:
        st.success("Görsel yakalandı! OCR analizi yapılıyor...")
        
        # Simüle Edilen OCR Metni (İleride buraya Tesseract/Google Vision bağlanacak)
        # Clear Men örneğimizdeki aktif maddeler
        mock_ocr_text = "Aqua, Sodium Laureth Sulfate, Menthol, Piroctone Olamine, Niacinamide, Glycerin"
        
        found_actives = []
        score = 50
        
        for ingredient, details in INCI_DATABASE.items():
            if ingredient in mock_ocr_text.lower():
                found_actives.append((ingredient.title(), details["type"], details["action"]))
                score += details["score"] * 8
                
        score = max(0, min(100, score))
        
        # --- UYUM RAPORU EKRANI ---
        st.markdown("---")
        st.markdown(f"<div class='score-badge'>Ürün Uyum Skoru: %{score} ✅</div>", unsafe_allow_html=True)
        st.progress(score / 100)
        
        st.write("### 🧪 TESPİT EDİLEN ETKEN MADDELER:")
        for ing, typ, act in found_actives:
            st.info(f"**{ing}** ({typ}): {act}")
            
        if score >= 70:
            st.success("💡 **AI Kararı:** Bu şampuan 'Yağlı/Mantar Kaynaklı Kepek' durumunuz için uygundur!")
        else:
            st.warning("💡 **AI Kararı:** Bu ürün kafa derinizin ihtiyacını tam karşılamıyor.")

with tab2:
    st.subheader("📋 Kafa Derisi Durum Analizi")
    st.write("Mevcut kafa derisi parametrelerini girin:")
    
    flake_size = st.slider("Pul Boyutu (mm)", 0.5, 5.0, 2.5)
    is_oily = st.toggle("Kafa derisi yağlı mı?", value=True)
    redness = st.slider("Kızarıklık / İritasyon Seviyesi", 0, 10, 2)
    
    if st.button("Teşhis Koy"):
        if redness > 6:
            diag, active = "Seborreik Dermatit / İltihaplı Kepek", "Piroctone Olamine"
        elif is_oily and flake_size >= 2.0:
            diag, active = "Yağlı Kafa Derisi Kepeği", "Salicylic Acid"
        else:
            diag, active = "Kuru Kafa Derisi Kepeği", "Glycerin / Panthenol"
            
        st.warning(f"**Teşhis:** {diag}")
        st.success(f"**İhtiyaç Duyulan Etken Madde:** {active}")
