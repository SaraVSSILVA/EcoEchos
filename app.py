import streamlit as st
import pandas as pd
from datetime import datetime
import json
import random
from config.fatores_emissao import FATORES_EMISSAO
from config.dicas import DICAS_REDUCAO
from services.db_service import init_db, register_user, login_user, save_user_daily_data, load_user_monthly_data, load_user_daily_data
from util.calculos_util import (
    calcular_pegada_energia, calcular_pegada_transporte_individual_combustivel,
    calcular_pegada_transporte_eletrico, calcular_pegada_transporte_coletivo,
    calcular_pegada_alimentacao, calcular_pegada_habitacao,
    calcular_pegada_consumo, calcular_pegada_residuos,    calcular_pegada_estilo_vida, calcular_creditos_sustentaveis,
    calcular_pegada_completa
)
from util.exibicao_util import exibir_resumo_e_feedback_total, exibir_dicas_personalizadas, exibir_grafico_pegada_por_categoria

# --- CONFIGURAÇÃO STREAMLIT ---
st.set_page_config(
    page_title="EcoEchos: Sua Pegada Verde em Jogo!",
    page_icon="🌍",
    layout="centered"
)       

st.title("🎮 EcoEchos: O Eco das Suas Escolhas! 🌍🌱")
st.markdown("Bem-vindo(a)! Vamos calcular sua pegada de carbono pessoal e descobrir como 'upar de nível' na sustentabilidade. 😉")

init_db()

# --- GERENCIAMENTO DE SESSÃO DE USUÁRIO ---
if 'user' not in st.session_state:
    st.session_state.user = None 

# --- LOGIN/CADASTRO ---
if st.session_state.user is None:
    st.sidebar.subheader("🔐 Entrar / Cadastrar")
    login_tab, register_tab = st.sidebar.tabs(["Entrar", "Cadastrar"])

    with login_tab:
        username_login = st.text_input("Usuário:", key="username_login")
        password_login = st.text_input("Senha:", type="password", key="password_login")
        if st.button("Entrar", key="login_button"):
             user_data = login_user(username_login, password_login)
             if user_data:
                 st.session_state.user = user_data
                 st.rerun() 

    with register_tab:
        username_register = st.text_input("Novo Usuário:", key="username_register")
        password_register = st.text_input("Nova Senha:", type="password", key="password_register")
        password_confirm = st.text_input("Confirme a Senha:", type="password", key="password_confirm")
        if st.button("Cadastrar", key="register_button"):
            if password_register == password_confirm:
               register_user(username_register, password_register)
            else:
                st.error("As senhas não coincidem. Tente novamente.")
    
    st.info("👋 Bem-vindo(a) ao EcoEchos! Por favor, faça login ou cadastre-se na barra lateral para começar a calcular sua pegada de carbono.")
