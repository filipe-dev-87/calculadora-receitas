# ---------------------------------------------
# 🧮 Calculadora de Preço de Receitas com Gráficos
# Streamlit + Plotly
# ---------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Calculadora de Receitas", page_icon="🍰", layout="centered")

st.title("🍰 Calculadora de Preço de Receitas")
st.write("Calcule o custo total, custo por porção e visualize a composição de custos por ingrediente.")

# -------------------------------
# Entrada de dados gerais
# -------------------------------
num_porcoes = st.number_input("Número de porções / fatias produzidas", min_value=1, value=6)
margem_lucro = st.number_input("Margem de lucro (%)", min_value=0.0, value=30.0, step=1.0)

st.markdown("---")

# -------------------------------
# Tabela de ingredientes dinâmica
# -------------------------------
st.subheader("🧾 Ingredientes da Receita")

ingredientes_exemplo = pd.DataFrame([
    {"Ingrediente": "Ovo", "Preço Pacote (R$)": 7.00, "Qtd. Pacote": 12, "Qtd. Usada": 1},
    {"Ingrediente": "Leite", "Preço Pacote (R$)": 3.50, "Qtd. Pacote": 1000, "Qtd. Usada": 190},
    {"Ingrediente": "Fubá", "Preço Pacote (R$)": 2.00, "Qtd. Pacote": 1000, "Qtd. Usada": 130},
    {"Ingrediente": "Açúcar", "Preço Pacote (R$)": 2.50, "Qtd. Pacote": 1000, "Qtd. Usada": 160},
    {"Ingrediente": "Óleo", "Preço Pacote (R$)": 6.00, "Qtd. Pacote": 900, "Qtd. Usada": 90},
    {"Ingrediente": "Farinha de trigo", "Preço Pacote (R$)": 3.60, "Qtd. Pacote": 1000, "Qtd. Usada": 96},
    {"Ingrediente": "Fermento", "Preço Pacote (R$)": 4.00, "Qtd. Pacote": 50, "Qtd. Usada": 15},
    {"Ingrediente": "Goiabada", "Preço Pacote (R$)": 2.99, "Qtd. Pacote": 300, "Qtd. Usada": 300},
    {"Ingrediente": "Erva-doce", "Preço Pacote (R$)": 15.00, "Qtd. Pacote": 1000, "Qtd. Usada": 10},
    {"Ingrediente": "Embalagem", "Preço Pacote (R$)": 6.80, "Qtd. Pacote": 3, "Qtd. Usada": 1}
])

ingredientes = st.data_editor(
    ingredientes_exemplo,
    num_rows="dynamic",
    use_container_width=True,
)

# -------------------------------
# Cálculo dos custos
# -------------------------------
if not ingredientes.empty:
    ingredientes["Custo (R$)"] = ingredientes["Preço Pacote (R$)"] * (ingredientes["Qtd. Usada"] / ingredientes["Qtd. Pacote"])
    custo_total = ingredientes["Custo (R$)"].sum()
    custo_unitario = custo_total / num_porcoes
    preco_venda_unitario = custo_unitario / (1 - margem_lucro / 100) if margem_lucro > 0 else custo_unitario

    st.markdown("### 💰 Resultado")
    col1, col2, col3 = st.columns(3)
    col1.metric("Custo total da receita", f"R$ {custo_total:.2f}")
    col2.metric("Custo por fatia/unidade", f"R$ {custo_unitario:.2f}")
    col3.metric(f"Preço de venda (lucro {margem_lucro:.0f}%)", f"R$ {preco_venda_unitario:.2f}")

    st.markdown("---")
    st.subheader("📊 Detalhamento dos custos por ingrediente")
    st.dataframe(ingredientes[["Ingrediente", "Custo (R$)"]], use_container_width=True)

    # -------------------------------
    # Gráfico de pizza
    # -------------------------------
    fig_pizza = px.pie(
        ingredientes,
        names="Ingrediente",
        values="Custo (R$)",
        title="Composição de custo por ingrediente",
        hover_data=["Custo (R$)"],
        labels={"Custo (R$)":"Custo (R$)"},
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

    # -------------------------------
    # Gráfico de barras
    # -------------------------------
    fig_bar = px.bar(
        ingredientes,
        x="Ingrediente",
        y="Custo (R$)",
        title="Custo de cada ingrediente",
        text="Custo (R$)",
        labels={"Custo (R$)":"Custo (R$)", "Ingrediente":"Ingrediente"}
    )
    fig_bar.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

    # -------------------------------
    # Download CSV
    # -------------------------------
    csv = ingredientes.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar planilha (CSV)", data=csv, file_name="custo_receita.csv", mime="text/csv")

else:
    st.warning("Adicione pelo menos um ingrediente para calcular o custo.")
