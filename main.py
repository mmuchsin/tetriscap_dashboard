import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from src.preprocessor import data_loader, data_cleaner

# Page Config
st.set_page_config(
    page_title="Muchsin | Tetris Capstone Project", page_icon=("🔥"), layout="wide"
)

st.image("./src/images/hoax.png")

st.markdown("# Hoaks dimana-mana, Literasi Digital di Indonesia Separah itu kah?")
st.write(
    "### Analisis Literasi Digital Indonesia Ditinjau dari Penyebaran Hoaks Tahun 2020-2021"
)

st.write(
    """
    by Muchsin
    """
)

# Ringkasan Eksekutif
st.subheader("Ringkasan Eksekutif")

st.markdown(
    """
    Literasi Digital di Indonesia belum sampai level “baik”. Jika skor indeks
    tertinggi adalah 5, indeks literasi digital Indonesia baru berada sedikit di
    atas angka 3. Lebih tepatnya Indeks Literasi Digital Indonesia pada tahun
    2020 dan 2021 masih berada pada level “sedang” dengan skor 3,46 dan 3,49.
    Dari 34 provinsi di Indonesia, DI Yogyakarta memiliki Indeks Literasi Digital
    tertinggi tahun 2021, skor 3,71 (dari skala 1-5). Sementara itu, Maluku Utara
    merupakan provinsi dengan skor indeks terendah, yaitu 3,18.

    """
)

# Pendahuluan
st.subheader("Pendahuluan")

st.markdown(
    """
    Perkembangan teknologi berkontribusi besar terhadap perkembangan media,
    khususnya media digital. Ditambah dengan adanya pandemi Covid-19 yang memicu
    terwujudnya new normal. Kebutuhan masyarakat akan informasi yang aktual dan
    faktual meningkat secara signifikan. Akan tetapi, seringkali berita yang
    disajikan media digital tidak lagi melalui proses penyuntingan yang ketat
    sehingga kebenaran informasi yang disajikan pun sulit untuk dipastikan.
    Bahkan, beberapa pihak, dengan sengaja menyebarkan hoaks untuk meraup
    keuntungan.
    Menurut Rifda Amrullah (2020) Penyebaran hoaks di Indonesia dinilai
    meresahkan sehingga diperlukan tindakan serius untuk menekan angka
    penyebaran hoaks. Namun masih banyak masyarakat yang secara tidak sadar
    menjadi sukarelawan dalam penyebaran hoaks. Sehingga perlu adanya upaya
    peningkatan literasi media bagi masyarakat, khususnya literasi digital.

    """
)


# Hoaks di Indonesia
st.subheader("Hoaks di Indonesia")

st.markdown(
    """
    Menurut Kamus besar Bahasa Indonesia (KBBI) hoax diartikan sebagai informasi
    bohong. Dijelaskan lebih lanjut oleh Diskominfo Bandung, hoaks yaitu informasi
    yang dibuat-buat atau direkayasa untuk menutupi informasi yang sebenarnya.
    Dengan kata lain, hoax diartikan sebagai upaya pemutarbalikan fakta menggunakan
    informasi yang seolah-olah meyakinkan akan tetapi tidak dapat diverifikasi kebenarannya.
    Berikut merupakan grafik trend jumlah hoaks yang tercatat oleh kominfo dan
    komunitas turnbackhoak pada tahun 2020-2021.
    """
)

combine = data_loader.get_combine()
cpd = (
    combine.groupby(["month", "order_month", "year"])["title"]
    .count()
    .reset_index()
    .rename(columns={"title": "total"})
    .sort_values(by=["order_month"])
)

fig, ax = plt.subplots(figsize=(10, 5))
palette = ["brown", "#38d655"]
lineplot = sns.lineplot(
    data=cpd,
    x="month",
    y="total",
    hue="year",
    markers=True,
    dashes=False,
    palette=palette,
)
ax.hlines(np.average(cpd.query("year == 2020").total), xmin=0, xmax=13, color='orange')
ax.hlines(np.average(cpd.query("year == 2021").total), xmin=0, xmax=13, color='green')

ax.annotate("avg: 287", (12, 292))
ax.annotate("avg: 160", (12, 165))

ax.set_title("Trend Jumlah Hoaks 2020-2021")
plt.xticks(rotation=30)

x_data = ax.get_lines()[0].get_xdata()
y_data = ax.get_lines()[0].get_ydata()

for x_value, y_value in zip(x_data, y_data):
            label = f"{y_value:.0f}"
            ax.annotate(label, (x_value, y_value))

x_data = ax.get_lines()[1].get_xdata()
y_data = ax.get_lines()[1].get_ydata()

for x_value, y_value in zip(x_data, y_data):
            label = f"{y_value:.0f}"
            ax.annotate(label, (x_value, y_value))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
frame = plt.gca()
frame.axes.get_yaxis().set_visible(False)
frame.grid(True)

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.pyplot(fig)
    st.markdown(
        """<div style='text-align: center'> Sumber data: kominfo dan turnbackhoax</div>""",
        unsafe_allow_html=True,
    )

