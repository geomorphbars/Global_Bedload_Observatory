# COMPLETE GUIDE - Filling CSV Files

**Last update: February 2026**

This guide explains how to fill the 4 CSV files of the Global Bedload Transport Database.

---

## 📋 Overview

The database consists of 4 hierarchical CSV files:

```
rivers.csv
  └─ sections.csv
      └─ campaigns.csv
          └─ measurements.csv
```

**Recommended filling order:**
1. `rivers.csv` (rivers)
2. `sections.csv` (measurement sites/sections)
3. `campaigns.csv` (measurement campaigns)
4. `measurements.csv` (individual measurements)

---

## 1️⃣ RIVERS.CSV - Rivers

### Structure (5 columns)

| Column | Type | Required | Example | Description |
|---------|------|-------------|---------|-------------|
| `river_id` | Text | ✅ YES | ARC_FRA | Unique river identifier |
| `river_name` | Text | ✅ YES | Arc | River name |
| `country` | Text | ✅ YES | FRA | ISO 3-letter country code (UPPERCASE) |
| `watershed_area_km2` | Number | ⚪ No | 2000.5 | Watershed area in km² |
| `notes` | Text | ⚪ No | Alpine river | Free notes |

### Validation rules

- ✅ **river_id**: Unique, no duplicates
- ✅ **country**: Exactly 3 UPPERCASE letters (FRA, USA, CHE, ITA, etc.)
- ✅ **watershed_area_km2**: Positive if provided

### Example rows

```csv
river_id,river_name,country,watershed_area_km2,notes
ARC_FRA,Arc,FRA,2000,Alpine river in French Alps
RHONE_CHE,Rhône,CHE,10000,Major European river
SNAKE_USA,Snake River,USA,280000,Columbia River tributary
```

### Common country codes

| Code | Country | Code | Country | Code | Country |
|------|---------|------|---------|------|---------|
| FRA | France | USA | United States | CHE | Switzerland |
| ITA | Italy | DEU | Germany | AUT | Austria |
| CAN | Canada | GBR | United Kingdom | ESP | Spain |

---

## 2️⃣ SECTIONS.CSV - Measurement sections

### Structure (10 columns)

| Column | Type | Required | Example | Description |
|---------|------|-------------|---------|-------------|
| `section_id` | Text | ✅ YES | ARC_BSM | Unique section identifier |
| `river_id` | Text | ✅ YES | ARC_FRA | River ID (must exist in rivers.csv) |
| `section_name` | Text | ✅ YES | Bourg-Saint-Maurice | Section name |
| `latitude` | Number | ✅ YES | 45.6195 | Decimal latitude WGS84 (-90 to 90) |
| `longitude` | Number | ✅ YES | 6.7693 | Decimal longitude WGS84 (-180 to 180) |
| `elevation_m` | Number | ⚪ No | 850 | Elevation in meters |
| `bankfull_width_m` | Number | ⚪ No | 45.5 | Bankfull width in meters |
| `channel_slope` | Number | ⚪ No | 0.008 | Channel slope (unitless, between 0 and 1) |
| `morphology_type` | Text | ⚪ No | braided | Channel morphological type |
| `notes` | Text | ⚪ No | Upstream of dam | Free notes |

### Validation rules

- ✅ **section_id**: Unique, no duplicates
- ✅ **river_id**: Must exist in rivers.csv
- ✅ **latitude**: Between -90 and 90
- ✅ **longitude**: Between -180 and 180
- ✅ **bankfull_width_m**: Positive if provided
- ✅ **channel_slope**: Between 0 and 1 (e.g., 0.008 = 0.8%)

### Important note: bankfull_width_m

⚠️ **Use `bankfull_width_m` (bankfull width)** not the wetted width which varies with discharge.

### Example rows

