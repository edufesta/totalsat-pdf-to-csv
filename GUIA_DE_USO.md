# Guia de Uso - Conversor PDF para CSV/Excel

## ✨ Sobre o Projeto

Este conversor foi criado para transformar arquivos PDF em formatos estruturados (CSV ou Excel), escolhendo automaticamente o formato mais adequado baseado no conteúdo do PDF.

## 🎯 Características Principais

- **Análise automática**: Determina o melhor formato de saída (CSV ou Excel)
- **Extração inteligente**: Detecta tabelas estruturadas e dados tabulares em texto
- **Limpeza de dados**: Remove linhas/colunas vazias e formata automaticamente
- **Suporte múltiplo**: Processa PDFs com uma ou várias páginas
- **Logging detalhado**: Acompanhe o processo de conversão

## 📋 Formatos Suportados

### Entrada
- **PDF**: Qualquer arquivo PDF com dados tabulares

### Saída
- **CSV**: Para dados simples e análise (recomendado para dados de rastreamento, relatórios lineares)
- **Excel**: Para PDFs complexos com múltiplas tabelas ou mais de 3 tabelas

## 🚀 Como Usar

### Método 1: Converter todos os PDFs
```bash
python3 pdf_converter.py
```

### Método 2: Converter um arquivo específico
```bash
python3 pdf_converter.py "nome_do_arquivo.pdf"
```

### Método 3: Usar o script de exemplo (recomendado)
```bash
python3 example.py
```

## 📁 Estrutura de Pastas

```
pdf2csv/
├── sourcePdfs/          # 📥 Coloque os PDFs aqui
├── output/              # 📤 Arquivos convertidos aparecem aqui
├── pdf_converter.py     # 🔧 Script principal
├── example.py           # 📖 Script de exemplo com relatório
├── requirements.txt     # 📦 Dependências
└── README.md           # 📚 Este guia
```

## 🔧 Instalação

1. **Instalar dependências**:
```bash
pip3 install -r requirements.txt
```

2. **Colocar PDFs na pasta sourcePdfs**:
```bash
# Criar pasta se não existir
mkdir -p sourcePdfs

# Copiar seus PDFs
cp meu_arquivo.pdf sourcePdfs/
```

3. **Executar conversão**:
```bash
python3 pdf_converter.py
```

## 📊 Exemplo Real

Para o arquivo `02 - Totalsat15.38.157474806731618454903.pdf` (dados de rastreamento):

**Entrada**: PDF com 99 páginas, 414.544 caracteres
**Processo**: Detectou dados de rastreamento em formato tabular
**Saída**: CSV com 4.401 registros estruturados

**Colunas extraídas**:
- Data/Hora
- Placa
- Evento
- Velocidade
- Localidade
- Motorista

## 🎯 Tipos de PDF Suportados

### ✅ Funcionam Bem
- Relatórios de rastreamento de veículos
- Extratos bancários estruturados
- Relatórios de vendas em formato tabular
- Listagens com dados organizados em colunas
- PDFs com padrões de data/hora, números, coordenadas

### ⚠️ Limitações
- PDFs puramente textuais sem estrutura tabular
- Imagens escaneadas (necessário OCR)
- PDFs com formatação muito complexa
- Tabelas desalinhadas ou mal formatadas

## 🛠️ Personalização

### Adicionar Novos Formatos de Dados

Para suportar novos tipos de dados, edite a função `_parse_data_line()` em `pdf_converter.py`:

```python
def _parse_data_line(self, line: str, expected_cols: int) -> List[str]:
    # Adicione seus padrões específicos aqui
    # Exemplo para novos formatos de data:
    if re.match(r'\d{4}-\d{2}-\d{2}', line):  # formato YYYY-MM-DD
        # Seu código de parsing aqui
        pass
```

### Modificar Cabeçalhos

Edite a função `_parse_header()` para suportar novos tipos de cabeçalhos:

```python
def _parse_header(self, header_line: str) -> List[str]:
    if 'Seu_Campo_Especifico' in header_line:
        return ['Campo1', 'Campo2', 'Campo3']
```

## 🐛 Solução de Problemas

### Erro: "Nenhuma tabela encontrada"
- **Causa**: PDF não tem dados em formato tabular estruturado
- **Solução**: Verifique se o PDF contém dados organizados em colunas

### Erro: "Dados extraídos incorretamente"
- **Causa**: Padrão de dados não reconhecido
- **Solução**: Ajuste a função `_parse_data_line()` para seu formato específico

### Erro: "Arquivo muito grande"
- **Causa**: PDF com muitas páginas pode demorar
- **Solução**: Aguarde ou processe páginas específicas

## 📈 Métricas de Performance

Para o exemplo testado:
- **Arquivo**: 99 páginas PDF
- **Tempo**: ~30 segundos
- **Dados extraídos**: 4.401 registros
- **Taxa de sucesso**: 100%

## 🤝 Contribuição

Para melhorar o conversor:

1. **Adicione suporte para novos formatos** editando as funções de parsing
2. **Melhore a detecção de padrões** na função `analyze_pdf_content()`
3. **Otimize a performance** para PDFs grandes

## 📞 Suporte

O conversor inclui logging detalhado. Em caso de problemas:

1. Verifique os logs no terminal
2. Examine o arquivo `examine_pdf.py` para entender a estrutura do seu PDF
3. Ajuste as funções de parsing conforme necessário

## 🏆 Casos de Sucesso

- ✅ Dados de rastreamento de frotas
- ✅ Relatórios de sensores IoT
- ✅ Extratos de movimentação financeira
- ✅ Logs de sistema em formato tabular
- ✅ Relatórios de vendas estruturados

---

**Desenvolvido com ❤️ para facilitar a conversão de PDFs em dados estruturados**
