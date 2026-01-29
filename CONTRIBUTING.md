# Contributing to the Global Bedload Transport Database

Thank you for your interest in contributing bedload transport data! 

This database aims to be a comprehensive, community-driven resource for bedload transport measurements worldwide. Your contributions help advance sediment transport research globally.

---

## 🎯 What data can I contribute?

We accept bedload transport measurements obtained through:
- ✅ Physical samplers (Helley-Smith, Toutle River, etc.)
- ✅ Passive acoustic monitoring
- ✅ Active acoustic methods
- ✅ Dune tracking (bathymetric surveys, photogrammetry)
- ✅ Tracers (RFID, painted clasts)
- ✅ Morphological budgets

**Requirements:**
- Published data (peer-reviewed papers) OR
- Unpublished field data with proper documentation
- Minimum information: location, date, bedload flux, discharge, grain size

---

## 📋 How to contribute

### Option 1: Simple submission (Email)

**For non-GitHub users or small datasets (<10 measurements):**

1. **Download the template:**
   - [Template spreadsheet (Excel)](link-to-template.xlsx)
   - Or use our [CSV templates](data/)

2. **Fill in your data:**
   - One row per measurement
   - See [Data Standards](#data-standards) below
   - Mark required vs optional fields

3. **Email to:** [your-email@institution.edu]
   - Subject: "Bedload database contribution - [River name]"
   - Attach filled template
   - Include: brief description, any related publications

4. **We will:**
   - Validate your data
   - Add to database with proper attribution
   - Notify you when integrated
   - Credit you in next release

---

### Option 2: GitHub Pull Request

**For GitHub users or larger datasets:**

1. **Fork this repository**
   - Click "Fork" button on GitHub

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/bedload-global-database.git
   cd bedload-global-database
   ```

3. **Add your data**
   - Edit the CSV files in `data/`:
     - `rivers.csv` - Add your river if not present
     - `sections.csv` - Add your measurement section(s)
     - `campaigns.csv` - Add your measurement campaign(s)
     - `measurements.csv` - Add your measurements

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
   - Go to your fork on GitHub
   - Click "Pull Request"
   - Describe your contribution
   - Submit!

7. **We will review and merge**
   - Usually within 1-2 weeks
   - May ask clarifying questions
   - Will acknowledge contribution

---

## 📏 Data Standards

### Required fields

**For all measurements:**
- River name and country
- Section location (lat/lon)
- Measurement date
- Measurement method
- **Bedload flux (kg/s)** - integrated over section width
- Discharge (m³/s)
- Grain size d50 (mm)
- Your contact information

### Recommended fields

**If available:**
- Number of measurement points across section
- Spatial integration method used
- Flow depth, velocity, shear stress
- Grain size d84
- Uncertainty estimate
- Hydrological context (flood/baseflow/etc.)

### Method-specific fields

**Passive acoustic:**
- Hydrophone type
- Processing software + version
- **Calibration equation** (critical!)
  - Use: `Le_Guern_2021`, `Nasr_2023`, or `site_specific`
  - If `site_specific`: provide equation details
- Calibration parameters

**Physical samplers:**
- Sampler type (e.g., "Helley-Smith 76mm")
- Number of samples
- Sampling duration per point

**Dune tracking:**
- Tracking method (bathymetry/photogrammetry)
- Survey interval
- Dune dimensions and celerity

---

## 🔍 Data Quality

We apply quality flags to all data:

- **A** (Excellent): Published, peer-reviewed, rigorous methodology
- **B** (Good): Reliable data, clear methodology
- **C** (Acceptable): Usable but some limitations
- **D** (Poor): Incomplete or questionable methodology

Your data will be assigned a quality flag during review. This helps users assess reliability.

---

## 🏷️ Attribution

**Your contributions will be acknowledged:**

1. **In the database:**
   - `data_provider` field contains your name/institution
   - `contact_email` for follow-up questions

2. **In releases:**
   - Contributors listed in release notes
   - Major contributors acknowledged in README

3. **In publications:**
   - Data papers will list all contributors
   - You can cite specific datasets with DOIs

4. **Authorship on data papers:**
   - Contributors of >50 measurements invited as co-authors
   - Contributors of >10 measurements acknowledged

---

## ✅ Data Submission Checklist

Before submitting:

- [ ] All required fields filled
- [ ] Units checked (kg/s for flux, m³/s for discharge, mm for grain size)
- [ ] Coordinates in WGS84 decimal degrees
- [ ] Dates in YYYY-MM-DD format
- [ ] Method-specific fields completed
- [ ] Data validated (if using GitHub workflow)
- [ ] Reference/DOI provided (if published data)
- [ ] Contact information included

---

## 🌍 Data Use and Licensing

**By contributing, you agree that:**

1. Your data will be released under **CC-BY-4.0** license
   - Free to use by anyone
   - Must cite original source
   - No commercial restrictions

2. Data will be publicly accessible via:
   - GitHub repository (CSV files)
   - Datasette web interface
   - API access

3. You retain ownership and copyright
   - Database provides access, not ownership transfer
   - You can publish your data elsewhere

4. Proper attribution will be maintained
   - Your name/institution stays with the data
   - Links to publications preserved

---

## ❓ FAQ

**Q: Can I contribute unpublished data?**  
A: Yes! Quality field work deserves to be shared, even if not (yet) published.

**Q: What if I only have partial information?**  
A: Submit what you have. Required minimum: location, date, flux, discharge, grain size. We prefer complete data, but partial data is valuable too.

**Q: Can I update data I previously contributed?**  
A: Yes! Email us or submit a new pull request with corrections.

**Q: How is data quality controlled?**  
A: The database maintainer validates all submissions. Obvious errors are flagged. Questionable data may be rejected or marked with lower quality flag.

**Q: Will my data be modified?**  
A: Only to standardize units or fix obvious typos. Substantive changes require your approval.

**Q: Can I withdraw my data?**  
A: Yes, contact the maintainer. Note that previously released versions (with DOIs) remain archived on Zenodo per scientific archiving best practices.

**Q: How often is the database updated?**  
A: New data integrated continuously. Major releases (with new DOI) approximately every 6 months.

**Q: Can I use the data for my research?**  
A: Absolutely! That's the goal. Please cite the database DOI.

**Q: How do I cite specific data points?**  
A: Cite both the database DOI AND the original publication if available. Example:
```
Data from Smith et al. (2020, DOI:10.xxxx/yyyy) accessed via 
Global Bedload Database v2.0 (DOI:10.5281/zenodo.xxxxx)
```

---

## 📞 Contact

**Questions about contributing?**

- Email: [your-email@institution.edu]
- GitHub Issues: [Submit a question](issues/new)
- Twitter/X: [@your-handle]

**Database maintainer:**  
[Your Name]  
[Your Institution]  
[Your Lab/Department]

---

## 🙏 Thank you!

Your contributions make this resource possible. Together we're building the most comprehensive bedload transport database in the world!

Every measurement adds value:
- Improves transport formulas
- Enables global comparisons
- Supports modeling efforts
- Advances our understanding of river processes

**Let's build this together! 🚀**
