import streamlit as st
import random
import pandas as pd
import plotly.express as px

# --- FATORES DE EMISSÃO ---
FATORES_EMISSAO = {
    "energia_combustivel": {
        "eletricidade_kWh": 0.065,
        "gas_cozinha_13kg": 3.02,
        "gasolina_litro": 2.32,
        "etanol_litro": 0.55,
        "diesel_litro": 2.68,
    },
    "transporte": {
        "carro_eletrico_km": 0.06,
        "moto_km": 0.09,
        "onibus_km": 0.11,
        "metro_km": 0.035,
        "aviao_domestico_km": 0.14,
        "aviao_internacional_km": 0.19
    },
    "alimentacao": {
        "carne_bovina_kg": 26.5,
        "carne_suina_kg": 7.0,
        "frango_kg": 9.5,
        "peixe_kg": 4.8,
        "leite_litro": 1.1,
        "queijo_kg": 13.0,
        "ovo_duzia": 1.5,
        "arroz_kg": 1.8,
        "feijao_kg": 1.1,
        "vegetais_kg": 0.85
    },
    "habitacao": {
        "residencia_comodo": 15.0,
        "ar_condicionado_hora": 1.3,
        "aquecedor_hora": 1.9
    },
    "consumo": {
        "celular": 75.0,
        "laptop": 390.0,
        "geladeira": 2900.0,
        "televisao": 950.0,
        "veiculo_eletrico": 1900.0,
        "roupas_peca": 7.5
    },
    "residuos": {
        "lixo_comum_saco_100l": 5.0,
        "lixo_reciclavel_kg": 0.6,
        "eletronico_kg": 2.4,
        "compostagem_kg": -0.2
    },
    "estilo_vida": {
        "voos_eventos_ano": 480.0,
        "streaming_hora": 0.4,
        "compras_online_mes": 3.8
    },
    "sustentavel": {
        "arvores_plantadas": -21.0,
        "creditos_carbono_kg": -1.0,
    }
}

