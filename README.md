# 🌍🌱 EcoEchos: O Eco das Suas Escolhas! 🌱🌍

Bem-vindo(a) ao EcoEchos, uma ferramenta simples e divertida para calcular sua pegada de carbono pessoal e descobrir como você pode reduzi-la! Este simulador te ajuda a entender o impacto das suas atividades diárias no meio ambiente, oferecendo feedback e dicas personalizadas.

## 🌟 O que é a Pegada de Carbono?

A pegada de carbono é a quantidade total de gases de efeito estufa (como o CO2) que são gerados direta ou indiretamente pelas nossas atividades. Calcular a sua pegada é o primeiro passo para entender onde você pode fazer a diferença e contribuir para um planeta mais sustentável.

## ✨ Funcionalidades

* **Cálculo Abrangente:** O EcoSimulador considera diversas categorias da sua vida diária:
    * **Energia e Combustível:** Consumo de eletricidade e gás em casa.
    * **Transporte:** Uso de carro (combustível e elétrico), moto, ônibus, metrô e avião.
    * **Alimentação:** Consumo de diferentes tipos de carne, laticínios, ovos, grãos e vegetais.
    * **Habitação:** Impacto da sua residência (número de cômodos, uso de ar condicionado/aquecedor).
    * **Consumo de Produtos:** Emissões relacionadas à compra de eletrônicos e roupas.
    * **Resíduos:** Descarte de lixo comum, reciclagem, eletrônicos e compostagem.
    * **Estilo de Vida:** Impacto de voos, streaming e compras online.
    * **Ações Sustentáveis:** Reduções na pegada por plantar árvores ou adquirir créditos de carbono.
* **Feedback Personalizado:** Após o cálculo, você receberá uma análise divertida sobre o tamanho da sua pegada.
* **Dicas de Redução:** O simulador identifica as categorias com maior impacto na sua pegada e oferece dicas práticas (e um tanto sarcásticas!) para você começar a fazer a diferença.

## 🚀 Como Usar

Para rodar o EcoSimulador, você precisará ter o Python instalado em seu computador.

1.  **Salve o Código:**
    Salve o código Python (o arquivo que contém todo o programa) em um arquivo com a extensão `.py` (por exemplo, `ecosimulador.py`).

2.  **Abra o Terminal/Prompt de Comando:**
    Navegue até o diretório onde você salvou o arquivo.

3.  **Execute o Programa:**
    Digite o seguinte comando e pressione Enter:
    ```bash
    python ecosimulador.py
    ```

4.  **Responda às Perguntas:**
    O programa fará uma série de perguntas sobre seus hábitos de consumo e estilo de vida. Digite suas respostas e pressione Enter após cada uma. Certifique-se de digitar números válidos quando solicitado (inteiros ou decimais).

5.  **Veja o Resultado:**
    Ao final, o EcoSimulador apresentará sua pegada de carbono total mensal e dará algumas dicas personalizadas para ajudar a reduzi-la.

## 📊 Fatores de Emissão

Os valores de emissão utilizados neste simulador são baseados em estimativas e podem variar dependendo da fonte, região e método de cálculo. Eles são uma referência para ajudar a visualizar o impacto das diferentes atividades.

**Exemplo de alguns fatores utilizados (em kg de CO2 equivalente - kgCO2e):**

```python
FATORES_EMISSAO = {
    "energia_combustivel": {
        "eletricidade_kWh": 0.065,
        "gasolina_litro": 2.32,
        # ... outros
    },
    "alimentacao": {
        "carne_bovina_kg": 26.5,
        "vegetais_kg": 0.85,
        # ... outros
    },
    # ... outras categorias
}
```

Observação: Valores negativos como os de "arvores_plantadas" ou "compostagem_kg" indicam uma redução (benefício) na pegada de carbono.

## 💡 Dicas de Redução
O simulador oferece dicas para as categorias que mais contribuem para sua pegada. As dicas são projetadas para serem informativas e, por vezes, bem-humoradas, incentivando a reflexão sobre seus hábitos.

## Próximos Passos (Backlog)

* [ ] Refatoração e testes iniciais.
* [ ] (Futuro) Migração para uma interface web com Streamlit.
* [ ] (Futuro) Adição de elementos de gamificação (níveis, conquistas).

## Contribuição

Este projeto é um esforço pessoal de aprendizado e desenvolvimento. Sugestões e ideias são bem-vindas!

## Licença

Este projeto está licenciado sob a Licença MIT. 

---
