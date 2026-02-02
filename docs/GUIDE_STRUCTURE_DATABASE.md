# GUIDE COMPLET - Structure de la Base de Données

**Version : Janvier 2026**  
**Global Bedload Transport Database**

---

## 📋 VUE D'ENSEMBLE

La base de données se compose de **4 tables hiérarchiques** :

```
RIVERS (Rivières)
    └── SECTIONS (Tronçons)
            └── CAMPAIGNS (Campagnes de mesure)
                    └── MEASUREMENTS (Mesures individuelles)
```

---

## 1️⃣ RIVERS - Rivières

**Fichier : `rivers.csv`**

### Colonnes OBLIGATOIRES ✅

| Colonne | Type | Format | Exemple | Description |
|---------|------|--------|---------|-------------|
| `river_id` | Texte | ID unique | `ARC_FR` | Identifiant unique de la rivière |
| `river_name` | Texte | - | `Arc` | Nom de la rivière |
| `country` | Texte | ISO 3166 (3 lettres) | `FRA` | Code pays (OBLIGATOIREMENT 3 LETTRES MAJUSCULES) |

### Colonnes FACULTATIVES ⚪

| Colonne | Type | Exemple | Description |
|---------|------|---------|-------------|
| `watershed_area_km2` | Nombre | `2170.5` | Superficie du bassin versant en km² |
| `notes` | Texte | `Alpine river...` | Notes supplémentaires |

### Codes pays (ISO 3166-1 alpha-3)
```
FRA = France          USA = États-Unis      CHE = Suisse
ITA = Italie          DEU = Allemagne       AUT = Autriche
ESP = Espagne         CAN = Canada          GBR = Royaume-Uni
JPN = Japon           AUS = Australie       NZL = Nouvelle-Zélande
```

### Exemple de données
```csv
river_id,river_name,country,watershed_area_km2,notes
ARC_FR,Arc,FRA,2170.5,Alpine glacial river
RHONE_FR,Rhône,FRA,97800,Major European river
SNAKE_USA,Snake River,USA,279719,Columbia River tributary
```

---

## 2️⃣ SECTIONS - Tronçons de rivière

**Fichier : `sections.csv`**

### Colonnes OBLIGATOIRES ✅

| Colonne | Type | Format | Exemple | Description |
|---------|------|--------|---------|-------------|
| `section_id` | Texte | ID unique | `ARC_BSM` | Identifiant unique du tronçon |
| `river_id` | Texte | Doit exister dans rivers.csv | `ARC_FR` | Lien vers la rivière |
| `section_name` | Texte | - | `Bourg-Saint-Maurice` | Nom du tronçon |
| `latitude` | Nombre | Décimal WGS84 (-90 à 90) | `45.6194` | Latitude en degrés décimaux |
| `longitude` | Nombre | Décimal WGS84 (-180 à 180) | `6.7686` | Longitude en degrés décimaux |

### Colonnes FACULTATIVES ⚪

| Colonne | Type | Unité | Exemple | Description |
|---------|------|-------|---------|-------------|
| `elevation_m` | Nombre | m | `840` | Altitude en mètres |
| `bankfull_width_m` | Nombre | m | `45.5` | Largeur à pleins bords (constante morphologique) |
| `channel_slope` | Nombre | - | `0.008` | Pente du lit (0-1, ex: 0.008 = 0.8%) |
| `morphology_type` | Texte | - | `braided` | Type morphologique (braided, meandering, straight) |
| `notes` | Texte | - | `Downstream of dam` | Notes supplémentaires |

### ⚠️ Important : bankfull_width_m
- **bankfull_width_m** = largeur à pleins bords (constante morphologique)
- Ne PAS utiliser "section_width_m" (largeur variable avec le débit)

### Exemple de données
```csv
section_id,river_id,section_name,latitude,longitude,elevation_m,bankfull_width_m,channel_slope,morphology_type,notes
ARC_BSM,ARC_FR,Bourg-Saint-Maurice,45.6194,6.7686,840,45.5,0.008,braided,Downstream of Tignes dam
ARC_AIMS,ARC_FR,Aime,45.5578,6.6478,690,52.3,0.006,braided,
RHONE_SIO,RHONE_FR,Sion,46.2344,7.3602,491,180.0,0.001,braided,Regulated section
```

