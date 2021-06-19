# Rastreador de Pacotes

Prova conceitual de aquisição de dados de rastreio a partir do site dos Correios BR.

Uma requisição ao site oficial é feita com o código de rastreio e o parsing do site retornado é feito com a biblioteca
BeautifulSoup para imprimir as informações do código no console.

### Falta validar:
* Inserção de vários códigos;
* Identificar quando o código de rastreio não retorna resultados.

### Possíveis implementações:
#### Bot de Telegram:
Um bot onde os códigos são cadastrados e a cada atualização o usuário é notificado via mensagem.

#### Análise dos códigos próximos:
Os códigos de rastreio são gerados em uma certa ordem, dessa forma, a partir de um código é possível gerar outros códigos
que em teoria foram criados próximo do original. Assim, no caso de importações, é possível visualizar se estes códigos
próximos já chegaram no Brasil e se já foram liberados da fiscalização. No fim das contas não é nada preciso, serve só
como curiosidade.