```csv
section_id,river_id,section_name,latitude,longitude,elevation_m,bankfull_width_m,channel_slope,morphology_type,notes
ARC_BSM,ARC_FRA,Bourg-Saint-Maurice,45.6195,6.7693,850,45.5,0.008,braided,Alpine section
ARC_AIG,ARC_FRA,Aigueblanche,45.5123,6.4567,780,52.0,0.006,meandering,Downstream section
```

---

## 3️⃣ CAMPAIGNS.CSV - Measurement campaigns

### Structure (7 columns)

| Column | Type | Required | Example | Description |
|---------|------|-------------|---------|-------------|
| `campaign_id` | Text | ✅ YES | ARC_2023_06 | Unique campaign identifier |
| `section_id` | Text | ✅ YES | ARC_BSM | Section ID (must exist in sections.csv) |
| `campaign_date` | Date | ✅ YES | 2023-06-15 | Campaign date (YYYY-MM-DD) |
| `data_provider` | Text | ⚪ No | John Doe | Data provider name |
| `contact_email` | Text | ⚪ No | john@university.edu | Contact email |
| `reference` | Text | ⚪ No | Doe et al. 2024 | Publication reference |
| `notes` | Text | ⚪ No | High flow event | Free notes |

### Validation rules

- ✅ **campaign_id**: Unique, no duplicates
- ✅ **section_id**: Must exist in sections.csv
- ✅ **campaign_date**: Strict format YYYY-MM-DD (e.g., 2023-06-15)
- ✅ **contact_email**: Valid email format if provided

### Example rows

```csv
campaign_id,section_id,campaign_date,data_provider,contact_email,reference,notes
ARC_2023_06,ARC_BSM,2023-06-15,John Doe,john@university.edu,Doe et al. 2024,Snowmelt period
ARC_2023_08,ARC_BSM,2023-08-20,John Doe,john@university.edu,Doe et al. 2024,Base flow
```

---

## 4️⃣ MEASUREMENTS.CSV - Measurements

### Structure (27 columns)

**The most complex file with 4 different measurement methods.**

### REQUIRED columns (4)

| Column | Type | Example | Description |
|---------|------|---------|-------------|
| `measurement_id` | Text | MEAS_001 | Unique measurement identifier |
| `campaign_id` | Text | ARC_2023_06 | Campaign ID (must exist in campaigns.csv) |
| `measurement_method` | Text | passive_acoustic | Measurement method (see below) |
| `bedload_rate_total_kg_s` | Number | 0.156 | Total bedload rate in kg/s ⭐ KEY DATA |

### Authorized methods (measurement_method)

Choose **ONE** from:
- `passive_acoustic` - Passive hydrophone
- `active_acoustic` - ADCP (Acoustic Doppler Current Profiler)
- `physical_sampler` - Physical sampler (Helley-Smith, etc.)
- `dune_tracking` - Dune tracking

---

### OPTIONAL GENERAL columns (9)

**Recommended for all measurement types:**

| Column | Type | Example | Description |
|---------|------|---------|-------------|
| `discharge_m3_s` | Number | 12.5 | Discharge in m³/s - HIGHLY RECOMMENDED |
| `discharge_source` | Text | hydrometric_station | Discharge source (see values below) |
| `discharge_station_code` | Text | V3324010 | Hydrometric station code |
| `discharge_station_name` | Text | Arc at Bourg-St-Maurice | Station name |
| `d50_mm` | Number | 35.2 | Median diameter in mm - HIGHLY RECOMMENDED |
| `d84_mm` | Number | 78.5 | 84th percentile diameter in mm |
| `d10_mm` | Number | 8.3 | 10th percentile diameter in mm |
| `water_depth_mean_m` | Number | 0.85 | Mean water depth in m |
| `flow_velocity_mean_m_s` | Number | 1.2 | Mean flow velocity in m/s |

### Values for discharge_source

