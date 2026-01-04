# Capital One Data Challenge - Notebook Evaluation Report
## Submission by: Abhigyan Ghosh

---

## EXECUTIVE SUMMARY

**Overall Assessment: STRONG SUBMISSION with some areas for improvement**

The notebook demonstrates solid data analysis skills, clean code organization, and addresses all 5 required questions. The candidate shows strong builder mindset with reusable functions, thorough data quality checks, and well-documented analysis. However, there are some technical issues with the cost calculations and metadata documentation that need attention.

**Score Breakdown:**
- ✅ All 5 questions answered: YES
- ✅ Data quality checks (3+ documented): YES (multiple issues found and documented)
- ✅ Reusable functions: YES (4 functions created)
- ⚠️ Metadata documentation: PARTIAL (inline comments present, no formal data dictionary)
- ✅ Visualizations & storytelling: YES (8 visualizations with clear narrative)
- ⚠️ Calculation correctness: ISSUES IDENTIFIED (see details below)

---

## 1. REQUIRED DELIVERABLES - DETAILED ASSESSMENT

### Question 1: Top 10 Busiest Routes ✅ COMPLETE
**Location:** Cells 80-82

**Implementation:**
- Correctly normalizes bidirectional routes (A→B and B→A) using min/max
- Properly excludes canceled flights (filtered earlier in Cell 31)
- Groups by route pairs and counts flights
- Ranks and selects top 10
- Provides visualization (Cell 82)

**Strengths:**
- Clean normalization logic: `final_merge[['ORIGIN','DESTINATION']].min(axis=1)`
- Good use of aggregation with .agg() for clarity
- Visualization is clear and labeled

**Code Quality:** Excellent

---

### Question 2: Top 10 Most Profitable Routes ⚠️ COMPLETE WITH ISSUES
**Location:** Cells 83-86

**Implementation:**
- Cell 84: Documents cost/revenue assumptions (matches requirements)
- Cell 85: Calculates per-flight costs and revenues
- Aggregates to route level
- Shows breakdown of total_cost, total_revenue, profit, flight counts

**CRITICAL ISSUES IDENTIFIED:**

#### Issue 1: Round Trip vs One-Way Confusion 🔴
The analysis treats each flight leg independently but the requirement asks for "round trip routes."

**Current approach:**
```python
final_merge['route_name'] = final_merge['ORIGIN'] + '-' + final_merge['DESTINATION']
# This creates: LAX-JFK and JFK-LAX as separate routes
```

**Problem:** When calculating profitability, the code should:
1. Either pair outbound and return legs as one round trip
2. Or clearly state that each directional leg is being analyzed separately

**Impact:** The route_name 'FLO-CLT' might only represent flights FROM Florence TO Charlotte, not the full round trip. This makes the breakeven analysis potentially incorrect.

#### Issue 2: Airport Fees - One-Way vs Round Trip
```python
final_merge['airport_fixed_cost'] = final_merge['TYPE_destination'].apply(
    lambda x: 5000 if x == 'medium_airport' else 10000
)
```

**Analysis:**
- This correctly charges ONE fee per landing
- For a true round trip, there should be TWO landing fees (one at each end)
- If each flight leg is analyzed separately (current approach), this is correct
- But the requirement asks for "round trip routes" suggesting paired analysis

#### Issue 3: Baggage Fee Calculation
```python
final_merge['revenue_from_baggage_fees'] = (
    final_merge['total_passengers'] * 0.5 * 35
).round(2)
```

**Requirement states:** "50% of passengers will be charged a total of 70 dollars in baggage fees for a round trip flight"

**Current calculation:** $35 per leg (correct for one-way)
**For round trip:** Should be $70 total per round trip passenger, not $35 per leg

**However:** Since the analysis appears to treat each leg separately, $35 per leg is actually correct. The issue is the semantic confusion about what a "round trip route" means in this analysis.