---

## 3️⃣ CAMPAIGNS - Campagnes de mesure

**Fichier : `campaigns.csv`**

### Colonnes OBLIGATOIRES ✅

| Colonne | Type | Format | Exemple | Description |
|---------|------|--------|---------|-------------|
| `campaign_id` | Texte | ID unique | `ARC_BSM_2023_06` | Identifiant unique de la campagne |
| `section_id` | Texte | Doit exister dans sections.csv | `ARC_BSM` | Lien vers le tronçon |
| `campaign_date` | Date | YYYY-MM-DD | `2023-06-15` | Date de la campagne (OBLIGATOIREMENT au format ISO) |

### Colonnes FACULTATIVES ⚪

| Colonne | Type | Exemple | Description |
|---------|------|---------|-------------|
| `data_provider` | Texte | `Jules Martin` | Nom du fournisseur de données |
| `contact_email` | Texte | `jules@univ.fr` | Email de contact |
| `reference` | Texte | `Martin et al. 2023` | Référence publication |
| `notes` | Texte | `High flow event` | Notes supplémentaires |

### Exemple de données
```csv
campaign_id,section_id,campaign_date,data_provider,contact_email,reference,notes
ARC_BSM_2023_06,ARC_BSM,2023-06-15,Jules Martin,jules@univ.fr,Martin et al. 2023,Snowmelt period
ARC_BSM_2023_08,ARC_BSM,2023-08-20,Jules Martin,jules@univ.fr,Martin et al. 2023,Low flow
RHONE_SIO_2022_05,RHONE_SIO,2022-05-12,Jean Dupont,jean@epfl.ch,,Spring flood
```

---

## 4️⃣ MEASUREMENTS - Mesures individuelles

**Fichier : `measurements.csv`**

**⭐ Table la plus complexe avec 27 colonnes**

### Colonnes OBLIGATOIRES ✅ (4 colonnes)

| Colonne | Type | Format | Exemple | Description |
|---------|------|--------|---------|-------------|
| `measurement_id` | Texte | ID unique | `MEAS_001` | Identifiant unique de la mesure |
| `campaign_id` | Texte | Doit exister dans campaigns.csv | `ARC_BSM_2023_06` | Lien vers la campagne |
| `measurement_method` | Texte | Valeur imposée | `passive_acoustic` | Méthode de mesure (voir ci-dessous) |
| `bedload_rate_total_kg_s` | Nombre | kg/s | `0.156` | **DONNÉE CLÉ** : Flux de charriage total |

#### Valeurs autorisées pour measurement_method :
- `passive_acoustic` - Acoustique passive (hydrophones)
- `active_acoustic` - Acoustique active (ADCP)
- `physical_sampler` - Échantillonneur physique (Helley-Smith, etc.)
- `dune_tracking` - Suivi de dunes

---

### Colonnes GÉNÉRALES FACULTATIVES ⚪ (9 colonnes)

| Colonne | Type | Unité | Exemple | Description |
|---------|------|-------|---------|-------------|
| `discharge_m3_s` | Nombre | m³/s | `12.5` | **Très recommandé** : Débit liquide |
| `discharge_source` | Texte | - | `hydrometric_station` | Source du débit (voir ci-dessous) |
| `discharge_station_code` | Texte | - | `V3324010` | Code de la station (si source = station) |
| `discharge_station_name` | Texte | - | `Arc à Bourg-St-Maurice` | Nom de la station (si source = station) |
| `d50_mm` | Nombre | mm | `35.2` | **Très recommandé** : Diamètre médian |
| `d84_mm` | Nombre | mm | `78.5` | 84ème percentile |
| `d10_mm` | Nombre | mm | `8.3` | 10ème percentile |
| `water_depth_mean_m` | Nombre | m | `0.85` | Profondeur moyenne |
| `flow_velocity_mean_m_s` | Nombre | m/s | `1.2` | Vitesse moyenne |

