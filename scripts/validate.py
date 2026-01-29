#!/usr/bin/env python3
"""
Script de validation pour la base de données mondiale du charriage
Structure hiérarchique : RIVERS → SECTIONS → CAMPAIGNS → MEASUREMENTS
Vérifie la cohérence et la complétude des fichiers CSV
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import json

class BedloadDatabaseValidator:
    """Validateur pour la base de données de charriage (structure hiérarchique)"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_rivers(self, rivers_file):
        """Valide le fichier rivers.csv"""
        print("\n=== VALIDATION DES RIVIÈRES ===")
        
        try:
            df = pd.read_csv(rivers_file)
        except Exception as e:
            self.errors.append(f"Erreur lecture {rivers_file}: {e}")
            return None
            
        # Vérifier colonnes obligatoires
        required_cols = ['river_id', 'river_name', 'country', 'watershed_area_km2']
        
        for col in required_cols:
            if col not in df.columns:
                self.errors.append(f"Colonne obligatoire manquante dans rivers: {col}")
        
        # Vérifier valeurs manquantes
        for col in required_cols:
            if col in df.columns:
                missing = df[col].isna().sum()
                if missing > 0:
                    self.errors.append(f"{missing} valeurs manquantes dans rivers.{col}")
        
        # Vérifier unicité des river_id
        if 'river_id' in df.columns:
            duplicates = df[df.duplicated('river_id', keep=False)]
            if len(duplicates) > 0:
                self.errors.append(f"river_id dupliqués: {duplicates['river_id'].tolist()}")
        
        # Vérifier codes pays (3 lettres majuscules)
        if 'country' in df.columns:
            invalid_country = df[~df['country'].str.match(r'^[A-Z]{3}$', na=False)]
            if len(invalid_country) > 0:
                self.warnings.append(f"Codes pays potentiellement invalides: {invalid_country['river_id'].tolist()}")
        
        # Vérifier watershed_area cohérente
        if 'watershed_area_km2' in df.columns:
            invalid_area = df[df['watershed_area_km2'] <= 0]
            if len(invalid_area) > 0:
                self.errors.append(f"Surfaces de bassin invalides (<= 0): {invalid_area['river_id'].tolist()}")
        
        print(f"✓ {len(df)} rivières vérifiées")
        return df
    
    def validate_sections(self, sections_file, rivers_df=None):
        """Valide le fichier sections.csv"""
        print("\n=== VALIDATION DES SECTIONS ===")
        
        try:
            df = pd.read_csv(sections_file)
        except Exception as e:
            self.errors.append(f"Erreur lecture {sections_file}: {e}")
            return None
        
        # Vérifier colonnes obligatoires
        required_cols = ['section_id', 'river_id', 'section_name', 'latitude', 
                        'longitude', 'elevation_m', 'section_width_m']
        
        for col in required_cols:
            if col not in df.columns:
                self.errors.append(f"Colonne obligatoire manquante dans sections: {col}")
        
        # Vérifier valeurs manquantes
        for col in required_cols:
            if col in df.columns:
                missing = df[col].isna().sum()
                if missing > 0:
                    self.errors.append(f"{missing} valeurs manquantes dans sections.{col}")
        
        # Vérifier unicité des section_id
        if 'section_id' in df.columns:
            duplicates = df[df.duplicated('section_id', keep=False)]
            if len(duplicates) > 0:
                self.errors.append(f"section_id dupliqués: {duplicates['section_id'].tolist()}")
        
        # Vérifier cohérence avec rivers
        if rivers_df is not None and 'river_id' in df.columns:
            unknown_rivers = set(df['river_id']) - set(rivers_df['river_id'])
            if unknown_rivers:
                self.errors.append(f"river_id inconnus dans sections: {list(unknown_rivers)}")
        
        # Vérifier plage de latitude/longitude
        if 'latitude' in df.columns:
            invalid_lat = df[(df['latitude'] < -90) | (df['latitude'] > 90)]
            if len(invalid_lat) > 0:
                self.errors.append(f"Latitudes invalides: {invalid_lat['section_id'].tolist()}")
                
        if 'longitude' in df.columns:
            invalid_lon = df[(df['longitude'] < -180) | (df['longitude'] > 180)]
            if len(invalid_lon) > 0:
                self.errors.append(f"Longitudes invalides: {invalid_lon['section_id'].tolist()}")
        
        # Vérifier section_width
        if 'section_width_m' in df.columns:
            invalid_width = df[df['section_width_m'] <= 0]
            if len(invalid_width) > 0:
                self.errors.append(f"Largeurs invalides (<= 0): {invalid_width['section_id'].tolist()}")
        
        # Vérifier pente
        if 'channel_slope' in df.columns:
            invalid_slope = df[(df['channel_slope'] < 0) | (df['channel_slope'] > 1)]
            if len(invalid_slope) > 0:
                self.warnings.append(f"Pentes suspectes (< 0 ou > 1): {invalid_slope['section_id'].tolist()}")
        
        print(f"✓ {len(df)} sections vérifiées")
        return df
    
    def validate_campaigns(self, campaigns_file, sections_df=None):
        """Valide le fichier campaigns.csv"""
        print("\n=== VALIDATION DES CAMPAGNES ===")
        
        try:
            df = pd.read_csv(campaigns_file)
        except Exception as e:
            self.errors.append(f"Erreur lecture {campaigns_file}: {e}")
            return None
        
        # Vérifier colonnes obligatoires
        required_cols = ['campaign_id', 'section_id', 'campaign_date', 
                        'data_provider', 'contact_email']
        
        for col in required_cols:
            if col not in df.columns:
                self.errors.append(f"Colonne obligatoire manquante dans campaigns: {col}")
        
        # Vérifier valeurs manquantes
        for col in required_cols:
            if col in df.columns:
                missing = df[col].isna().sum()
                if missing > 0:
                    self.errors.append(f"{missing} valeurs manquantes dans campaigns.{col}")
        
        # Vérifier unicité des campaign_id
        if 'campaign_id' in df.columns:
            duplicates = df[df.duplicated('campaign_id', keep=False)]
            if len(duplicates) > 0:
                self.errors.append(f"campaign_id dupliqués: {duplicates['campaign_id'].tolist()}")
        
        # Vérifier cohérence avec sections
        if sections_df is not None and 'section_id' in df.columns:
            unknown_sections = set(df['section_id']) - set(sections_df['section_id'])
            if unknown_sections:
                self.errors.append(f"section_id inconnus dans campaigns: {list(unknown_sections)}")
        
        # Vérifier format des dates
        if 'campaign_date' in df.columns:
            try:
                pd.to_datetime(df['campaign_date'], format='%Y-%m-%d', errors='raise')
            except:
                self.errors.append("Format de date invalide dans campaigns (attendu: YYYY-MM-DD)")
        
        # Vérifier quality_flag
        if 'quality_flag' in df.columns:
            valid_flags = ['A', 'B', 'C', 'D']
            invalid_flags = df[~df['quality_flag'].isin(valid_flags) & df['quality_flag'].notna()]
            if len(invalid_flags) > 0:
                self.errors.append(f"Quality flags invalides dans campaigns: {invalid_flags['quality_flag'].unique().tolist()}")
        
        # Vérifier emails
        if 'contact_email' in df.columns:
            invalid_email = df[~df['contact_email'].str.contains('@', na=False)]
            if len(invalid_email) > 0:
                self.warnings.append(f"Emails potentiellement invalides: {invalid_email['campaign_id'].tolist()}")
        
        print(f"✓ {len(df)} campagnes vérifiées")
        return df
    
    def validate_measurements(self, measurements_file, campaigns_df=None):
        """Valide le fichier measurements.csv"""
        print("\n=== VALIDATION DES MESURES ===")
        
        try:
            df = pd.read_csv(measurements_file)
        except Exception as e:
            self.errors.append(f"Erreur lecture {measurements_file}: {e}")
            return None
        
        # Vérifier colonnes obligatoires
        required_cols = ['measurement_id', 'campaign_id', 'measurement_method',
                        'bedload_rate_total_kg_s', 'discharge_m3_s', 'd50_mm', 'data_version']
        
        for col in required_cols:
            if col not in df.columns:
                self.errors.append(f"Colonne obligatoire manquante dans measurements: {col}")
        
        # Vérifier valeurs manquantes dans colonnes obligatoires
        for col in required_cols:
            if col in df.columns:
                missing = df[col].isna().sum()
                if missing > 0:
                    self.errors.append(f"{missing} valeurs manquantes dans measurements.{col}")
        
        # Vérifier unicité des measurement_id
        if 'measurement_id' in df.columns:
            duplicates = df[df.duplicated('measurement_id', keep=False)]
            if len(duplicates) > 0:
                self.errors.append(f"measurement_id dupliqués: {duplicates['measurement_id'].tolist()}")
        
        # Vérifier cohérence avec campaigns
        if campaigns_df is not None and 'campaign_id' in df.columns:
            unknown_campaigns = set(df['campaign_id']) - set(campaigns_df['campaign_id'])
            if unknown_campaigns:
                self.errors.append(f"campaign_id inconnus dans measurements: {list(unknown_campaigns)}")
        
        # Vérifier méthodes de mesure
        valid_methods = ['physical_sampler', 'dune_tracking', 'passive_acoustic', 
                        'active_acoustic', 'tracer', 'morphological_budget', 'other']
        if 'measurement_method' in df.columns:
            invalid_methods = df[~df['measurement_method'].isin(valid_methods)]
            if len(invalid_methods) > 0:
                self.errors.append(f"Méthodes invalides: {invalid_methods['measurement_method'].unique().tolist()}")
        
        # Vérifier flux de charriage
        if 'bedload_rate_total_kg_s' in df.columns:
            negative_bedload = df[df['bedload_rate_total_kg_s'] < 0]
            if len(negative_bedload) > 0:
                self.errors.append(f"Flux de charriage négatifs: {negative_bedload['measurement_id'].tolist()}")
            
            extreme_bedload = df[df['bedload_rate_total_kg_s'] > 1000]
            if len(extreme_bedload) > 0:
                self.warnings.append(f"Flux de charriage très élevés (> 1000 kg/s): {extreme_bedload['measurement_id'].tolist()}")
        
        # Vérifier débits
        if 'discharge_m3_s' in df.columns:
            negative_discharge = df[df['discharge_m3_s'] <= 0]
            if len(negative_discharge) > 0:
                self.errors.append(f"Débits invalides (<= 0): {negative_discharge['measurement_id'].tolist()}")
        
        # Vérifier granulométrie
        if 'd50_mm' in df.columns:
            invalid_d50 = df[(df['d50_mm'] <= 0) | (df['d50_mm'] > 1000)]
            if len(invalid_d50) > 0:
                self.warnings.append(f"D50 suspects (<= 0 ou > 1000 mm): {invalid_d50['measurement_id'].tolist()}")
        
        # Vérifier cohérence d50 < d84
        if 'd50_mm' in df.columns and 'd84_mm' in df.columns:
            invalid_grain_size = df[(df['d50_mm'] > df['d84_mm']) & df['d84_mm'].notna()]
            if len(invalid_grain_size) > 0:
                self.errors.append(f"D50 > D84 (incohérent): {invalid_grain_size['measurement_id'].tolist()}")
        
        # Vérifier cohérence flux unitaires
        if all(col in df.columns for col in ['bedload_rate_unit_mean_kg_s_m', 
                                              'bedload_rate_unit_min_kg_s_m', 
                                              'bedload_rate_unit_max_kg_s_m']):
            # min <= mean <= max
            invalid_range = df[
                (df['bedload_rate_unit_min_kg_s_m'] > df['bedload_rate_unit_mean_kg_s_m']) |
                (df['bedload_rate_unit_mean_kg_s_m'] > df['bedload_rate_unit_max_kg_s_m'])
            ]
            invalid_range = invalid_range[invalid_range[['bedload_rate_unit_min_kg_s_m', 
                                                         'bedload_rate_unit_mean_kg_s_m',
                                                         'bedload_rate_unit_max_kg_s_m']].notna().all(axis=1)]
            if len(invalid_range) > 0:
                self.errors.append(f"Flux unitaires incohérents (min > mean ou mean > max): {invalid_range['measurement_id'].tolist()}")
        
        # Vérifier incertitudes
        if 'uncertainty_percent' in df.columns:
            invalid_uncertainty = df[(df['uncertainty_percent'] < 0) | (df['uncertainty_percent'] > 100)]
            if len(invalid_uncertainty) > 0:
                self.warnings.append(f"Incertitudes hors plage [0-100%]: {invalid_uncertainty['measurement_id'].tolist()}")
        
        # Vérifier spatial_coverage_percent
        if 'spatial_coverage_percent' in df.columns:
            invalid_coverage = df[(df['spatial_coverage_percent'] < 0) | (df['spatial_coverage_percent'] > 100)]
            if len(invalid_coverage) > 0:
                self.warnings.append(f"Couverture spatiale hors plage [0-100%]: {invalid_coverage['measurement_id'].tolist()}")
        
        # Vérifications spécifiques à l'acoustique passive
        acoustic_measurements = df[df['measurement_method'] == 'passive_acoustic']
        if len(acoustic_measurements) > 0:
            # Vérifier que calibration_equation est renseigné
            missing_calib = acoustic_measurements[acoustic_measurements['calibration_equation'].isna()]
            if len(missing_calib) > 0:
                self.warnings.append(f"Équation de calibration manquante pour mesures acoustiques: {missing_calib['measurement_id'].tolist()}")
            
            # Vérifier équations de calibration valides
            valid_calibrations = ['Le_Guern_2021', 'Nasr_2023', 'site_specific']
            invalid_calib = acoustic_measurements[
                ~acoustic_measurements['calibration_equation'].isin(valid_calibrations) & 
                acoustic_measurements['calibration_equation'].notna()
            ]
            if len(invalid_calib) > 0:
                self.warnings.append(f"Équations de calibration non standard: {invalid_calib['calibration_equation'].unique().tolist()}")
            
            # Si site_specific, vérifier que calibration_reference est rempli
            site_specific = acoustic_measurements[acoustic_measurements['calibration_equation'] == 'site_specific']
            missing_ref = site_specific[site_specific['calibration_reference'].isna()]
            if len(missing_ref) > 0:
                self.errors.append(f"calibration_reference obligatoire pour site_specific: {missing_ref['measurement_id'].tolist()}")
        
        # Vérifier JSON dans calibration_parameters
        if 'calibration_parameters' in df.columns:
            for idx, row in df[df['calibration_parameters'].notna()].iterrows():
                try:
                    json.loads(row['calibration_parameters'])
                except json.JSONDecodeError:
                    # Si ce n'est pas du JSON, vérifier que c'est du texte simple acceptable
                    if not isinstance(row['calibration_parameters'], str):
                        self.warnings.append(f"calibration_parameters invalide pour {row['measurement_id']}: pas JSON ni texte")
        
        print(f"✓ {len(df)} mesures vérifiées")
        return df
    
    def validate_hierarchy(self, rivers_df, sections_df, campaigns_df, measurements_df):
        """Valide la cohérence de la hiérarchie complète"""
        print("\n=== VALIDATION DE LA HIÉRARCHIE ===")
        
        # Vérifier que chaque section a une rivière
        if rivers_df is not None and sections_df is not None:
            orphan_sections = set(sections_df['section_id']) - set(
                sections_df.merge(rivers_df, on='river_id')['section_id']
            )
            if orphan_sections:
                self.errors.append(f"Sections sans rivière valide: {list(orphan_sections)}")
        
        # Vérifier que chaque campagne a une section
        if sections_df is not None and campaigns_df is not None:
            orphan_campaigns = set(campaigns_df['campaign_id']) - set(
                campaigns_df.merge(sections_df, on='section_id')['campaign_id']
            )
            if orphan_campaigns:
                self.errors.append(f"Campagnes sans section valide: {list(orphan_campaigns)}")
        
        # Vérifier que chaque mesure a une campagne
        if campaigns_df is not None and measurements_df is not None:
            orphan_measurements = set(measurements_df['measurement_id']) - set(
                measurements_df.merge(campaigns_df, on='campaign_id')['measurement_id']
            )
            if orphan_measurements:
                self.errors.append(f"Mesures sans campagne valide: {list(orphan_measurements)}")
        
        print("✓ Hiérarchie validée")
    
    def generate_statistics(self, rivers_df, sections_df, campaigns_df, measurements_df):
        """Génère des statistiques sur la base"""
        print("\n=== STATISTIQUES ===")
        
        if rivers_df is not None:
            print(f"  Rivières: {len(rivers_df)}")
            if 'country' in rivers_df.columns:
                print(f"  Pays représentés: {rivers_df['country'].nunique()}")
        
        if sections_df is not None:
            print(f"  Sections: {len(sections_df)}")
        
        if campaigns_df is not None:
            print(f"  Campagnes: {len(campaigns_df)}")
            if 'campaign_date' in campaigns_df.columns:
                dates = pd.to_datetime(campaigns_df['campaign_date'])
                print(f"  Période: {dates.min()} à {dates.max()}")
        
        if measurements_df is not None:
            print(f"  Mesures: {len(measurements_df)}")
            if 'measurement_method' in measurements_df.columns:
                print(f"  Méthodes utilisées:")
                for method, count in measurements_df['measurement_method'].value_counts().items():
                    print(f"    - {method}: {count}")
    
    def generate_report(self):
        """Génère un rapport de validation"""
        print("\n" + "="*60)
        print("RAPPORT DE VALIDATION")
        print("="*60)
        
        if len(self.errors) == 0 and len(self.warnings) == 0:
            print("\n✓ AUCUNE ERREUR - Base de données valide!")
        else:
            if len(self.errors) > 0:
                print(f"\n❌ ERREURS CRITIQUES ({len(self.errors)}):")
                for i, error in enumerate(self.errors, 1):
                    print(f"  {i}. {error}")
            
            if len(self.warnings) > 0:
                print(f"\n⚠️  AVERTISSEMENTS ({len(self.warnings)}):")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"  {i}. {warning}")
        
        print("\n" + "="*60)
        
        return len(self.errors) == 0

