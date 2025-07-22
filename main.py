import random

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

def calcular_pegada_energia(consumo_kwh, num_botijoes_gas_13kg):
    pegada = 0
    pegada += consumo_kwh * FATORES_EMISSAO["energia_combustivel"]["eletricidade_kWh"]
    pegada += num_botijoes_gas_13kg * FATORES_EMISSAO["energia_combustivel"]["gas_cozinha_13kg"]
    return pegada

def calcular_pegada_transporte_individual_combustivel(distancia_km, tipo_combustivel):
    litros_consumidos = 0
    if tipo_combustivel == "gasolina":
        litros_consumidos = distancia_km / 10.0
        return litros_consumidos * FATORES_EMISSAO["energia_combustivel"]["gasolina_litro"]
    elif tipo_combustivel == "etanol":
        litros_consumidos = distancia_km / 7.0
        return litros_consumidos * FATORES_EMISSAO["energia_combustivel"]["etanol_litro"]
    elif tipo_combustivel == "diesel":
        litros_consumidos = distancia_km / 12.0
        return litros_consumidos * FATORES_EMISSAO["energia_combustivel"]["diesel_litro"]
    else:
        return 0

def calcular_pegada_transporte_eletrico(distancia_km, tipo_veiculo):
    if tipo_veiculo == "carro_eletrico":
        return distancia_km * FATORES_EMISSAO["transporte"]["carro_eletrico_km"]
    elif tipo_veiculo == "moto":
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

def calcular_pegada_habitacao(num_comodos, horas_ar_condicionado, horas_aquecedor):
    total = 0
    total += num_comodos * FATORES_EMISSAO["habitacao"]["residencia_comodo"]
    total += horas_ar_condicionado * FATORES_EMISSAO["habitacao"]["ar_condicionado_hora"]
    total += horas_aquecedor * FATORES_EMISSAO["habitacao"]["aquecedor_hora"]
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

def calcular_pegada_estilo_vida(num_voos_eventos_ano, horas_streaming, num_compras_online_mes):
    total = 0
    total += (num_voos_eventos_ano / 12) * FATORES_EMISSAO["estilo_vida"]["voos_eventos_ano"]
    total += horas_streaming * FATORES_EMISSAO["estilo_vida"]["streaming_hora"]
    total += num_compras_online_mes * FATORES_EMISSAO["estilo_vida"]["compras_online_mes"]
    return total

def calcular_creditos_sustentaveis(num_arvores_plantadas, kg_creditos_carbono):
    total = 0
    total += num_arvores_plantadas * FATORES_EMISSAO["sustentavel"]["arvores_plantadas"]
    total += kg_creditos_carbono * FATORES_EMISSAO["sustentavel"]["creditos_carbono_kg"]
    return total

def obter_input_numerico(pergunta, tipo=float):
    while True:
        try:
            resposta = tipo(input(pergunta + " "))
            if resposta < 0:
                print("Por favor, digite um número igual ou maior que zero.")
            else:
                return resposta
        except ValueError:
            print(f"Entrada inválida. Por favor, digite um número válido (inteiro ou decimal).")

def exibir_resumo_e_feedback_total(pegada_total_kgco2e):
    print("\n" + "="*40)
    print(f"SUA PEGADA DE CARBONO TOTAL MENSAL É: {pegada_total_kgco2e:.2f} kgCO2e")
    print("="*40)

    print("\n--- Análise da sua Pegada Criminal... digo, de Carbono ---")

    if pegada_total_kgco2e <= 150:
        print("Parabéns, seu pequeno elfo da floresta! Sua pegada é tão leve que mal deixou rastro. O planeta te agradece... por enquanto. Continue assim, ou a gente te manda para a reciclagem!")
    elif 150 < pegada_total_kgco2e <= 400:
        print("Bom, pelo menos você tenta, né?. Nem um pé-grande, nem uma fada. Parece que você está tentando, mas ainda dá para apertar um pouco mais essa bota. O planeta está de olho em você!")
    elif 400 < pegada_total_kgco2e <= 800:
        print("Olha só, achamos o Pé-Médio! Sua pegada já está deixando uma marca considerável. Talvez seja hora de trocar o carro por uma bicicleta... ou por um par de pernas. O aquecimento global manda lembranças!")
    elif 800 < pegada_total_kgco2e <= 1500:
        print("Cuidado para não esmagar o planeta! Sua pegada está ficando GIGANTE. Será que você está andando de dinossauro ou algo assim? O IBAMA já está a caminho, só pra avisar.")
    else:
        print("PARABÉNS! Você deve ser um dos maiores contribuidores para o APOCALIPSE climático! Tem nem o que falar, vai plantar uma árvore, ou melhor, um bosque inteiro! O planeta está chorando... e você é o motivo.")

    print("\nLembre-se: cada quilo de CO2e conta. Ou não. Depende do quanto você se importa com o futuro... e com a ironia do destino.")
    print("Obrigada por usar o EcoSimulador. Agora vá e faça algo útil pelo planeta... ou não. A escolha é sua, meliante ambiental.")

