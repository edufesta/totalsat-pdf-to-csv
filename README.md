# PDF to CSV/Excel Converter

Este projeto converte arquivos PDF para CSV ou Excel, escolhendo automaticamente o melhor formato baseado no conteúdo do PDF.

## Recursos

- **Análise automática**: Analisa o conteúdo do PDF para determinar o melhor formato de saída
- **Detecção de tabelas**: Identifica e extrai tabelas estruturadas dos PDFs
- **Formato inteligente**: Escolhe entre CSV (para dados simples) ou Excel (para múltiplas tabelas)
- **Limpeza de dados**: Remove linhas/colunas vazias e formata os dados
- **Suporte a múltiplas páginas**: Processa PDFs com várias páginas

## Instalação

1. Clone ou baixe o projeto
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

### Converter todos os PDFs na pasta sourcePdfs

```bash
python pdf_converter.py
```

### Converter um arquivo específico

```bash
python pdf_converter.py "nome_do_arquivo.pdf"
```

## Estrutura de pastas

```
pdf2csv/
├── sourcePdfs/          # Coloque os arquivos PDF aqui
├── output/              # Arquivos convertidos aparecerão aqui
├── pdf_converter.py     # Script principal
├── requirements.txt     # Dependências
└── README.md           # Este arquivo
```

## Como funciona

1. **Análise**: O script analisa cada PDF para:
   - Detectar presença de tabelas
   - Contar número de tabelas e páginas
   - Verificar estrutura dos dados

2. **Decisão de formato**:
   - **CSV**: Para PDFs simples com poucas tabelas estruturadas
   - **Excel**: Para PDFs complexos com múltiplas tabelas ou várias páginas

3. **Extração e limpeza**:
   - Extrai tabelas usando pdfplumber
   - Remove linhas/colunas vazias
   - Formata cabeçalhos automaticamente

4. **Saída**:
   - Arquivos salvos na pasta `output/`
   - Nomes preservados do arquivo original
   - Logs detalhados do processo

## Dependências

- `pdfplumber`: Extração de dados de PDF
- `pandas`: Manipulação de dados
- `openpyxl`: Criação de arquivos Excel
- `tabula-py`: Extração alternativa de tabelas
- `camelot-py`: Extração avançada de tabelas

## Limitações

- Funciona melhor com PDFs que contêm tabelas estruturadas
- PDFs com texto puro podem não produzir resultados úteis
- Qualidade da extração depende da qualidade do PDF original

## Exemplos de uso

Para o arquivo `02 - Totalsat15.38.157474806731618454903.pdf` na pasta sourcePdfs:

```bash
# Converter apenas este arquivo
python pdf_converter.py "02 - Totalsat15.38.157474806731618454903.pdf"

# Ou converter todos os PDFs
python pdf_converter.py
```

O arquivo será analisado e convertido para o formato mais adequado (CSV ou Excel) na pasta `output/`.
