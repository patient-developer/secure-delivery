import PyPDF2


def provide_pdf_file_reader(stream):
    try:
        return PyPDF2.PdfFileReader(stream), True
    except:
        return None, False