def exibir_dicas_personalizadas(pegadas_por_categoria):
    print("\n--- O Oráculo do Carbono Revela: Onde Você Está Falhando Mais (e como remediar, talvez) ---")

    categorias_com_impacto = {
        cat: val for cat, val in pegadas_por_categoria.items() if val > 5
    }

    if not categorias_com_impacto:
        print("Sua pegada é tão mínima que não consigo nem encontrar um 'maior impacto'. Ou você é um santo, ou mentiu em tudo. Sem dicas para você, prodígio ambiental!")
    else:
        top_categorias = sorted(categorias_com_impacto.items(), key=lambda item: item[1], reverse=True)

        num_dicas = min(len(top_categorias), 3)

        print(f"Pelas minhas contas (e minha paciência), suas maiores fontes de 'poluição gloriosa' são:")
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

            print(f"\n--- 🥉 Sua Pegada em {nome_amigavel} ({pegada_valor:.2f} kgCO2e) ---")

            dicas = DICAS_REDUCAO.get(categoria_nome_tecnico, ["Hmm, para essa categoria, a dica é... não faça mais isso!"])

            if len(dicas) > 0:
                dica1 = random.choice(dicas)
                print(f"Dica 1: {dica1}")
                if len(dicas) > 1:
                    dicas_restantes = [d for d in dicas if d != dica1]
                    if dicas_restantes:
                        print(f"Dica 2: {random.choice(dicas_restantes)}")
            else:
                print("Parece que até eu estou sem sarcasmo para te dar dicas aqui. Tente de novo, ou não. Pelo menos finja que se importa.")


