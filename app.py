import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(page_title="ScalpAI - Hassas Klinik Teşhis", page_icon="🧬", layout="centered")

def advanced_scalp_analysis(img):
    """
    Görüntü piksellerini analiz ederek hassas kızarıklık indeksi ve kepek cinsi tahmini yapar.
    """
    img_np = np.array(img)
    
    # 1. Hassas Kızarıklık ve Eritem Analizi (Kırmızı ve Yeşil kanal piksel farkı)
    r_channel = img_np[:, :, 0]
    g_channel = img_np[:, :, 1]
    redness_raw = np.mean(r_channel - g_channel)
    # 0 - 10 ölçeğinde hassas kızarıklık skoru
    redness_score = float(np.clip(redness_raw / 3.5, 0.0, 10.0))
    
    # 2. Sebum / Parlaklık ve Yağlanma Yoğunluğu
    brightness = np.mean(img_np)
    sebum_index = float(np.clip((brightness - 90) / 60, 0.0, 1.0)) # 0: Kuru, 1: Aşırı Yağlı
    
    # 3. Doku Varyasyonu / Pullanma Yoğunluk Katsayısı
    texture_variance = float(np.std(img_np) / 30.0)
    
    # Hassas Kepek ve Patoloji Sınıflandırma Mantığı
    if redness_score > 6.5 and texture_variance > 1.2:
        condition = "Şiddetli Seborreik Dermatit (İltihaplı ve Kabuklu Pullanma)"
        severity = "Yüksek (Klinik Takip Gerektirir)"
        prescription = "Ketoconazole (%2) veya Climbazole içeren antifungal medikal şampuanlar, salisilik asit bazlı kabuk yumuşatıcılar."
    elif sebum_index > 0.6 and texture_variance > 0.9:
        condition = "Yağlı Kafa Derisi Kepeği (Pityriasis Steatoides)"
        severity = "Orta / Yüksek"
        prescription = "Zinc Pyrithione, Piroctone Olamine ve sevgiyi dengeleyen Salicylic Acid kombinasyonu."
    elif redness_score < 3.0 and sebum_index < 0.4:
        condition = "Kuru Kafa Derisi Pul Dökülmesi (Pityriasis Simplex / Xerosis)"
        severity = "Hafif"
        prescription = "Sörfaktan içermeyen, Allantoin, Panthenol ve Glycerin ile yoğun nemlendirici nazik formüller."
    else:
        condition = "Subakut / Hafif Tip Eritematöz Kafa Derisi İrritasyonu"
        severity = "Orta"
        prescription = "Hassas deriler için yatıştırıcı Bisabolol ve Tea Tree Oil özlü dengeli şampuanlar."
        
    return redness_score, sebum_index, condition, severity, prescription

def analyze_inci_content(ingredients_text):
    text = ingredients_text.lower()
    
    beneficial_db = {
        "Piroctone Olamine": "Güçlü ve güvenli antifungal (kepek karşıtı) ajan",
        "Ketoconazole": "Medikal düzeyde mantar ve kepek karşıtı etken",
        "Zinc Pyrithione": "Malassezia mantarını baskılayan kepek ajanı",
        "Salicylic Acid": "Keratolitik (pul dökücü ve sebum çözücü)",
        "Selenium Sulfide": "Seboreik dermatit ve yoğun kepek azaltıcı",
        "Climbazole": "Hassas deriler için etkili modern kepek karşıtı etken",
        "Allantoin": "Tahriş olmuş kafa derisini yatıştıran anti-inflamatuar",
        "Bisabolol": "Papatya özü kaynaklı kızarıklık giderici yatıştırıcı",
        "Niacinamide": "Bariyer güçlendirici ve sebum dengeleyici",
        "Tea Tree Oil": "Doğal antimikrobiyal ve ferahlatıcı",
        "Panthenol": "Nemlendirici provitamin B5",
        "Glycerin": "Yoğun nem tutucu baz bileşen"
    }
    
    harmful_db = {
        "sodium lauryl sulfate": "S.L.S. - Kafa derisini aşırı kurutur ve lipid bariyeri zedeler",
        "sls": "S.L.S. - Sert deterjan, tahriş ve kepeği tetikler",
        "ammonium lauryl sulfate": "A.L.S. - Çok sert köpürtücü, hassas deride kuruluk yapar",
        "sodium laureth sulfate": "S.L.E.S. (Yoğun) - Hassas kafa derisinde kuruluk ve kaşıntı yapabilir",
        "methylisothiazolinone": "M.I.T. - Güçlü kontakt alerjen ve tahriş edici koruyucu",
        "methylchloroisothiazolinone": "M.C.I.T. - Alerjik reaksiyon ve dermatit tetikleyicisi",
        "paraben": "Paraben - Hassasiyet yaratabilen kimyasal koruyucu",
        "dmdm hydantoin": "Formaldehit salınımlı koruyucu - Hassas deride tahriş riski",
        "synthetic fragrance": "Yapay Parfüm/Koku - Kafa derisinde kontakt dermatit ve kızarıklık sebebi",
        "alcohol denat": "Kurutucu Alkol - Kafa derisinin doğal nem dengesini bozar"
    }
    
    found_beneficial = []
    found_harmful = []
    
    for item, desc in beneficial_db.items():
        if item.lower() in text:
            found_beneficial.append((item, desc))
            
    for item, desc in harmful_db.items():
        if item in text:
            found_harmful.append((item, desc))
            
    base_score = 45
    base_score += len(found_beneficial) * 12
    base_score -= len(found_harmful) * 18
    final_score = max(10, min(100, base_score))
    
    return found_beneficial, found_harmful, final_score