**Strengths Despite Issues:**
- All cost components are included
- Formulas match the stated assumptions
- Code is well-commented
- Proper aggregation and formatting

**Recommendation:** Clarify whether analyzing directional routes or true paired round trips. The current approach is internally consistent but may not match the requirement's intent.

---

### Question 3: 5 Recommended Routes ✅ EXCELLENT
**Location:** Cells 88-91

**Implementation:**
- Uses sophisticated airline metrics (CASM, RASM, unit margin)
- Filters for operational reliability (≥80% on-time)
- Ranks by unit margin (RASM - CASM)
- Provides clear business justification

**Recommended Routes:**
1. FLO-CLT
2. WRG-PSG
3. PHL-MDT
4. GSP-CLT
5. PSG-WRG

**Selection Criteria (Cell 91):**
- Maximum unit margin (RASM − CASM)
- Reliable operations (≥80% on-time)
- Sufficient scale (total round-trip volume)

**Strengths:**
- Uses industry-standard metrics (ASM, CASM, RASM)
- Clear definitions provided for each metric
- Multi-criteria selection (profitability + reliability + scale)
- Well-documented rationale

**This is the strongest section of the analysis** - shows deep understanding of airline economics.

---

### Question 4: Breakeven Analysis ⚠️ COMPLETE WITH ISSUES
**Location:** Cells 92-95

**Implementation:**
```python
upfront_cost = 90_000_000
breakeven_df['round_trips_to_breakeven'] = breakeven_df['profit_per_trip'] \
    .apply(lambda p: math.ceil(upfront_cost / p))
```

**Results:**
- FLO-CLT: 365 flights
- PHL-MDT: 799 flights
- GSP-CLT: 916 flights
- WRG-PSG: 1,892 flights
- PSG-WRG: 2,832 flights

**ISSUES:**

#### Issue 1: One-Way vs Round Trip Semantics
If `profit_per_trip` is calculated from one-way legs, then the breakeven calculation is dividing by one-way profit, not round-trip profit.

**Example:**
- If FLO→CLT makes $X profit per flight
- And CLT→FLO makes $Y profit per flight
- Then round-trip profit = $X + $Y
- Current calculation uses only $X (or only $Y depending on route_name)

**Verification Needed:** Check if the original flights data contains both directions or if each flight is a one-way leg.

#### Issue 2: Temporal Feasibility Not Discussed
- 365 flights at current quarterly volume would take X quarters
- This analysis should include timeline context

**Strengths:**
- Correct use of math.ceil() for whole flights
- Clear visualization (Cell 94)
- Good summary of results (Cell 95)

---

### Question 5: KPIs ✅ COMPLETE
**Location:** Cells 96-97

**KPIs Recommended:**
1. Seat Distribution (Business vs Economy)
2. Target Audience Analysis (demographics)
3. Local Economic Factors
4. Promotions and Pricing
5. Airport Load Factors
6. Weather Impacts
7. Government Support
8. Flight Change Management
9. Onboard Services Analysis

**Assessment:**
- Comprehensive list of KPIs
- Goes beyond basic operational metrics
- Includes strategic factors (economic, government, marketing)

**Weakness:**
- KPIs are generic airline metrics, not specific to the 5 recommended routes
- Missing route-specific KPIs like:
  - Market share on recommended routes
  - Competitor pricing on these routes
  - Seasonal demand patterns for these specific city pairs

**Overall:** Good but could be more targeted.

---

## 2. DATA QUALITY CHECKS ✅ EXCELLENT

**Requirement:** At least 3 data quality issues documented

**Found:** 27 cells with data quality checks covering:

### Airports Dataset (Cells 12-28)
1. **Filtering to US airports only** (Cell 16)
   - `ISO_COUNTRY == 'US'`

2. **Filtering to medium/large airports** (Cell 16)
   - `TYPE.isin(['medium_airport', 'large_airport'])`

3. **Duplicate check** (Cell 22)
   - Result: No duplicates found

