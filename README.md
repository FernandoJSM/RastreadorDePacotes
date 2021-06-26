# Rastreador de Pacotes

Prova conceitual de aquisição de dados de rastreio a partir do site dos Correios BR.

Uma requisição ao site oficial é feita com o código de rastreio e o parsing do site retornado é feito com a biblioteca
BeautifulSoup para imprimir as informações do código no console.

O código de rastreamento deve seguir o formato AA000000000AA, conforme o padrão 
[UPU Standard](https://en.wikipedia.org/wiki/S10_(UPU_standard)).

### ALGORITMOS:
singe_code.py: Resultado de apenas um código de rastreio, listando todos os eventos do pacote.

multiple_codes.py: Resultado de até 50 códigos de rastreio, listando o último evento de cada código.

### Possíveis implementações:
#### Bot de Telegram:
Um bot onde os códigos são cadastrados e a cada atualização o usuário é notificado via mensagem.
Um ótimo exemplo é o [RastreioBot](https://github.com/GabrielRF/RastreioBot), que inclusive tem várias funcionalidades
implementadas.

#### Análise dos códigos próximos:
Os códigos de rastreio são gerados em uma certa ordem, dessa forma, a partir de um código é possível gerar outros códigos
que em teoria foram criados próximo do original. Assim, no caso de importações, é possível visualizar se estes códigos
próximos já chegaram no Brasil e se já foram liberados da fiscalização. No fim das contas não é nada preciso, serve só
como curiosidade.