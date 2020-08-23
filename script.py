import io
import os
import pdfrw
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm,mm
space = 1.8*mm
space_q = (2*mm,3.7*mm)
max_h = 296.93*mm
w = -38.6*mm + 42.7*mm#-0.02*mm
h = (125.7*mm - 121.9*mm)#+1*mm
# print(h,w)
start_id = (38.6*mm, max_h-125.7*mm+0.45*mm)
start_q = (33.3*mm,max_h-192.3*mm+0.45*mm)
error = 0.25*mm

def transform(id,resp,pdf_name,name):
    canvas_data = fill_ID(id)
    form = merge(canvas_data, template_path='./'+pdf_name+'.pdf')
    save(form, filename=pdf_name+'_filled.pdf')
    canvas_data = fill_questions(resp.lower())
    form = merge(canvas_data, template_path='./'+pdf_name+'_filled.pdf')
    save(form, filename=pdf_name+'_filled.pdf')
    canvas_data = fill_name(name)
    form = merge(canvas_data, template_path='./'+pdf_name+'_filled.pdf')
    save(form, filename=pdf_name+'_filled.pdf')
def run():
    id = input("Matrícula: ")
    quest = input("Gabarito: ")
    cwd = os.getcwd()
    b = True
    while b:
        arq = input("Nome do pdf: ")
        if arq[-4:] == ".pdf":
            arq = arq[:-4]
        if os.path.exists(arq+".pdf"):
            break
        
        print(arq+".pdf não existe nesse diretório!")
        print("Digite o nome do arquivo corretamente: ")
            
    name = input("Nome e Sobrenome: ")
    transform(id,quest,arq,name)
    
    
def fill_ID(id_str):
    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    for i,j in enumerate(id_str):
        pdf.rect(start_id[0]+(w+space)*i-error, -error+start_id[1]-(space+0.4*mm+h)*int(j), w+2*error, 2*error+h, stroke=1, fill=1)
    pdf.save()
    data.seek(0)
    return data

def fill_questions(q_str):
    keys = {'a':0,'b':1,'c':2,'d':3,'e':4,}
    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    for i,j in enumerate(q_str):
        j = keys[j]
        pdf.rect(start_q[0]+(w+0.3*mm+space_q[0])*j-error, -error+start_q[1]-(space_q[1]+0.4*mm+h)*i, w+2*error, 2*error+h, stroke=1, fill=1)
    pdf.save()
    data.seek(0)
    return data
def fill_name(name) -> io.BytesIO:
    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    pdf.drawString(x=115*mm, y=max_h-166*mm, text=name)
    pdf.save()
    data.seek(0)
    return data

def merge(overlay_canvas: io.BytesIO, template_path: str) -> io.BytesIO:
    template_pdf = pdfrw.PdfReader(template_path)
    overlay_pdf = pdfrw.PdfReader(overlay_canvas)
    for page, data in zip(template_pdf.pages, overlay_pdf.pages):
        overlay = pdfrw.PageMerge().add(data)[0]
        pdfrw.PageMerge(page).add(overlay).render()
    form = io.BytesIO()
    pdfrw.PdfWriter().write(form, template_pdf)
    form.seek(0)
    return form


def save(form: io.BytesIO, filename: str):
    with open(filename, 'wb') as f:
        f.write(form.read())

# if __name__ == '__main__':
run()