# --- DICAS DE REDUÇÃO ---
DICAS_REDUCAO = {
    "energia_combustivel": [
        "Desligue as luzes, meliante! Não estamos iluminando um estádio. Ou você gosta de pagar caro e poluir?",
        "Banho rápido, por favor. A água quente não nasce em árvores... nem a energia para aquecê-la. E economiza na conta!",
        "Tire os aparelhos da tomada. Eles sugam energia mesmo desligados, tipo um vampiro ecológico. Ah, e a sua carteira também.",
        "Troque lâmpadas antigas por LED. Elas brilham mais e poluem menos. Quem diria que ser 'brilhante' também é ser verde?",
        "Use a luz do sol, seu morcego! Abra as cortinas e janelas. É de graça e ainda te ajuda a pegar um bronzeado (se o sol cooperar)."
    ],
    "transporte": [
        "Caminhe, pedale, use o transporte público. Suas pernas e o planeta agradecem. E talvez você perca aqueles quilinhos extras.",
        "Combine caronas. Um carro, vários criminosos ambientais (digo, cidadãos). Menos carros na rua, menos drama no ar.",
        "Pense duas vezes antes de voar. Cada voo é um 'adeus' para a camada de ozônio. A não ser que você seja um super-herói com capa de CO2.",
        "Se tiver um carro a combustão, dirija como um anjo (do inferno, claro). Acelerar demais e frear bruscamente gasta mais combustível... e sua paciência.",
        "Considere um veículo elétrico, mas não um tanque de guerra elétrico, ok? O planeta agradece o silêncio e a 'quase' zero emissão."
    ],
    "alimentacao": [
        "Menos carne vermelha, mais vegetais. Seu corpo e o planeta vão gostar. E talvez você descubra que brócolis não é tão ruim.",
        "Compre de produtores locais (até da lojinha daquele zé ruela que ninguem gosta). Menos transporte, menos CO2. E você ainda pode pechinchar com o fazendeiro.",
        "Evite o desperdício de alimentos. Aquela comida no lixo vira metano, um gás ainda pior que o CO2. Não seja um vilão dos restos!",
        "Coma menos ultraprocessados. Além de serem ruins para sua saúde, a produção deles é um pesadelo ambiental. Prefira algo que pareça comida de verdade.",
        "Explore a culinária vegetariana. Quem sabe você não descobre um novo superpoder culinário... e salva o planeta no processo."
    ],
    "habitacao": [
        "Isole sua casa. Menos energia para aquecer ou resfriar. Você economiza na conta e o planeta não pega um resfriado (ou um calorão).",
        "Ajuste a temperatura do ar condicionado. Cada grau a mais (no verão) ou a menos (no inverno) é uma tragédia para o seu bolso e para a atmosfera.",
        "Desligue o ar condicionado quando sair. Ele não precisa de uma festa particular de vento gelado enquanto você está fora, né?",
        "Aproveite a ventilação natural. Abra as janelas, sinta a brisa. É de graça e ecologicamente correto. Choque!",
        "Conserte vazamentos. Aquela torneira pingando não é só um incômodo, é um desperdício de água e energia. A Mãe Natureza está te observando."
    ],
    "consumo": [
        "Compre menos, use mais. Sua carteira e o planeta imploram. Você realmente precisa de mais um gadget que vai virar lixo em 6 meses?",
        "Repare antes de descartar. Seu sapato furado pode ter uma segunda chance. Não jogue fora, conserte! Seja um herói da remenda.",
        "Prefira produtos duráveis e de segunda mão. O vintage está na moda e é bom para o planeta. Seu avô já sabia disso.",
        "Pense no ciclo de vida do produto. De onde veio? Como foi feito? Para onde vai? Se for para o lixo em um mês, repense.",
        "Evite embalagens desnecessárias. Aquela sacola plástica extra é só mais um item para o aterro. O planeta não precisa de mais lixo, mas de mais consciência."
    ],
    "residuos": [
        "Recicle, por favor! Não é um bicho de sete cabeças. Separe seu lixo e ajude o mundo a não virar uma lixeira gigante.",
        "Composte seu lixo orgânico. Comida velha virando adubo? Sim, é mágica! E o chorume fica só no seu jardim, não nos rios.",
        "Reduza o lixo que você gera. Leve sua própria sacola, recuse canudos, compre a granel. Seja um ninja da redução de lixo.",
        "Descarte eletrônicos corretamente. Eles têm substâncias tóxicas que o planeta não quer engolir. Ache um ponto de coleta, não a lata de lixo comum!",
        "Reutilize. Aquela garrafa pode virar um vaso, o pote de sorvete um porta-treco. Sua criatividade é a única fronteira para o lixo."
    ],
    "estilo_vida": [
        "Reduza seu tempo de tela. Menos streaming, menos energia consumida pelos data centers. Vá ler um livro, a natureza lá fora te espera.",
        "Prefira lazer ao ar livre. Caminhadas, piqueniques, observar pássaros. É divertido, saudável e não emite carbono. Quase um crime ambiental ao contrário!",
        "Pense nas suas compras online. Cada entrega individual é um caminhão rodando. Junte suas compras, ou compre na loja física. Seja mais esperto que o algoritmo.",
        "Desconecte-se de eventos que exigem muitas viagens. Nem toda conferência precisa da sua presença física. Seja um fantasma do carbono.",
        "Considere um hobby mais 'verde'. Jardinagem, costura, marcenaria. Menos consumo de coisas prontas, mais criação e menos pegada."
    ]
}

# --- FUNÇÕES DE CÁLCULO ---
def calcular_pegada_energia(consumo_kwh, num_botijoes_gas_13kg):
    pegada = 0
    pegada += consumo_kwh * FATORES_EMISSAO["energia_combustivel"]["eletricidade_kWh"]
    pegada += num_botijoes_gas_13kg * FATORES_EMISSAO["energia_combustivel"]["gas_cozinha_13kg"]
    return pegada

def calcular_pegada_transporte_individual_combustivel(distancia_km, tipo_combustivel):
    litros_consumidos = 0
    if tipo_combustivel == "gasolina":
        litros_consumidos = distancia_km / 10.0 # Assumindo 10km/L para gasolina
        return litros_consumidos * FATORES_EMISSAO["energia_combustivel"]["gasolina_litro"]
    elif tipo_combustivel == "etanol":
        litros_consumidos = distancia_km / 7.0 # Assumindo 7km/L para etanol
        return litros_consumidos * FATORES_EMISSAO["energia_combustivel"]["etanol_litro"]
    elif tipo_combustivel == "diesel":
        litros_consumidos = distancia_km / 12.0 # Assumindo 12km/L para diesel
        return litros_consumidos * FATORES_EMISSAO["energia_combustivel"]["diesel_litro"]
    else:
        return 0

