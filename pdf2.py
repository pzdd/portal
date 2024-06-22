from PyPDF2 import PdfWriter,PdfReader

writer = PdfWriter()
reader = PdfReader("Of 122.pdf")

for i in range(0,len(reader.pages)):
    content_page = reader.pages[i]
    media_box = content_page.mediabox
    read_mark = PdfReader('exemplo.pdf')
    image_page = read_mark.pages[0]

    image_page.merge_page(content_page)
    image_page.mediabox = media_box

    writer.add_page(image_page)

with open('saida.pdf', 'wb') as pdf:
    writer.write(pdf)