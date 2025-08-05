# 🎮 EcoEchos: O Eco das Suas Escolhas\! 🌍🌱

Bem-vindo ao **EcoEchos**, o seu aplicativo interativo para calcular e entender sua pegada de carbono pessoal de forma divertida e envolvente\! Com o EcoEchos, você pode:

  * **Calcular Sua Pegada:** Preencha seus hábitos de consumo em diversas categorias (energia, transporte, alimentação, habitação, consumo, resíduos, estilo de vida) e descubra o impacto ambiental de suas escolhas em kg de CO2 equivalente.
  * **Identificar Áreas de Melhoria:** Veja quais categorias mais contribuem para sua pegada e receba dicas personalizadas para reduzi-la.
  * **Acompanhar Seu Progresso:** Monitore suas emissões ao longo do tempo e celebre suas conquistas na jornada pela sustentabilidade.
  * **Aprender e Agir:** Descubra novas formas de "upar de nível" na sustentabilidade, com ações que compensam ou reduzem sua pegada.

## ✨ Novidades e Funcionalidades Principais

  * **Sistema de Usuários (Login/Cadastro):** Agora você pode criar uma conta, fazer login e ter uma experiência personalizada. Seus dados e progresso são vinculados ao seu perfil.
  * **Persistência de Dados Mensais:** Salve e carregue seus dados de pegada de carbono e hábitos por mês/ano. Nunca perca seu progresso e acompanhe sua evolução\!
  * **Interface Intuitiva:** Um formulário dividido em abas torna o preenchimento dos dados fácil e organizado.
  * **Resultados Detalhados:** Obtenha um resumo claro da sua pegada total e uma análise por categoria para identificar seus maiores impactos.
  * **Dicas Personalizadas:** Receba sugestões práticas e específicas para reduzir sua pegada com base em seus hábitos.
  * **Arquitetura Modular:** O código foi refatorado e dividido em arquivos menores (configurações, serviços de banco de dados, utilitários de cálculo e exibição) para facilitar a manutenção, desenvolvimento e escalabilidade.

## 🚀 Como Rodar o EcoEchos Localmente

Siga estes passos para configurar e executar o aplicativo em sua máquina:

1.  **Pré-requisitos:**

      * Python 3.9+
      * `pip` (gerenciador de pacotes do Python)

2.  **Clone o Repositório:**

    ```bash
    git clone https://github.com/seu-usuario/EcoEchos.git
    cd EcoEchos
    ```

    *(**Nota:** Altere `https://github.com/seu-usuario/EcoEchos.git` para o URL real do seu repositório.)*

3.  **Crie e Ative um Ambiente Virtual (Recomendado):**

    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

4.  **Instale as Dependências:**

    ```bash
    pip install -r requirements.txt
    ```

    *(**Importante:** Certifique-se de que o seu `requirements.txt` contém todas as bibliotecas necessárias, como `streamlit`, `pandas`, `plotly`, `SQLAlchemy` (ou `mysql-connector-python` se estiver usando MySQL diretamente, mas seu `db_service` indica SQLite, então talvez `SQLAlchemy` seja suficiente para abstrair o banco de dados).*

5.  **Execute o Aplicativo Streamlit:**

    ```bash
    streamlit run app.py
    ```

    O aplicativo será aberto automaticamente no seu navegador padrão em `http://localhost:8501`.

## 🛠️ Estrutura do Projeto

  * `app.py`: O arquivo principal do Streamlit que orquestra a interface e as chamadas para os módulos.
  * `configuracao/` (ou `config/`): Contém arquivos de configuração, como `fatores_emissao.py` e `dicas.py`.
  * `servicos/` (ou `services/`): Contém `db_servico.py` (ou `db_service.py`), responsável pelas interações com o banco de dados (SQLite).
  * `utilitarios/` (ou `util/`): Inclui módulos para:
      * `calculos_util.py`: Funções para calcular a pegada de carbono por categoria.
      * `exibicao_util.py`: Funções para exibir os resultados, gráficos e dicas.
  * `README.md`: Este arquivo.
  * `requirements.txt`: Lista de dependências do projeto.
  * `database.db`: O arquivo do banco de dados SQLite (será criado automaticamente ao rodar o app pela primeira vez).

## 🌐 Em Breve: EcoEchos Online!
Estou trabalhando para que o EcoEchos possa ser acessado por todos, a qualquer momento e de qualquer lugar! Em breve, você poderá calcular sua pegada verde e explorar sua jornada de sustentabilidade diretamente em seu navegador, sem a necessidade de instalações ou configurações. Mantenha-se atento às atualizações!

## 🤝 Contribuições

Contribuições são bem-vindas\! Se você tiver ideias para melhorias, novas categorias de cálculo, dicas de redução ou qualquer outra funcionalidade, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## 📄 Licença

Este projeto está licenciado sob a licença [MIT].

-----
