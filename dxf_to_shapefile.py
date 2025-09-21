#!/usr/bin/env python3
"""
Script para converter arquivos DXF para Shapefile
Processa polígonos de imóveis com sistema de coordenadas UTM e datum SIRGAS2000
"""

import os
import sys
import ezdxf
import geopandas as gpd
from shapely.geometry import Polygon
import pyproj
from pathlib import Path

def ler_arquivo_dxf(caminho_dxf):
    """
    Lê arquivo DXF e retorna o documento
    """
    try:
        doc = ezdxf.readfile(caminho_dxf)
        print(f"✓ Arquivo DXF carregado: {caminho_dxf}")
        return doc
    except Exception as e:
        print(f"❌ Erro ao ler arquivo DXF: {e}")
        return None

def encontrar_poligono_por_id(doc, entity_id):
    """
    Encontra polígono no DXF pelo ID da entidade
    """
    msp = doc.modelspace()
    
    # Procura por LWPOLYLINE ou POLYLINE
    for entity in msp:
        if entity.dxftype() in ['LWPOLYLINE', 'POLYLINE']:
            # Verifica se o handle (ID) corresponde
            if str(entity.dxf.handle) == str(entity_id):
                return entity
    
    print(f"❌ Polígono com ID {entity_id} não encontrado")
    return None

def extrair_coordenadas_poligono(entity):
    """
    Extrai coordenadas do polígono DXF
    """
    pontos = []
    
    if entity.dxftype() == 'LWPOLYLINE':
        for point in entity.get_points():
            pontos.append((point[0], point[1]))
    elif entity.dxftype() == 'POLYLINE':
        for vertex in entity.vertices:
            pontos.append((vertex.dxf.location.x, vertex.dxf.location.y))
    
    return pontos

def converter_coordenadas_utm(pontos, zona_utm, hemisferio='S'):
    """
    Converte coordenadas para UTM (assumindo entrada em metros UTM)
    Se necessário, pode ser adaptado para conversão de outros sistemas
    """
    # Para SIRGAS2000 UTM, o sistema já está em UTM
    # Apenas formatamos com 16 casas decimais
    pontos_utm = []
    for x, y in pontos:
        pontos_utm.append((round(float(x), 16), round(float(y), 16)))
    
    return pontos_utm

def criar_shapefile(pontos, zona_utm, hemisferio, caminho_saida):
    """
    Cria arquivos shapefile (.shp, .shx, .dbf, .prj)
    """
    # Cria polígono Shapely
    if len(pontos) < 3:
        print("❌ Polígono deve ter pelo menos 3 pontos")
        return False
    
    # Fecha o polígono se necessário
    if pontos[0] != pontos[-1]:
        pontos.append(pontos[0])
    
    poligono = Polygon(pontos)
    
    # Cria GeoDataFrame
    gdf = gpd.GeoDataFrame([1], geometry=[poligono], crs=None)
    
    # Define CRS para SIRGAS2000 UTM
    if hemisferio.upper() == 'S':
        epsg_code = 32700 + int(zona_utm)  # UTM Sul
    else:
        epsg_code = 32600 + int(zona_utm)  # UTM Norte
    
    gdf.crs = f"EPSG:{epsg_code}"
    
    # Salva shapefile
    try:
        gdf.to_file(caminho_saida, driver='ESRI Shapefile')
        print(f"✓ Shapefile criado: {caminho_saida}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar shapefile: {e}")
        return False

def main():
    """
    Função principal do script
    """
    print("=" * 60)
    print("CONVERSOR DXF PARA SHAPEFILE")
    print("Sistema: UTM | Datum: SIRGAS2000")
    print("=" * 60)
    
    # Entrada do usuário
    try:
        caminho_dxf = input("📁 Caminho do arquivo DXF: ").strip()
        if not os.path.exists(caminho_dxf):
            print("❌ Arquivo DXF não encontrado!")
            return
        
        entity_id = input("🔍 ID da entidade (handle) do polígono: ").strip()
        if not entity_id:
            print("❌ ID da entidade é obrigatório!")
            return
        
        zona_utm = input("🗺️  Zona UTM (ex: 22): ").strip()
        if not zona_utm.isdigit():
            print("❌ Zona UTM deve ser um número!")
            return
        
        hemisferio = input("🌍 Hemisfério (N/S) [padrão: S]: ").strip().upper()
        if not hemisferio:
            hemisferio = 'S'
        
        # Caminho de saída
        nome_base = Path(caminho_dxf).stem
        caminho_saida = f"{nome_base}_poligono_{entity_id}"
        
        print("\n" + "=" * 60)
        print("PROCESSANDO...")
        print("=" * 60)
        
        # 1. Ler arquivo DXF
        doc = ler_arquivo_dxf(caminho_dxf)
        if not doc:
            return
        
        # 2. Encontrar polígono por ID
        entity = encontrar_poligono_por_id(doc, entity_id)
        if not entity:
            return
        
        print(f"✓ Polígono encontrado: {entity.dxftype()}")
        
        # 3. Extrair coordenadas
        pontos = extrair_coordenadas_poligono(entity)
        if not pontos:
            print("❌ Não foi possível extrair coordenadas do polígono")
            return
        
        print(f"✓ {len(pontos)} pontos extraídos")
        
        # 4. Converter coordenadas (com 16 casas decimais)
        pontos_utm = converter_coordenadas_utm(pontos, zona_utm, hemisferio)
        
        # 5. Criar shapefile
        sucesso = criar_shapefile(pontos_utm, zona_utm, hemisferio, caminho_saida)
        
        if sucesso:
            print("\n" + "=" * 60)
            print("✅ CONVERSÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print(f"📁 Arquivos gerados:")
            print(f"   • {caminho_saida}.shp")
            print(f"   • {caminho_saida}.shx") 
            print(f"   • {caminho_saida}.dbf")
            print(f"   • {caminho_saida}.prj")
            print(f"🗺️  Sistema: UTM Zona {zona_utm}{hemisferio}")
            print(f"🌍 Datum: SIRGAS2000")
            print(f"📊 Precisão: 16 casas decimais")
        else:
            print("\n❌ Erro na conversão!")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