def main():
    print("Bem-vindo(a) ao EcoSimulador: Minha Pegada Verde! 🌍🌱")
    print("Vamos calcular sua pegada de carbono pessoal. Responda algumas perguntas:")

    pegada_energia = 0.0
    pegada_transporte = 0.0
    pegada_alimentacao = 0.0
    pegada_habitacao = 0.0
    pegada_consumo = 0.0
    pegada_residuos = 0.0
    pegada_estilo_vida = 0.0
    creditos_sustentaveis = 0.0

    # --- 1. Perguntas sobre Energia e Combustível (Casa) ---
    print("\n--- Energia e Combustível (Casa) ---")
    consumo_energia_kwh = obter_input_numerico("Quantos kWh de energia elétrica você consumiu no último mês? (ex: 150):", float)
    num_botijoes_gas_13kg = obter_input_numerico("Quantos botijões de gás de cozinha (13kg) você usou no último mês? (ex: 0.5 para meio botijão):", float)

    pegada_energia = calcular_pegada_energia(consumo_energia_kwh, num_botijoes_gas_13kg)
    print(f"Sua pegada de energia e combustível é de {pegada_energia:.2f} kgCO2e.")

    # --- 2. Perguntas sobre Transporte ---
    print("\n--- Transporte ---")
    total_transporte_combustivel = 0
    total_transporte_eletrico = 0
    total_transporte_coletivo = 0

    # Carro/Moto a Combustível
    usa_carro_moto_combustivel = input("Você usa carro ou moto a gasolina/etanol/diesel? (sim/nao): ").lower()
    if usa_carro_moto_combustivel == "sim":
        distancia_carro_moto_combustivel = obter_input_numerico("Quantos km você percorreu com VEÍCULO A COMBUSTÍVEL no último mês?:", float)
        tipo_combustivel = ""
        while tipo_combustivel not in ["gasolina", "etanol", "diesel"]:
            tipo_combustivel = input("Qual o PRINCIPAL COMBUSTÍVEL do seu veículo? (gasolina/etanol/diesel): ").lower()
            if tipo_combustivel not in ["gasolina", "etanol", "diesel"]:
                print("Opção inválida. Por favor, escolha entre 'gasolina', 'etanol' ou 'diesel'.")
        total_transporte_combustivel = calcular_pegada_transporte_individual_combustivel(distancia_carro_moto_combustivel, tipo_combustivel)

    # Carro/Moto Elétrico
    usa_veiculo_eletrico = input("Você usa carro ou moto ELÉTRICA? (sim/nao): ").lower()
    if usa_veiculo_eletrico == "sim":
        tipo_veiculo_eletrico = ""
        while tipo_veiculo_eletrico not in ["carro_eletrico", "moto"]:
            tipo_veiculo_eletrico = input("Qual tipo de veículo elétrico? (carro_eletrico/moto): ").lower()
            if tipo_veiculo_eletrico not in ["carro_eletrico", "moto"]:
                print("Opção inválida. Por favor, escolha entre 'carro_eletrico' ou 'moto'.")
        distancia_veiculo_eletrico = obter_input_numerico(f"Quantos km você percorreu de {tipo_veiculo_eletrico.replace('_', ' ').upper()} no último mês? (0 se não usou):", float)
        total_transporte_eletrico += calcular_pegada_transporte_eletrico(distancia_veiculo_eletrico, tipo_veiculo_eletrico)

    # Transporte Coletivo e Avião
    km_onibus = obter_input_numerico("Quantos km você percorreu de ÔNIBUS no último mês? (0 se não usou):", float)
    km_metro = obter_input_numerico("Quantos km você percorreu de METRÔ no último mês? (0 se não usou):", float)
    km_aviao_domestico = obter_input_numerico("Quantos km você voou em viagens DOMÉSTICAS no último mês? (0 se não voou):", float)
    km_aviao_internacional = obter_input_numerico("Quantos km você voou em viagens INTERNACIONAIS no último mês? (0 se não voou):", float)

    total_transporte_coletivo = (
        calcular_pegada_transporte_coletivo(km_onibus, "onibus") +
        calcular_pegada_transporte_coletivo(km_metro, "metro") +
        calcular_pegada_transporte_coletivo(km_aviao_domestico, "aviao_domestico") +
        calcular_pegada_transporte_coletivo(km_aviao_internacional, "aviao_internacional")
    )

    pegada_transporte = total_transporte_combustivel + total_transporte_eletrico + total_transporte_coletivo
    print(f"Sua pegada de transporte é de {pegada_transporte:.2f} kgCO2e.")

    # --- 3. Perguntas sobre Alimentação ---
    print("\n--- Alimentação ---")
    kg_carne_bovina = obter_input_numerico("Quantos kg de CARNE BOVINA você consumiu no último mês? (ex: 2.5):", float)
    kg_carne_suina = obter_input_numerico("Quantos kg de CARNE SUÍNA você consumiu no último mês? (ex: 1.0):", float)
    kg_frango = obter_input_numerico("Quantos kg de FRANGO você consumiu no último mês? (ex: 3.0):", float)
    kg_peixe = obter_input_numerico("Quantos kg de PEIXE você consumiu no último mês? (ex: 0.5):", float)
    litros_leite = obter_input_numerico("Quantos LITROS de LEITE você consumiu no último mês? (ex: 5.0):", float)
    kg_queijo = obter_input_numerico("Quantos kg de QUEIJO você consumiu no último mês? (ex: 0.8):", float)
    duzias_ovo = obter_input_numerico("Quantas DÚZIAS de OVO você consumiu no último mês? (ex: 2):", int)
    kg_arroz = obter_input_numerico("Quantos kg de ARROZ você consumiu no último mês? (ex: 5.0):", float)
    kg_feijao = obter_input_numerico("Quantos kg de FEIJÃO você consumiu no último mês? (ex: 2.0):", float)
    kg_vegetais = obter_input_numerico("Quantos kg de VEGETAIS/FRUTAS você consumiu no último mês? (ex: 10.0):", float)

    pegada_alimentacao = calcular_pegada_alimentacao(
        kg_carne_bovina, kg_carne_suina, kg_frango, kg_peixe,
        litros_leite, kg_queijo, duzias_ovo, kg_arroz, kg_feijao, kg_vegetais
    )
    print(f"Sua pegada de alimentação é de {pegada_alimentacao:.2f} kgCO2e.")

    # --- 4. Perguntas sobre Habitação ---
    print("\n--- Habitação ---")
    num_comodos = obter_input_numerico("Quantos cômodos (quartos, sala, cozinha, banheiro, etc.) sua residência possui? (ex: 5):", int)
    horas_ar_condicionado_mensal = obter_input_numerico("Quantas HORAS por dia, em média, você usa AR CONDICIONADO? (ex: 4):", float) * 30
    horas_aquecedor_mensal = obter_input_numerico("Quantas HORAS por dia, em média, você usa AQUECEDOR? (ex: 0):", float) * 30

    pegada_habitacao = calcular_pegada_habitacao(num_comodos, horas_ar_condicionado_mensal, horas_aquecedor_mensal)
    print(f"Sua pegada de habitação é de {pegada_habitacao:.2f} kgCO2e.")

    # --- 5. Perguntas sobre Consumo de Produtos ---
    print("\n--- Consumo de Produtos ---")
    num_celulares = obter_input_numerico("Quantos CELULARES novos você comprou no último mês? (ex: 0):", int)
    num_laptops = obter_input_numerico("Quantos LAPTOPS novos você comprou no último mês? (ex: 0):", int)
    num_geladeiras = obter_input_numerico("Quantas GELADEIRAS novas você comprou no último mês? (ex: 0):", int)
    num_televisoes = obter_input_numerico("Quantas TELEVISÕES novas você comprou no último mês? (ex: 0):", int)
    num_veiculos_eletricos = obter_input_numerico("Quantos VEÍCULOS ELÉTRICOS novos você comprou no último mês? (ex: 0):", int)
    num_roupas_peca = obter_input_numerico("Quantas PEÇAS DE ROUPA novas você comprou no último mês? (ex: 5):", int)

    pegada_consumo = calcular_pegada_consumo(
        num_celulares, num_laptops, num_geladeiras,
        num_televisoes, num_veiculos_eletricos, num_roupas_peca
    )
    print(f"Sua pegada de consumo é de {pegada_consumo:.2f} kgCO2e.")

    # --- 6. Perguntas sobre Resíduos ---
    print("\n--- Resíduos ---")
    num_sacos_lixo_100l = obter_input_numerico("Quantos SACOS DE LIXO DE 100L (aqueles grandes) você descartou no último mês? (ex: 2.5 para 2 sacos e meio):", float)
    kg_lixo_reciclavel = obter_input_numerico("Quantos kg de LIXO RECICLÁVEL você separou no último mês? (ex: 5.0):", float)
    kg_eletronico = obter_input_numerico("Quantos kg de LIXO ELETRÔNICO você descartou no último mês? (ex: 0.2):", float)
    kg_compostagem = obter_input_numerico("Quantos kg de material você enviou para COMPOSTAGEM no último mês? (ex: 3.0):", float)

    pegada_residuos = calcular_pegada_residuos(num_sacos_lixo_100l, kg_lixo_reciclavel, kg_eletronico, kg_compostagem)
    print(f"Sua pegada de resíduos é de {pegada_residuos:.2f} kgCO2e.")

    # --- 7. Perguntas sobre Estilo de Vida ---
    print("\n--- Estilo de Vida ---")
    num_voos_eventos_ano = obter_input_numerico("Quantos VOOS (ou grandes eventos) você participou no ÚLTIMO ANO? (ex: 1):", int)
    horas_streaming_mensal = obter_input_numerico("Quantas HORAS de STREAMING (Netflix, YouTube) você assiste por dia, em média? (ex: 2.0):", float) * 30
    num_compras_online_mes = obter_input_numerico("Quantas COMPRAS ONLINE você fez no último mês? (ex: 4):", int)

    pegada_estilo_vida = calcular_pegada_estilo_vida(num_voos_eventos_ano, horas_streaming_mensal, num_compras_online_mes)
    print(f"Sua pegada de estilo de vida é de {pegada_estilo_vida:.2f} kgCO2e.")

    # --- 8. Perguntas sobre Ações Sustentáveis (Créditos) ---
    print("\n--- Ações Sustentáveis (Créditos de Carbono) ---")
    num_arvores_plantadas = obter_input_numerico("Quantas ÁRVORES você plantou ou contribuiu para plantar no último mês? (ex: 0):", int)
    kg_creditos_carbono = obter_input_numerico("Quantos kg de CRÉDITOS DE CARBONO você adquiriu no último mês? (ex: 0):", float)

    creditos_sustentaveis = calcular_creditos_sustentaveis(num_arvores_plantadas, kg_creditos_carbono)
    print(f"Seus créditos sustentáveis são de {creditos_sustentaveis:.2f} kgCO2e.")

    # Cálculo da Pegada de Carbono Total Mensal
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

    exibir_dicas_personalizadas(pegadas_por_categoria)

if __name__ == "__main__":
    main()