st.write(
    """
    Berdasarkan grafik di atas, dapat dilihat bahwa trend jumlah hoaks mengalami
    penurunan. Pada tahun 2020 tercatat total 3.447 total hoaks dengan rata-
    rata 287 hoaks/bulan. Jumlah hoaks tertinggi terdapat pada bulan Maret
    dengan total 360 hoaks dan terendah terdapat pada bulan November dan Desember
    dengan total 193 hoaks. Pada tahun 2021 tercatat total 1.921 total hoaks
    dengan rata-rata 160 hoaks/bulan. Jumlah hoaks tertinggi terdapat pada bulan
    Januari dengan total 228 hoaks dan terendah terdapat pada bulan September
    dengan total 193 hoaks
    """
)

st.write(
    """
    Berdasarkan survey yang dilakukan oleh Tim Katadata, rincian penyebaran
    hoaks tersaji  dalam grafik berikut.
    """
)

# saluran penyebaran hoaks
col1, col2, = st.columns(2)

with col1:
    data = data_cleaner.get_penyebaran_hoaks()
    labels = data.sort_values("persentase", ascending=False).media.unique()

    fig, ax = plt.subplots(figsize=(10, 5))
    bar = sns.barplot(
        data=data.sort_values("persentase", ascending=False),
        x="media",
        y="persentase",
        hue="tahun",
        palette=["#f57c73", "#f2493d"],
    )

    plt.xticks(rotation=30)
    ax.set_xticklabels(labels, ha="right")
    ax.set_title("Saluran Penyebaran Hoaks")
    ax.set_ylim(0, 100)

    for b in ax.containers:
        ax.bar_label(b)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)

with col2:
    st.write(
    """
    Dari segi platform, dapat dilihat bahwa platform dengan persentase penyebaran
    hoaks tertinggi adalah facebook disusul dengan aplikasi whatsapp dan youtube.
    """
    )

st.write("")

# isi hoaks
col1, col2, = st.columns(2)

with col1:
    st.write(
    """
    Dilihat dari sudut pandang isi, konten politik sebagai isu yang paling banyak
    mengandung hoaks atau informasi keliru. Disusul oleh konten kesehatan dan
    agama.
    """
    )


with col2:
    data = data_cleaner.get_isi_hoaks()
    #labels = data.groupby(["topik", "tahun"])["persentase"].max().reset_index().topik.unique()

    fig, ax = plt.subplots(figsize=(12, 5))
    bar = sns.barplot(
        data=data.sort_values("persentase", ascending=False),
        x="topik",
        y="persentase",
        hue="tahun",
        palette=["#f78e60", "#eb5a1c"],
    )

    plt.xticks(rotation=30)
    #ax.set_xticklabels(labels, ha="right")
    ax.set_title("Ragam Konten Hoaks")
    ax.set_ylim(0, 100)

    for b in ax.containers:
        ax.bar_label(b)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)

st.markdown(
        """<div style='text-align: center'> Sumber data: katadata</div>""",
        unsafe_allow_html=True,
    )

# Literasi Digital di Indonesia
st.subheader("Literasi Digital di Indonesia")

st.write(
    """
    Berdasarkan Wikipedia, Literasi digital adalah pengetahuan dan kecakapan
    untuk menggunakan media digital, alat-alat komunikasi, atau jaringan dalam
    menemukan, mengevaluasi, menggunakan, membuat informasi, dan memanfaatkannya
    secara sehat, bijak, cerdas, cermat, tepat, dan patuh hukum sesuai dengan
    kegunaannya dalam rangka membina komunikasi dan interaksi dalam kehidupan
    sehari-hari. Pada intinya literasi digital merupakan **skill dan pengetahuan**
    untuk **menggunakan dan memanfaatkan** digital tools untuk mencapai suatu
    hal. Untuk mengukur tingkat digital literasi membutuhkan framework khusus
    yaitu indeks literasi digital. Indeks literasi digital memiliki rentang
    skor 0-5 dengan kategori baik (5-4), sedang (4-2) dan buruk (2-0).
    """
)

col1, col2 = st.columns(2)

with col1:
    lp20 = data_cleaner.get_literasi_prov20_clean()
    colors = sns.color_palette("Blues_r", n_colors=34)
    fig, ax = plt.subplots(figsize=(8, 10))
    bar = sns.barplot(
        data=lp20.sort_values("indeks_literasi_digital", ascending=False),
        x="indeks_literasi_digital",
        y="provinsi",
        palette=colors,
        alpha=0.9
    )

    ax.set_title("Indeks Literasi Digital di 34 Provinsi 2020")
    ax.set_ylim(35, -1)
    ax.bar_label(ax.containers[0], padding=1)

    ax.vlines(np.average(lp20.indeks_literasi_digital), ymin=-1, ymax=34, color='grey', linestyles='dashed')
    ax.annotate("indeks nasional: 3.46", (3.46, -1.5))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)