def calcular_pegada_transporte_eletrico(distancia_km, tipo_veiculo):
    if tipo_veiculo == "carro_eletrico":
        return distancia_km * FATORES_EMISSAO["transporte"]["carro_eletrico_km"]
    elif tipo_veiculo == "moto_eletrica": 
        return distancia_km * FATORES_EMISSAO["transporte"]["moto_km"] 
    else:
        return 0

def calcular_pegada_transporte_coletivo(distancia_km, tipo_transporte):
    if tipo_transporte == "onibus":
        return distancia_km * FATORES_EMISSAO["transporte"]["onibus_km"]
    elif tipo_transporte == "metro":
        return distancia_km * FATORES_EMISSAO["transporte"]["metro_km"]
    elif tipo_transporte == "aviao_domestico":
        return distancia_km * FATORES_EMISSAO["transporte"]["aviao_domestico_km"]
    elif tipo_transporte == "aviao_internacional":
        return distancia_km * FATORES_EMISSAO["transporte"]["aviao_internacional_km"]
    else:
        return 0

def calcular_pegada_alimentacao(
    kg_carne_bovina, kg_carne_suina, kg_frango, kg_peixe,
    litros_leite, kg_queijo, duzias_ovo, kg_arroz, kg_feijao, kg_vegetais
):
    total = 0
    total += kg_carne_bovina * FATORES_EMISSAO["alimentacao"]["carne_bovina_kg"]
    total += kg_carne_suina * FATORES_EMISSAO["alimentacao"]["carne_suina_kg"]
    total += kg_frango * FATORES_EMISSAO["alimentacao"]["frango_kg"]
    total += kg_peixe * FATORES_EMISSAO["alimentacao"]["peixe_kg"]
    total += litros_leite * FATORES_EMISSAO["alimentacao"]["leite_litro"]
    total += kg_queijo * FATORES_EMISSAO["alimentacao"]["queijo_kg"]
    total += duzias_ovo * FATORES_EMISSAO["alimentacao"]["ovo_duzia"]
    total += kg_arroz * FATORES_EMISSAO["alimentacao"]["arroz_kg"]
    total += kg_feijao * FATORES_EMISSAO["alimentacao"]["feijao_kg"]
    total += kg_vegetais * FATORES_EMISSAO["alimentacao"]["vegetais_kg"]
    return total

def calcular_pegada_habitacao(num_comodos, horas_ar_condicionado_mensal, horas_aquecedor_mensal):
    total = 0
    total += num_comodos * FATORES_EMISSAO["habitacao"]["residencia_comodo"]
    total += horas_ar_condicionado_mensal * FATORES_EMISSAO["habitacao"]["ar_condicionado_hora"]
    total += horas_aquecedor_mensal * FATORES_EMISSAO["habitacao"]["aquecedor_hora"]
    return total

def calcular_pegada_consumo(
    num_celulares,
    num_laptops,
    num_geladeiras,
    num_televisoes,
    num_veiculos_eletricos,
    num_roupas_peca
):
    total = 0
    total += num_celulares * FATORES_EMISSAO["consumo"]["celular"]
    total += num_laptops * FATORES_EMISSAO["consumo"]["laptop"]
    total += num_geladeiras * FATORES_EMISSAO["consumo"]["geladeira"]
    total += num_televisoes * FATORES_EMISSAO["consumo"]["televisao"]
    total += num_veiculos_eletricos * FATORES_EMISSAO["consumo"]["veiculo_eletrico"]
    total += num_roupas_peca * FATORES_EMISSAO["consumo"]["roupas_peca"]
    return total