4. **Unnecessary columns removed** (Cell 26)
   - Dropped: CONTINENT, ISO_COUNTRY, MUNICIPALITY, COORDINATES, ELEVATION_FT

### Flights Dataset (Cells 29-53)
1. **Canceled flights exclusion** (Cell 31)
   - Critical: Removes CANCELLED == 1

2. **Duplicate rows** (Cells 40-41)
   - Found: 4,410 duplicates removed

3. **Missing values analysis** (Cells 46-49)
   - Identified missing values in: DEP_DELAY, ARR_DELAY, AIR_TIME, DISTANCE, OCCUPANCY_RATE
   - **Documented insight:** Outliers are legitimate operational data, not errors

4. **Outlier treatment strategy** (Cell 50)
   - Decision: Median imputation instead of removal
   - **Well-justified rationale:** Extreme delays are real events, removing them loses business insight

5. **Data type optimization** (Cells 32-38)
   - Converted dates, numeric fields

### Tickets Dataset (Cells 54-73)
1. **Round trip filter** (Cell 57)
   - `ROUNDTRIP == 1`

2. **Duplicate rows** (Cells 62-63)
   - Found: 47,564 duplicates removed (Cell 64)

3. **Missing values** (Cells 64, 71)
   - Median imputation for PASSENGERS and ITIN_FARE

4. **Invalid data filter** (Cell 77)
   - Removes zero/negative fares and passenger counts

### Summary (Cell 74)
Excellent comprehensive summary of all data quality steps across all three datasets.

**Assessment:** FAR EXCEEDS the requirement of 3 documented issues. Shows thorough data understanding.

---

## 3. BUILDER MINDSET - CODE QUALITY ✅ STRONG

### Reusable Functions (Cell 8)
**Found:** 4 well-designed functions

1. **`read_csv(file_name, base_path)`**
   - Purpose: Load CSV with standardized column names
   - Strips whitespace from headers
   - Configurable base path
   - Good docstring

2. **`optimize_data_types(df)`**
   - Purpose: Reduce memory usage
   - Downcasts integers and floats
   - Handles null values in object columns
   - Comprehensive docstring

3. **`to_number(df, field_names)`**
   - Purpose: Convert columns to numeric
   - Accepts single column or list
   - Uses errors='coerce' for safety
   - Flexible input handling

4. **`impute_with_median(df, columns_to_impute)`**
   - Purpose: Median imputation for missing values
   - Iterates over column list
   - Clear documentation

**Strengths:**
- All functions have docstrings
- Type hints on function signatures
- Defensive programming (error handling, none checks)
- DRY principle applied

**Code Formatting:**
- Consistent indentation
- Clear variable names
- Inline comments throughout analysis (15+ comment lines in Cell 85 alone)
- Logical section organization

**Data Joins (Cells 76-78):**
✅ Reusable pattern, not a dedicated function, but well-documented:
- Step-wise join approach explained
- Aggregation before join (reduces cardinality)
- Clear merge strategy documented
- Inner joins used appropriately

**Assessment:** Strong builder mindset. Code is production-quality with documentation.

**Minor Suggestion:** Could create a reusable merge function, but the current approach with detailed comments is acceptable.

---

## 4. METADATA DOCUMENTATION ⚠️ PARTIAL

**Requirement:** Metadata for created fields

**What Was Found:**

### Inline Comments in Code (Cell 85) ✅
```python
# Airport fee: one per arrival leg
final_merge['airport_fixed_cost'] = ...

# Variable per-mile costs
final_merge['fuel_cost'] = ...
final_merge['depreciation_cost'] = ...

# Delay penalties (first 15 min free, then $75/min)
final_merge['dep_delay_cost'] = ...

# Baggage fees: $35 × 50% pax per leg
final_merge['revenue_from_baggage_fees'] = ...

# Ticket revenue: pax × median fare
final_merge['revenue_from_tickets'] = ...
```

### Cost Assumptions Documentation (Cell 84) ✅
Complete list of all cost parameters with explanations