#### Valeurs autorisées pour discharge_source :
- `hydrometric_station` - Station de jaugeage (base de données)  
  → **Remplir obligatoirement** `discharge_station_code` et `discharge_station_name`
- `adcp_measurement` - Mesuré avec ADCP durant la campagne
- `rating_curve` - Calculé depuis hauteur d'eau + courbe de tarage
- `current_meter` - Mesuré avec moulinet/courantomètre
- `model` - Modèle hydrologique
- `estimated` - Estimé visuellement
- `other` - Autre méthode

---

### Colonnes MÉTHODE-SPÉCIFIQUES ⚪ (14 colonnes)

**❗ Remplir UNIQUEMENT les colonnes de la méthode utilisée**

#### 🎤 PASSIVE ACOUSTIC (6 colonnes)

| Colonne | Type | Unité | Exemple | Description |
|---------|------|-------|---------|-------------|
| `acoustic_hydrophone_type` | Texte | - | `HTI-96-MIN` | Type/modèle d'hydrophone |
| `acoustic_recorder_type` | Texte | - | `SM3BAT` | Type/modèle d'enregistreur |
| `acoustic_sensitivity_db` | Nombre | dB re 1µPa² | `-165` | Sensibilité hydrophone (-180 à -150 typique) |
| `acoustic_calibration` | Texte | - | `Nasr_2023` | Équation de calibration (voir ci-dessous) |
| `acoustic_calibration_a` | Nombre | - | `0.0015` | Paramètre 'a' dans Qb = a×Pa^b (si calibration=other) |
| `acoustic_calibration_b` | Nombre | - | `1.75` | Paramètre 'b' dans Qb = a×Pa^b (si calibration=other) |

**Valeurs autorisées pour acoustic_calibration :**
- `Nasr_2023` - Équation de Nasr et al. 2023
- `Le_Guern_2024` - Équation de Le Guern et al. 2024
- `other` - Équation personnalisée → **Remplir obligatoirement** `a` et `b`

#### 📡 ACTIVE ACOUSTIC / ADCP (3 colonnes)

| Colonne | Type | Unité | Exemple | Description |
|---------|------|-------|---------|-------------|
| `adcp_type` | Texte | - | `RiverRay` | Type/modèle d'ADCP |
| `adcp_equation_type` | Texte | - | `Rennie_2017` | Équation utilisée (ex: Rennie_2017, Wright_McEwan_2008) |
| `adcp_measurement_duration_s` | Nombre | s | `300` | Durée de mesure statique (180-900s typique) |

#### 🪣 PHYSICAL SAMPLER (1 colonne)

| Colonne | Type | Exemple | Description |
|---------|------|---------|-------------|
| `sampler_type` | Texte | `Helley-Smith 76mm` | Type et largeur d'échantillonneur |

**Exemples :**
- `Helley-Smith 76mm`
- `Helley-Smith 152mm`
- `Toutle River 305mm`
- `Delft bottle`
- `BL-84`

#### 🏔️ DUNE TRACKING (4 colonnes)

| Colonne | Type | Exemple | Description |
|---------|------|---------|-------------|
| `dune_survey_method` | Texte | `bathymetry` | Méthode de levé (bathymetry, photogrammetry, lidar, sonar) |
| `dune_echosounder_type` | Texte | `multibeam` | Type d'échosondeur (single_beam, multibeam) |
| `dune_equation_type` | Texte | `van_den_Berg_1987` | Équation de transport par dunes |
| `dune_interval_hours` | Nombre | `24` | Intervalle moyen entre levés (heures) |

**Équations dune tracking courantes :**
- `van_den_Berg_1987`
- `Simons_1965`
- `Yalin_1977`
- `Ashley_1990`
- `other`

---

## 📊 EXEMPLES COMPLETS PAR MÉTHODE