def calcular_pegada_residuos(num_sacos_lixo_100l, kg_lixo_reciclavel, kg_eletronico, kg_compostagem):
    total = 0
    total += num_sacos_lixo_100l * FATORES_EMISSAO["residuos"]["lixo_comum_saco_100l"]
    total += kg_lixo_reciclavel * FATORES_EMISSAO["residuos"]["lixo_reciclavel_kg"]
    total += kg_eletronico * FATORES_EMISSAO["residuos"]["eletronico_kg"]
    total += kg_compostagem * FATORES_EMISSAO["residuos"]["compostagem_kg"]
    return total

def calcular_pegada_estilo_vida(num_voos_eventos_ano, horas_streaming_mensal, num_compras_online_mes):
    total = 0
    total += (num_voos_eventos_ano / 12) * FATORES_EMISSAO["estilo_vida"]["voos_eventos_ano"] 
    total += horas_streaming_mensal * FATORES_EMISSAO["estilo_vida"]["streaming_hora"]
    total += num_compras_online_mes * FATORES_EMISSAO["estilo_vida"]["compras_online_mes"]
    return total

def calcular_creditos_sustentaveis(num_arvores_plantadas_mensal, kg_creditos_carbono): 
    total = 0
    total += num_arvores_plantadas_mensal * FATORES_EMISSAO["sustentavel"]["arvores_plantadas"]
    total += kg_creditos_carbono * FATORES_EMISSAO["sustentavel"]["creditos_carbono_kg"]
    return total

# --- FUNÇÕES DE FEEDBACK ---
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


def exibir_dicas_personalizadas(pegadas_por_categoria):
    st.subheader("\n--- O Oráculo do Carbono Revela: Onde Você Está Falhando Mais (e como remediar, talvez) ---")

    LIMIAR_PARA_DICAS = 50  # Limite para considerar uma categoria como "significativa"
    categorias_com_impacto = {
        cat: val for cat, val in pegadas_por_categoria.items() if val > LIMIAR_PARA_DICAS
    }

    if not categorias_com_impacto:
        st.info("Sua pegada é tão mínima que não consigo nem encontrar um 'maior impacto'. Ou você é um santo, ou mentiu em tudo. Sem dicas para você, prodígio ambiental!")
    else:
        top_categorias = sorted(categorias_com_impacto.items(), key=lambda item: item[1], reverse=True)

        num_dicas = min(len(top_categorias), 2) # Exibir até 2 categorias de maior impacto

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


# --- LÓGICA PRINCIPAL DO APLICATIVO STREAMLIT ---
st.set_page_config(
    page_title="EcoEchos: Sua Pegada Verde em Jogo!",
    page_icon="🌍",
    layout="centered"
)       

st.title("🎮 EcoEchos: O Eco das Suas Escolhas! 🌍🌱")
st.markdown("Bem-vindo(a)! Vamos calcular sua pegada de carbono pessoal e descobrir como 'upar de nível' na sustentabilidade. 😉")

st.subheader("Informe seus hábitos (valores mensais ou conforme solicitado):")

# --- 1. Perguntas sobre Energia e Combustível (Casa) ---
st.header("⚡ Energia e Combustível (Casa)")
consumo_energia_kwh = st.number_input("Consumo de energia elétrica (kWh/mês):", min_value=0.0, value=150.0, help="Média do seu consumo mensal de eletricidade.")
num_botijoes_gas_13kg = st.number_input("Quantos botijões de gás de cozinha (13kg) você usou no último mês? (ex: 0.5 para meio botijão):", min_value=0.0, value=0.5, help="Quantidade de botijões de gás de 13kg.")


# --- 2. Perguntas sobre Transporte ---
st.header("🚗 Transporte")

# Carro/Moto a Combustível
usa_carro_moto_combustivel = st.checkbox("Você usa carro ou moto a gasolina/etanol/diesel?")
distancia_carro_moto_combustivel = 0.0
tipo_combustivel = "Nenhum"
if usa_carro_moto_combustivel:
    distancia_carro_moto_combustivel = st.number_input("Quantos km você percorreu com VEÍCULO A COMBUSTÍVEL no último mês?:", min_value=0.0, value=200.0)
    tipo_combustivel = st.radio("Qual o PRINCIPAL COMBUSTÍVEL do seu veículo?", ["gasolina", "etanol", "diesel"], index=0)

