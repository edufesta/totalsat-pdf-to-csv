import pdfplumber
import re
from pathlib import Path

def examine_pdf(pdf_path):
    """Examina o conteúdo de um PDF para entender sua estrutura"""
    
    print(f"\n=== Análise do PDF: {pdf_path} ===\n")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Número de páginas: {len(pdf.pages)}")
            
            # Examinar as primeiras páginas
            for page_num in range(min(3, len(pdf.pages))):
                page = pdf.pages[page_num]
                print(f"\n--- Página {page_num + 1} ---")
                
                # Extrair texto
                text = page.extract_text()
                if text:
                    lines = text.split('\n')[:10]  # Primeiras 10 linhas
                    print("Primeiras linhas:")
                    for i, line in enumerate(lines, 1):
                        print(f"{i:2d}: {line}")
                    
                    # Estatísticas do texto
                    print(f"\nEstatísticas da página {page_num + 1}:")
                    print(f"- Linhas de texto: {len(text.split(chr(10)))}")
                    print(f"- Caracteres: {len(text)}")
                    
                    # Procurar padrões de dados
                    dates = re.findall(r'\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}', text)
                    numbers = re.findall(r'\d+[.,]\d+', text)
                    money = re.findall(r'R\$\s*\d+[.,]?\d*', text)
                    
                    print(f"- Padrões encontrados:")
                    print(f"  * Datas: {len(dates)} (ex: {dates[:3] if dates else 'nenhuma'})")
                    print(f"  * Números decimais: {len(numbers)} (ex: {numbers[:3] if numbers else 'nenhum'})")
                    print(f"  * Valores monetários: {len(money)} (ex: {money[:3] if money else 'nenhum'})")
                
                # Tentar extrair tabelas
                tables = page.extract_tables()
                if tables:
                    print(f"- Tabelas encontradas: {len(tables)}")
                    for i, table in enumerate(tables):
                        print(f"  Tabela {i+1}: {len(table)} linhas, {len(table[0]) if table else 0} colunas")
                else:
                    print("- Nenhuma tabela encontrada")
                
                print("-" * 50)
                
    except Exception as e:
        print(f"Erro ao examinar PDF: {e}")

if __name__ == "__main__":
    pdf_path = Path("sourcePdfs/02 - Totalsat15.38.157474806731618454903.pdf")
    examine_pdf(pdf_path)
