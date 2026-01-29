# Global Bedload Transport Database 🌊

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXX)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data](https://img.shields.io/badge/data-CSV-blue.svg)](data/)

A comprehensive, community-driven database of **bedload transport measurements** in rivers worldwide.

🔗 **[Explore the database interactively](https://bedload-database.datasette.cloud)** (Datasette interface)

---

## 📊 Database Statistics

- 🌍 **Countries**: 15
- 🏞️ **Rivers**: 45
- 📍 **Measurement sections**: 78
- 📅 **Campaigns**: 152
- 📈 **Total measurements**: 387
- 📅 **Time span**: 1985–2024
- 🔬 **Methods**: Physical samplers, Passive acoustic, Dune tracking, Tracers

*Last updated: 2025-01-29*

---

## 🎯 Purpose

This database aims to:
- Centralize scattered bedload transport data from worldwide sources
- Improve bedload transport formulas through large-scale analysis
- Enable global comparisons across rivers and methods
- Support numerical modeling validation
- Facilitate meta-analyses and synthesis studies
- Democratize access to bedload data

---

## 💾 Access the Data

### 🌐 Online Interface (Recommended)

**Datasette Web App:** [bedload-database.datasette.cloud](https://bedload-database.datasette.cloud)

Features:
- 🗺️ Interactive map of measurement sites
- 🔍 Filter and search measurements
- 📊 Pre-made summary views
- 📥 Export to CSV/JSON
- 💻 SQL query interface
- 📡 JSON API

### 📥 Direct Download (CSV)

Raw CSV files in the [`data/`](data/) directory:
- [`rivers.csv`](data/rivers.csv) - River characteristics
- [`sections.csv`](data/sections.csv) - Measurement sections
- [`campaigns.csv`](data/campaigns.csv) - Field campaigns
- [`measurements.csv`](data/measurements.csv) - Bedload measurements

### 🔌 API Access

JSON API endpoint:
```bash
# Get all measurements
curl https://bedload-database.datasette.cloud/bedload/measurements.json

# Filter by country
curl https://bedload-database.datasette.cloud/bedload/measurements.json?country=FRA

# Get summary by river
curl https://bedload-database.datasette.cloud/bedload/summary_by_river.json
```

### 🐍 Python Access

```python
import pandas as pd

# Load directly from GitHub
url = "https://raw.githubusercontent.com/USERNAME/bedload-global-database/main/data/measurements.csv"
df = pd.read_csv(url)

# Or from Datasette API
url = "https://bedload-database.datasette.cloud/bedload/measurements_full.json?_shape=array"
df = pd.read_json(url)
```

### 📦 Clone Entire Repository

```bash
git clone https://github.com/USERNAME/bedload-global-database.git
```

---

## 📖 Documentation

- **[Database Structure](docs/database_structure.md)** - Table schemas and relationships
- **[Field Definitions](docs/field_definitions.md)** - Detailed column descriptions
- **[Data Standards](docs/data_standards.md)** - Units, formats, quality control
- **[Contributing Guide](CONTRIBUTING.md)** - How to add your data
- **[Changelog](CHANGELOG.md)** - Version history

---

## 🤝 Contributing

**We welcome contributions!** 

This is a community-driven database. If you have bedload transport data to share:

1. 📧 **Email submission** (easiest): [contact@email.com](mailto:contact@email.com)
2. 🔀 **GitHub Pull Request** (for developers): See [CONTRIBUTING.md](CONTRIBUTING.md)

**What we accept:**
- Physical sampler data (Helley-Smith, etc.)
- Passive/active acoustic measurements
- Dune tracking results
- Tracer studies
- Morphological budget estimates

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.

---

## 📝 Citation

If you use this database in your research, please cite:

### Cite the database:
```
[Your Name] (2025). Global Bedload Transport Database (Version 1.0) [Data set]. 
Zenodo. https://doi.org/10.5281/zenodo.XXXXXX
```

### BibTeX:
```bibtex
@dataset{bedload_database_2025,
  author    = {Your Name},
  title     = {Global Bedload Transport Database},
  year      = {2025},
  publisher = {Zenodo},
  version   = {1.0},
  doi       = {10.5281/zenodo.XXXXXX},
  url       = {https://doi.org/10.5281/zenodo.XXXXXX}
}
```

### Cite specific data:
If using data from a specific publication, cite both:
1. The original publication (see `reference` field)
2. This database (for data access)

Example:
```
Data from Smith et al. (2020, DOI:10.xxxx/yyyy) accessed via Global Bedload 
Transport Database v1.0 (DOI:10.5281/zenodo.xxxxx).
```

---

## 📊 Database Structure

```
RIVER (e.g., Arc, Rhône)
  └── SECTION (measurement reach)
       └── CAMPAIGN (field campaign on specific date)
            └── MEASUREMENT (bedload flux measurement)
```

**4 main tables:**
1. **Rivers** - River characteristics (watershed area, country)
2. **Sections** - Measurement sections (location, width, slope)
3. **Campaigns** - Field campaigns (date, conditions, provider)
4. **Measurements** - Bedload data (flux, discharge, grain size, method)

See [database structure](docs/database_structure.md) for details.

---

## 🔬 Methods Included

| Method | n measurements | % of total |
|--------|----------------|------------|
| Physical samplers | 187 | 48% |
| Passive acoustic | 98 | 25% |
| Dune tracking | 65 | 17% |
| Tracers | 27 | 7% |
| Morphological budget | 10 | 3% |

---

## 🗺️ Geographic Coverage

**Continents:**
- Europe: 245 measurements
- North America: 89 measurements
- Asia: 32 measurements
- South America: 15 measurements
- Oceania: 6 measurements

**Top 5 countries by number of measurements:**
1. 🇫🇷 France: 98
2. 🇨🇭 Switzerland: 67
3. 🇺🇸 USA: 54
4. 🇮🇹 Italy: 32
5. 🇨🇦 Canada: 28

---

## 📜 License

**Data:** [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)  
You are free to use, share, and adapt the data with proper attribution.

**Code:** [MIT License](LICENSE)  
Scripts and tools in this repository are open source.

---

## 🙏 Acknowledgments

This database would not exist without contributions from:

**Major contributors (>50 measurements):**
- Dr. Jane Smith (University of XYZ) - 87 measurements, Arc River
- Prof. John Doe (ETH Zurich) - 65 measurements, Swiss Alpine rivers
- Dr. Marie Dupont (INRAE) - 54 measurements, French rivers

**All contributors:** See [CONTRIBUTORS.md](CONTRIBUTORS.md)

**Funding:**
- Project ANR-XXX "Bedload Dynamics" (2020-2024)
- ERC Grant XXX (2022-2027)

---

## 📧 Contact

**Database maintainer:**  
[Your Name]  
[Your Institution]  
Email: [your.email@institution.edu]

**Issues and questions:**  
- 🐛 Report bugs or issues: [GitHub Issues](https://github.com/USERNAME/bedload-global-database/issues)
- 💬 Ask questions: [GitHub Discussions](https://github.com/USERNAME/bedload-global-database/discussions)
- 📧 Email: [contact@email.com](mailto:contact@email.com)

---

## 📚 Related Resources

- **GRDC** (Global Runoff Data Centre): Water discharge data
- **GloRiC** (Global River Classification): River network database
- **Bedload databases by region:**
  - Alpine bedload database (Smith et al., 2020)
  - US bedload compilation (Doe et al., 2019)

---

## 🔄 Version History

- **v1.0.0** (2025-01-29): Initial release
  - 387 measurements from 45 rivers
  - Data from 1985-2024
  - DOI: 10.5281/zenodo.XXXXXX

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## 🚀 Future Plans

- [ ] Integrate additional published datasets from literature
- [ ] Develop rating curve analysis tools
- [ ] Add transport formula comparison module
- [ ] Create interactive visualization dashboard
- [ ] Develop machine learning predictive models
- [ ] Expand to include suspended load data (separate database)

---

## ⭐ Star this repository

If you find this database useful, please ⭐ star this repository to help others discover it!

---

**Built with:** Python, Pandas, SQLite, Datasette, GitHub, Zenodo

**Last updated:** January 2025
