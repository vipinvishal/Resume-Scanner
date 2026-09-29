from io import BytesIO
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def build_report(data:dict)->bytes:
    output=BytesIO(); doc=SimpleDocTemplate(output,pagesize=LETTER,leftMargin=.7*inch,rightMargin=.7*inch,topMargin=.65*inch,bottomMargin=.65*inch,title="Resume evidence report")
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name="Muted",parent=styles["BodyText"],textColor=HexColor("#5F6677"),fontSize=9,leading=13))
    story=[Paragraph("Resume Evidence Report",styles["Title"]),Paragraph(f"{data.get('candidate_code','Candidate')} · {data.get('job_title','Job')} · {data.get('analysis_id','')}",styles["Muted"]),Spacer(1,14)]
    scores=[["Job Match","Evidence coverage","ATS Readiness"],[str(data.get("job_match","—")),f"{data.get('evidence_coverage','—')}%",str(data.get("ats_readiness","—"))]]
    table=Table(scores,colWidths=[2.2*inch]*3,rowHeights=[.3*inch,.45*inch]); table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),HexColor("#EEF2FF")),("TEXTCOLOR",(0,0),(-1,0),HexColor("#3730A3")),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTNAME",(0,1),(-1,1),"Helvetica-Bold"),("FONTSIZE",(0,1),(-1,1),18),("GRID",(0,0),(-1,-1),.5,HexColor("#D9D9D9")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("ALIGN",(0,0),(-1,-1),"CENTER")]))
    story += [table,Spacer(1,16),Paragraph("ATS Readiness is separate and never changes Job Match. This report supports a human decision; it does not make one.",styles["Muted"]),Spacer(1,18),Paragraph("Requirement findings",styles["Heading2"])]
    for finding in data.get("findings",[]):
        story.extend([Paragraph(f"<b>{finding['status'].replace('_',' ').title()}</b> · {finding['requirement']}",styles["Heading3"]),Paragraph(finding["reason"],styles["BodyText"]),Paragraph(f"Evidence: {finding.get('quote','No quote cited')}",styles["Muted"]),Spacer(1,9)])
    doc.build(story); return output.getvalue()
