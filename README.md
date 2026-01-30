# 🌊 Global Bedload Transport Database

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/geomorphbars/Global_Bedload_Observatory)

A comprehensive, community-driven database of bedload transport measurements in rivers worldwide.

---

## 🚀 Quick Access

**🌐 Interactive Explorer:** [https://geomorphbars.github.io/Global_Bedload_Observatory/](https://geomorphbars.github.io/Global_Bedload_Observatory/)

Explore measurement sites on an interactive map, view detailed data, charts, and download datasets.

---

## 📊 Database Overview

*Statistics are automatically calculated from the latest data. Visit the [homepage](https://geomorphbars.github.io/Global_Bedload_Observatory/) for current numbers.*

**Content:**
- Bedload transport measurements from rivers worldwide
- Multiple measurement methods (physical samplers, passive acoustic, dune tracking, tracers)
- Data from published literature and field campaigns
- Temporal coverage: 1980s to present
- Hierarchical structure: Rivers → Sections → Campaigns → Measurements

**Geographic coverage:**
- Europe, North America, Asia, South America, Oceania
- Focus on mountainous and gravel-bed rivers
- Expanding to lowland and sandy rivers

---

## ✨ Features

### 🗺️ Interactive Map Explorer
- **Worldwide coverage**: Visualize all measurement sites on an interactive map
- **Click to explore**: Select any site to view detailed measurements
- **Automatic charts**: Flux vs discharge, temporal evolution, and more
- **Site-specific export**: Download data for individual sites (CSV/JSON)

### 📊 Browse & Filter
- **Global view**: Access all measurements in a searchable table
- **Advanced filters**: Filter by country, method, date range
- **Batch export**: Download filtered or complete datasets
- **Multiple formats**: CSV and JSON available

### 📈 Visualizations
- Flux-discharge relationships (log-log plots)
- Temporal evolution of bedload transport
- Statistics by method and country
- Grain size distributions

### 💾 Data Access Methods

**1. Web Interface (easiest)**
```
https://geomorphbars.github.io/Global_Bedload_Observatory/explorer.html
```

**2. Direct CSV Download**
- [Rivers](https://github.com/geomorphbars/Global_Bedload_Observatory/blob/main/data/rivers.csv)
- [Sections](https://github.com/geomorphbars/Global_Bedload_Observatory/blob/main/data/sections.csv)
- [Campaigns](https://github.com/geomorphbars/Global_Bedload_Observatory/blob/main/data/campaigns.csv)
- [Measurements](https://github.com/geomorphbars/Global_Bedload_Observatory/blob/main/data/measurements.csv)

**3. Static JSON API**
```
https://geomorphbars.github.io/Global_Bedload_Observatory/api/all.json
https://geomorphbars.github.io/Global_Bedload_Observatory/api/stats.json
https://geomorphbars.github.io/Global_Bedload_Observatory/api/summary_by_country.json
https://geomorphbars.github.io/Global_Bedload_Observatory/api/summary_by_method.json
```

**4. Git Clone (for developers)**
```bash
git clone https://github.com/geomorphbars/Global_Bedload_Observatory.git
```

---

## 🤝 How to Contribute

**This is a community database!** We welcome contributions of bedload transport data from researchers worldwide.

### What Data Can I Contribute?

We accept bedload measurements obtained through:
- ✅ **Physical samplers** (Helley-Smith, Toutle River, etc.)
- ✅ **Passive acoustic monitoring** (hydrophones)
- ✅ **Active acoustic methods** (ADCP, aDcp)
- ✅ **Dune tracking** (bathymetric surveys, photogrammetry, repeat surveys)
- ✅ **Tracers** (RFID, painted clasts, magnetic tracers)
- ✅ **Morphological budgets** (repeat topography)

**Requirements:**
- Minimum information: location (lat/lon), date, bedload flux, water discharge, grain size
- Published data (peer-reviewed) OR unpublished field data with documentation
- Proper metadata (method, equipment, calibration for acoustic)

### Three Ways to Contribute

#### Option 1: Email Submission (Easiest)

**For small datasets (<20 measurements) or non-GitHub users:**

1. **Download the template:**
   - [Measurement template (CSV)](https://github.com/geomorphbars/Global_Bedload_Observatory/blob/main/templates/measurement_template.csv)
   - Or fill directly in Excel using our structure

2. **Provide this information:**
   - **River**: Name, country, watershed area
   - **Section**: Location (lat/lon), width, slope, morphology
   - **Campaign**: Date, flow conditions, your contact
   - **Measurements**: Method, flux, discharge, grain size, uncertainty

3. **Email to:** [your-email@institution.edu]
   - Subject: "Bedload database contribution - [River name]"
   - Attach completed CSV or Excel file
   - Include any relevant publications (DOI)

4. **We will:**
   - Validate and integrate your data
   - Credit you as data provider
   - Notify you when published
   - Invite you as co-author if >50 measurements

**Timeline:** Usually integrated within 2 weeks

---

#### Option 2: GitHub Pull Request (Recommended for developers)

**For larger datasets or if you're comfortable with Git:**

1. **Fork this repository**
   ```bash
   # On GitHub: Click "Fork" button
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Global_Bedload_Observatory.git
   cd Global_Bedload_Observatory
   ```

3. **Add your data to CSV files**
   - Edit `data/rivers.csv` (add river if new)
   - Edit `data/sections.csv` (add section if new)
   - Edit `data/campaigns.csv` (add campaign info)
   - Edit `data/measurements.csv` (add measurements)

4. **Validate your data**
   ```bash
   python scripts/validate.py
   ```
   Fix any errors reported

5. **Commit and push**
   ```bash
   git add data/*.csv
   git commit -m "Add measurements from [River Name] - [Your Institution]"
   git push origin main
   ```

6. **Create Pull Request**
   - On GitHub: Click "Pull Request"
   - Describe your contribution
   - We'll review and merge (usually within 1 week)

---

#### Option 3: Collaborative Integration (For large datasets)

**For major contributions (>100 measurements) or complex datasets:**

Contact us first at [your-email@institution.edu] to discuss:
- Data format and structure
- Integration strategy
- Co-authorship on data paper
- Long-term collaboration

We can help with:
- Data formatting and validation
- Quality control
- Metadata completion
- Integration into the database

---

### Data Standards

**Please ensure:**
- ✅ **Units standardized:**
  - Bedload flux: kg/s (total) or kg/s/m (unit rate)
  - Discharge: m³/s
  - Grain size: mm
  - Distances: m
  - Slopes: m/m

- ✅ **Coordinates:**
  - Decimal degrees (WGS84)
  - Example: 45.6234, 6.7654

- ✅ **Dates:**
  - Format: YYYY-MM-DD
  - Example: 2023-06-15

- ✅ **Method-specific metadata:**
  - **Acoustic**: hydrophone type, calibration equation, parameters
  - **Physical sampler**: sampler type, sampling duration, efficiency
  - **Dune tracking**: survey method, interval, dune dimensions

**See our [Data Standards Guide](docs/data_standards.md) for details.**

---

### Quality Control

All contributions go through validation:
1. **Automated checks** (script validation)
   - Required fields present
   - Value ranges realistic
   - Hierarchical consistency
   - Date formats correct

2. **Manual review**
   - Methodology appropriate
   - Metadata complete
   - No duplicate entries
   - Publications verified

3. **Quality flags assigned:**
   - **A** (Excellent): Published, peer-reviewed, rigorous
   - **B** (Good): Reliable, clear methodology
   - **C** (Acceptable): Usable but limitations
   - **D** (Questionable): Incomplete metadata

---

### Attribution & Citation

**Your contribution will be credited:**

1. **In the database:**
   - `data_provider` field contains your name/institution
   - `contact_email` for questions (optional)
   - `reference` field links to your publication (if any)

2. **On the website:**
   - Contributors page lists all data providers
   - Statistics show contributions by institution

3. **In publications:**
   - Data papers acknowledge all contributors
   - Major contributors (>50 measurements) invited as co-authors

4. **Database citation:**
   When you contribute, users will cite both:
   - The database itself (with DOI)
   - Your original publication (if applicable)

**Example citation:**
```
Data from Smith et al. (2020, https://doi.org/10.xxxx/yyyy) accessed via 
Global Bedload Transport Database v2.0 (https://doi.org/10.5281/zenodo.xxxxx)
```

---

### What Happens After Contribution?

1. **Validation** (1-7 days)
   - Automated + manual checks
   - We may contact you for clarifications

2. **Integration** (1-2 weeks)
   - Data added to database
   - Statistics updated
   - Website reflects changes

3. **Notification**
   - Email confirmation when live
   - Link to your data on the map

4. **Long-term**
   - Data preserved with DOI
   - Versioned releases
   - Credit in perpetuity

---

### Need Help?

**Before contributing:**
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions
- Review [example datasets](examples/) for formatting
- Read [Data Standards Guide](docs/data_standards.md)

**Questions?**
- 📧 Email: [your-email@institution.edu]
- 💬 GitHub Discussions: [Ask a question](https://github.com/geomorphbars/Global_Bedload_Observatory/discussions)
- 🐛 Issues: [Report a problem](https://github.com/geomorphbars/Global_Bedload_Observatory/issues)

---

## 📖 Database Structure

**Hierarchical organization:**

```
RIVER (e.g., Arc, Rhine, Colorado)
  └─ SECTION (measurement reach)
      └─ CAMPAIGN (field campaign, specific date)
          └─ MEASUREMENT (bedload flux measurement)
```

**4 main tables:**
1. **Rivers** → River characteristics (name, country, watershed area)
2. **Sections** → Measurement sections (location, width, slope, morphology)
3. **Campaigns** → Field campaigns (date, conditions, provider)
4. **Measurements** → Bedload data (flux, discharge, grain size, method)

**See [Database Documentation](docs/database_structure.md) for complete field descriptions.**

---

## 📜 License & Terms of Use

**Data License:** [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)
- ✅ Free to use, share, and adapt
- ✅ Commercial use allowed
- ⚠️ Must provide attribution

**Code License:** [MIT](LICENSE)
- ✅ Open source scripts and tools
- ✅ Free to use and modify

**Terms:**
- Cite the database and original publications
- Acknowledge data providers
- Share improvements back to the community

---

## 📝 How to Cite

### Cite the database:
```
[Maintainer Name] (2025). Global Bedload Transport Database. 
Version 1.0. https://doi.org/10.5281/zenodo.XXXXXX
```

### BibTeX:
```bibtex
@dataset{bedload_database_2025,
  author    = {Maintainer Name},
  title     = {Global Bedload Transport Database},
  year      = {2025},
  publisher = {Zenodo},
  version   = {1.0},
  doi       = {10.5281/zenodo.XXXXXX},
  url       = {https://github.com/geomorphbars/Global_Bedload_Observatory}
}
```

### Cite specific data:
If using data from a specific study:
```
Data from Smith et al. (2020) accessed via Global Bedload Transport 
Database v1.0 (DOI: 10.5281/zenodo.XXXXXX).
```

---

## 👥 Contributors

**Database maintained by:** [Your Name], [Your Institution]

**Data contributors:**
- [Institution 1] - X measurements from [River/Region]
- [Institution 2] - Y measurements from [River/Region]
- See [CONTRIBUTORS.md](CONTRIBUTORS.md) for complete list

**Want to be listed?** Contribute data! (See above)

---

## 🗺️ Roadmap

**Current version: 1.0**

**Completed:**
- ✅ Database structure and validation
- ✅ Interactive web explorer
- ✅ CSV and JSON exports
- ✅ Basic visualizations
- ✅ Static API

**Planned (v2.0):**
- [ ] Time series data (continuous monitoring)
- [ ] Suspended sediment integration
- [ ] Transport formula comparison tools
- [ ] Machine learning predictions
- [ ] Mobile app

**Long-term vision:**
- Comprehensive global coverage (all continents)
- Integration with discharge databases (GRDC)
- Real-time data from monitoring networks
- Community-driven data curation

---

## 📧 Contact

**Maintainer:** [Your Name]  
**Institution:** [Your Institution/Lab]  
**Email:** [your-email@institution.edu]  
**GitHub:** [@geomorphbars](https://github.com/geomorphbars)

**For:**
- 💡 Data contributions → Email or Pull Request
- 🐛 Bug reports → [GitHub Issues](https://github.com/geomorphbars/Global_Bedload_Observatory/issues)
- 💬 Questions → [GitHub Discussions](https://github.com/geomorphbars/Global_Bedload_Observatory/discussions)
- 🤝 Collaborations → Email

---

## 🙏 Acknowledgments

**This database would not exist without:**
- All data contributors (see CONTRIBUTORS.md)
- Funding: [Your grants/projects]
- Infrastructure: GitHub, Leaflet, Chart.js, PapaParse
- Community: Sediment transport researchers worldwide

---

## 📚 Related Resources

**Other databases:**
- [GRDC](https://www.bafg.de/GRDC/) - Global Runoff Data Centre
- [GloRiC](https://www.hydrosheds.org/products/gloric) - Global River Classification
- [HydroSHEDS](https://www.hydrosheds.org/) - Hydrological data

**Relevant projects:**
- [Your related projects]

**Publications:**
- [Key papers using this database]

---

**⭐ If you find this database useful, please star this repository!**

**Last updated:** Auto-updated via homepage  
**Version:** 1.0  
**Status:** 🟢 Active development