### Metric Definitions (Cell 91) ✅
- CASM definition with example
- RASM definition with example
- Unit Margin (Spread) definition
- On-Time Performance threshold
- Total Round-Trips counting

**What Was NOT Found:**

### Formal Data Dictionary ❌
No centralized table or section listing:
- Field name | Type | Description | Calculation | Example

**Example of what's missing:**
```
| Field Name | Data Type | Description | Formula | Example |
|------------|-----------|-------------|---------|---------|
| airport_fixed_cost | float | Landing fee per airport | $5K (medium) or $10K (large) | 10000.00 |
| fuel_cost | float | Fuel/oil/maintenance/crew cost | DISTANCE × $8 | 1600.00 |
| total_passengers | int | Passengers on flight | 200 × OCCUPANCY_RATE | 156 |
```

**Assessment:**
- **Inline documentation:** Excellent
- **Assumptions documentation:** Excellent
- **Formal metadata table:** Missing

**Recommendation:** Add a markdown cell with a formal data dictionary for all calculated fields. Current inline comments are good but a centralized reference would be better.

**Does this meet the requirement?** Borderline. The inline comments provide metadata, but a formal data dictionary would be stronger.

---

## 5. VISUALIZATIONS & STORYTELLING ✅ STRONG

**Found:** 8 visualizations across the analysis

### Visualization 1: Missing Values Bar Chart (Cell 48)
**Purpose:** Show missing data patterns in flights dataset
**Type:** Horizontal bar chart
**Quality:**
- Professional styling (colors, fonts, gridlines)
- Value labels on bars
- Clear title and axis labels
- Supports data quality narrative

**Effectiveness:** Excellent for EDA

### Visualization 2: Outlier Box Plots (Cell 49)
**Purpose:** Visualize distributions and outliers in flight data
**Type:** Multi-panel box plots
**Quality:**
- Professional color palette
- Clear median line highlighting
- Grid layout for multiple variables
- Outliers marked clearly

**Effectiveness:** Strong support for imputation strategy justification

### Visualization 3: Top 10 Busiest Routes (Cell 82)
**Purpose:** Answer Q1 visually
**Type:** Horizontal bar chart
**Quality:**
- Clean design
- Routes sorted by count
- Value labels
- Inverted y-axis for readability

**Effectiveness:** Clear answer to Q1

### Visualization 4: Top 10 Profitable Routes (Cell 86)
**Purpose:** Answer Q2 visually
**Type:** Horizontal bar chart with dollar formatting
**Quality:**
- Professional styling
- Sorted by profit
- Dollar labels with formatting
- Clear title

**Effectiveness:** Strong visual summary of Q2

### Visualization 5: Recommended Routes by Unit Margin (Cell 90)
**Purpose:** Support Q3 recommendations
**Type:** Horizontal bar chart
**Quality:**
- Shows unit margin (RASM - CASM)
- Clear labeling
- Professional appearance

**Effectiveness:** Excellent business context for recommendations

### Visualization 6: Breakeven Flights Chart (Cell 94)
**Purpose:** Answer Q4 visually
**Type:** Horizontal bar chart
**Quality:**
- Sorted by breakeven flights (easiest first)
- Value labels with comma formatting
- Clear axis labels

**Effectiveness:** Makes breakeven analysis immediately understandable

**Overall Visualization Assessment:**

**Variety:** ✅
- Bar charts (multiple variations)
- Box plots
- Different orientations and stylings

**Storytelling:** ✅
- Each viz supports a specific business question
- Logical flow from EDA → Analysis → Recommendations
- Professional appearance throughout

**Technical Quality:** ✅
- Proper use of matplotlib
- Consistent styling
- Appropriate chart types
- Good data-ink ratio

**Areas for Improvement:**
1. Could add more variety (scatter plots, heatmaps for correlations)
2. No geographic visualization (route maps would be powerful)
3. No trend analysis (time series of metrics)

**Grade:** Strong B+ / A-

