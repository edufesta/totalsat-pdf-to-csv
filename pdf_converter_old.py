import pdfplumber
import pandas as pd
import os
import sys
from pathlib import Path
import re
from typing import List, Dict, Tuple, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFConverter:
    def __init__(self, source_dir: str = "sourcePdfs", output_dir: str = "output"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def analyze_pdf_content(self, pdf_path: str) -> Dict:
        """Analisa o conteúdo do PDF para determinar o melhor formato de saída"""
        analysis = {
            'has_tables': False,
            'table_count': 0,
            'text_length': 0,
            'pages': 0,
            'structured_data': False,
            'recommended_format': 'csv'
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                analysis['pages'] = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages):
                    # Extrair texto
                    text = page.extract_text() or ""
                    analysis['text_length'] += len(text)
                    
                    # Tentar extrair tabelas
                    tables = page.extract_tables()
                    if tables:
                        analysis['has_tables'] = True
                        analysis['table_count'] += len(tables)
                        
                        # Verificar se as tabelas têm estrutura consistente
                        for table in tables:
                            if len(table) > 1 and len(set(len(row) for row in table)) == 1:
                                analysis['structured_data'] = True
                
                # Determinar formato recomendado
                if analysis['table_count'] > 3 or (analysis['has_tables'] and analysis['pages'] > 2):
                    analysis['recommended_format'] = 'excel'
                elif analysis['has_tables'] and analysis['structured_data']:
                    analysis['recommended_format'] = 'csv'
                else:
                    analysis['recommended_format'] = 'csv'
                    
        except Exception as e:
            logger.error(f"Erro ao analisar PDF {pdf_path}: {e}")
            
        return analysis
    
    def extract_tables_from_pdf(self, pdf_path: str) -> List[pd.DataFrame]:
        """Extrai tabelas do PDF usando pdfplumber"""
        dataframes = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    
                    for table_num, table in enumerate(tables):
                        if table and len(table) > 0:
                            # Converter tabela para DataFrame
                            # Usar primeira linha como cabeçalho se parecer cabeçalho
                            if len(table) > 1:
                                # Verificar se primeira linha parece ser cabeçalho
                                first_row = table[0]
                                if all(isinstance(cell, str) and cell and not re.match(r'^\d+\.?\d*$', cell.strip()) for cell in first_row if cell):
                                    df = pd.DataFrame(table[1:], columns=first_row)
                                else:
                                    df = pd.DataFrame(table)
                            else:
                                df = pd.DataFrame(table)
                            
                            # Limpar DataFrame
                            df = self.clean_dataframe(df)
                            
                            if not df.empty:
                                df.name = f"Página_{page_num+1}_Tabela_{table_num+1}"
                                dataframes.append(df)
                                
        except Exception as e:
            logger.error(f"Erro ao extrair tabelas do PDF {pdf_path}: {e}")
            
        return dataframes
    
    def extract_text_as_table(self, pdf_path: str) -> List[pd.DataFrame]:
        """Extrai texto e tenta estruturar como tabela baseado em padrões"""
        dataframes = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                all_lines = []
                header_found = None
                
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        lines = text.split('\n')
                        
                        for line in lines:
                            line = line.strip()
                            if not line:
                                continue
                                
                            # Detectar cabeçalho comum
                            if 'Data/Hora' in line and 'Placa' in line:
                                if not header_found:
                                    header_found = line
                                continue
                            
                            # Detectar linhas de dados (começam com data)
                            if re.match(r'\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}', line):
                                all_lines.append(line)
                
                if all_lines and header_found:
                    # Processar cabeçalho
                    headers = self._parse_header(header_found)
                    
                    # Processar dados
                    data_rows = []
                    for line in all_lines:
                        row = self._parse_data_line(line, len(headers))
                        if row:
                            data_rows.append(row)
                    
                    if data_rows:
                        df = pd.DataFrame(data_rows, columns=headers)
                        df = self.clean_dataframe(df)
                        
                        if not df.empty:
                            df.name = "Dados_Rastreamento"
                            dataframes.append(df)
                
        except Exception as e:
            logger.error(f"Erro ao extrair texto como tabela do PDF {pdf_path}: {e}")
            
        return dataframes
    
    def _parse_header(self, header_line: str) -> List[str]:
        """Parse do cabeçalho para identificar colunas"""
        # Para o formato específico: Data/Hora Placa Evento Vel Localidade Motorista
        if 'Data/Hora' in header_line:
            return ['Data/Hora', 'Placa', 'Evento', 'Velocidade', 'Localidade', 'Motorista']
        
        # Fallback genérico
        return re.split(r'\s{2,}', header_line.strip())
    
    def _parse_data_line(self, line: str, expected_cols: int) -> List[str]:
        """Parse de uma linha de dados"""
        try:
            # Padrão específico para dados de rastreamento
            # Formato: DD/MM/YYYY HH:MM PLACA EVENTO VEL LOCALIDADE...
            
            # Extrair data/hora (primeiro grupo)
            date_match = re.match(r'(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})', line)
            if not date_match:
                return None
                
            date_time = date_match.group(1)
            remaining = line[len(date_time):].strip()
            
            # Usar regex para capturar o padrão completo
            # Padrão: PLACA EVENTO VELOCIDADE LOCALIDADE
            pattern = r'^(\S+\s+\d+)\s+(.*?)\s+(\d+)\s+(.+)$'
            match = re.match(pattern, remaining)
            
            if match:
                placa = match.group(1)
                evento = match.group(2)
                velocidade = match.group(3)
                localidade = match.group(4)
                motorista = ''  # Campo vazio conforme o PDF
                
                return [date_time, placa, evento, velocidade, localidade, motorista]
            else:
                # Fallback - dividir por espaços e tentar agrupar
                tokens = remaining.split()
                if len(tokens) >= 3:
                    # Primeiro token + número = placa (ex: "AZU 8900")
                    placa = f"{tokens[0]} {tokens[1]}" if len(tokens) > 1 else tokens[0]
                    
                    # Encontrar onde começa a velocidade (primeiro número isolado)
                    vel_index = -1
                    for i, token in enumerate(tokens[2:], 2):
                        if re.match(r'^\d+$', token):
                            vel_index = i
                            break
                    
                    if vel_index > 0:
                        evento = ' '.join(tokens[2:vel_index])
                        velocidade = tokens[vel_index]
                        localidade = ' '.join(tokens[vel_index+1:]) if vel_index+1 < len(tokens) else ''
                    else:
                        evento = ' '.join(tokens[2:-1]) if len(tokens) > 3 else tokens[2] if len(tokens) > 2 else ''
                        velocidade = '0'
                        localidade = tokens[-1] if tokens else ''
                    
                    motorista = ''
                    
                    return [date_time, placa, evento, velocidade, localidade, motorista]
            
        except Exception as e:
            logger.warning(f"Erro ao processar linha: {line[:50]}... - {e}")
            return None
        """Extrai tabelas do PDF usando pdfplumber"""
        dataframes = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    
                    for table_num, table in enumerate(tables):
                        if table and len(table) > 0:
                            # Converter tabela para DataFrame
                            # Usar primeira linha como cabeçalho se parecer cabeçalho
                            if len(table) > 1:
                                # Verificar se primeira linha parece ser cabeçalho
                                first_row = table[0]
                                if all(isinstance(cell, str) and cell and not re.match(r'^\d+\.?\d*$', cell.strip()) for cell in first_row if cell):
                                    df = pd.DataFrame(table[1:], columns=first_row)
                                else:
                                    df = pd.DataFrame(table)
                            else:
                                df = pd.DataFrame(table)
                            
                            # Limpar DataFrame
                            df = self.clean_dataframe(df)
                            
                            if not df.empty:
                                df.name = f"Página_{page_num+1}_Tabela_{table_num+1}"
                                dataframes.append(df)
                                
        except Exception as e:
            logger.error(f"Erro ao extrair tabelas do PDF {pdf_path}: {e}")
            
        return dataframes
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpa e formata o DataFrame"""
        # Remover linhas completamente vazias
        df = df.dropna(how='all')
        
        # Remover colunas completamente vazias
        df = df.dropna(axis=1, how='all')
        
        # Limpar espaços em branco
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
                # Substituir strings vazias ou 'None' por NaN
                df[col] = df[col].replace(['', 'None', 'nan', 'NaN'], pd.NA)
        
        return df
    
    def save_to_csv(self, dataframes: List[pd.DataFrame], output_path: str):
        """Salva DataFrames em arquivo CSV"""
        if len(dataframes) == 1:
            # Um único DataFrame
            dataframes[0].to_csv(output_path, index=False, encoding='utf-8-sig')
        else:
            # Múltiplos DataFrames - concatenar ou salvar separadamente
            if len(dataframes) > 1:
                # Tentar concatenar se tiverem estrutura similar
                try:
                    if all(len(df.columns) == len(dataframes[0].columns) for df in dataframes):
                        combined_df = pd.concat(dataframes, ignore_index=True)
                        combined_df.to_csv(output_path, index=False, encoding='utf-8-sig')
                    else:
                        # Salvar separadamente
                        base_path = output_path.rsplit('.', 1)[0]
                        for i, df in enumerate(dataframes):
                            df.to_csv(f"{base_path}_parte_{i+1}.csv", index=False, encoding='utf-8-sig')
                except Exception as e:
                    logger.warning(f"Erro ao concatenar DataFrames: {e}")
                    # Salvar separadamente como fallback
                    base_path = output_path.rsplit('.', 1)[0]
                    for i, df in enumerate(dataframes):
                        df.to_csv(f"{base_path}_parte_{i+1}.csv", index=False, encoding='utf-8-sig')
    
    def save_to_excel(self, dataframes: List[pd.DataFrame], output_path: str):
        """Salva DataFrames em arquivo Excel"""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            if len(dataframes) == 1:
                dataframes[0].to_excel(writer, sheet_name='Dados', index=False)
            else:
                for i, df in enumerate(dataframes):
                    sheet_name = getattr(df, 'name', f'Tabela_{i+1}')[:31]  # Excel sheet name limit
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    def convert_pdf(self, pdf_file: str) -> Dict:
        """Converte um arquivo PDF específico"""
        pdf_path = self.source_dir / pdf_file
        
        if not pdf_path.exists():
            return {'success': False, 'error': f'Arquivo {pdf_file} não encontrado'}
        
        logger.info(f"Processando: {pdf_file}")
        
        # Analisar conteúdo
        analysis = self.analyze_pdf_content(pdf_path)
        logger.info(f"Análise do PDF: {analysis}")
        
        # Extrair dados
        dataframes = self.extract_tables_from_pdf(pdf_path)
        
        # Se não encontrou tabelas, tentar extrair texto estruturado
        if not dataframes:
            logger.info("Nenhuma tabela encontrada, tentando extrair dados do texto...")
            dataframes = self.extract_text_as_table(pdf_path)
        
        if not dataframes:
            return {
                'success': False, 
                'error': 'Nenhuma tabela ou dados estruturados encontrados no PDF',
                'analysis': analysis
            }
        
        # Determinar nome do arquivo de saída
        base_name = pdf_file.rsplit('.', 1)[0]
        
        # Salvar no formato recomendado
        try:
            if analysis['recommended_format'] == 'excel':
                output_file = f"{base_name}.xlsx"
                output_path = self.output_dir / output_file
                self.save_to_excel(dataframes, output_path)
            else:
                output_file = f"{base_name}.csv"
                output_path = self.output_dir / output_file
                self.save_to_csv(dataframes, output_path)
            
            return {
                'success': True,
                'input_file': pdf_file,
                'output_file': str(output_path),
                'format': analysis['recommended_format'],
                'tables_found': len(dataframes),
                'analysis': analysis
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro ao salvar arquivo: {e}',
                'analysis': analysis
            }
    
    def convert_all_pdfs(self) -> List[Dict]:
        """Converte todos os PDFs na pasta source"""
        results = []
        
        if not self.source_dir.exists():
            logger.error(f"Diretório {self.source_dir} não existe")
            return results
        
        pdf_files = list(self.source_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning("Nenhum arquivo PDF encontrado")
            return results
        
        for pdf_file in pdf_files:
            result = self.convert_pdf(pdf_file.name)
            results.append(result)
            
            if result['success']:
                logger.info(f"✓ Convertido: {result['input_file']} → {result['output_file']} ({result['format']})")
            else:
                logger.error(f"✗ Erro: {pdf_file.name} - {result['error']}")
        
        return results

def main():
    """Função principal"""
    converter = PDFConverter()
    
    if len(sys.argv) > 1:
        # Converter arquivo específico
        pdf_file = sys.argv[1]
        result = converter.convert_pdf(pdf_file)
        
        if result['success']:
            print(f"Arquivo convertido com sucesso!")
            print(f"Entrada: {result['input_file']}")
            print(f"Saída: {result['output_file']}")
            print(f"Formato: {result['format']}")
            print(f"Tabelas encontradas: {result['tables_found']}")
        else:
            print(f"Erro na conversão: {result['error']}")
    else:
        # Converter todos os PDFs
        results = converter.convert_all_pdfs()
        
        if results:
            success_count = sum(1 for r in results if r['success'])
            print(f"\nResumo:")
            print(f"Total de arquivos: {len(results)}")
            print(f"Convertidos com sucesso: {success_count}")
            print(f"Erros: {len(results) - success_count}")
        else:
            print("Nenhum arquivo PDF encontrado para converter.")

if __name__ == "__main__":
    main()
