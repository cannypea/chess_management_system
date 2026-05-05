import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def generate_report(tournament, filename):
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    # 1. Header Information (Requirement: Name and Dates)
    elements.append(Paragraph(f"Tournament Report: {tournament.name}", styles["Title"]))
    elements.append(Paragraph(f"Venue: {tournament.venue}", styles["Heading2"]))
    elements.append(Paragraph(f"Dates: {tournament.start_date} to {tournament.end_date}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # 2. Standings (Requirement: Sorted by points descending)
    elements.append(Paragraph("Final Standings", styles["Heading2"]))
    standings_data = [["Player", "Chess ID", "Score", "Rating"]]
    
    for p in tournament.standings():
        standings_data.append([
            p.name, 
            p.chess_id, 
            str(p.score), 
            str(round(p.rating, 1))
        ])

    t_standings = Table(standings_data, colWidths=[200, 100, 50, 80])
    t_standings.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t_standings)
    elements.append(Spacer(1, 20))

    # 3. Rounds and Matches (Requirement: List of all rounds and matches)
    elements.append(Paragraph("Round History", styles["Heading2"]))
    
    for rnd in tournament.rounds:
        elements.append(Paragraph(f"Round: {rnd.name}", styles["Heading3"]))
        match_data = [["White", "vs", "Black", "Result"]]
        
        for m in rnd.matches:
            result_str = f"{m.s1} - {m.s2}" if m.s1 is not None else "Pending"
            match_data.append([m.p1.name, "vs", m.p2.name, result_str])

        t_match = Table(match_data, colWidths=[180, 30, 180, 60])
        t_match.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(t_match)
        elements.append(Spacer(1, 15))

    doc.build(elements)