---

## 6. CALCULATION CORRECTNESS - DETAILED REVIEW

### Cost Calculations

#### Fuel/Oil/Maintenance/Crew ✅
```python
final_merge['fuel_cost'] = final_merge['DISTANCE'] * 8
```
**Assessment:** CORRECT
- Matches requirement: $8/mile
- Applied to distance column

#### Depreciation/Insurance/Other ✅
```python
final_merge['depreciation_cost'] = (1.18 * final_merge['DISTANCE']).round(2)
```
**Assessment:** CORRECT
- Matches requirement: $1.18/mile
- Properly rounded

#### Airport Fees ✅ (for one-way legs)
```python
final_merge['airport_fixed_cost'] = final_merge['TYPE_destination'].apply(
    lambda x: 5000 if x == 'medium_airport' else 10000
)
```
**Assessment:** CORRECT for one-way analysis
- $5K for medium, $10K for large
- Charges destination airport (where plane lands)

**Issue:** For round trip analysis, should charge BOTH airports

#### Delay Costs ✅
```python
final_merge['dep_delay_cost'] = final_merge['DEP_DELAY'].apply(
    lambda x: (x - 15) * 75 if x > 15 else 0
)
final_merge['arr_delay_cost'] = final_merge['ARR_DELAY'].apply(
    lambda x: (x - 15) * 75 if x > 15 else 0
)
```
**Assessment:** CORRECT
- First 15 minutes free
- $75/min after that
- Separate for departure and arrival

### Revenue Calculations

#### Baggage Fees ✅ (for one-way legs)
```python
final_merge['revenue_from_baggage_fees'] = (
    final_merge['total_passengers'] * 0.5 * 35
).round(2)
```
**Assessment:** CORRECT for one-way analysis
- $35 per bag
- 50% of passengers check bags
- Per leg calculation

**Semantic Issue:** Requirement says "50% of passengers will be charged a total of 70 dollars in baggage fees for a round trip flight"
- This implies $70 total for round trip
- Which is $35 per leg (what the code does)
- So technically correct, but wording is confusing

#### Ticket Revenue ⚠️ POTENTIAL ISSUE
```python
final_merge['revenue_from_tickets'] = (
    final_merge['total_passengers'] * final_merge['median_fare']
).round(2)
```

**Question:** What does `median_fare` represent?

Looking at Cell 77:
```python
tickets_filtered = (
    tickets[...]
    .groupby(['ORIGIN', 'DESTINATION'])
    .agg(median_fare=('ITIN_FARE', 'median'))
    .reset_index()
)
```

**Issue:** `ITIN_FARE` in the tickets dataset is likely the TOTAL itinerary fare (round trip), not one-way fare.

**If ITIN_FARE is round-trip fare:**
- Using it for one-way revenue doubles the revenue
- This would overstate profitability significantly

**If ITIN_FARE is one-way fare:**
- Calculation is correct

**Recommendation:** VERIFY what ITIN_FARE represents in the original data. This is critical for accuracy.

#### Passenger Count ✅
```python
final_merge['total_passengers'] = (200 * final_merge['OCCUPANCY_RATE']).round().astype(int)
```
**Assessment:** CORRECT
- 200 seat capacity
- Uses occupancy rate from flights data (as required)
- Rounded to integer

### Aggregation Logic ⚠️

#### Route-Level Aggregation
```python
route_summary = (
    final_merge
    .groupby('route_name')
    .agg(
        total_cost        = ('total_cost',        'sum'),
        total_revenue     = ('total_revenue',     'sum'),
        profit            = ('profit',            'sum'),
        total_round_trips = ('ORIGIN',            'size')
    )
    .reset_index()
)
```

**Issue:** The variable name `total_round_trips` is misleading
- `.size()` counts the number of flight legs
- If route_name is 'LAX-JFK', this counts LAX→JFK flights only
- It does NOT count paired round trips (LAX→JFK→LAX)