| Value | When to use | Fill station code/name? |
|--------|------------------|----------------------------|
| `hydrometric_station` | Discharge from gauging station (Hydro, USGS, etc.) | ✅ YES |
| `adcp_measurement` | Discharge measured with ADCP during campaign | ❌ NO |
| `rating_curve` | Calculated from water level + rating curve | ❌ NO |
| `current_meter` | Measured with current meter | ❌ NO |
| `model` | Hydrological model | ❌ NO |
| `estimated` | Visually estimated | ❌ NO |
| `other` | Other method | ❌ NO |

**⚠️ Important:** The columns `discharge_station_code` and `discharge_station_name` must be filled **ONLY** if `discharge_source = hydrometric_station`.

---

### METHOD-SPECIFIC columns (14)

**Fill ONLY the columns corresponding to your method.**

---

#### 🎧 PASSIVE_ACOUSTIC (6 columns)

**Fill if `measurement_method = passive_acoustic`**

| Column | Type | Example | Description |
|---------|------|---------|-------------|
| `acoustic_hydrophone_type` | Text | HTI-96-MIN | Hydrophone type/model |
| `acoustic_recorder_type` | Text | SM3BAT | Acoustic recorder type |
| `acoustic_sensitivity_db` | Number | -165 | Sensitivity in dB re 1µPa² |
| `acoustic_calibration` | Text | Nasr_2023 | Calibration equation (see below) |
| `acoustic_calibration_a` | Number | 0.0015 | Parameter 'a' if calibration = other |
| `acoustic_calibration_b` | Number | 1.75 | Parameter 'b' if calibration = other |

**Values for acoustic_calibration:**
- `Nasr_2023` - Nasr et al. 2023 equation
- `Le_Guern_2024` - Le Guern et al. 2024 equation
- `other` - Custom equation (fill a and b: Qb = a × Pa^b)

**Example:**
```csv
measurement_method,acoustic_hydrophone_type,acoustic_recorder_type,acoustic_sensitivity_db,acoustic_calibration,acoustic_calibration_a,acoustic_calibration_b
passive_acoustic,HTI-96-MIN,SM3BAT,-165,Nasr_2023,,,
passive_acoustic,HTI-96-MIN,SM3BAT,-165,other,0.0015,1.75
```

---

#### 🌊 ACTIVE_ACOUSTIC / ADCP (3 columns)

**Fill if `measurement_method = active_acoustic`**

| Column | Type | Example | Description |
|---------|------|---------|-------------|
| `adcp_type` | Text | RiverRay | ADCP type/model |
| `adcp_equation_type` | Text | Rennie_2017 | Equation used for bedload |
| `adcp_measurement_duration_s` | Number | 600 | Static measurement duration in seconds |

**Examples of ADCP equations:**
- Rennie_2017
- Wright_McEwan_2008
- Rio_Matic_2020
- Latosinski_2017
- custom

**Example:**
```csv
measurement_method,adcp_type,adcp_equation_type,adcp_measurement_duration_s
active_acoustic,RiverRay,Rennie_2017,600
```

---

#### 🪣 PHYSICAL_SAMPLER (1 column)

**Fill if `measurement_method = physical_sampler`**

| Column | Type | Example | Description |
|---------|------|---------|-------------|
| `sampler_type` | Text | Helley-Smith 76mm | Sampler type and width |

**Examples of samplers:**
- Helley-Smith 76mm
- Helley-Smith 152mm
- Toutle River 305mm
- Delft bottle
- BL-84

**Example:**
```csv
measurement_method,sampler_type
physical_sampler,Helley-Smith 76mm
```

---

#### 🏔️ DUNE_TRACKING (4 columns)

**Fill if `measurement_method = dune_tracking`**

| Column | Type | Example | Description |
|---------|------|---------|-------------|
| `dune_survey_method` | Text | bathymetry | Survey method |
| `dune_echosounder_type` | Text | multibeam | Echosounder type |
| `dune_equation_type` | Text | van_den_Berg_1987 | Transport equation |
| `dune_interval_hours` | Number | 24 | Mean interval between surveys in hours |

