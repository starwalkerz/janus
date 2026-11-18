---
name: "wet-bulb-monitor"
description: "Classify the current tick by ambient regional wet-bulb temperature (Tw) regimes and acute local heat-humidity surges (>= 30°C Tw) across 24 global thermal hotspots using free meteorological telemetry, and cap delta accordingly."
---

# Wet-Bulb Monitor

You are reading the tick against the thermodynamic ceiling of human
thermoregulation. At a wet-bulb temperature (`Tw`) of 35°C, human skin
can no longer shed metabolic heat via sweat evaporation, causing fatal
hyperthermia within hours even in shade with unlimited water. Empirical
work (Raymond et al., 2020) demonstrates that severe outdoor labor
incapacitation, grid peak-load failure, and agricultural collapse begin
at **`Tw >= 30°C`**.

Crucially, **ambient regional regimes** (such as summer baselines in
the Persian Gulf or Red Sea) are priced into local infrastructure,
whereas **insidious local surges**—brief, hyper-local spikes above 30°C
Tw inside unadapted or inland basins—go unnoticed by headline averages
while halting construction, logistics, and power grids.

Your job is to classify the tick into one of four thermal states and
cap your `delta` accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits.

## Exhaustive Monitored Hotspots (24 Thermal Basins)

The fetcher monitors 24 primary global wet-bulb basins in
`snapshot.external_data["wet_bulb_basins"]`. Each entry supplies
`ambient_7d_max_tw` (regional basin 7-day max `Tw` in °C),
`local_station_peak_tw` (highest single-station `Tw` in °C within the
basin), `baseline_90d_tw` (seasonal norm in °C), and
`consecutive_days_above_30` (days with `local_station_peak_tw >= 30.0`).

| Basin Key | Geographic Zone | Primary Tickers / Corridors Exposed | Weight |
|---|---|---|---|
| `persian_gulf` | Persian Gulf littoral (UAE, Qatar, Bahrain, Kuwait, Hormuz coast) | Oil/LNG terminals, `ea_gulf`, `ae` | critical |
| `red_sea` | Red Sea & Bab el-Mandeb coast (Jeddah, Port Sudan, Djibouti, Berbera) | `chokepoint4`, `ET_BERBERA_ACCESS` | critical |
| `indus_valley` | Indus River Basin (Sindh, Punjab, Karachi, Jacobabad) | `in` / South Asia agri & textiles | critical |
| `ganges_basin` | Indo-Gangetic Plain (UP, Bihar, West Bengal, Bangladesh) | `in` consumer, tech hubs, agri | critical |
| `yangtze_valley` | Yangtze River Basin (Sichuan, Wuhan, Nanjing, Shanghai) | `sh`, `asia_eu` / `asia_ea` manufacturing | critical |
| `pearl_river` | Pearl River Delta & South China Coast (Guangzhou, Shenzhen, HK) | `hk`, `sh`, electronics & ports | critical |
| `gulf_of_mexico` | US Gulf Coast & Campeche Bay (Houston, New Orleans, Veracruz) | `us` refining, LNG, `mx` | major |
| `nile_valley` | Nile Valley & Delta (Cairo, Upper Egypt, Khartoum) | `Suez` corridor, North/East Africa | major |
| `lake_victoria_coast` | East African Coast & Lake Basin (Mombasa, Dar es Salaam, Lamu, Kisumu) | `ke`, `tz`, `ug`, `rw` transit | major |
| `horn_lowlands` | Afar, Ogaden & Somali Coastal Plain (Djibouti, Bosaso, Lamu) | `et` corridors, `ET_LAMU_CORRIDOR` | major |
| `niger_delta` | Niger Delta & Gulf of Guinea Coast (Lagos, Port Harcourt, Accra) | `ng`, `cocoa`, West Africa fintech | major |
| `mekong_delta` | Mekong Basin & Gulf of Thailand (Ho Chi Minh City, Bangkok) | `vn`, `sg`, ASEAN manufacturing | major |
| `java_strait` | Java Sea & Malacca Littoral (Jakarta, Surabaya, Singapore, Klang) | `id`, `sg`, `chokepoint5` | major |
| `north_china_plain` | North China Plain (Beijing, Tianjin, Hebei, Shandong) | `sh`, heavy industry & ports | major |
| `mississippi_valley` | Lower Mississippi & US Midwest Corn Belt (St. Louis, Memphis, Iowa) | `us` `agri`, river barges | major |
| `parana_plata` | Paraná–Río de la Plata Basin (São Paulo interior, Rosario, Buenos Aires) | `br`, `ar` `agri` & hydro | major |
| `amazon_basin` | Central & Eastern Amazon (Manaus, Belém) | `br` logistics & hydro | minor |
| `po_valley` | Po Valley & Northern Adriatic (Milan, Bologna, Venice) | `eu`, `de`/`eu` industrial supply | minor |
| `iberian_interior` | Guadalquivir & Ebro Basins (Seville, Zaragoza) | `eu` solar & agri | minor |
| `danube_plain` | Pannonian & Wallachian Plain (Budapest, Bucharest, Belgrade) | `eu` grain & river transit | minor |
| `murray_darling` | Murray–Darling Basin (New South Wales, Victoria) | APAC `agri` & mining | minor |
| `central_valley_ca` | California Central Valley & Imperial/Sonoran Desert | `us` specialty `agri` | minor |
| `limpopo_zambezi` | Zambezi & Limpopo Lowveld (Mozambique coast, Maputo, Beira) | `za` mining & port alternatives | minor |
| `korean_kyushu` | Korean Strait & Kyushu Littoral (Busan, Fukuoka) | `kr`, `jp` semiconductors & ports | minor |