with col2:
    lp21 = data_cleaner.get_literasi_prov21_clean()
    colors = sns.color_palette("Greens_r", n_colors=34)
    fig, ax = plt.subplots(figsize=(8, 10))
    bar = sns.barplot(
        data=lp21.sort_values("indeks_literasi_digital", ascending=False),
        x="indeks_literasi_digital",
        y="provinsi",
        palette=colors,
        alpha=0.9
    )

    ax.set_title("Indeks Literasi Digital di 34 Provinsi 2021")
    ax.set_ylim(35, -1)
    ax.bar_label(ax.containers[0], padding=1)

    ax.vlines(np.average(lp21.indeks_literasi_digital), ymin=-1, ymax=34, color='grey', linestyles='dashed')
    ax.annotate("indeks nasional: 3.49", (3.46, -1.5))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)

st.markdown(
    """<div style='text-align: center'> Sumber data: katadata</div>""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.write(
    """
    Pada tahun 2020 skor Indeks Literasi Digital per provinsi ada di rentang 4,06
    hingga 3,11. Skor tertinggi dimiliki oleh Provinsi Sulawesi Tengah (4,06) dan
    skor terendah dimiliki oleh Provinsi Jawa Timur (3,17). Sementara itu,
    DKI Jakarta sebagai ibu kota negara memiliki skor Indeks Literasi Digital
    3,26 atau dibawah rata-rata nasional (3,46).
    """
    )

with col2:
    st.write(
    """
    Pada tahun 2021 skor Indeks Literasi Digital per provinsi ada di rentang 3,71
    hingga 3,18. Skor tertinggi dimiliki oleh Provinsi DI Yogyakarta (3,71) dan
    skor terendah dimiliki oleh Provinsi Maluku Utara (3,18). Sementara itu,
    DKI Jakarta sebagai ibu kota negara memiliki skor Indeks Literasi Digital
    3,51 atau sedikit diatas rata-rata nasional (3,49).
    """
    )


# Korelasi
st.subheader("Hoaks vs Literasi Digital")

st.write(
    """
    >*Secara statistik, korelasi antara jumlah hoaks dan skor literasi digital sebesar -1.*

    Dengan kata lain, hubungan antara hoaks dan literasi digital
    berbanding terbalik, dimana saat yang satu naik yang satunya lagi turun,
    begitu juga sebaliknya.
    """
)


# Penutup
st.subheader("Penutup")

st.write(
    """
        - Tingkat literasi digital di Indonesia belum bisa dikatakan tinggi.
        Mengacu pada skor indeks literasi digital yang hanya berada sedikit
        di atas 3 pada tahun 2020. Dan Hanya bertambah 0.03 poin di tahun 2021.
        Walaupun demikian trend penyebaran hoaks secara umum menurun dari awal tahun
        2020 sampai pertengahan 2021.
        - indeks literasi digital dan penyebaran hoaks berkorelasi sangat kuat secara negatif.


        """
)


# Daftar Pustaka
st.subheader("Daftar Pustaka")

st.markdown(
    """
    - Amrullah, Firda, Abdul Hakim Yassi, Gusnawaty Gusnawaty. 2020. [Modalitas Dalam Teks Berita Hoaks: Kajian Linguistik Sistemik Fungsional](https://journal.unhas.ac.id/index.php/jib/article/view/8831/4976). *Jurnal Ilmu Budaya*
    - Diskominfo Bandung. 2022. [*Pengertian Hoax dan Cara Menangkalnya*.](https://diskominfo.badungkab.go.id/artikel/42985-pengertian-hoax-dan-cara-menangkalnya#:~:text=Hoax%20merupakan%20informasi%2C%20kabar%2C%20berita,diartikan%20sebagai%20berita%20yang%20bohong)
    - Fauzan Jamaludin. 2017. [*Rendahnya literasi digital jadi penyebab penyebaran berita hoax*.](https://www.merdeka.com/teknologi/rendahnya-literasi-digital-jadi-penyebab-penyebaran-berita-hoax.html)
    - Kominfo. [*Informasi Publik Setiap Saat*.](https://eppid.kominfo.go.id/informasi_publik/Informasi%20Publik%20Setiap%20Saat)
    - Kontributor Wikipedia, [*Literasi digital*](https://id.wikipedia.org/w/index.php?title=Literasi_digital&oldid=21764697), Wikipedia, Ensiklopedia Bebas, (diakses pada Oktober 9, 2022).
    - Mastel. [*Hasil Survey Wabah HOAX Nasional 2019*](https://mastel.id/hasil-survey-wabah-hoax-nasional-2019/)
    - Vika Azkiya Dihni. 2022. [*Indeks Literasi Digital Indonesia Membaik pada 2021*.](https://databoks.katadata.co.id/datapublish/2022/07/13/indeks-literasi-digital-indonesia-membaik-pada-2021)
    """
)