**Values for dune_echosounder_type:**
- `single_beam` - Single beam
- `multibeam` - Multibeam
- (empty if no echosounder)

**Examples of equations:**
- van_den_Berg_1987
- Simons_1965
- Yalin_1977
- Ashley_1990

**Example:**
```csv
measurement_method,dune_survey_method,dune_echosounder_type,dune_equation_type,dune_interval_hours
dune_tracking,bathymetry,multibeam,van_den_Berg_1987,24
```

---

## 📊 COMPLETE EXAMPLES BY METHOD

### Example 1: Passive Acoustic

```csv
measurement_id,campaign_id,measurement_method,bedload_rate_total_kg_s,discharge_m3_s,discharge_source,discharge_station_code,discharge_station_name,d50_mm,d84_mm,d10_mm,water_depth_mean_m,flow_velocity_mean_m_s,acoustic_hydrophone_type,acoustic_recorder_type,acoustic_sensitivity_db,acoustic_calibration,acoustic_calibration_a,acoustic_calibration_b,adcp_type,adcp_equation_type,adcp_measurement_duration_s,sampler_type,dune_survey_method,dune_echosounder_type,dune_equation_type,dune_interval_hours
MEAS_001,ARC_2023_06,passive_acoustic,0.156,12.5,adcp_measurement,,,35.2,78.5,8.3,0.85,1.2,HTI-96-MIN,SM3BAT,-165,Nasr_2023,,,,,,,,,,
```

### Example 2: Active Acoustic (ADCP)

```csv
measurement_id,campaign_id,measurement_method,bedload_rate_total_kg_s,discharge_m3_s,discharge_source,discharge_station_code,discharge_station_name,d50_mm,d84_mm,d10_mm,water_depth_mean_m,flow_velocity_mean_m_s,acoustic_hydrophone_type,acoustic_recorder_type,acoustic_sensitivity_db,acoustic_calibration,acoustic_calibration_a,acoustic_calibration_b,adcp_type,adcp_equation_type,adcp_measurement_duration_s,sampler_type,dune_survey_method,dune_echosounder_type,dune_equation_type,dune_interval_hours
MEAS_002,ARC_2023_06,active_acoustic,0.245,18.7,hydrometric_station,V3324010,Arc at Bourg-St-Maurice,28.5,62.3,6.2,1.05,1.45,,,,,,,RiverRay,Rio_Matic_2020,300,,,,
```

### Example 3: Physical Sampler

```csv
measurement_id,campaign_id,measurement_method,bedload_rate_total_kg_s,discharge_m3_s,discharge_source,discharge_station_code,discharge_station_name,d50_mm,d84_mm,d10_mm,water_depth_mean_m,flow_velocity_mean_m_s,acoustic_hydrophone_type,acoustic_recorder_type,acoustic_sensitivity_db,acoustic_calibration,acoustic_calibration_a,acoustic_calibration_b,adcp_type,adcp_equation_type,adcp_measurement_duration_s,sampler_type,dune_survey_method,dune_echosounder_type,dune_equation_type,dune_interval_hours
MEAS_003,ARC_2023_08,physical_sampler,0.178,12.5,adcp_measurement,,,35.2,78.5,8.3,0.85,1.2,,,,,,,,,Helley-Smith 76mm,,,,
```

### Example 4: Dune Tracking

```csv
measurement_id,campaign_id,measurement_method,bedload_rate_total_kg_s,discharge_m3_s,discharge_source,discharge_station_code,discharge_station_name,d50_mm,d84_mm,d10_mm,water_depth_mean_m,flow_velocity_mean_m_s,acoustic_hydrophone_type,acoustic_recorder_type,acoustic_sensitivity_db,acoustic_calibration,acoustic_calibration_a,acoustic_calibration_b,adcp_type,adcp_equation_type,adcp_measurement_duration_s,sampler_type,dune_survey_method,dune_echosounder_type,dune_equation_type,dune_interval_hours
MEAS_004,SNAKE_2023_05,dune_tracking,1.156,95.3,hydrometric_station,USGS-13313000,Snake River at Hells Canyon,45.8,98.2,12.5,2.15,2.35,,,,,,,,,,bathymetry,multibeam,van_den_Berg_1987,24
```