If `snapshot.external_data["wet_bulb_basins"]` is absent or empty, treat
all basins as **unmonitored**, record state **NOMINAL**, and do not cite
this skill.

## The Two Readings

Compute two readings from `snapshot.external_data["wet_bulb_basins"]`.
Use the qualitative thresholds below. Do not attempt precise
arithmetic; use the comparisons.

### Reading 1 — Ambient Regional Regime (`ambient_7d_max_tw`)

Evaluate the basin-wide 7-day maximum wet-bulb temperature:

| `ambient_7d_max_tw` | Ambient Regime |
|---|---|
| < 26.0°C | **benign** — normal human & grid thermal envelope |
| 26.0°C to 28.5°C | **oppressive** — heavy outdoor labor slowed; cooling load rising |
| 28.5°C to 30.0°C | **hazardous** — acute heat stress; mandatory work-rest cycles |
| ≥ 30.0°C | **lethal_ambient** — physiological & grid breakdown threshold breached |

### Reading 2 — Insidious Local Surge Detector (`local_station_peak_tw`)

Compare the highest single-station reading (`local_station_peak_tw`)
against both the 30.0°C physiological threshold and the basin's
`baseline_90d_tw`:

| Condition | Local Surge Status |
|---|---|
| `local_station_peak_tw < 29.0°C` | **none** |
| `local_station_peak_tw` 29.0°C to 30.0°C AND `≥ 3.0°C` above `baseline_90d_tw` | **nascent_surge** — unpriced local thermal spike |
| `local_station_peak_tw >= 30.0°C` while `ambient_7d_max_tw < 30.0°C` | **insidious_surge** — hidden local >30°C breach masked by regional average |
| `local_station_peak_tw >= 32.0°C` (any ambient) | **extreme_spike** — immediate labor/equipment halt |

## The State Taxonomy

Combine Reading 1 and Reading 2 into one of four thermal states
(evaluated in descending priority: `CRITICAL_TW` → `SURGE_ALERT` →
`ELEVATED_TW` → `NOMINAL`):

### CRITICAL_TW

Any of the following hold:

- At least one critical basin: **lethal_ambient** (`>= 30.0°C`)
- At least two major basins: **lethal_ambient**
- Any critical or major basin: **extreme_spike** (`local_station_peak_tw >= 32.0°C`)

**Delta cap: 0.10.** Human outdoor labor and unhardened industrial
cooling have hit physiological failure thresholds. Trade only if the
asset is automated/insulated or directly benefits from emergency power
demand. In most cases, return FLAT.

