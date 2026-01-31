# Alite

O **Alite** é um motor de processamento desenvolvido em Python que utiliza um mecanismo de diálogo baseado em padrões e busca por similaridade para criar interações inteligentes e dinâmicas. 

Ao contrário das IAs generativas, o chatbot criado via Alite **não pensa, ele processa**. Ele utiliza um banco de dados de perguntas e respostas para garantir que cada interação seja controlada, extremamente rápida e 100% livre de alucinações.

---

## Por que usar o Alite?

O Alite surgiu da necessidade de uma solução determinística. Enquanto modelos generativos podem ser imprevisíveis e pesados, o Alite oferece:
- **Precisão:** Respostas fiéis ao que foi treinado.
- **Leveza:** Roda em qualquer hardware<sup>[1]</sup> com Python.
- **Privacidade:** Processamento totalmente offline através de arquivos `.PTC`.

---

## Como usar

### 1. Preparação
Baixe os scripts `main.py` e `export.py` (disponíveis na pasta `/src`) ou faça o download do pacote completo `AlitePyUtils.zip` e extraia-o em sua pasta de trabalho.

### 2. Obtendo um Dataset
O "cérebro" do Alite é o arquivo **.PTC**, uma sigla para "Pre-Trained Chatbot". Você tem duas opções:
* **Baixar:** Encontre modelos prontos na pasta `/dataset`.
* **Criar:** Siga as instruções abaixo para treinar seu próprio modelo.

---

## Criando um Dataset .PTC

Para criar seu próprio conhecimento, você precisará do script `export.py` e de um arquivo de texto bruto (ex: `train.txt`).

### A. O Cabeçalho (Configuração)
A primeira linha do seu arquivo de texto define a identidade do bot:

```text
!# Name: '<NomeDoBot>' | ModelName: '<VersãoDoModelo>'

```

* **Name:** O nome que aparecerá no prompt de conversa.
* **ModelName:** A versão técnica (Ex: `ACBSV-1 BRP`).
* *Nota: Se omitido, o padrão será `Chatbot | Generic Chatbot Model v?`.*

### B. Instruções e Respostas

Defina os gatilhos (perguntas) e as possíveis saídas (respostas):

```text
> Olá | Oi | E aí?
- Olá! Como posso ajudar?
- Oi! Tudo bem por aqui.
- Opa! Em que posso ser útil?

```

* Use `|` para separar variações da mesma pergunta.
* Use `-` para listar diferentes respostas (o motor escolherá uma aleatoriamente).
* Sempre quebre uma linha antes de inserir o -.
* 
### C. Exportação

Com o arquivo pronto, execute o exportador no terminal:

```batch
python export.py train.txt

```

Isso gerará o seu arquivo `.PTC` pronto para ser usado pelo motor.

---

## Licença

Este repositório usa a licença MIT.

```

## Notas


[1]: Qualquer hardware que tenha capacidade de rodar Python, o motor e o dataset.