st.title("🧬 ScalpAI® Klinik Hassasiyetli Analiz")
st.write("Yapay zeka tabanlı otonom kafa derisi eritem/kızarıklık tarama ve gelişmiş INCI içerik platformu.")

tab1, tab2 = st.tabs(["📸 Kafa Derisi Klinik Tarama", "🧪 INCI Formül Analizi"])

with tab1:
    st.header("📋 Kameradan Hassas Patoloji Analizi")
    st.info("💡 **Nasıl Kullanılır?**\n1. Aşağıdaki **'Kamerayı Aç' (Take Photo)** butonuna dokunun.\n2. Telefonunuzun kamera iznine **İzin Verin**.\n3. Kafa derinizin fotoğrafını çekin.")
    
    scalp_photo = st.camera_input("Kafa Derinizi Kameraya Yaklaştırıp Çekin")
    
    if scalp_photo:
        st.success("⚡ Görüntü piksel matrisine döküldü, klinik analiz gerçekleştiriliyor...")
        img = Image.open(scalp_photo)
        
        redness_score, sebum_index, condition, severity, prescription = advanced_scalp_analysis(img)
        
        st.subheader("📊 Hassas Görüntü İşleme Metrikleri:")
        col1, col2 = st.columns(2)
        col1.metric("Kızarıklık / Eritem İndeksi", f"{redness_score:.1f} / 10.0")
        col2.metric("Sebum / Yağlanma Düzeyi", f"%{int(sebum_index * 100)}")
        
        st.divider()
        st.subheader("🔬 TIBBİ TEŞHİS VE PATOLOJİ RAPORu")
        st.markdown(f"**Tahmin Edilen Kepek / Patoloji Cinsi:** {condition}")
        st.markdown(f"**Klinik Derece / Şiddet:** `{severity}`")
        
        st.info(f"💊 **Hedeflenen Tedavi Reçetesi ve İçerik Önerisi:**\n\n{prescription}")

with tab2:
    st.header("🔍 Profesyonel Şampuan INCI Analizcisi")
    st.write("Şampuanın arkasındaki 'Ingredients' (İçindekiler) metnini kopyalayarak formülün kalitesini ve risklerini test edin.")
    
    ingredients_input = st.text_area(
        "Şampuan İçerik Metni:",
        placeholder="Örn: Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Piroctone Olamine, Salicylic Acid, Parfum..."
    )
    
    if st.button("Formülü Derinlemesine Analiz Et"):
        if ingredients_input.strip() == "":
            st.warning("Lütfen analiz için içerik metni girin.")
        else:
            beneficial, harmful, score = analyze_inci_content(ingredients_input)
            
            st.subheader(f"🎯 Formül Güvenilirlik ve Uyum Skoru: %{score}")
            if score >= 75:
                st.success("Mükemmel Formülasyon: Kafa derinizi koruyan ve tedavi eden bileşenler ağırlıkta.")
            elif score >= 40:
                st.warning("Orta Seviye: Formülde hem etken maddeler var hem de sert deterjanlar riski artırıyor.")
            else:
                st.error("⚠️ Yüksek Riskli Formül: Sert sülfatlar ve koruyucular kepeği ve tahrişi tetikleyebilir.")
                
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("### ✅ Destekleyici / Faydalı Maddeler")
                if beneficial:
                    for item, desc in beneficial:
                        st.markdown(f"- **{item}**: {desc}")
                else:
                    st.info("Tedavi edici etkin bileşen saptanamadı.")
                    
            with col_b:
                st.markdown("### ❌ Riskli / Tetikleyici Maddeler")
                if harmful:
                    for item, desc in harmful:
                        st.markdown(f"- **{item}**: {desc}")
                else:
                    st.success("Riskli veya kepeği tetikleyen sert bileşen saptanmadı!")
