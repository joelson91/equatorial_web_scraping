# Equatorial Web Scraping

Este projeto é um script de automação desenvolvido em Python para acessar e baixar o histórico completo de faturas de energia do site da [Equatorial Pará](https://pa.equatorialenergia.com.br). O objetivo é simplificar o acesso e o arquivamento digital das contas mensais em formato PDF.

## 🚀 Funcionalidades

-   **Login automático** no portal da Equatorial com as credenciais do usuário.
-   **Navegação automática** até a página de consulta de faturas.
-   **Download de todas as faturas** disponíveis na tabela de histórico.
-   **Organização dos arquivos** em uma pasta local chamada `faturas_equatorial`.

## 📋 Pré-requisitos

1.   **Python 3.10+**
2.   **Selenium**
3.   **python-dotenv**

## ⚙️ Instalação e Configuração

Siga os passos abaixo para configurar o ambiente e executar o projeto.

**1. Clone o repositório:**

```bash
git clone https://github.com/joelson91/equatorial_web_scraping.git
```

**2. Navegue até o diretório do projeto:**

```bash
cd equatorial_web_scraping
```

**3. Crie e ative um ambiente virtual (Recomendado):**

```bash
# Criar o ambiente
python -m venv venv

# Ativar no Windows
.\venv\Scripts\activate

# Ativar no Linux/Mac
source venv/bin/activate
```

**4. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**5. Configure suas credenciais:**

Crie um arquivo chamado `.env` na raiz do projeto, seguindo o modelo abaixo. Adicione suas informações pessoais a ele:

```ini
# .env
CPF="123.456.789-10"
NASCIMENTO="01/02/2003"
```

## ▶️ Como Executar

Com o ambiente virtual ativado e o arquivo `.env` configurado, basta executar o script principal:

```bash
python src/script.py
```

As faturas serão baixadas automaticamente na pasta `faturas_equatorial`.