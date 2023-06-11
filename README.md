# Projeto_Impacta

Explorador de Frete
O Explorador de Frete é uma aplicação desktop desenvolvida em Python que automatiza a pesquisa de preços de frete em um website específico e armazena os resultados em um banco de dados. Ele utiliza a biblioteca Selenium para interagir com o navegador web e a biblioteca tkinter para criar a interface gráfica.

Funcionalidades
Pesquisa de preços de frete entre uma origem e um destino específicos.
Armazenamento dos resultados da pesquisa em um banco de dados SQLite.
Consulta dos resultados previamente pesquisados.
Pré-requisitos
Python 3.6 ou superior.
Bibliotecas Python: tkinter, selenium, sqlite3, PIL.
Instalação
Clone este repositório para o seu ambiente local:


git clone https://github.com/seu-usuario/explorador-de-frete.git
Instale as dependências necessárias:


pip install tkinter selenium pillow
Certifique-se de ter o navegador Chrome instalado em seu sistema.

Baixe o driver do Chrome para a versão correspondente ao seu navegador no seguinte link: ChromeDriver

Extraia o arquivo do driver baixado e coloque-o em um diretório de sua escolha.

Abra o arquivo main.py e localize a linha onde é definido o caminho para o driver do Chrome:


webdriver.Chrome("caminho/para/o/chromedriver")
Substitua "caminho/para/o/chromedriver" pelo caminho completo para o driver do Chrome que você baixou.

Uso
Abra o terminal e navegue até o diretório do projeto.

Execute o seguinte comando para iniciar a aplicação:

python main.py
Será exibida a janela principal da aplicação com duas opções: "Explorar" e "Consultar".

Para pesquisar um frete, selecione a opção "Explorar" e preencha os campos de origem e destino corretamente.

Clique no botão "Executar" para iniciar a pesquisa. O navegador será aberto e os resultados serão exibidos na área de resultado.

Os resultados da pesquisa também serão armazenados no banco de dados.

Para consultar resultados previamente pesquisados, selecione a opção "Consultar" e preencha os campos de origem e destino corretamente.

Clique no botão "Executar" para buscar os resultados no banco de dados. Os resultados serão exibidos na área de resultado.

Contribuição
Contribuições são bem-vindas! Se você deseja contribuir para este projeto, por favor, abra uma issue para discutir as alterações propostas ou submeta um pull request.

Licença
Este projeto está licenciado sob a MIT License.

Contato
Se você tiver alguma dúvida ou sugestão, sinta-se à vontade para entrar em contato:

Nome: Bruno de Carvalho
E-mail: bcarvalho.dev@gmail.com