def main():
    """Point d'entrée principal"""
    
    print("="*60)
    print("VALIDATEUR - Base de Données Mondiale du Charriage")
    print("Structure hiérarchique : RIVERS → SECTIONS → CAMPAIGNS → MEASUREMENTS")
    print("="*60)
    
    validator = BedloadDatabaseValidator()
    
    # Validation hiérarchique
    rivers_df = validator.validate_rivers('data/rivers.csv')
    sections_df = validator.validate_sections('data/sections.csv', rivers_df)
    campaigns_df = validator.validate_campaigns('data/campaigns.csv', sections_df)
    measurements_df = validator.validate_measurements('data/measurements.csv', campaigns_df)
    
    # Validation de la hiérarchie complète
    if all(df is not None for df in [rivers_df, sections_df, campaigns_df, measurements_df]):
        validator.validate_hierarchy(rivers_df, sections_df, campaigns_df, measurements_df)
        validator.generate_statistics(rivers_df, sections_df, campaigns_df, measurements_df)
    
    # Génération du rapport
    is_valid = validator.generate_report()
    
    if is_valid:
        print("\n✅ Validation réussie - Prêt pour intégration!")
        return 0
    else:
        print("\n❌ Validation échouée - Corriger les erreurs avant de continuer")
        return 1

if __name__ == "__main__":
    sys.exit(main())
