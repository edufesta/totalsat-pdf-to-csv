#!/usr/bin/env python3
"""
Script de teste para validar a correção de quebras de linha em PDFs
"""

import pandas as pd
import os
from pathlib import Path

def test_csv_coordinates(csv_file):
    """Testa se um arquivo CSV tem coordenadas completas"""
    try:
        df = pd.read_csv(csv_file)
        
        # Verificar se existe a coluna Localidade
        if 'Localidade' not in df.columns:
            return {'status': 'erro', 'message': 'Coluna Localidade não encontrada'}
        
        # Contar linhas com coordenadas incompletas (terminam com vírgula ou traço)
        incomplete_coords = 0
        total_coords = 0
        
        for idx, location in enumerate(df['Localidade']):
            if pd.isna(location):
                continue
                
            location_str = str(location)
            
            # Se contém parênteses, deve ter coordenadas
            if '(' in location_str:
                total_coords += 1
                
                # Verificar se termina com padrões incompletos
                if (location_str.endswith(',-') or 
                    location_str.endswith(',') or 
                    location_str.endswith('(-') or
                    not location_str.endswith(')')):
                    incomplete_coords += 1
                    if incomplete_coords <= 3:  # Mostrar apenas as primeiras 3
                        print(f"  Linha {idx+2}: {location_str[:80]}...")
        
        return {
            'status': 'sucesso',
            'total_coordinates': total_coords,
            'incomplete_coordinates': incomplete_coords,
            'accuracy': ((total_coords - incomplete_coords) / total_coords * 100) if total_coords > 0 else 100
        }
        
    except Exception as e:
        return {'status': 'erro', 'message': str(e)}

def main():
    """Testa todos os arquivos CSV na pasta output"""
    output_dir = Path('output')
    
    if not output_dir.exists():
        print("Pasta 'output' não encontrada!")
        return
    
    csv_files = list(output_dir.glob("*.csv"))
    
    if not csv_files:
        print("Nenhum arquivo CSV encontrado na pasta output!")
        return
    
    print(f"Testando {len(csv_files)} arquivos CSV...\n")
    
    total_files = 0
    successful_files = 0
    
    for csv_file in csv_files:
        print(f"📄 {csv_file.name}")
        result = test_csv_coordinates(csv_file)
        
        total_files += 1
        
        if result['status'] == 'sucesso':
            successful_files += 1
            coords = result['total_coordinates']
            incomplete = result['incomplete_coordinates']
            accuracy = result['accuracy']
            
            if incomplete == 0:
                print(f"  ✅ Perfeito! {coords} coordenadas, 100% completas")
            else:
                print(f"  ⚠️  {coords} coordenadas, {incomplete} incompletas ({accuracy:.1f}% de precisão)")
        else:
            print(f"  ❌ Erro: {result['message']}")
        
        print()
    
    print(f"📊 Resumo: {successful_files}/{total_files} arquivos processados com sucesso")

if __name__ == "__main__":
    main()
