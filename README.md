# OpenSSH7_7

O OpenSSH Username Validator é um script em Python projetado para verificar a validade de nomes de usuário em um servidor OpenSSH. Ele utiliza a biblioteca ssh2-python para estabelecer conexões SSH e autenticar usuários.
Essa é uma versão atualizada do projeto: https://www.exploit-db.com/exploits/45939 
CVE-2018-15473

## Visão Geral

Este script verifica a validade de nomes de usuário em um servidor OpenSSH, tentando autenticar cada nome de usuário fornecido. Ele suporta a verificação de um único nome de usuário ou uma lista de nomes de usuários.

## Pré-requisitos

- Python 3.x
- Biblioteca ssh2-python
  - Você pode instalá-la usando: `pip install ssh2-python`

## Uso

### Sintaxe

```bash
sudo python3 openssh_username_validator.py [--port PORT] [--threads THREADS] [--outputFile OUTPUTFILE] [--outputFormat {list,json,csv}] (--username USERNAME | --userList USERLIST) hostname
```

### Opções

- `--port PORT`: Especifica a porta de destino (padrão: 22).
- `--threads THREADS`: Especifica o número de threads a serem usadas (padrão: 5).
- `--outputFile OUTPUTFILE`: Especifica o local do arquivo de saída.
- `--outputFormat {list,json,csv}`: Especifica o formato do arquivo de saída (padrão: list).
- `--username USERNAME`: Especifica o único nome de usuário a ser validado.
- `--userList USERLIST`: Especifica o arquivo contendo uma lista de nomes de usuários para enumeração.

### Exemplos

```bash
sudo python3 openssh_username_validator.py --username alice example.com
sudo python3 openssh_username_validator.py --userList users.txt example.com
```

## Formatos de Saída

O script fornece saída em diferentes formatos com base na opção `--outputFormat`:

- **List:** Formato de lista legível por humanos.
- **JSON:** Formato JSON.
- **CSV:** Formato de valores separados por vírgulas.

## Contribuição

Se desejar contribuir para este projeto, sinta-se à vontade para enviar solicitações de pull. Siga quaisquer diretrizes mencionadas na documentação de contribuição.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
