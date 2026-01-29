#!/usr/bin/env python3
"""
Convertit les CSV en base SQLite pour Datasette
Crée également des vues utiles pour l'analyse
"""

import sqlite3
import pandas as pd
from pathlib import Path
import sys

def build_database():
    """Crée la base SQLite depuis les CSV"""
    
    data_dir = Path('data')
    db_path = data_dir / 'bedload.db'
    
    # Vérifier que les CSV existent
    required_files = ['rivers.csv', 'sections.csv', 'campaigns.csv', 'measurements.csv']
    for filename in required_files:
        if not (data_dir / filename).exists():
            print(f"❌ Erreur : {filename} introuvable dans data/")
            return False
    
    # Supprimer ancienne version si existe
    if db_path.exists():
        db_path.unlink()
        print("🗑️  Ancienne base supprimée")
    
    # Connexion SQLite
    conn = sqlite3.connect(db_path)
    
    print("\n🔄 Conversion CSV → SQLite...")
    
    # Charger chaque CSV dans une table
    tables = {
        'rivers': 'rivers.csv',
        'sections': 'sections.csv',
        'campaigns': 'campaigns.csv',
        'measurements': 'measurements.csv'
    }
    
    total_rows = 0
    for table_name, csv_filename in tables.items():
        csv_path = data_dir / csv_filename
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"  ✓ {table_name:15} {len(df):5} lignes")
        total_rows += len(df)
    
    # Créer des vues utiles
    print("\n🔗 Création des vues jointes...")
    
    # Vue complète : toutes les infos en une table
    conn.execute("""
    CREATE VIEW measurements_full AS
    SELECT 
        m.measurement_id,
        m.measurement_method,
        m.bedload_rate_total_kg_s,
        m.bedload_rate_unit_mean_kg_s_m,
        m.bedload_rate_unit_std_kg_s_m,
        m.number_of_measurement_points,
        m.integration_method,
        m.spatial_coverage_percent,
        m.discharge_m3_s,
        m.water_depth_mean_m,
        m.flow_velocity_mean_m_s,
        m.shear_stress_mean_Pa,
        m.d50_mm,
        m.d84_mm,
        m.uncertainty_percent,
        m.data_version,
        m.calibration_equation,
        m.hydrophone_type,
        m.sampler_type,
        m.notes,
        c.campaign_id,
        c.campaign_date,
        c.hydrological_context,
        c.data_provider,
        c.contact_email,
        c.quality_flag,
        s.section_id,
        s.section_name,
        s.latitude,
        s.longitude,
        s.elevation_m,
        s.section_width_m,
        s.channel_slope,
        s.morphology_type,
        r.river_id,
        r.river_name,
        r.country,
        r.watershed_area_km2
    FROM measurements m
    JOIN campaigns c ON m.campaign_id = c.campaign_id
    JOIN sections s ON c.section_id = s.section_id
    JOIN rivers r ON s.river_id = r.river_id
    """)
    print("  ✓ measurements_full (vue principale)")
    
    # Vue résumé par rivière
    conn.execute("""
    CREATE VIEW summary_by_river AS
    SELECT 
        r.river_id,
        r.river_name,
        r.country,
        r.watershed_area_km2,
        COUNT(DISTINCT s.section_id) as n_sections,
        COUNT(DISTINCT c.campaign_id) as n_campaigns,
        COUNT(m.measurement_id) as n_measurements,
        MIN(c.campaign_date) as first_measurement,
        MAX(c.campaign_date) as last_measurement,
        ROUND(AVG(m.bedload_rate_total_kg_s), 4) as avg_bedload_rate_kg_s,
        ROUND(MIN(m.bedload_rate_total_kg_s), 4) as min_bedload_rate_kg_s,
        ROUND(MAX(m.bedload_rate_total_kg_s), 4) as max_bedload_rate_kg_s,
        ROUND(AVG(m.discharge_m3_s), 2) as avg_discharge_m3_s,
        ROUND(AVG(m.d50_mm), 1) as avg_d50_mm
    FROM rivers r
    LEFT JOIN sections s ON r.river_id = s.river_id
    LEFT JOIN campaigns c ON s.section_id = c.section_id
    LEFT JOIN measurements m ON c.campaign_id = m.campaign_id
    GROUP BY r.river_id, r.river_name, r.country, r.watershed_area_km2
    ORDER BY n_measurements DESC
    """)
    print("  ✓ summary_by_river")
    
    # Vue résumé par méthode
    conn.execute("""
    CREATE VIEW summary_by_method AS
    SELECT 
        measurement_method,
        COUNT(*) as n_measurements,
        ROUND(AVG(bedload_rate_total_kg_s), 4) as avg_bedload_rate_kg_s,
        ROUND(AVG(discharge_m3_s), 2) as avg_discharge_m3_s,
        ROUND(AVG(d50_mm), 1) as avg_d50_mm,
        ROUND(AVG(number_of_measurement_points), 1) as avg_n_points
    FROM measurements
    GROUP BY measurement_method
    ORDER BY n_measurements DESC
    """)
    print("  ✓ summary_by_method")
    
    # Vue résumé par pays
    conn.execute("""
    CREATE VIEW summary_by_country AS
    SELECT 
        r.country,
        COUNT(DISTINCT r.river_id) as n_rivers,
        COUNT(DISTINCT s.section_id) as n_sections,
        COUNT(m.measurement_id) as n_measurements,
        ROUND(AVG(m.bedload_rate_total_kg_s), 4) as avg_bedload_rate_kg_s
    FROM rivers r
    LEFT JOIN sections s ON r.river_id = s.river_id
    LEFT JOIN campaigns c ON s.section_id = c.section_id
    LEFT JOIN measurements m ON c.campaign_id = m.campaign_id
    GROUP BY r.country
    ORDER BY n_measurements DESC
    """)
    print("  ✓ summary_by_country")
    
    # Vue pour équations de calibration acoustique
    conn.execute("""
    CREATE VIEW acoustic_calibrations AS
    SELECT 
        calibration_equation,
        COUNT(*) as n_measurements,
        AVG(bedload_rate_total_kg_s) as avg_bedload_rate,
        AVG(discharge_m3_s) as avg_discharge,
        GROUP_CONCAT(DISTINCT hydrophone_type) as hydrophone_types,
        GROUP_CONCAT(DISTINCT processing_software) as software_versions
    FROM measurements
    WHERE measurement_method = 'passive_acoustic'
    GROUP BY calibration_equation
    """)
    print("  ✓ acoustic_calibrations")
    
    # Créer des index pour performances
    print("\n⚡ Création des index...")
    conn.execute("CREATE INDEX idx_measurements_method ON measurements(measurement_method)")
    conn.execute("CREATE INDEX idx_campaigns_date ON campaigns(campaign_date)")
    conn.execute("CREATE INDEX idx_sections_coords ON sections(latitude, longitude)")
    conn.execute("CREATE INDEX idx_rivers_country ON rivers(country)")
    print("  ✓ Index créés")
    
    conn.commit()
    
    # Statistiques finales
    cursor = conn.execute("SELECT COUNT(*) FROM measurements_full")
    n_measurements = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(DISTINCT country) FROM rivers")
    n_countries = cursor.fetchone()[0]
    
    conn.close()
    
    # Afficher résumé
    print("\n" + "="*60)
    print("✅ BASE SQLITE CRÉÉE AVEC SUCCÈS")
    print("="*60)
    print(f"📁 Fichier       : {db_path}")
    print(f"💾 Taille        : {db_path.stat().st_size / 1024:.1f} KB")
    print(f"📊 Mesures       : {n_measurements}")
    print(f"🌍 Pays          : {n_countries}")
    print(f"📋 Total lignes  : {total_rows}")
    print("\n🚀 Tester avec : datasette data/bedload.db")
    print("="*60)
    
    return True

if __name__ == "__main__":
    try:
        success = build_database()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
