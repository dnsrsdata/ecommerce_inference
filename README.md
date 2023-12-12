### Sobre o problema

O SISU é um evento esperado por muitos estudantes que desejam ingressar em uma 
universidade pública. O processo seletivo é realizado duas vezes ao ano, no 
início de cada semestre letivo, e utiliza a nota do ENEM como critério de 
seleção. 

Dado ao número alto de participantes, um dos principais questionamentos que toma 
conta dos estudantes é: "Será que minha nota é o suficiente?".

### Objetivo

Como objetivo inicial, é necessário a criação de um relatório que apresente
informações probabilísticas sobre o processo seletivo do SISU. O relatório deve
passar por tópicos como: turno, cotas, grau, etc.

Como objetivo final, é necessário a criação de um modelo de aprendizado de
máquina que seja capaz de prever a probabilidade do estudante de ser aprovado 
nos cursos que ele escolheu. Também é necessário realizar o deploy do modelo em
conjunto com um relatório sobre as universidades e cursos.

### Sobre os dados

Os dados utilizados foram obtidos através do portal de dados abertos do governo
federal. Os dados são referentes ao SISU 2022.1.

### Métricas de avaliação

Como o interesse é a probabilidade de aprovação, a métrica de avaliação será a
**Log Loss**.

### Melhorias

[⌛] Testar mais hiperparâmetros

[⌛] Realizar o deploy do modelo

[⌛] Criar um relatório sobre as universidades e cursos

### Instruções para execução do projeto

Siga os seguintes passos para rodar o projeto localmente:

1. Clone o repositório:
```sh
git clone https://github.com/dnsrsdata/sisu_analysis
```
2. Crie um ambiente virtual:
```sh
python -m venv venv
```
3. Ative o ambiente virtual de acordo com o seu sistema operacional.

4. Instale as dependências:
```sh
pip install -r requirements.txt
```

### Descrição dos arquivos


### Resultados

A análise probabilística pode ser conferida no pdf ```SISU com Dados.pdf``` na pasta
relatorio.