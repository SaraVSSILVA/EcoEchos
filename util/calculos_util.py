from config.fatores_emissao import FATORES_EMISSAO # Importa os fatores

# ... (Todas as suas funções de cálculo: calcular_pegada_energia, etc.) ...
def calcular_pegada_energia(consumo_kwh, num_botijoes_gas_13kg):
    pegada = 0
    pegada += consumo_kwh * FATORES_EMISSAO["energia_combustivel"]["eletricidade_kWh"]
    pegada += num_botijoes_gas_13kg * FATORES_EMISSAO["energia_combustivel"]["gas_cozinha_13kg"]
    return pegada

def calcular_pegada_transporte_individual_combustivel(distancia_km, tipo_combustivel):
    litros_consumidos = 0
    if tipo_combustivel == "gasolina":
        litros_consumidos = distancia_km / 10.0 # Assumindo 10 km/litro para gasolina
        return litros_consumidos * FATORES_EMISSAO["energia_combustivel"]["gasolina_litro"]
    elif tipo_combustivel == "etanol":
        litros_consumidos = distancia_km / 7.0 # Assumindo 7 km/litro para etanol
        return litros_consumidos * FATORES_EMISSAO["energia_combustivel"]["etanol_litro"]
    elif tipo_combustivel == "diesel":
        litros_consumidos = distancia_km / 12.0 # Assumindo 12 km/litro para diesel
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
    # Dividindo por 12 para estimativa mensal da emissão anual de voos
    total += (num_voos_eventos_ano / 12) * FATORES_EMISSAO["estilo_vida"]["voos_eventos_ano"]
    total += horas_streaming_mensal * FATORES_EMISSAO["estilo_vida"]["streaming_hora"]
    total += num_compras_online_mes * FATORES_EMISSAO["estilo_vida"]["compras_online_mes"]
    return total

def calcular_creditos_sustentaveis(num_arvores_plantadas_mensal, kg_creditos_carbono):
    total = 0
    total += num_arvores_plantadas_mensal * FATORES_EMISSAO["sustentavel"]["arvores_plantadas"]
    total += kg_creditos_carbono * FATORES_EMISSAO["sustentavel"]["creditos_carbono_kg"]
    return total