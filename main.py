fatores_emissao = {
    "energia_combustivel": {
        "eletricidade_kWh": 0.065,           # kgCO₂e/kWh - média do SIN com predominância de fontes renováveis
        "gas_cozinha_13kg": 3.02,               # GLP
        "gasolina_litro": 2.32,
        "etanol_litro": 0.55,
        "diesel_litro": 2.68,
    },
    "transporte": {
        "carro_comum_km": 0.19,
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
        "residencia_m2": 0.18,               # considerando consumo médio de energia e construção
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
        "lixo_comum_kg": 1.8,                # média para aterros sem captura de metano
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