# Carro/Moto Elétrico
usa_veiculo_eletrico = st.checkbox("Você usa carro ou moto ELÉTRICA?")
distancia_veiculo_eletrico = 0.0
tipo_veiculo_eletrico = "Nenhum"
if usa_veiculo_eletrico:
    tipo_veiculo_eletrico = st.radio("Qual tipo de veículo elétrico?", ["carro_eletrico", "moto_eletrica"], index=0)
    distancia_veiculo_eletrico = st.number_input(f"Quantos km você percorreu de {tipo_veiculo_eletrico.replace('_', ' ').upper()} no último mês?:", min_value=0.0, value=0.0)

# Transporte Coletivo e Avião
st.markdown("Km percorridos em transporte coletivo e avião:")
km_onibus = st.number_input("ÔNIBUS (km/mês):", min_value=0.0, value=50.0)
km_metro = st.number_input("METRÔ (km/mês):", min_value=0.0, value=50.0)
km_aviao_domestico = st.number_input("Viagens DOMÉSTICAS de avião (km/mês estimado):", min_value=0.0, value=0.0)
km_aviao_internacional = st.number_input("Viagens INTERNACIONAIS de avião (km/mês estimado):", min_value=0.0, value=0.0)


# --- 3. Perguntas sobre Alimentação ---
st.header("🍔 Alimentação")
st.markdown("Consumo estimado por mês (kg):")
kg_carne_bovina = st.number_input("Carne Bovina (kg/mês):", min_value=0.0, value=2.5)
kg_carne_suina = st.number_input("Carne Suína (kg/mês):", min_value=0.0, value=1.0)
kg_frango = st.number_input("Frango (kg/mês):", min_value=0.0, value=3.0)
kg_peixe = st.number_input("Peixe (kg/mês):", min_value=0.0, value=0.5)
litros_leite = st.number_input("Leite (litros/mês):", min_value=0.0, value=5.0)
kg_queijo = st.number_input("Queijo (kg/mês):", min_value=0.0, value=0.8)
duzias_ovo = st.number_input("Ovo (dúzias/mês):", min_value=0, value=2, step=1)
kg_arroz = st.number_input("Arroz (kg/mês):", min_value=0.0, value=5.0)
kg_feijao = st.number_input("Feijão (kg/mês):", min_value=0.0, value=2.0)
kg_vegetais = st.number_input("Vegetais/Frutas (kg/mês):", min_value=0.0, value=10.0)


# --- 4. Perguntas sobre Habitação ---
st.header("🏠 Habitação")
num_comodos = st.number_input("Quantos cômodos (quartos, sala, cozinha, etc.) sua residência possui? (ex: 5):", min_value=1, value=5, step=1)
horas_ar_condicionado_dia = st.number_input("Horas de ar-condicionado por dia (média):", min_value=0.0, value=2.0)
horas_aquecedor_dia = st.number_input("Horas de aquecedor por dia (média):", min_value=0.0, value=0.0)
# Convertendo para mensal aqui, antes de passar para a função
horas_ar_condicionado_mensal = horas_ar_condicionado_dia * 30
horas_aquecedor_mensal = horas_aquecedor_dia * 30


# --- 5. Perguntas sobre Consumo de Produtos ---
st.header("🛍️ Consumo de Produtos")
st.markdown("Média de produtos novos adquiridos por mês (0 para nenhum, 0.1 para 1 a cada 10 meses):")
num_celulares = st.number_input("Celulares:", min_value=0.0, value=0.0)
num_laptops = st.number_input("Laptops:", min_value=0.0, value=0.0)
num_geladeiras = st.number_input("Geladeiras:", min_value=0.0, value=0.0)
num_televisoes = st.number_input("Televisões:", min_value=0.0, value=0.0)
num_veiculos_eletricos_consumo = st.number_input("Veículos elétricos:", min_value=0.0, value=0.0) # Renomeado para não conflitar com transporte
num_roupas_peca = st.number_input("Peças de Roupa:", min_value=0.0, value=5.0)


# --- 6. Perguntas sobre Resíduos ---
st.header("🗑️ Resíduos")
num_sacos_lixo_100l = st.number_input("Sacos de lixo de 100L descartados (unid./mês):", min_value=0.0, value=2.5, help="Ex: 2.5 para 2 sacos e meio")
kg_lixo_reciclavel = st.number_input("Lixo reciclável separado (kg/mês):", min_value=0.0, value=5.0)
kg_eletronico = st.number_input("Lixo eletrônico descartado (kg/mês):", min_value=0.0, value=0.2)
kg_compostagem = st.number_input("Material enviado para compostagem (kg/mês):", min_value=0.0, value=3.0)


