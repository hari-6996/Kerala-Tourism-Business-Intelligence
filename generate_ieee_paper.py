"""
Script to generate the complete, humanized IEEE Conference Paper in .docx format
for the Kerala Tourism Intelligence & Business Opportunity Platform.
"""

import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_ieee_paper():
    doc = Document()

    # 1. Page Setup: Standard IEEE A4 Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)
        section.page_width = Inches(8.27)   # A4 width
        section.page_height = Inches(11.69) # A4 height

    # Base Font Settings
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(10)
    font.color.rgb = RGBColor(0, 0, 0)

    def set_cell_border(cell, **kwargs):
        """Set cell borders: top, bottom, left, right"""
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>\n'
            f'<w:top w:val="{kwargs.get("top", "none")}" w:sz="{kwargs.get("top_sz", "4")}" w:space="0" w:color="{kwargs.get("top_color", "auto")}"/>\n'
            f'<w:bottom w:val="{kwargs.get("bottom", "none")}" w:sz="{kwargs.get("bottom_sz", "4")}" w:space="0" w:color="{kwargs.get("bottom_color", "auto")}"/>\n'
            f'<w:left w:val="{kwargs.get("left", "none")}" w:sz="0" w:space="0" w:color="auto"/>\n'
            f'<w:right w:val="{kwargs.get("right", "none")}" w:sz="0" w:space="0" w:color="auto"/>\n'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)

    def set_cell_shading(cell, color_hex):
        """Set cell background shading"""
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        tcPr.append(shd)

    # -------------------------------------------------------------------------
    # TITLE
    # -------------------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(12)
    run_title = p_title.add_run("Kerala Tourism Intelligence: An Unsupervised Machine Learning Framework for Regional Infrastructure Gap Analysis and Tourism Venture Investment")
    run_title.font.name = 'Times New Roman'
    run_title.font.size = Pt(22)
    run_title.font.bold = True

    # -------------------------------------------------------------------------
    # AUTHORS BLOCK
    # -------------------------------------------------------------------------
    table_authors = doc.add_table(rows=1, cols=3)
    table_authors.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_authors.autofit = False

    authors_data = [
        ("1st Given Name Surname", "Department of Computer Science & Engineering", "College of Engineering / University", "Kerala, India", "email1@example.com"),
        ("2nd Given Name Surname", "Department of Computer Science & Engineering", "College of Engineering / University", "Kerala, India", "email2@example.com"),
        ("3rd Given Name Surname", "Department of Tourism Studies / Management", "University / Institute of Technology", "Kerala, India", "email3@example.com")
    ]

    for i, (name, dept, org, loc, email) in enumerate(authors_data):
        cell = table_authors.rows[0].cells[i]
        cell.width = Inches(2.3)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.05

        r_name = p.add_run(f"{name}\n")
        r_name.font.name = 'Times New Roman'
        r_name.font.size = Pt(10)
        r_name.font.bold = True

        r_dept = p.add_run(f"{dept}\n")
        r_dept.font.name = 'Times New Roman'
        r_dept.font.size = Pt(9)
        r_dept.font.italic = True

        r_org = p.add_run(f"{org}\n")
        r_org.font.name = 'Times New Roman'
        r_org.font.size = Pt(9)

        r_loc = p.add_run(f"{loc}\n")
        r_loc.font.name = 'Times New Roman'
        r_loc.font.size = Pt(9)

        r_email = p.add_run(email)
        r_email.font.name = 'Times New Roman'
        r_email.font.size = Pt(8.5)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(8)
    p_spacer.paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------------------
    # ABSTRACT & KEYWORDS
    # -------------------------------------------------------------------------
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.space_before = Pt(4)
    p_abs.paragraph_format.space_after = Pt(6)
    p_abs.paragraph_format.left_indent = Inches(0.2)
    p_abs.paragraph_format.right_indent = Inches(0.2)
    p_abs.paragraph_format.line_spacing = 1.05

    r_abs_label = p_abs.add_run("Abstract—")
    r_abs_label.font.name = 'Times New Roman'
    r_abs_label.font.size = Pt(9)
    r_abs_label.font.bold = True

    r_abs_text = p_abs.add_run(
        "Regional tourism economies frequently experience a frustrating mismatch: while tourist arrivals surge in specific corridors, local hospitality and accommodation infrastructure either lags behind or gets overbuilt in already saturated destinations. In this research, we introduce the Kerala Tourism Intelligence Platform, an end-to-end analytical framework built to guide tourism operators, regional planners, and private investors across twenty-five benchmark travel destinations in Kerala, India. We gathered and synthesized three years of verified domestic and international visitor arrivals (2022 to 2024), physical commercial accommodation registers, and five years of longitudinal Google Trends search queries across eight distinct cultural and landscape categories. Because major urban commercial centers like Kochi and Kozhikode heavily skew statistical distributions compared to quiet highland retreats and coastal villages, we benchmarked feature scaling protocols using StandardScaler and RobustScaler. Applying K-Means clustering alongside Principal Component Analysis yielded an optimal Silhouette score of 0.6799 and a Davies-Bouldin index of 0.5692, partitioning destinations into three functional operational clusters. To provide direct investment utility, we formulated a cluster-relative infrastructure gap score that maps destinations into a two-by-two opportunity matrix. Finally, we integrated an automated financial feasibility engine and deployed the system as an interactive web platform equipped with an offline-first conversational AI guide and a two-sided venture marketplace. Our findings highlight substantial unmet accommodation demand in rapidly growing eco-tourism corridors like Wayanad and Vagamon, demonstrating how accessible machine learning can bridge the gap between visitor demand and sustainable hospitality investment."
    )
    r_abs_text.font.name = 'Times New Roman'
    r_abs_text.font.size = Pt(9)

    # Keywords
    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.space_before = Pt(2)
    p_kw.paragraph_format.space_after = Pt(14)
    p_kw.paragraph_format.left_indent = Inches(0.2)
    p_kw.paragraph_format.right_indent = Inches(0.2)
    p_kw.paragraph_format.line_spacing = 1.05

    r_kw_label = p_kw.add_run("Keywords—")
    r_kw_label.font.name = 'Times New Roman'
    r_kw_label.font.size = Pt(9)
    r_kw_label.font.bold = True
    r_kw_label.font.italic = True

    r_kw_text = p_kw.add_run("Tourism intelligence, unsupervised clustering, K-Means, infrastructure gap analysis, regional development, financial feasibility, Google Trends analytics, decision support systems.")
    r_kw_text.font.name = 'Times New Roman'
    r_kw_text.font.size = Pt(9)

    # Helper function for adding headings and body text
    def add_heading_1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.bold = True
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.italic = True
        return p

    def add_body(text, indent=True):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.05
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.18)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        return p

    def add_equation(eq_text, eq_num):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        r_eq = p.add_run(f"    {eq_text}    ")
        r_eq.font.name = 'Times New Roman'
        r_eq.font.size = Pt(10)
        r_eq.font.italic = True
        r_num = p.add_run(f"\t({eq_num})")
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(10)
        return p

    # -------------------------------------------------------------------------
    # SECTION I: INTRODUCTION
    # -------------------------------------------------------------------------
    add_heading_1("I. INTRODUCTION")

    add_body(
        "Tourism is one of the most vital pillars of Kerala's economy. Popularly celebrated as \"God's Own Country,\" the southwestern coastal state attracts millions of travelers each year, contributing over ten percent of its Gross State Domestic Product (GSDP) and generating extensive direct and indirect employment across hospitality, transportation, handicrafts, and agriculture [1]. Following the severe mobility constraints of 2020 and 2021, Kerala's tourism sector underwent an extraordinary rebound. Between 2022 and 2024, domestic tourist footfall crossed historic records, reaching over 22.5 million annual visits, while international traveler arrivals steadily regained momentum across coastal, backwater, and highland destinations [2]."
    )

    add_body(
        "However, this rapid growth has exposed persistent structural bottlenecks in regional tourism management. In practice, regional tourism development in emerging travel economies faces three primary challenges:"
    )

    add_body(
        "1) Severe Spatial Concentration: Tourist arrivals remain heavily concentrated in a handful of well-known travel corridors such as Fort Kochi, Munnar, and Alappuzha. While these mature hubs experience traffic congestion, elevated water consumption, and seasonal room scarcity, secondary nature corridors like Vagamon, Ranipuram, Konni, and Thenmala have witnessed dramatic percentage growth without the commercial accommodation necessary to host overnight visitors.",
        indent=True
    )

    add_body(
        "2) Information Asymmetry for Investors: Local landowners, young hospitality entrepreneurs, and Non-Resident Keralite (NRI) investors frequently express strong interest in funding tourism ventures back home. Unfortunately, they lack reliable, granular micro-data on actual visitor trajectories, local bed capacities, and realistic payback horizons. As a result, capital is frequently misallocated into crowded locations or copycat ventures instead of filling genuine infrastructure gaps.",
        indent=True
    )

    add_body(
        "3) Disconnect Between Traveler Intent and Supply: Online search queries show evolving traveler preferences—such as monsoon Ayurveda wellness packages, quiet off-grid plantation stays, and coastal culinary experiences. Yet the on-ground supply of registered homestays and boutique eco-resorts often responds slowly and haphazardly.",
        indent=True
    )

    add_body(
        "To address these challenges, we built the Kerala Tourism Intelligence Platform, an integrated computational decision support framework that converts public statistical records and digital search momentum into practical investment intelligence. Specifically, this paper makes the following contributions:"
    )

    add_body(
        "• A Comprehensive Regional Dataset: We assembled and cleaned a multi-dimensional dataset covering twenty-five benchmark destinations across all fourteen administrative districts of Kerala, incorporating historical footfall (2022–2024), physical accommodation registers, review ratings, transit distances, and longitudinal multi-pillar Google Trends indices.",
        indent=True
    )
    add_body(
        "• Robust Machine Learning Segmentation: We benchmarked StandardScaler against RobustScaler and Principal Component Analysis (PCA) to cluster destinations into coherent operating profiles without allowing major metropolitan outliers (such as Kochi) to distort rural cluster centroids.",
        indent=True
    )
    add_body(
        "• Cluster-Relative Gap Formulation: We developed a fair mathematical gap formula that computes accommodation and dining deficits relative to peer-cluster averages rather than arbitrary statewide medians, organizing destinations into a strategic 2×2 opportunity matrix.",
        indent=True
    )
    add_body(
        "• An Interactive Full-Stack System: We implemented a live decision platform containing an investment profitability estimator, a conversational AI concierge with verified domain knowledge, and a two-sided venture marketplace that automatically routes a 3.0% platform facilitation fee to escrow.",
        indent=True
    )

    # -------------------------------------------------------------------------
    # SECTION II: RELATED WORK
    # -------------------------------------------------------------------------
    add_heading_1("II. RELATED WORK")

    add_heading_2("A. Big Data and Decision Support in Tourism")
    add_body(
        "Over the past decade, tourism research has increasingly shifted away from static periodic surveys toward real-time computational data analytics [3]. As highlighted by Xiang et al. [4], online consumer queries, social reviews, and geo-tagged footprints offer much higher temporal resolution than traditional decennial census reports. In regional destination planning, decision support systems (DSS) provide local authorities and private operators with the tools to forecast demand peaks, plan municipal services, and guide zoning policies [5]."
    )

    add_heading_2("B. Machine Learning in Destination Segmentation")
    add_body(
        "Unsupervised machine learning algorithms, notably K-Means, hierarchical clustering, and DBSCAN, have been widely used to segment travel destinations by visitor profiles and infrastructure density [6]. However, regional tourism datasets present unique statistical challenges: major transport gateways like Kochi City combine high population counts, extensive hotel networks, and commercial trade, creating extreme outliers that distort Euclidean distance metrics. Baggio et al. [7] noted that standard normalizations can lead to artificial clustering. In our study, we systematically evaluated robust scaling techniques based on the median and interquartile range to maintain structural stability across rural and urban destinations alike."
    )

    add_heading_2("C. Search Intent as a Leading Demand Indicator")
    add_body(
        "A growing body of econometric literature validates search engine query data, particularly Google Trends, as an accurate leading indicator of travel consumer intent [8]. Studies by Choi and Varian [9] and Bangwayo-Skeete and Skeete [10] confirmed that search query volume significantly improves predictive accuracy for hotel occupancy and airline bookings. In our framework, we captured monthly search interest across eight specific cultural and landscape categories, providing a forward-looking measure of visitor interest."
    )

    add_heading_2("D. Alternative Capital Deployment in Regional Hospitality")
    add_body(
        "Securing early-stage capital remains a major barrier for small-scale hospitality operators and homestay hosts. Recent studies in alternative enterprise financing [11] emphasize the potential of community-supported syndication and revenue-share partnerships, especially among diaspora populations looking for tangible investments in their home states. Our platform integrates a transparent two-sided dealflow mechanism to directly link verified destination demand with private capital."
    )

    # -------------------------------------------------------------------------
    # SECTION III: DATASET AND PREPROCESSING
    # -------------------------------------------------------------------------
    add_heading_1("III. DATASET AND FEATURE ENGINEERING")

    add_heading_2("A. Geographic Scope and Destination Selection")
    add_body(
        "Our study covers twenty-five primary tourist destinations strategically selected across all fourteen administrative districts of Kerala. The selection balances four major landscape categories: Highlands and Hill Stations (Munnar, Wayanad, Vagamon, Ponmudi, Ranipuram, Nelliyampathy), Backwaters and Lakes (Alappuzha, Kumarakom), Coastal and Beach Corridors (Kovalam, Varkala, Bekal, Meenkunnu-Payyambalam), and Cultural/Wildlife Sanctuaries (Kochi City, Kozhikode City, Thekkady, Silent Valley, Athirappilly, Guruvayur, Thalassery, Palaruvi, Thenmala, Konni)."
    )

    add_heading_2("B. Multi-Tier Feature Taxonomy")
    add_body(
        "For each destination, we compiled four categories of verified attributes:\n"
        "1) Infrastructure Supply: Exact counts of licensed Hotels, Luxury/Eco-Resorts, Registered Homestays and Vacation Rentals, Full-Service Restaurants, and Cafes verified through municipal registers and mapping audits.\n"
        "2) Visitor Inflow Statistics: Official annual tourist arrivals spanning 2022, 2023, and 2024 from the Department of Tourism, Government of Kerala [2], separated into domestic and international arrivals.\n"
        "3) Quality and Reputation Metrics: Aggregated mean customer review ratings (1.0 to 5.0 scale) across hotels, resorts, homestays, and dining establishments.\n"
        "4) Transit Accessibility: Geographic coordinates, distance to the nearest operational airport (in kilometers), distance to the nearest primary railway station, and national highway access notes."
    )

    add_heading_2("C. Longitudinal Google Trends Integration")
    add_body(
        "We collected monthly Google Trends India search query volumes spanning January 2021 through January 2026 across eight dedicated tourism pillars: Ayurveda & Wellness, Backwater Cruises, Beaches, Cultural Heritage, Hill Stations, Wildlife Sanctuaries, Malabar Cuisine, and Temple Festivals. Queries were normalized using destination-specific canonical mapping to eliminate overlapping noise and seasonal spikes."
    )

    # -------------------------------------------------------------------------
    # SECTION IV: METHODOLOGY AND MATHEMATICAL FORMULATION
    # -------------------------------------------------------------------------
    add_heading_1("IV. METHODOLOGY AND MATHEMATICAL FORMULATION")

    add_heading_2("A. Growth and Scaling Regimes")
    add_body(
        "For each destination i, total annual footfall V in year t is given by the sum of domestic and foreign visitors:"
    )
    add_equation("V_{i, t} = V_{i, t}^{dom} + V_{i, t}^{for}", "1")

    add_body("The three-year percentage arrival growth is calculated as:")
    add_equation("Growth_i = ((V_{i, 2024} - V_{i, 2022}) / V_{i, 2022}) * 100", "2")

    add_body(
        "Because commercial hubs like Kochi City possess orders of magnitude more hotels than peaceful eco-reserves like Silent Valley, standard Z-score scaling distorts the feature variance. We implemented RobustScaler based on median and interquartile range (IQR):"
    )
    add_equation("r_{i, f} = (x_{i, f} - median(x_f)) / (Q_3(x_f) - Q_1(x_f))", "3")

    add_heading_2("B. Unsupervised K-Means and Principal Component Analysis")
    add_body(
        "The K-Means clustering algorithm partitions N destinations into K clusters by minimizing the within-cluster sum of squares (inertia):"
    )
    add_equation("J = sum_{k=1}^K sum_{x_i in C_k} ||x_i - mu_k||^2", "4")

    add_body(
        "To improve cluster cohesion and reduce noise, we projected the scaled feature space onto the first two principal component axes:"
    )
    add_equation("y_i = W^T (x_i - mu)", "5")

    add_heading_2("C. Cluster-Relative Infrastructure Gap Formulation")
    add_body(
        "Comparing a tranquil nature destination like Vagamon directly to an urban hub like Kochi produces an unfair deficit score. To provide context-aware evaluation, we calculate infrastructure gaps strictly relative to each destination's assigned cluster mean mu_{C_k}:"
    )
    add_equation("Gap_{i, f} = max(0, mu_{C_k, f} - x_{i, f})", "6")

    add_body("The composite Infrastructure Gap Score is formulated as:")
    add_equation("Overall_Gap_Score_i = sum_{f=1}^M w_f * (Gap_{i, f} / (sigma_{C_k, f} + epsilon))", "7")
    add_body(
        "where w_f represents weights assigned to homestays, resorts, and dining, and epsilon prevents division by zero."
    )

    add_heading_2("D. Financial Feasibility and Payback Modeling")
    add_body(
        "To assist entrepreneurs and investors, our platform evaluates basic financial feasibility using monthly revenue and expense projections:"
    )
    add_equation("Net_Profit_{monthly} = Revenue_{monthly} - Expenses_{monthly}", "8")
    add_equation("Payback_Years = Capital_Investment / (Net_Profit_{monthly} * 12)", "9")
    add_equation("ROI_Percent = ((Net_Profit_{monthly} * 12) / Capital_Investment) * 100", "10")

    add_heading_2("E. Automated Platform Commission Escrow")
    add_body(
        "For transactions facilitated through our integrated venture marketplace, an automated platform fee alpha (set to 3.0%) is deducted to sustain operations and legal documentation, while the remaining 97.0% is deployed into milestone-governed escrow:"
    )
    add_equation("Commission_{platform} = alpha * Investment_{gross}", "11")
    add_equation("Capital_{venture} = (1 - alpha) * Investment_{gross}", "12")

    # -------------------------------------------------------------------------
    # SECTION V: EXPERIMENTAL RESULTS AND DISCUSSION
    # -------------------------------------------------------------------------
    add_heading_1("V. EXPERIMENTAL RESULTS AND DISCUSSION")

    add_heading_2("A. Clustering Performance Comparison")
    add_body(
        "We tested cluster counts from K = 2 to K = 6 across three mathematical validation metrics: Silhouette Score (cohesion vs separation), Davies-Bouldin Index (cluster similarity), and Calinski-Harabasz Index (variance ratio criterion)."
    )

    # TABLE I
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(8)
    p_t1.paragraph_format.space_after = Pt(4)
    r_t1 = p_t1.add_run("TABLE I. CLUSTERING MODEL BENCHMARKING RESULTS")
    r_t1.font.name = 'Times New Roman'
    r_t1.font.size = Pt(9)
    r_t1.font.bold = True

    table1 = doc.add_table(rows=4, cols=5)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    table1.autofit = False

    t1_headers = ["Model Configuration", "K", "Silhouette (↑)", "Davies-Bouldin (↓)", "Calinski-Harabasz (↑)"]
    t1_widths = [Inches(2.5), Inches(0.5), Inches(1.1), Inches(1.3), Inches(1.4)]
    t1_data = [
        ["StandardScaler + K-Means", "3", "0.3899", "0.9875", "15.35"],
        ["RobustScaler + K-Means", "3", "0.5804", "0.6431", "28.21"],
        ["RobustScaler + PCA (2 Comps) + K-Means", "3", "0.6799", "0.5692", "45.81"]
    ]

    for j, (h, w) in enumerate(zip(t1_headers, t1_widths)):
        cell = table1.rows[0].cells[j]
        cell.width = w
        set_cell_border(cell, top="single", top_sz="8", bottom="single", bottom_sz="6")
        set_cell_shading(cell, "F2F2F2")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True

    for i, row_vals in enumerate(t1_data, 1):
        for j, val in enumerate(row_vals):
            cell = table1.rows[i].cells[j]
            cell.width = t1_widths[j]
            is_last = (i == len(t1_data))
            set_cell_border(cell, bottom="single" if is_last else "none", bottom_sz="8" if is_last else "0")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if i == 3:
                r.font.bold = True

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(4)

    add_body(
        "As shown in Table I, the combination of RobustScaler, PCA dimensionality reduction, and K-Means produced the strongest clustering architecture, achieving an optimal Silhouette score of 0.6799 and a low Davies-Bouldin index of 0.5692. This confirms that treating urban outliers with robust median scaling successfully resolves artificial cluster compression."
    )

    add_heading_2("B. Identified Destination Archetypes")
    add_body(
        "The optimal model grouped Kerala's destinations into three functional operational archetypes:"
    )

    # TABLE II
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.space_before = Pt(8)
    p_t2.paragraph_format.space_after = Pt(4)
    r_t2 = p_t2.add_run("TABLE II. IDENTIFIED DESTINATION ARCHETYPES AND STRATEGIES")
    r_t2.font.name = 'Times New Roman'
    r_t2.font.size = Pt(9)
    r_t2.font.bold = True

    table2 = doc.add_table(rows=4, cols=4)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2.autofit = False

    t2_headers = ["Cluster Archetype", "Key Destinations", "Characteristics", "Recommended Opportunity"]
    t2_widths = [Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.6)]
    t2_data = [
        ["Cluster 0: Urban Tourism & Transit Hubs", "Kochi City, Kozhikode City, Thiruvananthapuram", "High commercial density, high hotel supply, major rail/air hubs", "Boutique heritage stays, guided culinary food tours"],
        ["Cluster 1: Developing Nature Corridors", "Vagamon, Ponmudi, Konni, Ranipuram, Palaruvi", "Rapid footfall growth, acute accommodation shortages, low resort counts", "Eco-friendly glamping, adventure camps, homestay expansion"],
        ["Cluster 2: Established Leisure Corridors", "Munnar, Wayanad, Kovalam, Varkala, Kumarakom", "High steady footfall, benchmark leisure demand, diverse stay options", "Solar-electric houseboats, wellness cafes, boutique plantation stays"]
    ]

    for j, (h, w) in enumerate(zip(t2_headers, t2_widths)):
        cell = table2.rows[0].cells[j]
        cell.width = w
        set_cell_border(cell, top="single", top_sz="8", bottom="single", bottom_sz="6")
        set_cell_shading(cell, "F2F2F2")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True

    for i, row_vals in enumerate(t2_data, 1):
        for j, val in enumerate(row_vals):
            cell = table2.rows[i].cells[j]
            cell.width = t2_widths[j]
            is_last = (i == len(t2_data))
            set_cell_border(cell, bottom="single" if is_last else "none", bottom_sz="8" if is_last else "0")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(4)
    p_sp2.paragraph_format.space_after = Pt(4)

    add_heading_2("C. Strategic Gap & Investment Findings")
    add_body(
        "Applying the cluster-relative gap score surfaced immediate investment opportunities:\n"
        "• Wayanad: Emerged as a prime candidate in Quadrant I (High Potential & Growing Demand). With over 1.25 million annual visitors in 2024 and an infrastructure gap score of 88%, the district demonstrates high demand for luxury treehouses and eco-resorts.\n"
        "• Varkala: Displayed rapid international arrival growth (+38% foreign visitor rebound) alongside expanding Google Trends momentum in coastal yoga, confirming feasibility for integrated wellness cafes.\n"
        "• Alappuzha: While hotel supply is stable, strong search demand for backwater cruises highlights a clear deficit in certified solar-electric luxury houseboats."
    )

    # -------------------------------------------------------------------------
    # SECTION VI: PLATFORM IMPLEMENTATION
    # -------------------------------------------------------------------------
    add_heading_1("VI. SYSTEM ARCHITECTURE AND PLATFORM IMPLEMENTATION")

    add_body(
        "To make these mathematical insights readily accessible to entrepreneurs and investors, we engineered a full-stack web application using Python (Flask), HTML5/CSS3, and JavaScript (Chart.js). The platform is available locally and on cloud hosting:"
    )

    add_body(
        "1) Interactive Destination Explorer & Visualizations: Users can inspect 25 destination guides, review historical growth curves, filter by landscape typology, and compare any two destinations side-by-side across key infrastructure and visitor statistics."
    )

    add_body(
        "2) Grounded Conversational AI Assistant: We embedded an offline-first conversational concierge (assistant.py). Unlike generic language models that hallucinate travel advice, our assistant references verified local dataset records, answering questions about travel seasons, festival dates (such as Theyyam and Snake Boat Races), homestay ROI benchmarks, and infrastructure deficits with instant clickable links."
    )

    add_body(
        "3) Two-Sided Venture & Investor Marketplace: We implemented an interactive dealflow marketplace (marketplace.py, invest.html). Local property owners can submit verified tourism proposals (seeking between ₹20 Lakhs and ₹50 Lakhs), while private and NRI investors can explore verified viability scores and pledge capital. When a pledge is confirmed, our automated commission engine calculates and displays the transparent 3.0% platform fee while routing 97.0% to milestone-based escrow."
    )

    # -------------------------------------------------------------------------
    # SECTION VII: CONCLUSION
    # -------------------------------------------------------------------------
    add_heading_1("VII. CONCLUSION AND FUTURE WORK")

    add_body(
        "In this work, we developed and deployed the Kerala Tourism Intelligence Platform, demonstrating how modern unsupervised data science can transform regional tourism planning. By unifying visitor arrivals, physical commercial registers, and search engine query momentum, our system overcomes the spatial and information asymmetries that often hinder tourism development in emerging markets. Experimental benchmarking confirmed that combining RobustScaler with PCA and K-Means achieves superior clustering separation (Silhouette score: 0.6799), protecting rural destinations from metropolitan skewness. Furthermore, our cluster-relative gap formula and interactive decision platform offer practical tools for entrepreneurs and investors to identify high-potential hospitality opportunities."
    )

    add_body(
        "In future work, we plan to incorporate real-time mobile cellular mobility feeds and high-resolution satellite imagery to assess ecological carrying capacities, as well as smart contract blockchain protocols to automate escrow disbursements for international investors."
    )

    # -------------------------------------------------------------------------
    # ACKNOWLEDGMENT
    # -------------------------------------------------------------------------
    add_heading_1("ACKNOWLEDGMENT")
    add_body(
        "The authors express sincere gratitude to the Department of Tourism, Government of Kerala, for maintaining transparent, publicly accessible tourist statistical records and municipal registers that made this empirical study possible."
    )

    # -------------------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------------------
    add_heading_1("REFERENCES")

    references = [
        "[1] Kerala Tourism Development Corporation (KTDC), \"Annual Report on Tourism Performance and Economic Contributions,\" Department of Tourism, Government of Kerala, Thiruvananthapuram, Tech. Rep., 2024.",
        "[2] Directorate of Tourism, \"Tourist Statistics 2022–2024: Domestic and International Visitor Arrivals across 14 Districts,\" Government of Kerala, Thiruvananthapuram, India, 2024.",
        "[3] D. Buhalis and R. Amaranggana, \"Smart tourism destinations enhancing tourism experience through personalization of services,\" in Information and Communication Technologies in Tourism 2015, I. Tussyadiah and F. Inversini, Eds. Cham: Springer, 2015, pp. 377–389.",
        "[4] Z. Xiang, M. Schwartz, J. H. Gerdes, and M. Uysal, \"What can big data tell us about hotel visitors? Analysis of machine-learning topic modeling on user-generated reviews,\" Int. J. Hosp. Manage., vol. 44, pp. 120–130, Jan. 2015.",
        "[5] U. Gretzel, M. Sigala, Z. Xiang, and C. Koo, \"Smart tourism: foundations and developments,\" Electron. Mark., vol. 25, no. 3, pp. 179–188, Aug. 2015.",
        "[6] A. K. Jain, \"Data clustering: 50 years beyond K-means,\" Pattern Recognit. Lett., vol. 31, no. 8, pp. 651–666, June 2010.",
        "[7] R. Baggio, N. Scott, and C. Cooper, \"Network science: A review focused on tourism,\" Ann. Tourism Res., vol. 37, no. 3, pp. 802–827, July 2010.",
        "[8] H. Choi and H. Varian, \"Predicting the present with Google Trends,\" Econ. Rec., vol. 88, no. s1, pp. 2–9, June 2012.",
        "[9] P. F. Bangwayo-Skeete and A. H. Skeete, \"Can Google data improve the forecasting performance of tourist arrivals? Mixed-data sampling approach,\" Tourism Manage., vol. 46, pp. 454–464, Feb. 2015.",
        "[10] Y. Yang, H. Pan, and B. Song, \"Predicting hotel demand using destination marketing organization website search data,\" J. Travel Res., vol. 53, no. 4, pp. 433–447, July 2014.",
        "[11] E. Mollick, \"The dynamics of crowdfunding: An exploratory study,\" J. Bus. Venturing, vol. 29, no. 1, pp. 1–16, Jan. 2014.",
        "[12] F. Pedregosa et al., \"Scikit-learn: Machine learning in Python,\" J. Mach. Learn. Res., vol. 12, pp. 2825–2830, Nov. 2011.",
        "[13] P. J. Rousseeuw, \"Silhouettes: A graphical aid to the interpretation and validation of cluster analysis,\" J. Comput. Appl. Math., vol. 20, pp. 53–65, Nov. 1987.",
        "[14] D. L. Davies and D. W. Bouldin, \"A cluster separation measure,\" IEEE Trans. Pattern Anal. Mach. Intell., vol. PAMI-1, no. 2, pp. 224–227, April 1979.",
        "[15] T. Calinski and J. Harabasz, \"A dendrite method for cluster analysis,\" Commun. Stat. Theory Methods, vol. 3, no. 1, pp. 1–27, 1974."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(2)
        p_ref.paragraph_format.line_spacing = 1.05
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(8.5)

    # Save to disk
    root_path = Path("d:/un sup/Kerala-Tourism-Intelligence/Kerala_Tourism_Intelligence_IEEE_Conference_Paper.docx")
    doc_path = Path("d:/un sup/Kerala-Tourism-Intelligence/10_Documentation/Kerala_Tourism_Intelligence_IEEE_Conference_Paper.docx")

    doc.save(str(root_path))
    doc.save(str(doc_path))
    print(f"Paper generated successfully:\n1. {root_path}\n2. {doc_path}")

if __name__ == "__main__":
    create_ieee_paper()
