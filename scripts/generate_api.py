#!/usr/bin/env python3
"""
Génère des fichiers JSON statiques pour simuler une API REST
Usage: python generate_api.py
"""

import pandas as pd
import json
from pathlib import Path

def generate_api_files():
    """Génère des fichiers JSON statiques à partir des CSV"""
    
    # Chemins
    data_dir = Path('data')
    api_dir = Path('api')
    api_dir.mkdir(exist_ok=True)
    
    print("🔄 Chargement des CSV...")
    
    # Charger CSV
    rivers = pd.read_csv(data_dir / 'rivers.csv')
    sections = pd.read_csv(data_dir / 'sections.csv')
    campaigns = pd.read_csv(data_dir / 'campaigns.csv')
    measurements = pd.read_csv(data_dir / 'measurements.csv')
    
    print(f"  ✓ {len(rivers)} rivières")
    print(f"  ✓ {len(sections)} sections")
    print(f"  ✓ {len(campaigns)} campagnes")
    print(f"  ✓ {len(measurements)} mesures")
    
    print("\n📝 Génération des fichiers JSON...")
    
    # 1. all.json - Toutes les données jointes
    print("  → all.json (toutes données)")
    full_data = measurements.merge(campaigns, on='campaign_id', how='left')
    full_data = full_data.merge(sections, on='section_id', how='left')
    full_data = full_data.merge(rivers, on='river_id', how='left')
    
    # Nettoyer NaN
    full_data = full_data.where(pd.notnull(full_data), None)
    
    with open(api_dir / 'all.json', 'w') as f:
        json.dump(full_data.to_dict('records'), f, indent=2)
    
    # 2. rivers.json
    print("  → rivers.json")
    rivers_clean = rivers.where(pd.notnull(rivers), None)
    with open(api_dir / 'rivers.json', 'w') as f:
        json.dump(rivers_clean.to_dict('records'), f, indent=2)
    
    # 3. sections.json  
    print("  → sections.json")
    sections_clean = sections.where(pd.notnull(sections), None)
    with open(api_dir / 'sections.json', 'w') as f:
        json.dump(sections_clean.to_dict('records'), f, indent=2)
    
    # 4. measurements.json
    print("  → measurements.json")
    measurements_clean = measurements.where(pd.notnull(measurements), None)
    with open(api_dir / 'measurements.json', 'w') as f:
        json.dump(measurements_clean.to_dict('records'), f, indent=2)
    
    # 5. summary_by_country.json
    print("  → summary_by_country.json")
    by_country = full_data.groupby('country').agg({
        'measurement_id': 'count',
        'bedload_rate_total_kg_s': ['mean', 'min', 'max'],
        'discharge_m3_s': 'mean',
        'river_id': 'nunique'
    }).reset_index()
    
    by_country.columns = ['country', 'n_measurements', 'avg_flux', 'min_flux', 'max_flux', 'avg_discharge', 'n_rivers']
    by_country = by_country.round(4)
    by_country = by_country.where(pd.notnull(by_country), None)
    
    with open(api_dir / 'summary_by_country.json', 'w') as f:
        json.dump(by_country.to_dict('records'), f, indent=2)
    
    # 6. summary_by_method.json
    print("  → summary_by_method.json")
    by_method = measurements.groupby('measurement_method').agg({
        'measurement_id': 'count',
        'bedload_rate_total_kg_s': ['mean', 'min', 'max'],
        'discharge_m3_s': 'mean',
        'd50_mm': 'mean'
    }).reset_index()
    
    by_method.columns = ['method', 'n_measurements', 'avg_flux', 'min_flux', 'max_flux', 'avg_discharge', 'avg_d50']
    by_method = by_method.round(4)
    by_method = by_method.where(pd.notnull(by_method), None)
    
    with open(api_dir / 'summary_by_method.json', 'w') as f:
        json.dump(by_method.to_dict('records'), f, indent=2)
    
    # 7. summary_by_river.json
    print("  → summary_by_river.json")
    by_river = full_data.groupby(['river_id', 'river_name', 'country']).agg({
        'measurement_id': 'count',
        'section_id': 'nunique',
        'bedload_rate_total_kg_s': ['mean', 'min', 'max'],
        'campaign_date': ['min', 'max']
    }).reset_index()
    
    by_river.columns = ['river_id', 'river_name', 'country', 'n_measurements', 'n_sections', 
                        'avg_flux', 'min_flux', 'max_flux', 'first_date', 'last_date']
    by_river = by_river.round(4)
    by_river = by_river.where(pd.notnull(by_river), None)
    
    with open(api_dir / 'summary_by_river.json', 'w') as f:
        json.dump(by_river.to_dict('records'), f, indent=2)
    
    # 8. stats.json - Statistiques globales
    print("  → stats.json (statistiques globales)")
    stats = {
        'total_measurements': len(measurements),
        'total_rivers': rivers['river_id'].nunique(),
        'total_countries': rivers['country'].nunique(),
        'total_sections': len(sections),
        'total_campaigns': len(campaigns),
        'methods': measurements['measurement_method'].unique().tolist(),
        'countries': rivers['country'].unique().tolist(),
        'date_range': {
            'first': campaigns['campaign_date'].min(),
            'last': campaigns['campaign_date'].max()
        },
        'flux_range': {
            'min': float(measurements['bedload_rate_total_kg_s'].min()),
            'max': float(measurements['bedload_rate_total_kg_s'].max()),
            'mean': float(measurements['bedload_rate_total_kg_s'].mean())
        }
    }
    
    with open(api_dir / 'stats.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    # Créer index.json listant tous les endpoints
    print("  → index.json (liste endpoints)")
    endpoints = {
        'version': '1.0',
        'description': 'Global Bedload Transport Database - Static JSON API',
        'endpoints': {
            'all': 'https://geomorphbars.github.io/Global_Bedload_Observatory/api/all.json',
            'rivers': 'https://geomorphbars.github.io/Global_Bedload_Observatory/api/rivers.json',
            'sections': 'https://geomorphbars.github.io/Global_Bedload_Observatory/api/sections.json',
            'measurements': 'https://geomorphbars.github.io/Global_Bedload_Observatory/api/measurements.json',
            'summary_by_country': 'https://geomorphbars.github.io/Global_Bedload_Observatory/api/summary_by_country.json',
            'summary_by_method': 'https://geomorphbars.github.io/Global_Bedload_Observatory/api/summary_by_method.json',
            'summary_by_river': 'https://geomorphbars.github.io/Global_Bedload_Observatory/api/summary_by_river.json',
            'stats': 'https://geomorphbars.github.io/Global_Bedload_Observatory/api/stats.json'
        },
        'usage': 'Access any endpoint URL directly in your browser or via HTTP GET request'
    }
    
    with open(api_dir / 'index.json', 'w') as f:
        json.dump(endpoints, f, indent=2)
    
    print("\n" + "="*60)
    print("✅ API STATIQUE GÉNÉRÉE AVEC SUCCÈS")
    print("="*60)
    print(f"📁 Dossier : {api_dir.absolute()}")
    print(f"📊 Fichiers créés : 9")
    print("\n🌐 Endpoints disponibles (après push sur GitHub) :")
    for name, url in endpoints['endpoints'].items():
        print(f"  • {name:20} → {url}")
    print("\n📝 Prochaines étapes :")
    print("  1. git add api/")
    print("  2. git commit -m 'Add static JSON API'")
    print("  3. git push")
    print("  4. Attendre 2-3 min pour GitHub Pages")
    print("  5. Tester : https://geomorphbars.github.io/.../api/stats.json")
    print("="*60)

if __name__ == '__main__':
    try:
        generate_api_files()
    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
        import traceback
        traceback.print_exc()