# --- 7. Perguntas sobre Estilo de Vida ---
st.header("🧘‍♀️ Estilo de Vida")
num_voos_eventos_ano = st.number_input("Voos (ou grandes eventos) que exigiram viagem no ÚLTIMO ANO:", min_value=0, value=0, step=1)
horas_streaming_dia = st.number_input("Horas de streaming de vídeo por dia (média):", min_value=0.0, value=2.0)
num_compras_online_mes = st.number_input("Compras online (número de pedidos/mês):", min_value=0, value=4, step=1)
horas_streaming_mensal = horas_streaming_dia * 30 # Convertendo para mensal aqui


# --- 8. Perguntas sobre Ações Sustentáveis (Créditos) ---
st.header("🌳 Ações Sustentáveis (Redução da Pegada)")
num_arvores_plantadas_mensal = st.number_input("Árvores plantadas ou contribuiu para plantar no último mês:", min_value=0.0, value=0.0)
kg_creditos_carbono = st.number_input("Créditos de carbono adquiridos (kg/mês):", min_value=0.0, value=0.0)


# --- BOTÃO DE CÁLCULO ---
st.markdown("---")
if st.button("Calcular Minha Pegada Verde!"):
    # --- REALIZA OS CÁLCULOS QUANDO O BOTÃO É CLICADO ---
    pegada_energia = calcular_pegada_energia(consumo_energia_kwh, num_botijoes_gas_13kg)

    total_transporte_combustivel = 0
    if usa_carro_moto_combustivel:
        total_transporte_combustivel = calcular_pegada_transporte_individual_combustivel(distancia_carro_moto_combustivel, tipo_combustivel)

    total_transporte_eletrico = 0
    if usa_veiculo_eletrico:
        total_transporte_eletrico = calcular_pegada_transporte_eletrico(distancia_veiculo_eletrico, tipo_veiculo_eletrico)

    total_transporte_coletivo = (
        calcular_pegada_transporte_coletivo(km_onibus, "onibus") +
        calcular_pegada_transporte_coletivo(km_metro, "metro") +
        calcular_pegada_transporte_coletivo(km_aviao_domestico, "aviao_domestico") +
        calcular_pegada_transporte_coletivo(km_aviao_internacional, "aviao_internacional")
    )
    pegada_transporte = total_transporte_combustivel + total_transporte_eletrico + total_transporte_coletivo

    pegada_alimentacao = calcular_pegada_alimentacao(
        kg_carne_bovina, kg_carne_suina, kg_frango, kg_peixe,
        litros_leite, kg_queijo, duzias_ovo, kg_arroz, kg_feijao, kg_vegetais
    )

    pegada_habitacao = calcular_pegada_habitacao(num_comodos, horas_ar_condicionado_mensal, horas_aquecedor_mensal)

    pegada_consumo = calcular_pegada_consumo(
        num_celulares, num_laptops, num_geladeiras,
        num_televisoes, num_veiculos_eletricos_consumo, num_roupas_peca # Use a variável renomeada aqui
    )

    pegada_residuos = calcular_pegada_residuos(num_sacos_lixo_100l, kg_lixo_reciclavel, kg_eletronico, kg_compostagem)

    pegada_estilo_vida = calcular_pegada_estilo_vida(num_voos_eventos_ano, horas_streaming_mensal, num_compras_online_mes)

    creditos_sustentaveis = calcular_creditos_sustentaveis(num_arvores_plantadas_mensal, kg_creditos_carbono)

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

    exibir_resumo_e_feedback_total(pegada_total_kgco2e)

    pegadas_por_categoria = {
        "energia_combustivel": pegada_energia,
        "transporte": pegada_transporte,
        "alimentacao": pegada_alimentacao,
        "habitacao": pegada_habitacao,
        "consumo": pegada_consumo,
        "residuos": pegada_residuos,
        "estilo_vida": pegada_estilo_vida
    }

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

    exibir_dicas_personalizadas(pegadas_por_categoria)


