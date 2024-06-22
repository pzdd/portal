from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import HexColor

def GeneratePDF():
    nome_pdf = 'exemplo'
    pdf = canvas.Canvas('{}.pdf'.format(nome_pdf), pagesize=A4)
    pdf.setFillColor(HexColor('#D8D8D8'))
    for i in range(0,840,20):
        pdf.drawString(0,i, 'teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste')
    #pdf.drawString(0,820, 'teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste')
    #pdf.drawString(0,800, 'teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste')
    #pdf.drawString(0,780, 'teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste')
    #pdf.drawString(0,760, 'teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste')
    #pdf.drawString(0,740, 'teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste')
    #pdf.drawString(0,720, 'teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste')
    #pdf.drawString(0,700, 'teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste teste')
    pdf.rotate(45)
    pdf.save()
    print('{}.pdf criado com sucesso!'.format(nome_pdf))

GeneratePDF()