### Exemple 1 : Passive Acoustic
```csv
measurement_id,campaign_id,measurement_method,bedload_rate_total_kg_s,discharge_m3_s,discharge_source,discharge_station_code,discharge_station_name,d50_mm,d84_mm,d10_mm,water_depth_mean_m,flow_velocity_mean_m_s,acoustic_hydrophone_type,acoustic_recorder_type,acoustic_sensitivity_db,acoustic_calibration,acoustic_calibration_a,acoustic_calibration_b,adcp_type,adcp_equation_type,adcp_measurement_duration_s,sampler_type,dune_survey_method,dune_echosounder_type,dune_equation_type,dune_interval_hours
MEAS_001,ARC_BSM_2023_06,passive_acoustic,0.156,12.5,adcp_measurement,,,35.2,78.5,8.3,0.85,1.2,HTI-96-MIN,SM3BAT,-165,Nasr_2023,,,,,,,,,,
```

### Exemple 2 : Active Acoustic (ADCP)
```csv
MEAS_002,ARC_BSM_2023_06,active_acoustic,0.245,18.7,hydrometric_station,V3324010,Arc à Bourg-St-Maurice,28.5,62.3,6.2,1.05,1.45,,,,,,,RiverRay,Rio_Matic_2020,300,,,,
```

### Exemple 3 : Physical Sampler
```csv
MEAS_003,ARC_BSM_2023_08,physical_sampler,0.178,12.5,adcp_measurement,,,35.2,78.5,8.3,0.85,1.2,,,,,,,,,Helley-Smith 76mm,,,
```

### Exemple 4 : Dune Tracking
```csv
MEAS_004,RHONE_SIO_2022_05,dune_tracking,1.156,95.3,hydrometric_station,CH-RHONE-SIO,Rhône à Sion,45.8,98.2,12.5,2.15,2.35,,,,,,,,,,bathymetry,multibeam,van_den_Berg_1987,24
```

---

## ✅ RÈGLES DE VALIDATION

### Identifiants uniques
- `river_id` doit être unique dans rivers.csv
- `section_id` doit être unique dans sections.csv
- `campaign_id` doit être unique dans campaigns.csv
- `measurement_id` doit être unique dans measurements.csv

### Liens hiérarchiques
- Chaque `river_id` dans sections.csv doit exister dans rivers.csv
- Chaque `section_id` dans campaigns.csv doit exister dans sections.csv
- Chaque `campaign_id` dans measurements.csv doit exister dans campaigns.csv

### Formats obligatoires
- **Dates** : YYYY-MM-DD (ex: 2023-06-15)
- **Pays** : 3 lettres majuscules (ex: FRA, USA, CHE)
- **Coordonnées** : Degrés décimaux WGS84
  - Latitude : -90 à 90
  - Longitude : -180 à 180

### Valeurs numériques
- Les valeurs négatives ne sont pas autorisées (sauf coordonnées)
- Granulométrie : d10 < d50 < d84

### Colonnes méthode-spécifiques
- **Remplir UNIQUEMENT** les colonnes de la méthode utilisée
- **Laisser VIDES** les colonnes des autres méthodes

---

## 🔧 WORKFLOW DE TRAVAIL

### 1. Télécharger les templates
```
template_rivers.csv
template_sections.csv
template_campaigns.csv
template_measurements.csv
```

### 2. Remplir avec vos données
- Supprimer les lignes d'instructions (commençant par #)
- Remplir ligne par ligne
- Respecter les formats

### 3. Valider les données
```bash
python scripts/validate.py
```

### 4. Construire la base SQLite
```bash
python scripts/build_database.py
```

### 5. Visualiser dans l'interface web
- Ouvrir `explorer.html`
- Ou pousser sur GitHub Pages

---

## 📞 CONTACT

Pour toute question sur la structure des données :
- Consulter les templates CSV (contiennent des instructions détaillées)
- Lancer le script de validation pour identifier les erreurs
- Consulter la documentation technique

---

**Version du guide : Janvier 2026**  
**Dernière mise à jour de la structure : 02/02/2026**
