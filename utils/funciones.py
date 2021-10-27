# importar librerías
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import streamlit.components.v1 as components
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from plotly.offline import init_notebook_mode, iplot, plot
import sys, os
import utils.textos as tx

    

# configuración página
def config_page():
    st.set_page_config(
        page_title = 'COVID-19',
        layout = 'wide'
    )

    st.markdown("""
    <style>
    .big-font {
        font-size:25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# cache
st.cache(suppress_st_warning = True)

def cargar_datos(path):
    df = pd.read_csv(path)
    return df

def home():
    import sys
# insert at 1, 0 is the script path (or '' in REPL)

    img = Image.open ('data\covid.jpg')
    st.image(img, width=1300)

    with st.expander('PRIMER OBJETIVO'):
            st.write(tx.hip1)

    with st.expander('SEGUNDO OBJETIVO'):
            st.write(tx.hip2)
       

def salud():

    boton = st.sidebar.radio('Elija entre:', ('Defunciones', 'Vacunación' ))

    if boton == 'Defunciones':

        bt = st.sidebar.radio('Selecciona la variable a visualizar:', ('Sexo', 'Edad', 'Comunidad Autónoma'))

        if bt == 'Sexo':

            col1, col2 = st.columns(2)            
            with col1:
                img = Image.open('data\muertes_virus.png')
                st.image(img, use_column_width = 'auto')
            with col2:
                img = Image.open('data\muertes_virus2.png')
                st.image(img, use_column_width = 'auto')

            col1, col2 = st.columns(2)
            with col1:
                df = pd.read_csv('data\covid1.csv')
                st.write(df)
            with col2:                
                df = pd.read_csv('data\covid2.csv')
                st.write(df)

            with st.expander('INFLUENCIA EN EL NÚMERO DE MUERTES'):
                st.write(tx.influencia)

            bt_totales = st.checkbox('¿Desea ver la gráfica completa de defunciones en España?')

            if bt_totales: 
                file_html = open('data\defunciones.html', 'r')
                sc = file_html.read()
                components.html(sc, height = 500)

                with st.expander('1ª OLA 31 DE ENERO (S4/20) - 27 DE ABRIL (S16/20)'):
                    st.write(tx.primera_ola)

                with st.expander('2ª OLA 20 DE JULIO (S30/20) - 20 DE DICIEMBRE (S51/20)'):
                    st.write(tx.segunda_ola)
                
                with st.expander('3ª OLA PRINCIPIOS DE ENERO (S1/21) - FINALES DE FEBRERO (S8/21)'):
                    st.write(tx.tercera_ola)
            
            bt_acum = st.checkbox('¿Desea ver la gráfica de defunciones acumuladas?')

            if bt_acum:
                file_html = open('data\def_acum_sexo.html', 'r')
                sc = file_html.read()
                components.html(sc, height = 500)

        if bt == 'Edad':
            file_html = open('data\def_edades.html', 'r')
            sc = file_html.read()
            components.html(sc, height = 500)

            edades = pd.read_csv('data\edades.csv')

            col1, col2 = st.columns(2)
            with col1:
                tabla = edades.groupby('Edad', sort = False)['Total'].agg(['mean', 'max'])
                st.write(tabla)
            with col2:
                tasa = pd.read_csv('data\\tasa.csv')
                st.write(tasa)
                
            file_html = open('data\scatter_edades.html', 'r')
            sc = file_html.read()
            components.html(sc, height = 500)

        if bt == 'Comunidad Autónoma':

            file_html = open('data\def_com_temp.html', 'r')
            sc = file_html.read()
            components.html(sc, height = 500)

            with st.expander('MADRID'):
                st.write(tx.madrid)

            total = pd.read_csv('data\com_total.csv')
            array = np.arange(0, 1500000, 10000)
            num_min = array.min()
            num_max = array.max()
            intervalo = array
            filtro_def = st.sidebar.select_slider('Selecciona el intervalo de defunciones', intervalo, value = (num_min, num_max))
            intervalo, value = (num_min, num_max)
            mask1 = total['Total'] >= filtro_def[0]
            mask2 = total['Total'] <= filtro_def[1]
            total = total[mask1 & mask2]
            
            trace = go.Bar(
                x = total['Comunidades autónomas'],
                y = total['Total'],
                name = 'Muertes',
                marker = dict(color = 'rgba(0, 190, 0, 0.5)',
                                line = dict(color='rgb(0,0,0)', width = 1.5)),
                text = total['Comunidades autónomas'])
            data = [trace]

            layout = go.Layout(title = "Muertes por comunidad")

            fig2 = go.Figure(data = data, layout = layout)
            fig2.write_html('data\\bar_com.html')

            col1, col2 = st.columns(2)
            with col1:
                file_html2 = open('data\\bar_com.html', 'r')
                sc2 = file_html2.read()
                components.html(sc2, height = 500)

            with col2:
                st.map(total)      
    
    if boton == 'Vacunación':

        col1, col2 = st.columns(2)
        with col1:
            file_html = open('data\pie_vac.html', 'r')
            sc = file_html.read()
            components.html(sc, height = 700)
        
        with col2:
            st.markdown('##')
            st.markdown('##')
            st.markdown('##')
            st.markdown('##')
            st.markdown('##')
            st.markdown('##')
            st.markdown('##')
            st.markdown('<p class="big-font">' + tx.pfizer + '</p>', unsafe_allow_html=True)
            st.markdown('<p class="big-font">' + tx.moderna + '</p>', unsafe_allow_html=True)
            st.markdown('<p class="big-font">' + tx.astra + '</p>', unsafe_allow_html=True)
            st.markdown('<p class="big-font">' + tx.janssen + '</p>', unsafe_allow_html=True)

        img = Image.open('data\VacunasComunidad.jpg')
        st.image(img, use_column_width = 'auto')

        dosis1 = st.sidebar.checkbox('¿Quieres ver los datos de la 1ª dosis?')
        if dosis1:
            img = Image.open('data\\1Dosis-Com.jpg')
            st.image(img, use_column_width = 'auto')

        dosis2 = st.sidebar.checkbox('¿Quieres ver los datos de la 2ª dosis?')
        if dosis2:
            img = Image.open('data\PautaCompleta-Com.jpg')
            st.image(img, use_column_width = 'auto')

def econom():

    bt = st.sidebar.radio('Selecciona a visualizar:', ('Variables generales', 'Turismo', 'Hostelería'))

    if bt == 'Variables generales':

        file_html = open('data\pib.html', 'r')
        sc = file_html.read()
        components.html(sc, height = 500)

        with st.expander('PIB'):
                st.write(tx.pib)

        file_html = open('data\paro.html', 'r')
        sc = file_html.read()
        components.html(sc, height = 500)

        with st.expander('PARO'):
            st.write(tx.paro)

        file_html = open('data\erte.html', 'r')
        sc = file_html.read()
        components.html(sc, height = 500)

        with st.expander('ERTE'):
            st.write(tx.erte)

    if bt == 'Turismo':

        file_html = open('data\\turistas.html', 'r')
        sc = file_html.read()
        components.html(sc, height = 500)

        with st.expander('TURSIMO'):
            st.write(tx.turismo)

        file_html = open('data\gasto_turistas.html', 'r')
        sc = file_html.read()
        components.html(sc, height = 500)

        with st.expander('GASTO'):
            st.write(tx.gasto_turismo)

    if bt == 'Hostelería':

        img = Image.open('data\Pernoctaciones-por-Fecha.jpg')
        st.image(img, use_column_width = 'auto')

        with st.expander('PERNOCTACIONES'):
            st.write(tx.pernoctaciones)

        file_html = open('data\\var_fact.html', 'r')
        sc = file_html.read()
        components.html(sc, height = 500)

        with st.expander('VARIACIÓN DE FACTURACIÓN'):
            st.write(tx.facturacion)

        file_html = open('data\des_emp_com.html', 'r')
        sc = file_html.read()
        components.html(sc, height = 500)

        with st.expander('DESTRUCCIÓN EMPRESAS'):
            st.write(tx.empresas)

def conclusion():
    st.markdown('##')
    st.markdown('<p class="big-font">CONCLUSIONES</p>', unsafe_allow_html=True)
    with st.expander('Según Sexo:'):
        st.write(tx.con3)
    with st.expander('Según Edad:'):
        st.write(tx.con1)
    with st.expander('Según Comunidad:'):
        st.write(tx.con2)
    with st.expander('Distribución Vacunación:'):
        st.write(tx.con4)
    with st.expander('Según Variables Económicas:'):
        st.write(tx.con5)



