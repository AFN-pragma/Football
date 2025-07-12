import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image

# Configuration de la page
st.set_page_config(page_title="TKFIT Football Analytics", 
                   layout="wide")
# Appliquer les styles CSS personnalisés
st.markdown(
    """
    <style>
    /* Couleur de fond globale */
    .stApp {
        background-color: #000000;
        color: #;
    }
    
    /* Couleur de la sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffc107 !important;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Dashboard of TKFIT performance")
st.subheader("Real-time analysis of biomechanical and physiological data")

# Génération de données simulées
def generate_football_data():
    np.random.seed(42)
    start_time = datetime(2023, 11, 15, 15, 0, 0)
    timestamps = [start_time + timedelta(seconds=i*15) for i in range(360)]  # 90 min de données
    
    # Stadium center
    stadium_center_lat = 14.7140
    stadium_center_lon = -17.1850
    
    # Dimensions du terrain (105m x 68m) en degrés
    length_deg = 0.00095  # ~105m en degrés
    width_deg = 0.00060   # ~68m en degrés
    
    # Génération de trajectoire réaliste
    t = np.linspace(0, 10*np.pi, 360)
    x = 0.4 * length_deg * np.sin(t/3)
    y = 0.3 * width_deg * np.cos(t/2)
    
    # Ajout de variations aléatoires
    x += np.random.normal(0, 0.0001, 360)
    y += np.random.normal(0, 0.00007, 360)
    
    # Points chauds (zones d'activité intense)
    hot_spots = [
        {'lat': stadium_center_lat + 0.0003, 'lon': stadium_center_lon - 0.0003, 'intensity': 0.9},
        {'lat': stadium_center_lat - 0.0002, 'lon': stadium_center_lon + 0.0004, 'intensity': 0.7},
        {'lat': stadium_center_lat + 0.0001, 'lon': stadium_center_lon + 0.0001, 'intensity': 0.8}
    ]
    
    data = {
        "timestamp": timestamps,
        "heart_rate": np.clip(np.cumsum(np.random.normal(0, 2, 360)) + 80, 60, 200),
        "speed_kmh": np.abs(np.random.normal(0, 8, 360)),
        "acceleration": np.random.normal(0, 1.5, 360),
        "emg_quadriceps": np.abs(np.random.normal(0, 0.8, 360)),
        "emg_hamstring": np.abs(np.random.normal(0, 0.6, 360)),
        "player_load": np.cumsum(np.abs(np.random.normal(1, 0.3, 360))),
        "gps_lat": stadium_center_lat + y,
        "gps_lon": stadium_center_lon + x
    }
    
    # Ajout d'événements sportifs
    for i in [30, 100, 180, 250, 320]:
        data["speed_kmh"][i:i+5] = np.random.uniform(20, 28, 5)
        data["heart_rate"][i:i+5] = np.random.uniform(170, 195, 5)
        data["acceleration"][i:i+5] = np.random.uniform(3, 4.5, 5)
        data["emg_quadriceps"][i:i+5] = np.random.uniform(2.5, 3.5, 5)
    
    return pd.DataFrame(data), hot_spots

# Chargement des données
df, hot_spots = generate_football_data()

# Sidebar - Filtres
st.sidebar.image("TKFIT LOGO.jpg")
st.sidebar.header("Filtres d'analyse")
selected_period = st.sidebar.slider(
    "Période du match (min)",
    0, 90, (15, 75)
)

player_position = st.sidebar.selectbox(
    "Position", 
    ("Midfilder (Le Bach) ", "Forwarder", "Défender", "Goalkeeper")
)

# Métriques clés
st.header("Performance metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total distance", "10.8 km", "+1.2km vs moyenne")
col2.metric("Max speed", "27.3 km/h", "Record personnel")
col3.metric("Avg Heart rate", "132 bpm", "Zone 4 - Haute intensité")
col4.metric("Muscle load", "285 N·m/s", "+15% quadriceps")

# Visualisations
st.header("Temporary analysis")
tab1, tab2, tab3 = st.tabs(["Physiology", "Mouvement", "Muscle"])

with tab1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], 
                             y=df['heart_rate'], 
                             name="Fréquence cardiaque"))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['speed_kmh'], name="Vitesse", yaxis="y2"))
    
    fig.update_layout(
        title="Heart rate and speed",
        yaxis=dict(title="FC (bpm)"),
        yaxis2=dict(title="Speed (km/h)", overlaying="y", side="right"),
        xaxis_title="Temps"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.line(df, x='timestamp', y='acceleration', 
                 title="Accélération et décélération")
    fig.add_hline(y=2.0, line_dash="dash", line_color="red", 
                 annotation_text="Seuil d'intensité élevée")
    st.plotly_chart(fig, use_container_width=True)
    
    # Carte GPS avec terrain réaliste
    st.subheader(" GPS -  TKF⚡T Stadium")
    
    # Création du terrain de football
    fig = go.Figure()
    
    # Dimensions du terrain (105m x 68m)
    field_length = 105
    field_width = 68
    
    # Ajout du rectangle du terrain (vert)
    fig.add_shape(type="rect",
                 x0=-field_length/2, y0=-field_width/2,
                 x1=field_length/2, y1=field_width/2,
                 line=dict(color="white", width=2),
                 fillcolor="green", opacity=0.7)
    
    # Ligne médiane et cercle central
    fig.add_shape(type="line",
                  x0=0, y0=-field_width/2,
                  x1=0, y1=field_width/2,
                  line=dict(color="white", width=2, dash="dash"))
    
    fig.add_shape(type="circle",
                  x0=-9.15, y0=-9.15,
                  x1=9.15, y1=9.15,
                  line=dict(color="white", width=2))
    
    # Surfaces de réparation
    penalty_area_length = 16.5
    penalty_area_width = 40.3
    goal_area_length = 5.5
    goal_area_width = 18.32
    
    # Surface gauche
    fig.add_shape(type="rect",
                 x0=-field_length/2, y0=-penalty_area_width/2,
                 x1=-field_length/2 + penalty_area_length, y1=penalty_area_width/2,
                 line=dict(color="white", width=2))
    
    # Surface droite
    fig.add_shape(type="rect",
                 x0=field_length/2 - penalty_area_length, y0=-penalty_area_width/2,
                 x1=field_length/2, y1=penalty_area_width/2,
                 line=dict(color="white", width=2))
    
    # Buts
    fig.add_shape(type="rect",
                 x0=-field_length/2 - 2, y0=-3.66,
                 x1=-field_length/2, y1=3.66,
                 line=dict(color="white", width=2),
                 fillcolor="white", opacity=0.5)
    
    fig.add_shape(type="rect",
                 x0=field_length/2, y0=-3.66,
                 x1=field_length/2 + 2, y1=3.66,
                 line=dict(color="white", width=2),
                 fillcolor="white", opacity=0.5)
    
    # Points de penalty
    fig.add_trace(go.Scatter(x=[-field_length/2 + 11], y=[0], 
                            mode='markers', marker=dict(size=10, color='white')))
    fig.add_trace(go.Scatter(x=[field_length/2 - 11], y=[0], 
                            mode='markers', marker=dict(size=10, color='white')))
    
    # Conversion des coordonnées GPS en coordonnées terrain
    field_center_x, field_center_y = 0, 0
    scale_x = field_length / 0.00095
    scale_y = field_width / 0.00061
    
    # Trajectoire du joueur
    player_x = (df['gps_lon'] - df['gps_lon'].mean()) * scale_x
    player_y = (df['gps_lat'] - df['gps_lat'].mean()) * scale_y
    
    fig.add_trace(go.Scatter(x=player_x[::5], y=player_y[::5],
                             mode='lines+markers',
                             marker=dict(size=6, color='red'),
                             line=dict(width=2, color='red'),
                             name='Trajectoire joueur'))
    
    # Points chauds
    for spot in hot_spots:
        hot_x = (spot['lon'] - df['gps_lon'].mean()) * scale_x
        hot_y = (spot['lat'] - df['gps_lat'].mean()) * scale_y
        fig.add_trace(go.Scatter(x=[hot_x], y=[hot_y],
                                mode='markers',
                                marker=dict(
                                    size=20*spot['intensity'],
                                    color='orange',
                                    opacity=0.6
                                ),
                                name='Zone intense'))
    
    # Configuration finale
    fig.update_layout(
        title="TKF⚡T Stadium",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=600,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x", scaleratio=1),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df, x='timestamp', y=['emg_quadriceps', 'emg_hamstring'],
                     title="Muscle activity")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[df['emg_quadriceps'].mean(), df['emg_hamstring'].mean(), 0],
            theta=['Quadriceps', 'Ischios', ' '],
            fill='toself',
            name='Balance musculaire'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 3])),
            title="Équilibre musculaire",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

# Analyse des événements
st.header("Key events")
events = {
    "Sprint": {"time": "15:12", "speed": "26.1 km/h", "fc": 187, "emg": 2.78},
    "Tackle": {"time": "15:30", "accel": "3.8 m/s²", "impact": "8.5G"},
    "Strike": {"time": "15:50", "puissance": "540W", "vitesse balle": "112 km/h"}
}
     
for event, data in events.items():
    with st.expander(f"{event} à {data['time']}"):
        cols = st.columns(len(data))
        for i, (k, v) in enumerate(data.items()):
            if k != "time":
                cols[i].metric(k.replace('_', ' ').title(), v)

# Recommandations
st.header("Training recommendation")
rec_col1, rec_col2, rec_col3 = st.columns(3)
rec_col1.success("**Endurance cardiovasculaire**\n\n- 2x8 min à 90% FCmax\n- Récup 3 min entre")
rec_col2.warning("**Puissance musculaire**\n\n- 4x5 sprints de 20m\n- 45s récup entre sprints")
rec_col3.info("**Récupération**\n\n- Cryothérapie 3 min\n- Protéines: 30g post-match")

# Téléchargement des données
st.sidebar.header("Export des données")
if st.sidebar.button("Exporter rapport complet PDF"):
    st.sidebar.success("Rapport généré! [Télécharger](#)")

if st.sidebar.button("Télécharger données brutes CSV"):
    st.sidebar.success("Fichier prêt! [Télécharger](#)")

# Pied de page
st.caption("Données collectées par le système TKFIT |  2023 Sport Analytics")
