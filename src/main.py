import io
import PyPDF2
import pyodide

pyodide.loadPackage('numpy')

def compress_pdf(file_data, compression_level):
    input_pdf = PyPDF2.PdfFileReader(file_data)
    output_pdf = PyPDF2.PdfFileWriter()

    for page_num in range(input_pdf.getNumPages()):
        page = input_pdf.getPage(page_num)
        if compression_level == 'minimal':
            page.compressContentStreams()
        elif compression_level == 'medium':
            page.compressContentStreams(False)
        elif compression_level == 'maximum':
            page.compressContentStreams(True)
        output_pdf.addPage(page)

    output_buffer = io.BytesIO()
    output_pdf.write(output_buffer)
    return output_buffer.getvalue()

# Convert the function to WebAssembly
compress_pdf_wasm = pyodide.to_js_function(compress_pdf, 'Uint8Array', 'string')

# Save the wasm file
with open('pdf-compressor.wasm', 'wb') as f:
    f.write(compress_pdf_wasm)