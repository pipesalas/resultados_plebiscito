import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import pandas as pd
import numpy as np
import descartes

def main():
    st.title('Exploración de resultados del plebiscito para una nueva constitución en Chile :balloon:')
    st.subheader('Para ello utilizaremos la base de datos generada por academiaespacial')
    texto('Ojo, sacaremos Isla de Pascua y Juan Fernandez para hacer mejor los mapitas', 14)
    texto(' ')
    
    
    df = cargamos_datos_consolidados()
    gdf = gpd.GeoDataFrame(df,geometry='geometry')
    
    
    st.markdown('**Seleccionamos una variable a mirar**')
    col1, col2 = st.beta_columns(2)
    with col1:
        columnas_posibles = {'Total votos apruebo': 'apruebo',
                             'Total votos rechazo': 'rechazo', 
                             'Total votos blancos': 'blancos',
                             'Total votos nulos': 'nulos',
                             'Porcentaje de votos apruebo': 'p_apruebo', 
                             'Porcentaje de votos rechazo': 'p_rechazo',
                             'Participación elecciones 2020': 'part_2020',
                             'Participación elecciones 2017' :'part_2017'}
        
        col_linda = st.selectbox('', list(columnas_posibles.keys()), index=4)
        col = columnas_posibles[col_linda]
    
    with st.beta_expander('Miramos el mapa nacional'):
        col1, col2 = st.beta_columns(2)
        with col1:
            plot_mapita(gdf, 'p_apruebo', 'Porcentaje de apruebo por comuna', regional=False)
        with col2:
            plot_mapita(gdf, 'dif_pct', 'Diferencia en % de participación c/r a 2017', regional=False)

        
    

    with st.beta_expander('Miramos una región en particular'):
        lista_regiones = gdf.region.unique()
        region_seleccionada = st.selectbox('Seleccionamos una región', lista_regiones, index=12)
        
        gdf_regional = gdf.query(f'region=="{region_seleccionada}"')
        provincias = list(gdf_regional.provincia.unique())
        provincia_seleccionada = st.selectbox('Seleccionamos una provincia', ['todas'] + provincias)
        if provincia_seleccionada == 'todas':

            plot_mapita(gdf_regional, 'p_apruebo', 'Porcentaje de apruebo por comuna', figsize=(10,20))
            plot_mapita(gdf_regional, 'dif_pct', 'Diferencia en % de participación c/r a 2017', figsize=(10,20))
                        
        else:
            gdf_provincial = gdf_regional.query(f'provincia=="{provincia_seleccionada}"')
            plot_mapita(gdf_provincial, 'p_apruebo', 'Porcentaje de apruebo por comuna', figsize=(10,20))
            plot_mapita(gdf_provincial, 'dif_pct', 'Diferencia en % de participación c/r a 2017', figsize=(10,20))

    

def plot_mapita(gdf : gpd.GeoDataFrame,
                col : str,
                title : str,
                figsize=(20,40),
                regional=True):
    fig, ax = plt.subplots(figsize=figsize)
    gdf.plot(column=col, ax=ax, cmap='RdBu')
    plt.title(title)
    if regional:
        gdf.apply(lambda x: ax.annotate(text=x.comuna +' '+ str(int(100*np.round(x[col],2))) + '%',
                                        xy=x.geometry.centroid.coords[0], 
                                        ha='center', 
                                        color='white')
                  ,axis=1);

    ax.set_axis_off()
    st.pyplot(fig)
    
    
    
    
@st.cache
def cargamos_datos_votacion():
    df = pd.read_csv('BBDD Plebiscito 2020 - CPE UDLA en base a SERVEL, 2020 - 2020.csv')
    df.rename(columns={col: col.lower() for col in df.columns}, inplace=True)
    for col in ['p_apruebo','p_rechazo', 'part_2017','part_2020']:
        df[col] = df[col].apply(lambda x: x.replace(',','.')).astype(float)
    for col in ['comuna']:
        df[col] = df[col].apply(lambda x: x.lower())
    return df

@st.cache
def cargamos_datos_comuna():
    gdf_comunas = gpd.read_file('./Comunas/comunas.shp')
    gdf_comunas.rename(columns= {'cod_comuna': 'cod_com'}, inplace=True)
    gdf_comunas.rename(columns={col: col.lower() for col in gdf_comunas.columns}, inplace=True)
    return gdf_comunas

@st.cache
def cargamos_datos_consolidados(sacamos_islas : int = True):
    df = cargamos_datos_votacion()
    gdf = cargamos_datos_comuna()
    df_consolidado = df.merge(gdf[['region', 'provincia', 'geometry','cod_com']], on=['cod_com'])
    
    if sacamos_islas:
        islas = ['juan fernandez', 'isla de pascua']
        df_consolidado = df_consolidado.query(f'comuna not in {islas}')
    df_consolidado['dif_pct'] = df_consolidado.eval("(part_2020 - part_2017)/part_2017")

    return df_consolidado

    
def texto(texto : str = 'holi',
          nfont : int = 16,
          color : str = 'black',
          line_height : float =None):
    

    st.markdown(
        body=generate_html(
            text=texto,
            color=color,
            font_size=f"{nfont}px",
            line_height=line_height
        ),
        unsafe_allow_html=True,
        )
    
COLOR_MAP = {"default": "#262730",
             "pink": "#E22A5B",
             "purple": "#985FFF",}
def generate_html(
    text,
    color=COLOR_MAP["default"],
    bold=False,
    font_family=None,
    font_size=None,
    line_height=None,
    tag="div",
):
    if bold:
        text = f"<strong>{text}</strong>"
    css_style = f"color:{color};"
    if font_family:
        css_style += f"font-family:{font_family};"
    if font_size:
        css_style += f"font-size:{font_size};"
    if line_height:
        css_style += f"line-height:{line_height};"

    return f"<{tag} style={css_style}>{text}</{tag}>"

    
main()