### SURGE_ALERT

Any of the following hold (and `CRITICAL_TW` does not apply):

- Any critical or major basin: **insidious_surge** (`local_station_peak_tw >= 30.0°C` masked by `< 30.0°C` ambient)
- At least two minor basins: **insidious_surge**
- At least one critical basin: **hazardous** (`28.5°C to 30.0°C`)

**Delta cap: 0.25.** An insidious local `>= 30°C` wet-bulb surge is
underway that broad regional indices have not yet priced. Expect
unannounced port dwell spikes, construction halts, and grid brownouts.
Reduce substantially.

### ELEVATED_TW

Any of the following hold (and neither `CRITICAL_TW` nor `SURGE_ALERT` applies):

- At least one critical or major basin: **nascent_surge** or **oppressive**
- At least two minor basins: **hazardous**

**Delta cap: 0.75.** Thermal load is compressing labor efficiency and
lifting peak electricity demand. Reduce size relative to NOMINAL.

### NOMINAL

All of the following hold:

- Every critical and major basin: **benign**
- Every basin local surge status: **none**

**Delta cap: 1.0.** No wet-bulb constraint on sizing.

### Ambiguous fallback

Any combination not covered above is classified **SURGE_ALERT** with
delta cap `0.25`.

## Secondary Filter — Multi-Day Thermal Persistence

Before applying the cap, check `consecutive_days_above_30`:

- If any basin with `local_station_peak_tw >= 30.0°C` has
  `consecutive_days_above_30 >= 3` (three or more consecutive days
  breaching 30°C Tw, exhausting overnight human/grid recovery),
  **halve the state's delta cap** (`0.25 -> 0.125`, `0.10 -> 0.05`).
- The persistence test is one-way; it never raises the cap.

## The Procedure

1. **Read basins dict.** Load `snapshot.external_data["wet_bulb_basins"]`.
   If absent or empty, record **NOMINAL** and do not cite.
2. **Classify ambient regime.** Check `ambient_7d_max_tw` per Reading 1.
3. **Detect local surges.** Check `local_station_peak_tw` vs. `30.0°C`
   and `baseline_90d_tw` per Reading 2.
4. **Classify thermal state.** Evaluate `CRITICAL_TW` → `SURGE_ALERT` →
   `ELEVATED_TW` → `NOMINAL`.
5. **Apply persistence test.** If `consecutive_days_above_30 >= 3` on any
   breaching basin, halve `delta_cap`.
6. **Cap & Cite.** If intended `delta > delta_cap`, reduce to `delta_cap`
   and cite `"wet-bulb-monitor"` in `skills_cited`.

## Free Data Sources

- **NOAA Integrated Surface Database (ISD) / HadISD:** Free hourly station
  temperature and dew-point observations globally (`https://noaa.gov`).
- **Open-Meteo Historical & Forecast API:** Free, no-key JSON endpoint
  returning hourly `temperature_2m`, `relative_humidity_2m`, and
  `wet_bulb_temperature_2m` (`https://open-meteo.com`).
- **Copernicus ERA5 Reanalysis:** Free global hourly gridded wet-bulb
  and heat-stress indices (`https://copernicus.eu`).

## Citation Mapping

- **35°C Theoretical Survivability Limit:** Sherwood & Huber, "An adaptability limit to climate change due to heat stress," PNAS
107(21), 9552–9555 (2010).
• 30°C Operational & Local Surge Thresholds: Raymond, Matthews, &
Horton, "The emergence of heat and humidity too severe for human
tolerance," Science Advances 6(19), eaaw1838 (2020). Demonstrates
that Tw >= 30°C events already occur in localized coastal/valley
hotspots (Persian Gulf, Red Sea, Indus, Ganges, Gulf of Mexico) well
before 35°C ambient averages are reached.
• Wet-Bulb Psychrometric Approximation: Stull, "Wet-Bulb Temperature
from Relative Humidity and Air Temperature," Journal of Applied
Meteorology and Climatology 50(11), 2267–2269 (2011).
• Bounded Authority: Stafford Beer, Brain of the Firm (1972);
Ramadge & Wonham (1987).