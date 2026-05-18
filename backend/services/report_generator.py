import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

def generate_roi_report(analysis: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Normal"],
        fontSize=22,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#111827"),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        fontName="Helvetica",
        textColor=colors.HexColor("#6B7280"),
        spaceAfter=16
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Normal"],
        fontSize=13,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#111827"),
        spaceBefore=16,
        spaceAfter=8
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        fontName="Helvetica",
        textColor=colors.HexColor("#374151"),
        spaceAfter=4
    )
    alert_style = ParagraphStyle(
        "Alert",
        parent=styles["Normal"],
        fontSize=10,
        fontName="Helvetica",
        textColor=colors.HexColor("#92400E"),
        spaceAfter=4
    )

    prop = analysis.get("property", {})
    roi = analysis.get("roi_analysis", {})
    rehab = analysis.get("rehab_estimate", {})
    market = analysis.get("market_data", {})
    vision = analysis.get("vision_analysis", {})
    over_imp = analysis.get("over_improvement", {})

    elements.append(Paragraph("PropValue AI", title_style))
    elements.append(Paragraph(
        f"Property Analysis Report — {datetime.now().strftime('%B %d, %Y')}",
        subtitle_style
    ))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E5E7EB")))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Property overview", section_style))
    prop_data = [
        ["ZIP code", prop.get("zip_code", "—"),
         "Square footage", f"{prop.get('square_footage', 0):,.0f} sqft"],
        ["Asking price", f"${prop.get('purchase_price', 0):,.0f}",
         "Images analyzed", str(vision.get("images_analyzed", 0))],
        ["Overall condition", vision.get("overall_condition_grade", "—"),
         "Worst condition", vision.get("worst_condition_grade", "—")]
    ]
    prop_table = Table(prop_data, colWidths=[1.3*inch, 1.8*inch, 1.5*inch, 1.8*inch])
    prop_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#6B7280")),
        ("TEXTCOLOR", (2, 0), (2, -1), colors.HexColor("#6B7280")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#111827")),
        ("TEXTCOLOR", (3, 0), (3, -1), colors.HexColor("#111827")),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTNAME", (3, 0), (3, -1), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#F9FAFB"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))
    elements.append(prop_table)

    elements.append(Paragraph("ROI analysis", section_style))
    roi_color = colors.HexColor("#16A34A") if roi.get("roi_percentage", 0) >= 15 else \
                colors.HexColor("#CA8A04") if roi.get("roi_percentage", 0) >= 0 else \
                colors.HexColor("#DC2626")
    roi_data = [
        ["ROI", f"{roi.get('roi_percentage', 0):.1f}%",
         "Verdict", roi.get("verdict", "—")],
        ["Net profit", f"${roi.get('net_profit', 0):,.0f}",
         "Total investment", f"${roi.get('total_investment', 0):,.0f}"],
        ["ARV", f"${roi.get('arv', 0):,.0f}",
         "Holding cost", f"${roi.get('holding_cost', 0):,.0f}"],
        ["70% rule max", f"${roi.get('seventy_percent_rule_max_purchase', 0):,.0f}",
         "Passes 70% rule", "Yes" if roi.get("passes_70_percent_rule") else "No"]
    ]
    roi_table = Table(roi_data, colWidths=[1.3*inch, 1.8*inch, 1.5*inch, 1.8*inch])
    roi_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#6B7280")),
        ("TEXTCOLOR", (2, 0), (2, -1), colors.HexColor("#6B7280")),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTNAME", (3, 0), (3, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (1, 0), (1, 0), roi_color),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#F9FAFB"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))
    elements.append(roi_table)

    elements.append(Paragraph("Rehab cost estimate", section_style))
    line_items = rehab.get("line_items", [])
    if line_items:
        rehab_data = [["Room", "Condition", "Priority", "Estimate"]]
        for item in line_items:
            rehab_data.append([
                item["room_type"].replace("_", " ").title(),
                item["condition_grade"],
                item["priority"].title(),
                f"${item['midpoint_estimate']:,.0f}"
            ])
        rehab_data.append([
            "Recommended budget (incl. 15% contingency)", "", "",
            f"${rehab.get('recommended_budget', 0):,.0f}"
        ])
        rehab_table = Table(rehab_data, colWidths=[2.2*inch, 1.1*inch, 1.1*inch, 1.9*inch])
        rehab_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#374151")),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#EFF6FF")),
            ("SPAN", (0, -1), (2, -1)),
            ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#F9FAFB")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("ALIGN", (3, 0), (3, -1), "RIGHT")
        ]))
        elements.append(rehab_table)
        elements.append(Paragraph(
            f"Labor multiplier for this ZIP code: {rehab.get('labor_multiplier', 1.0)}x national average",
            body_style
        ))

    elements.append(Paragraph("Market data", section_style))
    market_data = [
        ["Estimated ARV", f"${market.get('arv_estimate', 0):,.0f}",
         "ARV range", f"${market.get('arv_low', 0):,.0f} – ${market.get('arv_high', 0):,.0f}"],
        ["Avg price/sqft", f"${market.get('avg_price_per_sqft', 0):,.0f}",
         "Comps used", str(market.get("comps_used", 0))],
        ["Days on market", str(market.get("primary_market", {}).get("days_on_market", "—")),
         "ARV confidence", market.get("arv_confidence", "—").title()]
    ]
    market_table = Table(market_data, colWidths=[1.3*inch, 1.8*inch, 1.5*inch, 1.8*inch])
    market_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#6B7280")),
        ("TEXTCOLOR", (2, 0), (2, -1), colors.HexColor("#6B7280")),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTNAME", (3, 0), (3, -1), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#F9FAFB"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))
    elements.append(market_table)

    alerts = over_imp.get("alerts", [])
    if alerts:
        elements.append(Paragraph("Over-improvement warnings", section_style))
        for alert in alerts:
            elements.append(Paragraph(f"⚠ {alert}", alert_style))

    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB")))
    elements.append(Spacer(1, 6))
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontSize=8,
        fontName="Helvetica",
        textColor=colors.HexColor("#9CA3AF")
    )
    elements.append(Paragraph(
        "This report is generated by PropValue AI for informational purposes only. "
        "All estimates are based on AI analysis and market data and should not be "
        "considered professional appraisals or investment advice. Always consult a "
        "licensed contractor and real estate professional before making investment decisions.",
        disclaimer_style
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()