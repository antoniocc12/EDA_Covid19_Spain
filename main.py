import streamlit as st
import utils.funciones as fc

# configurar página
fc.config_page()

st.title('Análisis Impacto COVID-19 en España')

# menu
menu = st.sidebar.selectbox('Datos COVID-19', ['Portada', 'Salud', 'Economía', 'Conclusiones'])

if menu == 'Portada':
    fc.home()

elif menu == 'Salud':
    fc.salud()

elif menu == 'Economía':
    fc.econom()

else:
    fc.conclusion()

