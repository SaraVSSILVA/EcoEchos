import streamlit as st
import pandas as pd
import plotly.express as px
import random

from config.dicas import DICAS_REDUCAO 

def exibir_resumo_e_feedback_total(pegada_total_kgco2e):
    st.markdown("---")
    st.header(f"SUA PEGADA DE CARBONO TOTAL MENSAL É: {pegada_total_kgco2e:.2f} kgCO2e")
    st.markdown("---")

    st.subheader("--- Análise da sua Pegada Criminal... digo, de Carbono ---")

    if pegada_total_kgco2e <= 150:
        st.success("🎉 Parabéns, seu pequeno elfo da floresta! Sua pegada é tão leve que mal deixou rastro. O planeta te agradece... por enquanto. Continue assim, ou a gente te manda para a reciclagem!")
    elif 150 < pegada_total_kgco2e <= 400:
        st.info("👍 Bom, pelo menos você tenta, né?. Nem um pé-grande, nem uma fada. Parece que você está tentando, mas ainda dá para apertar um pouco mais essa bota. O planeta está de olho em você!")
    elif 400 < pegada_total_kgco2e <= 800:
        st.warning("🧐 Olha só, achamos o Pé-Grande! Sua pegada já está deixando uma marca considerável. Talvez seja hora de trocar o carro por uma bicicleta... ou por um par de pernas. O aquecimento global manda lembranças!")
    elif 800 < pegada_total_kgco2e <= 1500:
        st.error("🚨  Alerta ambiental! Sua pegada tá tão colossal que o planeta pediu arrego. Será que você está pilotando um mamute ou só esquecendo de pensar antes de consumir? Se continuar assim, o Greenpeace vai te adicionar no grupo VIP deles.")
    else:
        st.error("🔥 PARABÉNS! Você deve ser um dos maiores contribuidores para o APOCALIPSE climático! Tem nem o que falar, vai plantar uma árvore, ou melhor, um bosque inteiro! O planeta está chorando... e você é o motivo.")

    st.markdown("_Lembre-se: cada quilo de CO2e conta. Ou não. Depende do quanto você se importa com o futuro... e com a ironia do destino._")
    st.markdown("_Obrigada por usar o EcoEchos. Agora vá e faça algo útil pelo planeta... ou não. A escolha é sua, meliante ambiental._")


def exibir_grafico_pegada_por_categoria(pegadas_por_categoria):
    st.subheader("📊 Visualização da Pegada de Carbono")

    df_pegada = pd.DataFrame(pegadas_por_categoria.items(), columns=["Categoria", "Pegada (kgCO2e)"])
    df_pegada["Categoria"] = df_pegada["Categoria"].map({
        "energia_combustivel": "Energia e Combustível",
        "transporte": "Transporte",
        "alimentacao": "Alimentação",
        "habitacao": "Habitação",
        "consumo": "Consumo de Produtos",
        "residuos": "Resíduos",
        "estilo_vida": "Estilo de Vida"
    })

    fig = px.bar(df_pegada,
                 x="Categoria",
                 y="Pegada (kgCO2e)",
                 title="Contribuição de Cada Categoria para sua Pegada de Carbono",
                 labels={"Pegada (kgCO2e)": "Pegada de Carbono (kgCO2e)"},
                 color="Pegada (kgCO2e)",
                 color_continuous_scale=px.colors.sequential.Greens_r)
    st.plotly_chart(fig, use_container_width=True)

def exibir_dicas_personalizadas(pegadas_por_categoria):
    st.subheader("\n--- O Oráculo do Carbono Revela: Onde Você Está Falhando Mais (e como remediar, talvez) ---")

    LIMIAR_PARA_DICAS = 50
    categorias_com_impacto = {
        cat: val for cat, val in pegadas_por_categoria.items() if val > LIMIAR_PARA_DICAS
    }

    if not categorias_com_impacto:
        st.info("Sua pegada é tão mínima que não consigo nem encontrar um 'maior impacto'. Ou você é um santo, ou mentiu em tudo. Sem dicas para você, prodígio ambiental!")
    else:
        top_categorias = sorted(categorias_com_impacto.items(), key=lambda item: item[1], reverse=True)

        num_dicas = min(len(top_categorias), 2)

        st.write("Pelas minhas contas (e minha paciência), suas maiores fontes de 'poluição gloriosa' são:")
        for i in range(num_dicas):
            categoria_nome_tecnico = top_categorias[i][0]
            pegada_valor = top_categorias[i][1]

            nome_amigavel = {
                "energia_combustivel": "ENERGIA E COMBUSTÍVEL EM CASA",
                "transporte": "TRANSPORTE",
                "alimentacao": "ALIMENTAÇÃO",
                "habitacao": "HABITAÇÃO",
                "consumo": "CONSUMO DE PRODUTOS",
                "residuos": "RESÍDUOS",
                "estilo_vida": "ESTILO DE VIDA"
            }.get(categoria_nome_tecnico, categoria_nome_tecnico.replace('_', ' ').upper())

            st.markdown(f"--- 🥉 **Sua Pegada em {nome_amigavel} ({pegada_valor:.2f} kgCO2e)** ---")

            dicas = DICAS_REDUCAO.get(categoria_nome_tecnico, ["Hmm, para essa categoria, a dica é... não faça mais isso!"])

            if len(dicas) > 0:
                dica1 = random.choice(dicas)
                st.write(f"Dica 1: {dica1}")
                if len(dicas) > 1:
                    dicas_restantes = [d for d in dicas if d != dica1]
                    if dicas_restantes:
                        st.write(f"Dica 2: {random.choice(dicas_restantes)}")
            else:
                st.write("Parece que até eu estou sem sarcasmo para te dar dicas aqui. Tente de novo, ou não. Pelo menos finja que se importa.")