**Impact:**
- Breakeven calculation divides $90M by profit_per_trip
- If profit_per_trip is based on one-way legs, the result is one-way legs needed
- Not round trips needed

**This is the most significant calculation issue in the notebook.**

### Recommended Fix

To properly analyze round trips:

```python
# Create bidirectional route identifier
final_merge['route_pair'] = final_merge[['ORIGIN','DESTINATION']].apply(
    lambda x: '-'.join(sorted([x['ORIGIN'], x['DESTINATION']])), axis=1
)

# Aggregate to route pair level
route_summary = (
    final_merge
    .groupby('route_pair')
    .agg(...)
)

# For true round trip profit, sum outbound + return legs
```

---

## 7. OVERALL STRENGTHS

1. **Excellent Code Organization**
   - Clear section headers
   - Logical flow from data loading → cleaning → analysis → recommendations
   - 99 cells well-organized into 42 markdown + 57 code

2. **Strong Data Quality Mindset**
   - 27 cells dedicated to data quality
   - Thoughtful treatment of outliers (kept as real data)
   - Well-justified imputation strategy
   - Comprehensive summary of all cleaning steps

3. **Professional Documentation**
   - Docstrings on all functions
   - Inline comments throughout
   - Clear markdown explanations
   - Business context provided

4. **Sophisticated Analysis**
   - Use of airline industry metrics (CASM, RASM, ASM)
   - Multi-criteria route selection
   - Operational reliability considered (on-time performance)

5. **Good Visualizations**
   - Professional styling
   - Appropriate chart types
   - Clear labeling
   - Supports narrative

6. **Reusable Code**
   - 4 utility functions
   - Configurable parameters
   - Type hints
   - Error handling

---

## 8. AREAS FOR IMPROVEMENT

### Critical Issues

1. **Round Trip Semantics** 🔴
   - Current analysis treats directional routes (A→B) as separate from (B→A)
   - Requirement asks for "round trip routes"
   - Need to clarify: Are we analyzing one-way routes or paired round trips?
   - **Impact:** Affects Q1, Q2, Q3, Q4 interpretations

2. **Revenue Calculation Verification** 🔴
   - Need to verify if ITIN_FARE is round-trip or one-way
   - If round-trip, current calculation doubles revenue
   - **Impact:** Profitability and recommendations may be overstated

3. **Breakeven Analysis** 🟡
   - Currently calculates one-way legs needed, not round trips
   - Variable naming is misleading (`total_round_trips` counts one-way legs)
   - **Impact:** Q4 answer may not match requirement intent

### Documentation Issues

4. **Metadata Format** 🟡
   - Inline comments are good but not comprehensive metadata
   - Missing formal data dictionary
   - **Recommendation:** Add a markdown cell with structured field documentation

5. **Route-Specific KPIs** 🟡
   - Q5 KPIs are generic airline metrics
   - Missing route-specific tracking metrics
   - **Recommendation:** Add market share, competitor pricing for recommended routes

### Analysis Enhancements

6. **Temporal Analysis** 🟢
   - No time-to-breakeven calculation
   - "365 flights needed" but no timeline given
   - **Recommendation:** Calculate quarters/years to breakeven at current volume

7. **Visualization Variety** 🟢
   - All visualizations are bar charts or box plots
   - Could add: route maps, scatter plots, correlation heatmaps
   - **Recommendation:** Add 1-2 different visualization types

8. **Sensitivity Analysis** 🟢
   - No analysis of what happens if occupancy drops or costs rise
   - **Recommendation:** Show how breakeven changes with ±10% occupancy

---

## 9. SPECIFIC TECHNICAL RECOMMENDATIONS

### Fix 1: Clarify Round Trip Analysis

**Current Code (Cell 81):**
```python
final_merge['route_start'] = final_merge[['ORIGIN','DESTINATION']].min(axis=1)
final_merge['route_end']   = final_merge[['ORIGIN','DESTINATION']].max(axis=1)
```

