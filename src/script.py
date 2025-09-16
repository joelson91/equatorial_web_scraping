# Importando as bibliotecas
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv

# Configuração do Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Constantes e Configurações
URL_BASE = "https://pa.equatorialenergia.com.br"
TIMEOUT_SECONDS = 30
CPF = os.getenv("CPF")
NASCIMENTO = os.getenv("NASCIMENTO")
DOWNLOAD_PATH = os.path.join(os.getcwd(), "faturas_equatorial")


def configurar_driver():
    """
    Configura e retorna uma instância do WebDriver com as opções
    necessárias para o download automático de PDFs.
    """
    logging.info("Configurando o driver.")
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    options = Options()

    prefs = {
    "plugins.always_open_pdf_externally": True,
    "plugins.plugins_disabled": ["Chrome PDF Viewer"],
    "profile.default_content_settings.popups": 0,
    "profile.default_content_setting_values.automatic_downloads": 1,
    "download.default_directory": DOWNLOAD_PATH,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
    }

    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    return webdriver.Chrome(options=options)


def realizar_login(driver, wait):
    """
    Executa o processo de login no site da Equatorial.
    Retorna True em caso de sucesso, False caso contrário.
    """
    try:
        logging.info(f"Acessando a URL base: {URL_BASE}")
        driver.get(URL_BASE)

        logging.info("Aceitando cookies e pop-ups iniciais.")
        wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pm__close"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "aviso_aceite"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "lgpd_accept"))).click()

        logging.info("Inserindo CPF.")
        wait.until(EC.visibility_of_element_located((By.ID, "identificador-otp"))).send_keys(CPF)
        driver.find_element(By.ID, "envia-identificador-otp").click()

        logging.info("Inserindo data de nascimento.")
        wait.until(EC.visibility_of_element_located((By.ID, "senha-identificador"))).send_keys(NASCIMENTO)
        driver.find_element(By.ID, "envia-identificador").click()

        logging.info("Login realizado com sucesso.")
        return True

    except TimeoutException:
        logging.error("Tempo excedido durante o processo de login. Um elemento não foi encontrado a tempo.")
        return False
    except NoSuchElementException as e:
        logging.error("Elemento não encontrado durante o login: %s", e)
        return False


def navegar_para_faturas(wait):
    """
    Navega até a página de consulta de faturas após o login.
    """
    try:
        logging.info("Navegando para a página de faturas.")
        faturas_menu_item = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li#menu-item-3888 a")))
        faturas_menu_item.click()

        # Aguarda a tabela de faturas carregar
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, "fa-spinner")))
        logging.info("Página de faturas carregada.")
        return True
    except TimeoutException:
        logging.error("Não foi possível navegar para a página de faturas. A tabela não foi encontrada.")
        return False


def baixar_faturas(driver, wait):
    """
    Encontra todas as faturas na tabela e realiza o download de cada uma.
    """
    try:
        logging.info("Procurando a tabela de faturas.")
        table = driver.find_element(By.TAG_NAME, "table")

        rows = table.find_elements(By.TAG_NAME, "tr")
        logging.info(f"Encontradas {len(rows)} faturas para download.")

        if not rows:
            logging.warning("Nenhuma linha de fatura encontrada com o seletor atual.")
            return

        for i, row in enumerate(rows, 1):
            try:
                logging.info(f"Processando fatura {i} de {len(rows)}...")

                # Clica na linha para abrir o modal
                row.click()

                # Espera o botão de download aparecer e ser clicável
                wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "download-pdf"), "Ver Fatura"))
                btn_download = driver.find_element(By.CLASS_NAME, "download-pdf")
                btn_download.click()
                logging.info(f"Download da fatura {i} iniciado.")

                # Fecha o modal
                close_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modal-close")))
                close_button.click()

                # Pequena pausa para garantir que o modal fechou completamente
                wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-content")))

            except TimeoutException:
                logging.error(f"Erro ao processar a fatura {i}. O modal ou botão de download não apareceu.")
                # Tenta fechar o modal se ele ainda estiver aberto para não travar o loop
                try:
                    driver.find_element(By.CLASS_NAME, "modal-close").click()
                except NoSuchElementException:
                    pass

    except NoSuchElementException:
        logging.error("A tabela de faturas não foi encontrada na página.")


def main():
    """
    Função principal que orquestra a execução do script.
    """
    driver = configurar_driver()
    wait = WebDriverWait(driver, TIMEOUT_SECONDS)

    try:
        if realizar_login(driver, wait):
            if navegar_para_faturas(wait):
                baixar_faturas(driver, wait)
        else:
            logging.error("Falha no login. O script não pode continuar.")

    except KeyboardInterrupt:
        logging.warning("Execução interrompida pelo usuário.")
    except Exception as e:
        logging.critical(f"Ocorreu um erro inesperado: {e}")
    finally:
        logging.info("Script finalizado. Fechando o driver.")
        driver.quit()


if __name__ == "__main__":
    main()
