#!/usr/bin/env python3
"""
Validation script for Global Bedload Transport Database CSV files
Validates data structure, required fields, data types, and hierarchical consistency
"""

import pandas as pd
import sys
from pathlib import Path
import re

class BedloadDatabaseValidator:
    """Validator for bedload transport database CSV files"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_rivers(self, filepath):
        """Validate rivers.csv"""
        print(f"\n{'='*60}")
        print(f"Validating RIVERS: {filepath}")
        print(f"{'='*60}")
        
        # Required columns
        required_cols = ['river_id', 'river_name', 'country']
        optional_cols = ['watershed_area_km2', 'notes']
        all_cols = required_cols + optional_cols
        
        # Load CSV
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            self.errors.append(f"Cannot read {filepath}: {e}")
            return None
        
        # Check required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            self.errors.append(f"Missing required columns in rivers.csv: {missing_cols}")
            return None
        
        # Check for unexpected columns
        unexpected_cols = [col for col in df.columns if col not in all_cols]
        if unexpected_cols:
            self.warnings.append(f"Unexpected columns in rivers.csv: {unexpected_cols}")
        
        # Check required fields are not empty
        for col in required_cols:
            empty_count = df[col].isna().sum()
            if empty_count > 0:
                self.errors.append(f"Column '{col}' has {empty_count} empty values (required field)")
        
        # Check country codes (should be 3 letters)
        if 'country' in df.columns:
            invalid_countries = df[~df['country'].str.match(r'^[A-Z]{3}$', na=False)]['country'].unique()
            if len(invalid_countries) > 0:
                self.errors.append(f"Invalid country codes (should be 3 letters): {invalid_countries.tolist()}")
        
        # Check for duplicate river_id
        duplicates = df[df.duplicated(subset=['river_id'], keep=False)]
        if len(duplicates) > 0:
            self.errors.append(f"Duplicate river_id found: {duplicates['river_id'].tolist()}")
        
        # Check watershed_area_km2 is positive
        if 'watershed_area_km2' in df.columns:
            negative = df[df['watershed_area_km2'] < 0]
            if len(negative) > 0:
                self.errors.append(f"Negative watershed_area_km2 for: {negative['river_id'].tolist()}")
        
        print(f"✓ Loaded {len(df)} rivers")
        return df
    
    def validate_sections(self, filepath, rivers_df):
        """Validate sections.csv"""
        print(f"\n{'='*60}")
        print(f"Validating SECTIONS: {filepath}")
        print(f"{'='*60}")
        
        # Required columns
        required_cols = ['section_id', 'river_id', 'section_name', 'latitude', 'longitude']
        optional_cols = ['elevation_m', 'bankfull_width_m', 'channel_slope', 'morphology_type', 'notes']
        all_cols = required_cols + optional_cols
        
        # Load CSV
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            self.errors.append(f"Cannot read {filepath}: {e}")
            return None
        
        # Check required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            self.errors.append(f"Missing required columns in sections.csv: {missing_cols}")
            return None
        
        # Check for unexpected columns
        unexpected_cols = [col for col in df.columns if col not in all_cols]
        if unexpected_cols:
            self.warnings.append(f"Unexpected columns in sections.csv: {unexpected_cols}")
        
        # Check required fields are not empty
        for col in required_cols:
            empty_count = df[col].isna().sum()
            if empty_count > 0:
                self.errors.append(f"Column '{col}' has {empty_count} empty values (required field)")
        
        # Check for duplicate section_id
        duplicates = df[df.duplicated(subset=['section_id'], keep=False)]
        if len(duplicates) > 0:
            self.errors.append(f"Duplicate section_id found: {duplicates['section_id'].tolist()}")
        
        # Check latitude range (-90 to 90)
        if 'latitude' in df.columns:
            invalid_lat = df[(df['latitude'] < -90) | (df['latitude'] > 90)]
            if len(invalid_lat) > 0:
                self.errors.append(f"Invalid latitude (must be -90 to 90): {invalid_lat['section_id'].tolist()}")
        
        # Check longitude range (-180 to 180)
        if 'longitude' in df.columns:
            invalid_lon = df[(df['longitude'] < -180) | (df['longitude'] > 180)]
            if len(invalid_lon) > 0:
                self.errors.append(f"Invalid longitude (must be -180 to 180): {invalid_lon['section_id'].tolist()}")
        
        # Check river_id exists in rivers.csv
        if rivers_df is not None:
            missing_rivers = df[~df['river_id'].isin(rivers_df['river_id'])]
            if len(missing_rivers) > 0:
                self.errors.append(f"river_id not found in rivers.csv: {missing_rivers['section_id'].tolist()}")
        
        # Check bankfull_width_m is positive
        if 'bankfull_width_m' in df.columns:
            negative = df[df['bankfull_width_m'] < 0]
            if len(negative) > 0:
                self.errors.append(f"Negative bankfull_width_m for: {negative['section_id'].tolist()}")
        
        # Check channel_slope is between 0 and 1
        if 'channel_slope' in df.columns:
            invalid_slope = df[(df['channel_slope'] < 0) | (df['channel_slope'] > 1)]
            if len(invalid_slope) > 0:
                self.errors.append(f"Invalid channel_slope (must be 0-1): {invalid_slope['section_id'].tolist()}")
        
        print(f"✓ Loaded {len(df)} sections")
        return df
    
    def validate_campaigns(self, filepath, sections_df):
        """Validate campaigns.csv"""
        print(f"\n{'='*60}")
        print(f"Validating CAMPAIGNS: {filepath}")
        print(f"{'='*60}")
        
        # Required columns
        required_cols = ['campaign_id', 'section_id', 'campaign_date']
        optional_cols = ['data_provider', 'contact_email', 'reference', 'notes']
        all_cols = required_cols + optional_cols
        
        # Load CSV
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            self.errors.append(f"Cannot read {filepath}: {e}")
            return None
        
        # Check required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            self.errors.append(f"Missing required columns in campaigns.csv: {missing_cols}")
            return None
        
        # Check for unexpected columns
        unexpected_cols = [col for col in df.columns if col not in all_cols]
        if unexpected_cols:
            self.warnings.append(f"Unexpected columns in campaigns.csv: {unexpected_cols}")
        
        # Check required fields are not empty
        for col in required_cols:
            empty_count = df[col].isna().sum()
            if empty_count > 0:
                self.errors.append(f"Column '{col}' has {empty_count} empty values (required field)")
        
        # Check for duplicate campaign_id
        duplicates = df[df.duplicated(subset=['campaign_id'], keep=False)]
        if len(duplicates) > 0:
            self.errors.append(f"Duplicate campaign_id found: {duplicates['campaign_id'].tolist()}")
        
        # Check date format (YYYY-MM-DD)
        if 'campaign_date' in df.columns:
            try:
                pd.to_datetime(df['campaign_date'], format='%Y-%m-%d', errors='coerce')
                invalid_dates = df[pd.to_datetime(df['campaign_date'], format='%Y-%m-%d', errors='coerce').isna()]
                if len(invalid_dates) > 0:
                    self.errors.append(f"Invalid date format (use YYYY-MM-DD): {invalid_dates['campaign_id'].tolist()}")
            except:
                self.errors.append(f"Cannot parse campaign_date")
        
        # Check section_id exists in sections.csv
        if sections_df is not None:
            missing_sections = df[~df['section_id'].isin(sections_df['section_id'])]
            if len(missing_sections) > 0:
                self.errors.append(f"section_id not found in sections.csv: {missing_sections['campaign_id'].tolist()}")
        
        # Check email format (if provided)
        if 'contact_email' in df.columns:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            invalid_emails = df[df['contact_email'].notna() & ~df['contact_email'].str.match(email_pattern, na=False)]
            if len(invalid_emails) > 0:
                self.warnings.append(f"Invalid email format: {invalid_emails['campaign_id'].tolist()}")
        
        print(f"✓ Loaded {len(df)} campaigns")
        return df
    
    def validate_measurements(self, filepath, campaigns_df):
        """Validate measurements.csv"""
        print(f"\n{'='*60}")
        print(f"Validating MEASUREMENTS: {filepath}")
        print(f"{'='*60}")
        
        # Required columns
        required_cols = ['measurement_id', 'campaign_id', 'measurement_method', 'bedload_rate_total_kg_s']
        
        # Optional general columns
        optional_general = ['discharge_m3_s', 'discharge_source', 'discharge_station_code', 
                           'discharge_station_name', 'd50_mm', 'd84_mm', 'd10_mm', 
                           'water_depth_mean_m', 'flow_velocity_mean_m_s']
        
        # Method-specific columns
        passive_acoustic_cols = ['acoustic_hydrophone_type', 'acoustic_recorder_type', 
                                'acoustic_sensitivity_db', 'acoustic_calibration', 
                                'acoustic_calibration_a', 'acoustic_calibration_b']
        
        active_acoustic_cols = ['adcp_type', 'adcp_equation_type', 'adcp_measurement_duration_s']
        
        sampler_cols = ['sampler_type']
        
        dune_cols = ['dune_survey_method', 'dune_echosounder_type', 
                     'dune_equation_type', 'dune_interval_hours']
        
        all_cols = (required_cols + optional_general + passive_acoustic_cols + 
                   active_acoustic_cols + sampler_cols + dune_cols)
        
        # Load CSV
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            self.errors.append(f"Cannot read {filepath}: {e}")
            return None
        
        # Check required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            self.errors.append(f"Missing required columns in measurements.csv: {missing_cols}")
            return None
        
        # Check for unexpected columns
        unexpected_cols = [col for col in df.columns if col not in all_cols]
        if unexpected_cols:
            self.warnings.append(f"Unexpected columns in measurements.csv: {unexpected_cols}")
        
        # Check required fields are not empty
        for col in required_cols:
            empty_count = df[col].isna().sum()
            if empty_count > 0:
                self.errors.append(f"Column '{col}' has {empty_count} empty values (required field)")
        
        # Check for duplicate measurement_id
        duplicates = df[df.duplicated(subset=['measurement_id'], keep=False)]
        if len(duplicates) > 0:
            self.errors.append(f"Duplicate measurement_id found: {duplicates['measurement_id'].tolist()}")
        
        # Check measurement_method values
        allowed_methods = ['passive_acoustic', 'active_acoustic', 'physical_sampler', 'dune_tracking']
        if 'measurement_method' in df.columns:
            invalid_methods = df[~df['measurement_method'].isin(allowed_methods)]
            if len(invalid_methods) > 0:
                self.errors.append(f"Invalid measurement_method (allowed: {allowed_methods}): {invalid_methods['measurement_id'].tolist()}")
        
        # Check discharge_source values
        allowed_sources = ['hydrometric_station', 'adcp_measurement', 'rating_curve', 
                          'current_meter', 'model', 'estimated', 'other']
        if 'discharge_source' in df.columns:
            invalid_sources = df[df['discharge_source'].notna() & ~df['discharge_source'].isin(allowed_sources)]
            if len(invalid_sources) > 0:
                self.errors.append(f"Invalid discharge_source (allowed: {allowed_sources}): {invalid_sources['measurement_id'].tolist()}")
        
        # Check that discharge_station_code/name are filled only when source=hydrometric_station
        if 'discharge_source' in df.columns and 'discharge_station_code' in df.columns:
            has_station_without_source = df[(df['discharge_station_code'].notna()) & 
                                           (df['discharge_source'] != 'hydrometric_station')]
            if len(has_station_without_source) > 0:
                self.warnings.append(f"discharge_station_code filled but source != hydrometric_station: {has_station_without_source['measurement_id'].tolist()}")
        
        # Check campaign_id exists in campaigns.csv
        if campaigns_df is not None:
            missing_campaigns = df[~df['campaign_id'].isin(campaigns_df['campaign_id'])]
            if len(missing_campaigns) > 0:
                self.errors.append(f"campaign_id not found in campaigns.csv: {missing_campaigns['measurement_id'].tolist()}")
        
        # Check bedload_rate is positive
        negative_flux = df[df['bedload_rate_total_kg_s'] < 0]
        if len(negative_flux) > 0:
            self.errors.append(f"Negative bedload_rate_total_kg_s: {negative_flux['measurement_id'].tolist()}")
        
        # Check discharge is positive
        if 'discharge_m3_s' in df.columns:
            negative_q = df[df['discharge_m3_s'] < 0]
            if len(negative_q) > 0:
                self.errors.append(f"Negative discharge_m3_s: {negative_q['measurement_id'].tolist()}")
        
        # Check grain sizes are positive and logical (d10 < d50 < d84)
        if all(col in df.columns for col in ['d10_mm', 'd50_mm', 'd84_mm']):
            invalid_grain = df[(df['d10_mm'] >= df['d50_mm']) | (df['d50_mm'] >= df['d84_mm'])]
            if len(invalid_grain) > 0:
                self.warnings.append(f"Grain size not in order d10 < d50 < d84: {invalid_grain['measurement_id'].tolist()}")
        
        # Method-specific validation
        for method, method_cols in [
            ('passive_acoustic', passive_acoustic_cols),
            ('active_acoustic', active_acoustic_cols),
            ('physical_sampler', sampler_cols),
            ('dune_tracking', dune_cols)
        ]:
            method_rows = df[df['measurement_method'] == method]
            if len(method_rows) > 0:
                # Check that at least some method-specific columns are filled
                filled_cols = sum([method_rows[col].notna().any() for col in method_cols if col in df.columns])
                if filled_cols == 0:
                    self.warnings.append(f"Method '{method}' used but no {method}-specific columns filled")
        
        print(f"✓ Loaded {len(df)} measurements")
        print(f"  - passive_acoustic: {len(df[df['measurement_method'] == 'passive_acoustic'])}")
        print(f"  - active_acoustic: {len(df[df['measurement_method'] == 'active_acoustic'])}")
        print(f"  - physical_sampler: {len(df[df['measurement_method'] == 'physical_sampler'])}")
        print(f"  - dune_tracking: {len(df[df['measurement_method'] == 'dune_tracking'])}")
        
        return df
    
    def print_summary(self):
        """Print validation summary"""
        print(f"\n{'='*60}")
        print("VALIDATION SUMMARY")
        print(f"{'='*60}")
        
        if len(self.errors) == 0 and len(self.warnings) == 0:
            print("✅ ALL CHECKS PASSED - NO ERRORS OR WARNINGS")
        else:
            if len(self.errors) > 0:
                print(f"\n❌ ERRORS ({len(self.errors)}):")
                for i, error in enumerate(self.errors, 1):
                    print(f"  {i}. {error}")
            
            if len(self.warnings) > 0:
                print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"  {i}. {warning}")
        
        print(f"\n{'='*60}")
        
        if len(self.errors) > 0:
            print("❌ VALIDATION FAILED - Fix errors before using data")
            return False
        elif len(self.warnings) > 0:
            print("⚠️  VALIDATION PASSED WITH WARNINGS - Review warnings")
            return True
        else:
            print("✅ VALIDATION PASSED - Data is ready to use")
            return True

def main():
    """Main validation function"""
    # File paths
    data_dir = Path('data')
    
    rivers_file = data_dir / 'rivers.csv'
    sections_file = data_dir / 'sections.csv'
    campaigns_file = data_dir / 'campaigns.csv'
    measurements_file = data_dir / 'measurements.csv'
    
    # Check files exist
    for filepath in [rivers_file, sections_file, campaigns_file, measurements_file]:
        if not filepath.exists():
            print(f"❌ ERROR: File not found: {filepath}")
            print(f"   Make sure you run this script from the project root directory")
            print(f"   and that all CSV files are in the 'data/' folder")
            sys.exit(1)
    
    # Create validator
    validator = BedloadDatabaseValidator()
    
    # Validate in hierarchical order
    rivers_df = validator.validate_rivers(rivers_file)
    sections_df = validator.validate_sections(sections_file, rivers_df)
    campaigns_df = validator.validate_campaigns(campaigns_file, sections_df)
    measurements_df = validator.validate_measurements(measurements_file, campaigns_df)
    
    # Print summary
    success = validator.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