**Issue:** This normalizes A-B and B-A, but then groups them separately later

**Recommended Approach:**
```python
# Create bidirectional route identifier
def create_route_pair(row):
    return '-'.join(sorted([row['ORIGIN'], row['DESTINATION']]))

final_merge['route_pair'] = final_merge.apply(create_route_pair, axis=1)

# Identify direction
final_merge['direction'] = final_merge.apply(
    lambda x: 'outbound' if x['ORIGIN'] < x['DESTINATION'] else 'return',
    axis=1
)

# For round trip analysis, sum both directions
round_trip_summary = (
    final_merge
    .groupby(['route_pair', 'direction'])
    .agg(...)
    .unstack(fill_value=0)
)
```

### Fix 2: Verify Ticket Fare Interpretation

**Add this analysis cell:**
```python
# Verify ITIN_FARE interpretation
print("Ticket data roundtrip filter:", tickets['ROUNDTRIP'].unique())
print("Average fare by roundtrip flag:")
print(tickets.groupby('ROUNDTRIP')['ITIN_FARE'].mean())

# If ITIN_FARE is round-trip, divide by 2 for one-way revenue
if ITIN_FARE_is_roundtrip:
    final_merge['fare_per_leg'] = final_merge['median_fare'] / 2
else:
    final_merge['fare_per_leg'] = final_merge['median_fare']
```

### Fix 3: Add Formal Metadata

**Add this markdown cell before Cell 85:**
```markdown
## Data Dictionary - Calculated Fields

| Field Name | Data Type | Description | Formula | Example |
|------------|-----------|-------------|---------|---------|
| airport_fixed_cost | float64 | Landing fee at destination airport | $5,000 (medium) or $10,000 (large) | 10000.00 |
| fuel_cost | float64 | Fuel, oil, maintenance, crew cost | DISTANCE × $8 | 1600.00 |
| depreciation_cost | float64 | Depreciation, insurance, other | DISTANCE × $1.18 | 236.00 |
| dep_delay_cost | float64 | Departure delay penalty | max(0, (DEP_DELAY - 15) × $75) | 750.00 |
| arr_delay_cost | float64 | Arrival delay penalty | max(0, (ARR_DELAY - 15) × $75) | 375.00 |
| total_passengers | int64 | Passengers on flight | round(200 × OCCUPANCY_RATE) | 156 |
| revenue_from_baggage_fees | float64 | Baggage fee revenue | total_passengers × 0.5 × $35 | 2730.00 |
| revenue_from_tickets | float64 | Ticket sale revenue | total_passengers × median_fare | 31200.00 |
| total_cost | float64 | Total flight cost | sum of all cost components | 12586.00 |
| total_revenue | float64 | Total flight revenue | tickets + baggage | 33930.00 |
| profit | float64 | Flight profitability | total_revenue - total_cost | 21344.00 |
```

### Fix 4: Enhance KPIs for Recommended Routes

**Add to Cell 97:**
```markdown
## Route-Specific KPIs for Recommended Routes

For the 5 recommended routes (FLO-CLT, WRG-PSG, PHL-MDT, GSP-CLT, PSG-WRG), track:

1. **Market Share:** % of passengers on this route using our airline vs competitors
2. **Yield Management:** Average fare vs. competitor fares on same route
3. **Load Factor Trend:** Monthly occupancy rate trend (target: maintain >75%)
4. **On-Time Performance:** Maintain >80% on-time (leading indicator of customer satisfaction)
5. **Unit Margin Trend:** Track RASM - CASM over time (detect deterioration early)
6. **Customer Satisfaction:** NPS score for passengers on these specific routes
7. **Frequency Competitiveness:** Number of daily flights vs. competitors
8. **Breakeven Progress:** Flights completed toward 90M payback goal
9. **Route-Specific Delays:** Track delay patterns by route to identify operational issues
10. **Seasonal Demand:** Quarter-over-quarter volume changes to adjust capacity
```

---

## 10. FINAL ASSESSMENT SUMMARY

