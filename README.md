# Conversor DXF para Shapefile

Script Python para converter arquivos DXF (CAD) para formato Shapefile com sistema de coordenadas UTM e datum SIRGAS2000.

## Características

- ✅ Processa arquivos DXF contendo polígonos de imóveis
- ✅ Identifica polígonos por ID da entidade (handle)
- ✅ Sistema de coordenadas UTM com datum SIRGAS2000
- ✅ Precisão de 16 casas decimais nas coordenadas
- ✅ Gera os 4 arquivos principais do Shapefile (.shp, .shx, .dbf, .prj)
- ✅ Interface simples e intuitiva

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o script:
```bash
python dxf_to_shapefile.py
```

O script solicitará:
1. **Caminho do arquivo DXF**: Localização do arquivo CAD
2. **ID da entidade**: Handle do polígono no arquivo DXF
3. **Zona UTM**: Número da zona UTM (ex: 22)
4. **Hemisfério**: N ou S (padrão: S)

## Exemplo de Uso

```
============================================================
CONVERSOR DXF PARA SHAPEFILE
Sistema: UTM | Datum: SIRGAS2000
============================================================
📁 Caminho do arquivo DXF: /caminho/para/imovel.dxf
🔍 ID da entidade (handle) do polígono: 1A2B
🗺️  Zona UTM (ex: 22): 22
🌍 Hemisfério (N/S) [padrão: S]: S
```

## Arquivos Gerados

O script gera 4 arquivos:
- `nome_arquivo_poligono_ID.shp` - Geometria do polígono
- `nome_arquivo_poligono_ID.shx` - Índice espacial
- `nome_arquivo_poligono_ID.dbf` - Atributos
- `nome_arquivo_poligono_ID.prj` - Sistema de coordenadas

## Requisitos

- Python 3.7+
- Arquivo DXF com polígonos (LWPOLYLINE ou POLYLINE)
- ID da entidade (handle) do polígono desejado

## Dependências

- `ezdxf`: Leitura de arquivos DXF
- `geopandas`: Manipulação de dados geoespaciais
- `shapely`: Geometrias
- `pyproj`: Projeções cartográficas
- `fiona`: I/O de formatos geoespaciais
