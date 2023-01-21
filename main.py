import calmap
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
import os
import pandas as pd
from PIL import Image
import requests
import streamlit as st


# ---Environment---
load_dotenv('.env')
API_KEY = os.environ.get("API_KEY") # Or write your API KEY directly
today = date.today()
yesterday = today - timedelta(days=1)
start_date = date(2022, 12, 1) # Put the date you started tracking
year = today.year


# ---Get Tracking Data---
params = {
    "start_date": start_date,
    "end_date": yesterday
}

data = requests.get('https://api.track.toggl.com/api/v9/me/time_entries',auth=(API_KEY, "api_token"), params=params)


# ---Choose which year to see---
st.title("朝活記録")
year_radio = st.radio("", ('今年', '1年前', '2年前'), horizontal=True)

if year_radio == '2年前':
    year -= 2
elif year_radio == '1年前':
    year -= 1
else:
    pass


# ---Data Processing---
df = pd.DataFrame.from_records(data.json())

df["start"] = pd.to_datetime(df["start"])
df["stop"] = pd.to_datetime(df["stop"])
df["start"] = df["start"] + timedelta(hours=9) # Adjust time difference
df["year"] = df["start"].dt.year
df["date"] = df["start"].astype(str).str[:10]
df["date"] = pd.to_datetime(df["date"])

df_year = df[(datetime(year, 1, 1) <= df["date"]) & (df["date"] <= datetime(year, 12, 31))]
df_group = df_year.groupby(["date", "project_id"], as_index=False).sum()


# Create with your tracking name and id. Here's my example.
training = df_group[df_group["project_id"] == 187670676.0][["date", "duration"]].rename(columns={"duration":"training"})
self_study = df_group[df_group["project_id"] == 187670689.0][["date", "duration"]].rename(columns={"duration":"self_study"})
english = df_group[df_group["project_id"] == 187670686.0][["date", "duration"]].rename(columns={"duration":"english"})
books = df_group[df_group["project_id"] == 187670687.0][["date", "duration"]].rename(columns={"duration":"books"})

data_total = pd.DataFrame()
data_total["date"] = pd.date_range(datetime(year, 1, 1), datetime(year, 12, 31))
data_total = pd.merge(data_total, training, on="date", how="left")
data_total = pd.merge(data_total, self_study, on="date", how="left")
data_total = pd.merge(data_total, english, on="date", how="left")
data_total = pd.merge(data_total, books, on="date", how="left")
data_total = data_total.set_index("date") # To use calmap, set date into index.


# ---Output---
st.markdown("## トレーニング")
st.write(calmap.yearplot(data_total["training"], year=year, linewidth=0.1, cmap="BuGn").figure)

st.markdown("## 読書・オーディオブック")
st.write(calmap.yearplot(data_total["books"], year=year, linewidth=0.1, cmap="BuGn").figure)

st.markdown("## 英語学習")
st.write(calmap.yearplot(data_total["english"], year=year, linewidth=0.1, cmap="BuGn").figure)

st.markdown("## プログラミング・その他")
st.write(calmap.yearplot(data_total["self_study"], year=year, linewidth=0.1, cmap="BuGn").figure)


# ---Extra; My profile in sidebar---
with st.sidebar:
    img = Image.open("ダウンロード (29)_0118044807.png")
    st.image(img, caption="作：Stable Diffusion", use_column_width=True)
    st.markdown("## 主な生息地")
    st.markdown("[Twitter](https://twitter.com/uwasanoaitsu910)", unsafe_allow_html=True)
    
    st.markdown("## 本棚")
    st.markdown("[ブクログ](https://booklog.jp/users/86fd751fa08e1d1a)", unsafe_allow_html=True)
    expander = st.expander("おすすめ本10冊（意識高め）")
    expander.markdown("[多様性の科学 画一的で凋落する組織、複数の視点で問題を解決する組織](https://amzn.to/3XGxCnG)")
    expander.markdown("[知ってるつもり 無知の科学](https://amzn.to/3iVCExW)")
    expander.markdown("[失敗の科学 失敗から学習する組織、学習出来ない組織](https://amzn.to/3QZpZqC)")
    expander.markdown("[代表的日本人](https://amzn.to/3HiHChQ)")
    expander.markdown("[HIGH OUTPUT MANAGEMENT](https://amzn.to/3iYSKa3)")
    expander.markdown("[PRINCIPLES 人生と仕事の原則](https://amzn.to/3GRcdBA)")
    expander.markdown("[リスクを取らないリスク](https://amzn.to/3GXE8jj)")
    expander.markdown("[人望が集まる人の考え方](https://amzn.to/3J6pRn8)")
    expander.markdown("[6ミニッツダイアリー 人生を変えるノート術](https://amzn.to/3wfwxrz)")
    expander.markdown("[脳を鍛えるには運動しかない！最新科学でわかった脳細胞の増やし方](https://amzn.to/3iS9Y95)")
    
    st.markdown("## 映画とか")
    st.markdown("[Filmarks](https://filmarks.com/users/uwasanoaitsu)", unsafe_allow_html=True)
    expander_movies = st.expander("好きな映画10作（かっこいいのがお好き）")
    expander_movies.markdown("[オデッセイ](https://filmarks.com/movies/59606?mark_id=124488725)")
    expander_movies.markdown("[アメイジング・スパイダーマン2](https://filmarks.com/movies/54983?mark_id=124488381)")
    expander_movies.markdown("[スパイダーマン：ノー・ウェイ・ホーム](https://filmarks.com/movies/86717?mark_id=130674288)")
    expander_movies.markdown("[グラン・トリノ](https://filmarks.com/movies/24424?mark_id=124487700)")
    expander_movies.markdown("[きっと、うまくいく](https://filmarks.com/movies/53954?mark_id=124487979)")
    expander_movies.markdown("[LEON](https://filmarks.com/movies/33501?mark_id=124487607)")
    expander_movies.markdown("[浅草キッド](https://filmarks.com/movies/94105?mark_id=124197771)")
    expander_movies.markdown("[エクストリーム・ジョブ](https://filmarks.com/movies/82544?mark_id=125624553)")
    expander_movies.markdown("[バーレスク](https://filmarks.com/movies/15130?mark_id=124488582)")
    expander_movies.markdown("[言の葉の庭](https://filmarks.com/movies/54374?mark_id=124489880)")