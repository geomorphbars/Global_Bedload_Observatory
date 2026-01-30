#!/usr/bin/env python3
"""
Build SQLite database from CSV files
Creates bedload_transport.db with proper schema and relationships
"""

import sqlite3
import pandas as pd
from pathlib import Path
import sys

class DatabaseBuilder:
    """Builds SQLite database from validated CSV files"""
    
    def __init__(self, db_path='bedload_transport.db'):
        self.db_path = db_path
        self.conn = None
        
    def create_schema(self):
        """Create database tables with proper schema"""
        print("\n📦 Creating database schema...")
        
        cursor = self.conn.cursor()
        
        # RIVERS table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rivers (
                river_id TEXT PRIMARY KEY,
                river_name TEXT NOT NULL,
                country TEXT NOT NULL,
                watershed_area_km2 REAL,
                notes TEXT
            )
        ''')
        
        # SECTIONS table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sections (
                section_id TEXT PRIMARY KEY,
                river_id TEXT NOT NULL,
                section_name TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                elevation_m REAL,
                bankfull_width_m REAL,
                channel_slope REAL,
                morphology_type TEXT,
                notes TEXT,
                FOREIGN KEY (river_id) REFERENCES rivers(river_id)
            )
        ''')
        
        # CAMPAIGNS table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                campaign_id TEXT PRIMARY KEY,
                section_id TEXT NOT NULL,
                campaign_date TEXT NOT NULL,
                data_provider TEXT,
                contact_email TEXT,
                reference TEXT,
                notes TEXT,
                FOREIGN KEY (section_id) REFERENCES sections(section_id)
            )
        ''')
        
        # MEASUREMENTS table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS measurements (
                measurement_id TEXT PRIMARY KEY,
                campaign_id TEXT NOT NULL,
                measurement_method TEXT NOT NULL,
                bedload_rate_total_kg_s REAL NOT NULL,
                discharge_m3_s REAL,
                discharge_source TEXT,
                discharge_station_code TEXT,
                discharge_station_name TEXT,
                d50_mm REAL,
                d84_mm REAL,
                d10_mm REAL,
                water_depth_mean_m REAL,
                flow_velocity_mean_m_s REAL,
                acoustic_hydrophone_type TEXT,
                acoustic_recorder_type TEXT,
                acoustic_sensitivity_db REAL,
                acoustic_calibration TEXT,
                acoustic_calibration_a REAL,
                acoustic_calibration_b REAL,
                adcp_type TEXT,
                adcp_equation_type TEXT,
                adcp_measurement_duration_s REAL,
                sampler_type TEXT,
                dune_survey_method TEXT,
                dune_echosounder_type TEXT,
                dune_equation_type TEXT,
                dune_interval_hours REAL,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id)
            )
        ''')
        
        # Create indexes for faster queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sections_river ON sections(river_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_campaigns_section ON campaigns(section_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_measurements_campaign ON measurements(campaign_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_measurements_method ON measurements(measurement_method)')
        
        self.conn.commit()
        print("  ✓ Schema created")
        
    def load_rivers(self, csv_path):
        """Load rivers from CSV into database"""
        print(f"\n📋 Loading {csv_path}...")
        
        df = pd.read_csv(csv_path)
        
        # Replace NaN with None for SQL
        df = df.where(pd.notnull(df), None)
        
        # Insert into database
        df.to_sql('rivers', self.conn, if_exists='append', index=False)
        
        print(f"  ✓ Loaded {len(df)} rivers")
        
    def load_sections(self, csv_path):
        """Load sections from CSV into database"""
        print(f"\n📋 Loading {csv_path}...")
        
        df = pd.read_csv(csv_path)
        
        # Replace NaN with None
        df = df.where(pd.notnull(df), None)
        
        # Insert into database
        df.to_sql('sections', self.conn, if_exists='append', index=False)
        
        print(f"  ✓ Loaded {len(df)} sections")
        
    def load_campaigns(self, csv_path):
        """Load campaigns from CSV into database"""
        print(f"\n📋 Loading {csv_path}...")
        
        df = pd.read_csv(csv_path)
        
        # Replace NaN with None
        df = df.where(pd.notnull(df), None)
        
        # Insert into database
        df.to_sql('campaigns', self.conn, if_exists='append', index=False)
        
        print(f"  ✓ Loaded {len(df)} campaigns")
        
    def load_measurements(self, csv_path):
        """Load measurements from CSV into database"""
        print(f"\n📋 Loading {csv_path}...")
        
        df = pd.read_csv(csv_path)
        
        # Replace NaN with None
        df = df.where(pd.notnull(df), None)
        
        # Insert into database
        df.to_sql('measurements', self.conn, if_exists='append', index=False)
        
        # Print method distribution
        methods = df['measurement_method'].value_counts()
        print(f"  ✓ Loaded {len(df)} measurements:")
        for method, count in methods.items():
            print(f"    - {method}: {count}")
        
    def print_statistics(self):
        """Print database statistics"""
        print("\n" + "="*60)
        print("DATABASE STATISTICS")
        print("="*60)
        
        cursor = self.conn.cursor()
        
        # Count records in each table
        tables = ['rivers', 'sections', 'campaigns', 'measurements']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table.upper():15s}: {count:5d} records")
        
        # Method distribution
        cursor.execute("""
            SELECT measurement_method, COUNT(*) as count 
            FROM measurements 
            GROUP BY measurement_method
            ORDER BY count DESC
        """)
        
        print("\nMeasurement methods:")
        for row in cursor.fetchall():
            print(f"  {row[0]:20s}: {row[1]:5d}")
        
        # Countries
        cursor.execute("""
            SELECT country, COUNT(*) as count 
            FROM rivers 
            GROUP BY country
            ORDER BY count DESC
        """)
        
        print("\nCountries:")
        for row in cursor.fetchall():
            print(f"  {row[0]:20s}: {row[1]:5d} rivers")
        
        print("="*60)
        
    def build(self, data_dir='data'):
        """Build complete database from CSV files"""
        data_path = Path(data_dir)
        
        # Check files exist
        required_files = ['rivers.csv', 'sections.csv', 'campaigns.csv', 'measurements.csv']
        for filename in required_files:
            filepath = data_path / filename
            if not filepath.exists():
                print(f"❌ ERROR: File not found: {filepath}")
                print(f"   Make sure all CSV files are in the '{data_dir}/' folder")
                sys.exit(1)
        
        print("="*60)
        print("BUILDING BEDLOAD TRANSPORT DATABASE")
        print("="*60)
        
        # Delete existing database
        db_file = Path(self.db_path)
        if db_file.exists():
            print(f"\n🗑️  Removing existing database: {self.db_path}")
            db_file.unlink()
        
        # Connect to database
        self.conn = sqlite3.connect(self.db_path)
        
        try:
            # Create schema
            self.create_schema()
            
            # Load data in hierarchical order
            self.load_rivers(data_path / 'rivers.csv')
            self.load_sections(data_path / 'sections.csv')
            self.load_campaigns(data_path / 'campaigns.csv')
            self.load_measurements(data_path / 'measurements.csv')
            
            # Print statistics
            self.print_statistics()
            
            print(f"\n✅ Database built successfully: {self.db_path}")
            print(f"   Size: {db_file.stat().st_size / 1024:.1f} KB")
            
        except Exception as e:
            print(f"\n❌ ERROR building database: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        finally:
            if self.conn:
                self.conn.close()

def main():
    """Main function"""
    builder = DatabaseBuilder('bedload_transport.db')
    builder.build('data')

if __name__ == '__main__':
    main()
