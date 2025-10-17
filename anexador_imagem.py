import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pdfrw import PdfReader, PdfWriter, PageMerge

# Variáveis (iguais às suas)
input_pdf = "jogo_demo.pdf"
output_pdf = "saida.pdf"
imagem_png = "papelParede.png"

# Verifica se existe um PDF base; se não, cria um PDF branco temporário
if not os.path.exists(input_pdf):
    c = canvas.Canvas(input_pdf, pagesize=A4)
    c.showPage()
    c.save()
    print(f"Criado PDF base em branco: {input_pdf}")

# Cria um PDF temporário contendo a imagem (usando reportlab)
pdf_temp = "_temp_imagem.pdf"
c = canvas.Canvas(pdf_temp, pagesize=A4)

# Desenha a imagem — você pode ajustar a posição e tamanho conforme desejar
# Exemplo: (x=100, y=400, largura=300, altura=200)
c.drawImage(imagem_png, 0, 0, width=612, height=792)
c.showPage()
c.save()

# Lê o PDF base e o PDF da imagem
base = PdfReader(input_pdf)
imagem = PdfReader(pdf_temp)

# Mescla a imagem na primeira página do PDF base
PageMerge(base.pages[0]).add(imagem.pages[0]).render()

# Grava o PDF final
PdfWriter().write(output_pdf, base)

# Limpa o PDF temporário
os.remove(pdf_temp)

print(f"✅ PDF gerado com sucesso: {output_pdf}")
