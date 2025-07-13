# EcoSimulador: Minha Pegada Verde 🌍🌱

## Visão Geral

Este é o projeto inicial do **EcoSimulador: Minha Pegada Verde**, uma calculadora pessoal de pegada de carbono inspirada na mecânica "Pegada Verde" do The Sims 4. O objetivo é ajudar as pessoas a entenderem o impacto ambiental de seus hábitos diários de forma lúdica e interativa.

Esta é a versão **MVP (Produto Mínimo Viável)**, focada no funcionamento via terminal (console).

## Status do Projeto

Atualmente, o projeto está na fase inicial de configuração e pesquisa.

## Como Usar (Versão Console - Em Desenvolvimento)

1.  **Pré-requisitos:**
    * Python 3.x instalado no seu sistema.

2.  **Configuração do Ambiente:**
    * Clone este repositório para sua máquina local:
        ```bash
        git clone [https://github.com/SeuUsuario/EcoSimulador-PegadaVerde.git](https://github.com/SaraVSSILVA/EcoSimulador.git)
        ```
    * Navegue até a pasta do projeto:
        ```bash
        cd EcoSimulador-PegadaVerde
        ```
    * Crie e ative um ambiente virtual (altamente recomendado para isolar as dependências do projeto):
        * No Windows:
            ```bash
            python -m venv .venv
            .\.venv\Scripts\activate
            ```
        * No macOS/Linux:
            ```bash
            python3 -m venv .venv
            source ./.venv/bin/activate
            ```
    * (Por enquanto, não há bibliotecas para instalar)

3.  **Executar o Programa:**
    * Com o ambiente virtual ativado, execute o script principal:
        ```bash
        python main.py
        ```
    * Siga as instruções que aparecerão no terminal para inserir suas informações.

## Funcionalidades Planejadas para o MVP (Versão Console)

* Coleta de dados sobre consumo de energia, transporte, alimentação e lixo.
* Cálculo da pegada de carbono pessoal com base em fatores de emissão.
* Feedback lúdico e classificações da pegada (ex: "Eco-Herói", "Sustentável", "Alerta Vermelho") no terminal, usando mensagens e emojis.
* Dicas simples para redução de impacto, baseadas nas áreas de maior emissão do usuário.

## Próximos Passos (Backlog)

* [ ] Pesquisa e refinamento detalhado dos fatores de emissão.
* [ ] Implementação da lógica de perguntas e cálculo da pegada.
* [ ] Desenvolvimento do sistema de feedback lúdico.
* [ ] Refatoração e testes iniciais.
* [ ] (Futuro) Migração para uma interface web com Streamlit.
* [ ] (Futuro) Adição de elementos de gamificação (níveis, conquistas).

## Contribuição

Este projeto é um esforço pessoal de aprendizado e desenvolvimento. Sugestões e ideias são bem-vindas!

## Licença

Este projeto está licenciado sob a Licença MIT. (Você pode manter esta licença, que é bem comum e permissiva).

---