---

## ✅ CHECKLIST BEFORE VALIDATION

### For all files

- [ ] UTF-8 format
- [ ] No spaces in column names
- [ ] Comma (`,`) as separator
- [ ] No empty lines
- [ ] Delete all instruction lines (starting with `#`)

### For rivers.csv

- [ ] All `river_id` are unique
- [ ] All `country` are 3 UPPERCASE letters
- [ ] `watershed_area_km2` are positive

### For sections.csv

- [ ] All `section_id` are unique
- [ ] All `river_id` exist in rivers.csv
- [ ] Latitude between -90 and 90
- [ ] Longitude between -180 and 180
- [ ] Use `bankfull_width_m` (not section_width_m)

### For campaigns.csv

- [ ] All `campaign_id` are unique
- [ ] All `section_id` exist in sections.csv
- [ ] Dates in YYYY-MM-DD format
- [ ] Valid emails if provided

### For measurements.csv

- [ ] All `measurement_id` are unique
- [ ] All `campaign_id` exist in campaigns.csv
- [ ] `measurement_method` among 4 authorized values
- [ ] `bedload_rate_total_kg_s` positive
- [ ] `discharge_m3_s` positive if provided
- [ ] `discharge_source` among authorized values
- [ ] Station code/name filled IF AND ONLY IF source = hydrometric_station
- [ ] Method-specific columns filled for correct method
- [ ] Logical order: d10 < d50 < d84

---

## 🔧 VALIDATION

**Command:**
```bash
python scripts/validate.py
```

**The script checks:**
- File structure
- Required fields
- Referential integrity (IDs)
- Formats (dates, emails, coordinates)
- Authorized values
- Data consistency

**Expected result:**
```
✅ ALL VALIDATIONS PASSED!
```

---

## 🗄️ DATABASE BUILDING

**Once validated:**
```bash
python scripts/build_database.py
```

**Generates:**
- `bedload_transport.db` (SQLite)
- With indexes for fast queries

---

## 📚 RESOURCES

**CSV Templates:**
- `template_rivers.csv` - Examples + instructions
- `template_sections.csv` - Examples + instructions
- `template_campaigns.csv` - Examples + instructions
- `template_measurements.csv` - Examples + instructions

**Python Scripts:**
- `scripts/validate.py` - Data validation
- `scripts/build_database.py` - SQLite database building

**Web Interface:**
- `explorer.html` - Interactive visualization
- Filters: Country, River, Section, Method, Date
- Export CSV/JSON

---

## ❓ Frequently Asked Questions

### Q: Can I have multiple sections on the same river?
**A:** Yes! Create as many sections as needed with different `section_id` but the same `river_id`.

### Q: Can I have multiple campaigns on the same section?
**A:** Yes! Create a new line in campaigns.csv for each campaign with different dates.

### Q: Can I mix multiple methods in the same campaign?
**A:** Yes! Create multiple lines in measurements.csv, one per method, with the same `campaign_id`.

### Q: What if I don't have discharge?
**A:** Leave `discharge_m3_s` empty. But it's highly recommended to fill it for analyses.

### Q: What to put in discharge_station_code if I don't have the info?
**A:** Leave empty if you don't know the exact code.

### Q: Is grain size d10/d50/d84 required?
**A:** No, but highly recommended. At minimum, provide d50.

---

## 📧 Contact

**For questions about filling:**
- Consult CSV templates (lines with `#`)
- Run `python scripts/validate.py` to see errors
- Contact database administrator

---

**Guide version: 2.0 - February 2026**
**Corresponds to templates: v2.0 (with discharge_source and 4 methods)**