### Does the Submission Meet Requirements?

| Requirement | Status | Details |
|-------------|--------|---------|
| Q1: Top 10 Busiest Routes | ✅ PASS | Correct logic, good viz, excludes canceled |
| Q2: Top 10 Profitable Routes | ⚠️ CONDITIONAL | All components present, but semantic issues with round-trip interpretation |
| Q3: 5 Recommended Routes | ✅ PASS | Excellent criteria, strong justification |
| Q4: Breakeven Analysis | ⚠️ CONDITIONAL | Calculation present but one-way vs round-trip confusion |
| Q5: KPIs | ✅ PASS | Good list, could be more route-specific |
| Data Quality (3+ checks) | ✅ EXCEEDS | 27 cells with multiple documented insights |
| Reusable Functions | ✅ PASS | 4 well-designed functions |
| Data Joins | ✅ PASS | Clear step-wise join with documentation |
| Metadata | ⚠️ PARTIAL | Inline comments good, missing formal dictionary |
| Visualizations | ✅ PASS | 8 professional visualizations with narrative |
| Code Quality | ✅ EXCEEDS | Clean, commented, organized |

### Scoring

**Technical Requirements:**
- All 5 questions answered: ✅ 5/5
- Data quality checks: ✅ 3/3 (far exceeded)
- Reusable functions: ✅ 1/1
- Metadata: ⚠️ 0.6/1 (inline comments but no formal dictionary)
- Visualizations: ✅ 1/1

**Analysis Quality:**
- Calculation correctness: ⚠️ 7/10 (semantic issues, verification needed)
- Business insight: ✅ 9/10 (strong airline economics understanding)
- Documentation: ✅ 9/10 (comprehensive)

### Overall Grade: B+ / A-

**This is a strong submission that demonstrates:**
- Excellent data cleaning and quality mindset
- Professional code organization
- Strong business acumen
- Good visualization skills

**However, it has semantic issues around:**
- Round trip vs one-way route interpretation
- Breakeven calculation interpretation
- Metadata formalization

**Recommendation for Candidate:**
1. Clarify round trip semantics and potentially rework aggregation
2. Verify ITIN_FARE interpretation
3. Add formal data dictionary
4. Make route-specific KPI recommendations

**Recommendation for Evaluator:**
If one-way route analysis is acceptable (not paired round trips), this is an A- submission. If true paired round trips are required, candidate needs to rework aggregation logic.

---

## 11. POSITIVE HIGHLIGHTS

1. **Outstanding Data Quality Section**
   - Most thorough I've seen
   - Well-justified imputation strategy
   - Comprehensive documentation

2. **Excellent Use of Airline Metrics**
   - CASM, RASM, ASM show industry knowledge
   - Unit margin is the right business metric
   - On-time performance filter is smart

3. **Professional Code Quality**
   - Clean, readable, well-commented
   - Reusable functions with docstrings
   - Defensive programming

4. **Strong Storytelling**
   - Logical narrative flow
   - Visualizations support analysis
   - Business context throughout

5. **Sophisticated Route Selection**
   - Multi-criteria approach (profit + reliability + scale)
   - Thoughtful ranking methodology

---

## CONCLUSION

Abhigyan Ghosh has submitted a strong Capital One Data Challenge analysis that demonstrates solid data science skills, professional coding practices, and good business acumen. The notebook is well-organized, thoroughly documented, and addresses all required questions.

The main concerns are semantic: the interpretation of "round trip routes" and whether the analysis should treat directional routes separately or pair them. This affects the accuracy of the profitability and breakeven calculations. Additionally, verification is needed on whether ticket fares represent one-way or round-trip prices.

With clarification and minor corrections to the round-trip semantics, this would be an excellent submission. As it stands, it's a solid B+ / A- with strong potential.

**Recommendation:** Request clarification from candidate on round-trip interpretation and ticket fare meaning. If answers are satisfactory, this is a strong hire signal.