else:
# --- INTERFACE PARA USUÁRIO LOGADO ---
    st.sidebar.success(f"Logado como: {st.session_state.user['username']}")
    if st.sidebar.button("Sair"):
        st.session_state.user = None
        if 'inputs' in st.session_state:
            del st.session_state.inputs
        if 'last_calculated_pegada_total' in st.session_state:
            del st.session_state.last_calculated_pegada_total
        if 'last_calculated_pegadas_por_categoria' in st.session_state:
            del st.session_state.last_calculated_pegadas_por_categoria
        st.rerun()

    # --- Inicialização dos inputs no session_state para o usuário logado ---
    if 'inputs' not in st.session_state:
        st.session_state.inputs = {
            "consumo_energia_kwh": 150.0,
            "num_botijoes_gas_13kg": 0.5,
            "usa_carro_moto_combustivel": False,
            "distancia_carro_moto_combustivel": 200.0,
            "tipo_combustivel": "gasolina",
            "usa_veiculo_eletrico": False,
            "distancia_veiculo_eletrico": 0.0,
            "tipo_veiculo_eletrico": "carro_eletrico",
            "km_onibus": 50.0,
            "km_metro": 50.0,
            "km_aviao_domestico": 0.0,
            "km_aviao_internacional": 0.0,
            "kg_carne_bovina": 2.5,
            "kg_carne_suina": 1.0,
            "kg_frango": 3.0,
            "kg_peixe": 0.5,
            "litros_leite": 5.0,
            "kg_queijo": 0.8,
            "duzias_ovo": 2,
            "kg_arroz": 5.0,
            "kg_feijao": 2.0,
            "kg_vegetais": 10.0,
            "num_comodos": 5,
            "horas_ar_condicionado_dia": 2.0,
            "horas_aquecedor_dia": 0.0,
            "num_celulares": 0.0,
            "num_laptops": 0.0,
            "num_geladeiras": 0.0,
            "num_televisoes": 0.0,
            "num_veiculos_eletricos_consumo": 0.0,
            "num_roupas_peca": 5.0,
            "num_sacos_lixo_100l": 2.5,
            "kg_lixo_reciclavel": 5.0,
            "kg_eletronico": 0.2,
            "kg_compostagem": 3.0,
            "num_voos_eventos_ano": 0,
            "horas_streaming_dia": 2.0,
            "num_compras_online_mes": 4,
            "num_arvores_plantadas_mensal": 0.0,
            "kg_creditos_carbono": 0.0
        }

    # Inicializa as variáveis da pegada com valores padrão (0.0)
    pegada_total_kgco2e = st.session_state.get('last_calculated_pegada_total', 0.0)
    pegadas_por_categoria = st.session_state.get('last_calculated_pegadas_por_categoria', {
        "energia_combustivel": 0.0,
        "transporte": 0.0,
        "alimentacao": 0.0,
        "habitacao": 0.0,
        "consumo": 0.0,
        "residuos": 0.0,
        "estilo_vida": 0.0
    })

    today = datetime.today().date()
    selected_date = st.sidebar.date_input ("Selecione a data para registrar:", today)
    
    with st.sidebar:
        if st.button("💾 Salvar Dados do Dia"):
            if st.session_state.user and 'id' in st.session_state.user:
                save_user_daily_data(
                    st.session_state.user['id'],
                    str(selected_date),
                    st.session_state.get('last_calculated_pegada_total', 0.0),
                    st.session_state.inputs
                )
            else:
                st.error("Erro: Usuário não logado. Por favor, faça login novamente para salvar os dados.")

        if st.button("⬆️ Carregar Dados do Dia"):
            if st.session_state.user and 'id' in st.session_state.user:
                dados_carregados = load_user_daily_data(
                    st.session_state.user['id'],
                    str(selected_date)
                )
                if dados_carregados:
                    st.session_state.inputs = dados_carregados['input_data']
                    st.session_state['last_calculated_pegada_total'] = dados_carregados['pegada_total']
                    st.session_state['last_calculated_pegadas_por_categoria'] = calcular_pegada_completa(dados_carregados['input_data'])['pegadas_por_categoria']
                    # O gráfico só será atualizado após um novo clique em "Calcular",
                    st.rerun()
                else:
                    st.info(f"Nenhum dado encontrado para {selected_date}.")
            else:
                st.error("Erro: Usuário não logado. Por favor, faça login para carregar dados.")

        st.markdown("---")
        st.subheader("Visualizar Pegada Mensal")
        selected_month_year = st.text_input("Mês (YYYY-MM)", value=today.strftime('%Y-%m'))
        if st.button("Ver Pegada Mensal"):
            if st.session_state.user and 'id' in st.session_state.user:
                pegada_total_mensal = load_user_monthly_data(
                    st.session_state.user['id'],
                    selected_month_year
                )
                if pegada_total_mensal is not None and pegada_total_mensal > 0:
                    st.session_state['last_calculated_pegada_total'] = pegada_total_mensal
                    st.success(f"Pegada total do mês {selected_month_year}: {pegada_total_mensal:.2f} kgCO2e")
                    st.rerun() # Para atualizar a tela
                else:
                    st.info(f"Nenhum dado encontrado para o mês {selected_month_year}.")
            else:
                st.error("Erro: Usuário não logado. Por favor, faça login.")

    # --- Coleta de Dados do Usuário ---
    st.subheader("🎮 Sua Jornada Ecológica: Preencha as Etapas!")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "⚡ Energia/Combustível",
        "🚗 Transporte",
        "🍔 Alimentação",
        "🏠 Habitação",
        "🛍️ Consumo",
        "🗑️ Resíduos",
        "🧘‍♀️ Estilo de Vida",
        "🌳 Ações Sustentáveis"
    ])

    with tab1:
        st.markdown("### ⚡ Energia e Combustível (Casa)")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.inputs["consumo_energia_kwh"] = st.number_input(
                "Consumo de energia elétrica (kWh/mês):", min_value=0.0,
                value=st.session_state.inputs.get("consumo_energia_kwh", 150.0),
                key="consumo_energia_kwh_tab1",
                help="Média do seu consumo mensal de eletricidade."
            )
        with col2:
            st.session_state.inputs["num_botijoes_gas_13kg"] = st.number_input(
                "Quantos botijões de gás de cozinha (13kg) você usou no último mês? (ex: 0.5 para meio botijão):", min_value=0.0,
                value=st.session_state.inputs.get("num_botijoes_gas_13kg", 0.5),
                key="num_botijoes_gas_13kg_tab1",
                help="Quantidade de botijões de gás de 13kg."
            )

    with tab2:
        st.markdown("### 🚗 Transporte")

        st.session_state.inputs["usa_carro_moto_combustivel"] = st.checkbox(
            "Você usa carro ou moto a gasolina/etanol/diesel?",
            value=st.session_state.inputs.get("usa_carro_moto_combustivel", False),
            key="usa_carro_moto_combustivel_tab2"
        )
        if st.session_state.inputs["usa_carro_moto_combustivel"]:
            st.session_state.inputs["distancia_carro_moto_combustivel"] = st.number_input(
                "Quantos km você percorreu com VEÍCULO A COMBUSTÍVEL no último mês?:", min_value=0.0,
                value=st.session_state.inputs.get("distancia_carro_moto_combustivel", 200.0),
                key="distancia_carro_moto_combustivel_tab2"
            )
            opcoes_combustivel = ["gasolina", "etanol", "diesel"]
            default_index_combustivel = opcoes_combustivel.index(
                st.session_state.inputs.get("tipo_combustivel", "gasolina")
            ) if st.session_state.inputs.get("tipo_combustivel") in opcoes_combustivel else 0
            st.session_state.inputs["tipo_combustivel"] = st.radio(
                "Qual o PRINCIPAL COMBUSTÍVEL do seu veículo?",
                opcoes_combustivel,
                index=default_index_combustivel,
                key="tipo_combustivel_tab2"
            )

        st.session_state.inputs["usa_veiculo_eletrico"] = st.checkbox(
            "Você usa carro ou moto ELÉTRICA?",
            value=st.session_state.inputs.get("usa_veiculo_eletrico", False),
            key="usa_veiculo_eletrico_tab2"
        )
        if st.session_state.inputs["usa_veiculo_eletrico"]:
            opcoes_veiculo_eletrico = ["carro_eletrico", "moto_eletrica"]
            default_index_veiculo_eletrico = opcoes_veiculo_eletrico.index(
                st.session_state.inputs.get("tipo_veiculo_eletrico", "carro_eletrico")
            ) if st.session_state.inputs.get("tipo_veiculo_eletrico") in opcoes_veiculo_eletrico else 0

            st.session_state.inputs["tipo_veiculo_eletrico"] = st.radio(
                "Qual tipo de veículo elétrico?",
                opcoes_veiculo_eletrico,
                index=default_index_veiculo_eletrico,
                key="tipo_veiculo_eletrico_tab2"
            )
            st.session_state.inputs["distancia_veiculo_eletrico"] = st.number_input(
                f"Quantos km você percorreu de {st.session_state.inputs['tipo_veiculo_eletrico'].replace('_', ' ').upper()} no último mês?:", min_value=0.0,
                value=st.session_state.inputs.get("distancia_veiculo_eletrico", 0.0),
                key="distancia_veiculo_eletrico_tab2"
            )

        st.markdown("Km percorridos em transporte coletivo e avião:")
        st.session_state.inputs["km_onibus"] = st.number_input("ÔNIBUS (km/mês):", min_value=0.0, value=st.session_state.inputs.get("km_onibus", 50.0), key="km_onibus_tab2")
        st.session_state.inputs["km_metro"] = st.number_input("METRÔ (km/mês):", min_value=0.0, value=st.session_state.inputs.get("km_metro", 50.0), key="km_metro_tab2")
        st.session_state.inputs["km_aviao_domestico"] = st.number_input("Viagens DOMÉSTICAS de avião (km/mês estimado):", min_value=0.0, value=st.session_state.inputs.get("km_aviao_domestico", 0.0), key="km_aviao_domestico_tab2")
        st.session_state.inputs["km_aviao_internacional"] = st.number_input("Viagens INTERNACIONAIS de avião (km/mês estimado):", min_value=0.0, value=st.session_state.inputs.get("km_aviao_internacional", 0.0), key="km_aviao_internacional_tab2")

    with tab3:
        st.markdown("### 🍔 Alimentação")
        st.markdown("Consumo estimado por mês (kg):")
        st.session_state.inputs["kg_carne_bovina"] = st.number_input("Carne Bovina (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_carne_bovina", 2.5), key="kg_carne_bovina_tab3")
        st.session_state.inputs["kg_carne_suina"] = st.number_input("Carne Suína (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_carne_suina", 1.0), key="kg_carne_suina_tab3")
        st.session_state.inputs["kg_frango"] = st.number_input("Frango (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_frango", 3.0), key="kg_frango_tab3")
        st.session_state.inputs["kg_peixe"] = st.number_input("Peixe (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_peixe", 0.5), key="kg_peixe_tab3")
        st.session_state.inputs["litros_leite"] = st.number_input("Leite (litros/mês):", min_value=0.0, value=st.session_state.inputs.get("litros_leite", 5.0), key="litros_leite_tab3")
        st.session_state.inputs["kg_queijo"] = st.number_input("Queijo (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_queijo", 0.8), key="kg_queijo_tab3")
        st.session_state.inputs["duzias_ovo"] = st.number_input("Ovo (dúzias/mês):", min_value=0, value=st.session_state.inputs.get("duzias_ovo", 2), step=1, key="duzias_ovo_tab3")
        st.session_state.inputs["kg_arroz"] = st.number_input("Arroz (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_arroz", 5.0), key="kg_arroz_tab3")
        st.session_state.inputs["kg_feijao"] = st.number_input("Feijão (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_feijao", 2.0), key="kg_feijao_tab3")
        st.session_state.inputs["kg_vegetais"] = st.number_input("Vegetais/Frutas (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_vegetais", 10.0), key="kg_vegetais_tab3")

    with tab4:
        st.markdown("### 🏠 Habitação")
        st.session_state.inputs["num_comodos"] = st.number_input("Quantos cômodos (quartos, sala, cozinha, etc.) sua residência possui? (ex: 5):", min_value=1, value=st.session_state.inputs.get("num_comodos", 5), step=1, key="num_comodos_tab4")
        st.session_state.inputs["horas_ar_condicionado_dia"] = st.number_input("Horas de ar-condicionado por dia (média):", min_value=0.0, value=st.session_state.inputs.get("horas_ar_condicionado_dia", 2.0), key="horas_ar_condicionado_dia_tab4")
        st.session_state.inputs["horas_aquecedor_dia"] = st.number_input("Horas de aquecedor por dia (média):", min_value=0.0, value=st.session_state.inputs.get("horas_aquecedor_dia", 0.0), key="horas_aquecedor_dia_tab4")

    with tab5:
        st.markdown("### 🛍️ Consumo de Produtos")
        st.markdown("Média de produtos novos adquiridos por mês (0 para nenhum, 0.1 para 1 a cada 10 meses):")
        st.session_state.inputs["num_celulares"] = st.number_input("Celulares:", min_value=0.0, value=st.session_state.inputs.get("num_celulares", 0.0), key="num_celulares_tab5")
        st.session_state.inputs["num_laptops"] = st.number_input("Laptops:", min_value=0.0, value=st.session_state.inputs.get("num_laptops", 0.0), key="num_laptops_tab5")
        st.session_state.inputs["num_geladeiras"] = st.number_input("Geladeiras:", min_value=0.0, value=st.session_state.inputs.get("num_geladeiras", 0.0), key="num_geladeiras_tab5")
        st.session_state.inputs["num_televisoes"] = st.number_input("Televisões:", min_value=0.0, value=st.session_state.inputs.get("num_televisoes", 0.0), key="num_televisoes_tab5")
        st.session_state.inputs["num_veiculos_eletricos_consumo"] = st.number_input("Veículos elétricos:", min_value=0.0, value=st.session_state.inputs.get("num_veiculos_eletricos_consumo", 0.0), key="num_veiculos_eletricos_consumo_tab5")
        st.session_state.inputs["num_roupas_peca"] = st.number_input("Peças de Roupa:", min_value=0.0, value=st.session_state.inputs.get("num_roupas_peca", 5.0), key="num_roupas_peca_tab5")

    with tab6:
        st.markdown("### 🗑️ Resíduos")
        st.session_state.inputs["num_sacos_lixo_100l"] = st.number_input("Sacos de lixo de 100L descartados (unid./mês):", min_value=0.0, value=st.session_state.inputs.get("num_sacos_lixo_100l", 2.5), help="Ex: 2.5 para 2 sacos e meio", key="num_sacos_lixo_100l_tab6")
        st.session_state.inputs["kg_lixo_reciclavel"] = st.number_input("Lixo reciclável separado (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_lixo_reciclavel", 5.0), key="kg_lixo_reciclavel_tab6")
        st.session_state.inputs["kg_eletronico"] = st.number_input("Lixo eletrônico descartado (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_eletronico", 0.2), key="kg_eletronico_tab6")
        st.session_state.inputs["kg_compostagem"] = st.number_input("Material enviado para compostagem (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_compostagem", 3.0), key="kg_compostagem_tab6")

    with tab7:
        st.markdown("### 🧘‍♀️ Estilo de Vida")
        st.session_state.inputs["num_voos_eventos_ano"] = st.number_input("Voos (ou grandes eventos) que exigiram viagem no ÚLTIMO ANO:", min_value=0, value=st.session_state.inputs.get("num_voos_eventos_ano", 0), step=1, key="num_voos_eventos_ano_tab7")
        st.session_state.inputs["horas_streaming_dia"] = st.number_input("Horas de streaming de vídeo por dia (média):", min_value=0.0, value=st.session_state.inputs.get("horas_streaming_dia", 2.0), key="horas_streaming_dia_tab7")
        st.session_state.inputs["num_compras_online_mes"] = st.number_input("Compras online (número de pedidos/mês):", min_value=0, value=st.session_state.inputs.get("num_compras_online_mes", 4), step=1, key="num_compras_online_mes_tab7")

    with tab8:
        st.markdown("### 🌳 Ações Sustentáveis (Redução da Pegada)")
        st.session_state.inputs["num_arvores_plantadas_mensal"] = st.number_input("Árvores plantadas ou contribuiu para plantar no último mês:", min_value=0.0, value=st.session_state.inputs.get("num_arvores_plantadas_mensal", 0.0), key="num_arvores_plantadas_mensal_tab8")
        st.session_state.inputs["kg_creditos_carbono"] = st.number_input("Créditos de carbono adquiridos (kg/mês):", min_value=0.0, value=st.session_state.inputs.get("kg_creditos_carbono", 0.0), key="kg_creditos_carbono_tab8")

    # --- BOTÃO DE CÁLCULO E EXIBIÇÃO DE RESULTADOS ---
    st.markdown("---")
    if st.button("Calcular Minha Pegada Verde!"):
        pegada_energia = calcular_pegada_energia(
            st.session_state.inputs["consumo_energia_kwh"],
            st.session_state.inputs["num_botijoes_gas_13kg"]
        )

        total_transporte_combustivel = 0
        if st.session_state.inputs["usa_carro_moto_combustivel"]:
            total_transporte_combustivel = calcular_pegada_transporte_individual_combustivel(
                st.session_state.inputs["distancia_carro_moto_combustivel"],
                st.session_state.inputs["tipo_combustivel"]
            )

        total_transporte_eletrico = 0
        if st.session_state.inputs["usa_veiculo_eletrico"]:
            total_transporte_eletrico = calcular_pegada_transporte_eletrico(
                st.session_state.inputs["distancia_veiculo_eletrico"],
                st.session_state.inputs["tipo_veiculo_eletrico"]
            )

        total_transporte_coletivo = (
            calcular_pegada_transporte_coletivo(st.session_state.inputs["km_onibus"], "onibus") +
            calcular_pegada_transporte_coletivo(st.session_state.inputs["km_metro"], "metro") +
            calcular_pegada_transporte_coletivo(st.session_state.inputs["km_aviao_domestico"], "aviao_domestico") +
            calcular_pegada_transporte_coletivo(st.session_state.inputs["km_aviao_internacional"], "aviao_internacional")
        )
        pegada_transporte = total_transporte_combustivel + total_transporte_eletrico + total_transporte_coletivo

        pegada_alimentacao = calcular_pegada_alimentacao(
            st.session_state.inputs["kg_carne_bovina"], st.session_state.inputs["kg_carne_suina"], st.session_state.inputs["kg_frango"], st.session_state.inputs["kg_peixe"],
            st.session_state.inputs["litros_leite"], st.session_state.inputs["kg_queijo"], st.session_state.inputs["duzias_ovo"], st.session_state.inputs["kg_arroz"], st.session_state.inputs["kg_feijao"], st.session_state.inputs["kg_vegetais"]
        )

        horas_ar_condicionado_mensal = st.session_state.inputs["horas_ar_condicionado_dia"] * 30
        horas_aquecedor_mensal = st.session_state.inputs["horas_aquecedor_dia"] * 30
        pegada_habitacao = calcular_pegada_habitacao(st.session_state.inputs["num_comodos"], horas_ar_condicionado_mensal, horas_aquecedor_mensal)

        pegada_consumo = calcular_pegada_consumo(
            st.session_state.inputs["num_celulares"], st.session_state.inputs["num_laptops"], st.session_state.inputs["num_geladeiras"],
            st.session_state.inputs["num_televisoes"], st.session_state.inputs["num_veiculos_eletricos_consumo"], st.session_state.inputs["num_roupas_peca"]
        )

        pegada_residuos = calcular_pegada_residuos(st.session_state.inputs["num_sacos_lixo_100l"], st.session_state.inputs["kg_lixo_reciclavel"], st.session_state.inputs["kg_eletronico"], st.session_state.inputs["kg_compostagem"])

        horas_streaming_mensal = st.session_state.inputs["horas_streaming_dia"] * 30
        pegada_estilo_vida = calcular_pegada_estilo_vida(st.session_state.inputs["num_voos_eventos_ano"], horas_streaming_mensal, st.session_state.inputs["num_compras_online_mes"])

        creditos_sustentaveis = calcular_creditos_sustentaveis(st.session_state.inputs["num_arvores_plantadas_mensal"], st.session_state.inputs["kg_creditos_carbono"])

        pegada_total_kgco2e = (
            pegada_energia +
            pegada_transporte +
            pegada_alimentacao +
            pegada_habitacao +
            pegada_consumo +
            pegada_residuos +
            pegada_estilo_vida +
            creditos_sustentaveis
        )

        st.session_state.last_calculated_pegada_total = pegada_total_kgco2e

        pegadas_por_categoria = {
            "energia_combustivel": pegada_energia,
            "transporte": pegada_transporte,
            "alimentacao": pegada_alimentacao,
            "habitacao": pegada_habitacao,
            "consumo": pegada_consumo,
            "residuos": pegada_residuos,
            "estilo_vida": pegada_estilo_vida
        }
        st.session_state.last_calculated_pegadas_por_categoria = pegadas_por_categoria

        # --- EXIBIÇÃO DOS RESULTADOS (SÓ APARECE APÓS O CÁLCULO) ---
        exibir_resumo_e_feedback_total(pegada_total_kgco2e)
        exibir_grafico_pegada_por_categoria(pegadas_por_categoria)
        exibir_dicas_personalizadas(pegadas_por_categoria)

    # Exibir resultados persistidos (se houver), mesmo sem clicar em "Calcular" novamente
    elif st.session_state.get('last_calculated_pegada_total', 0.0) > 0:
        st.info("Resultados da última sessão carregados:")
        exibir_resumo_e_feedback_total(st.session_state['last_calculated_pegada_total'])
        if 'last_calculated_pegadas_por_categoria' in st.session_state:
            exibir_grafico_pegada_por_categoria(st.session_state['last_calculated_pegadas_por_categoria'])
            exibir_dicas_personalizadas(st.session_state['last_calculated_pegadas_por_categoria'])
