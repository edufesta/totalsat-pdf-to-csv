#!/usr/bin/env python3
"""
Script de exemplo para usar o conversor PDF to CSV/Excel
"""

from pdf_converter import PDFConverter
from pathlib import Path

def example_usage():
    """Exemplos de uso do conversor"""
    
    print("=== Conversor PDF para CSV/Excel ===\n")
    
    # Criar instância do conversor
    converter = PDFConverter()
    
    # Verificar se existem PDFs na pasta
    pdf_files = list(converter.source_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ Nenhum arquivo PDF encontrado na pasta 'sourcePdfs'")
        print("💡 Coloque seus arquivos PDF na pasta 'sourcePdfs' e execute novamente.")
        return
    
    print(f"📁 Encontrados {len(pdf_files)} arquivo(s) PDF:")
    for pdf_file in pdf_files:
        print(f"   - {pdf_file.name}")
    
    print("\n🔄 Iniciando conversão...\n")
    
    # Converter todos os PDFs
    results = converter.convert_all_pdfs()
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE CONVERSÃO")
    print("="*60)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ Conversões bem-sucedidas: {len(successful)}")
    print(f"❌ Erros: {len(failed)}")
    print(f"📈 Taxa de sucesso: {len(successful)/len(results)*100:.1f}%")
    
    if successful:
        print("\n📄 Arquivos gerados:")
        for result in successful:
            print(f"   ✓ {result['input_file']}")
            print(f"     → {result['output_file']} ({result['format'].upper()})")
            print(f"     📊 {result['tables_found']} tabela(s) extraída(s)")
            
            # Verificar tamanho do arquivo
            output_path = Path(result['output_file'])
            if output_path.exists():
                if result['format'] == 'csv':
                    # Contar linhas do CSV
                    with open(output_path, 'r', encoding='utf-8-sig') as f:
                        lines = sum(1 for _ in f)
                    print(f"     📏 {lines-1} registros de dados")
                else:
                    # Para Excel, mostrar tamanho do arquivo
                    size_mb = output_path.stat().st_size / (1024 * 1024)
                    print(f"     📏 {size_mb:.1f} MB")
            print()
    
    if failed:
        print("\n❌ Erros encontrados:")
        for result in failed:
            print(f"   ✗ {result.get('input_file', 'Arquivo desconhecido')}")
            print(f"     🚫 {result['error']}")
            print()
    
    print("\n💡 Dicas:")
    print("   • Os arquivos convertidos estão na pasta 'output'")
    print("   • CSV é recomendado para dados simples e análise")
    print("   • Excel é usado para PDFs com múltiplas tabelas complexas")
    print("   • O conversor detecta automaticamente o melhor formato")

if __name__ == "__main__":
    example_usage()
