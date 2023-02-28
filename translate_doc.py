import json
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pdf2docx import parse
from docx2pdf import convert
import os
## Load the credentials and project config
with open('credentials.json', 'r') as f:
  credential = json.load(f)
apiKey = str(credential["apiKey"])
url = str(credential["url"])



# Set up the Watson Language Translator client
authenticator = IAMAuthenticator(apiKey)
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

language_translator.set_service_url(url)



input_directory = 'documents_to_translate'
target_language = 'en'

for filename in os.listdir(input_directory):
    # document_name = os.path.join(input_directory, filename)
    # checking if it is a file
    print(f)


    # Set up the source and target languages
    # source_language = 'zh'  # Replace with your source language
    # Replace with your target language


    # Set up the file paths
    untranslated_doc_name = filename.replace('.pdf', '.doc')
    translated_doc_name = 'translated_' + untranslated_doc_name
    untranslated_pdf_file_path = input_directory + '/' + filename
    untranslated_doc_file_path = untranslated_pdf_file_path.replace('.pdf', '.doc')
    # input_file_path = input_directory + '/' + document.docx
    output_file_path = 'documents_to_translate' + '/translated_'+ filename

    # parse input file from pdf to word 

    parse(untranslated_pdf_file_path, untranslated_doc_file_path)

    # Upload the PDF file to Watson Language Translator
    with open(untranslated_doc_file_path, 'rb') as file:
        response = language_translator.translate_document(file=file, filename=os.path.basename(untranslated_doc_file_path), target=target_language, file_content_type='application/msword')
        document_id = response.get_result().get('document_id')
        print(f'Docx uploaded. Document ID: {document_id}')


    translation_complete = False
    while not translation_complete:
        status_response = language_translator.get_document_status(document_id=document_id).get_result()
        status = status_response.get('status')

        if status == 'available':
            document_translation = status_response.get('document_translation')
            with open('translated_documents/' + translated_doc_name, 'wb') as f:
                result = language_translator.get_translated_document(
                    document_id=document_id,
                    accept='application/msword').get_result()
                f.write(result.content)

            translation_complete = True
        elif status == 'failed':
            print('Translation failed.')
            break


    #convert("translated.doc", "translated.pdf")




