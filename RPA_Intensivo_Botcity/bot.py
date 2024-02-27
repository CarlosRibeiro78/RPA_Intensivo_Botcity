"""
WARNING:

Please make sure you install the bot with `pip install -e .` in order to get all the dependencies
on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the bot.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install -e .`
- Use the same interpreter as the one used to install the bot (`pip install -e .`)

# Please refer to the documentation for more information at https://documentation.botcity.dev/
"""

from botcity.web import WebBot, Browser
# Uncomment the line below for integrations with BotMaestro
# Using the Maestro SDK
from botcity.maestro import *
from botcity.web.util import element_as_select
from botcity.web.parsers import table_to_dict
from botcity.web import By


class Bot(WebBot):
    def action(self, execution=None):
        # Uncomment to silence Maestro errors when disconnected
        # if self.maestro:
        #     self.maestro.RAISE_NOT_CONNECTED = False

        # Configure whether or not to run on headless mode
        self.headless = False

        # Uncomment to change the default Browser to Firefox
        self.browser = Browser.CHROME

        # Uncomment to set the WebDriver path
        self.driver_path = r"C:\Projetos\BotCity\DriverWeb\chromedriver-win64\chromedriver.exe"

        # Fetch the Activity ID from the task:
        # task = self.maestro.get_task(execution.task_id)
        # activity_id = task.activity_id

        # Opens the BotCity website.
        self.browse("https://buscacepinter.correios.com.br/app/faixa_cep_uf_localidade/index.php")

        drop_uf = element_as_select(self.find_element("//select[@id='uf']", By.XPATH))
        drop_uf.select_by_value("SC")

        btn_pesquisar = self.find_element("//button[@id='btn_pesquisar']", By.XPATH)
        btn_pesquisar.click()

        table_dados = self.find_element("//table[@id='resultado-DNEC']", By.XPATH)
        table_dados = table_to_dict(table=table_dados)

        self.browse("https://cidades.ibge.gov.br/brasil/sc/panorama")

        for cidade in table_dados:

            str_cidade = cidade["localidade"]

            campo_pesquisa = self.find_element("//input[@placeholder='O que você procura?']", By.XPATH)
            campo_pesquisa.send_keys(str_cidade)

            opcao_cidade = self.find_element(f"//a[contains(span, {str_cadade})", By.XPATH)
            opcao_cidade.click
            self.wait(1000)

        # Uncomment to mark this task as finished on BotMaestro
        # self.maestro.finish_task(
        #     task_id=execution.task_id,
        #     status=AutomationTaskFinishStatus.SUCCESS,
        #     message="Task Finished OK."
        # )

        # Wait for 10 seconds before closing
        self.wait(1000)

        # Stop the browser and clean up
        self.stop_browser()

    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
   Bot.main()
