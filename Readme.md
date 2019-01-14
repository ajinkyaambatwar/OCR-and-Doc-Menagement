### OCR ### 
stands for OPTICAL CHARACTER RECOGNITION is a vey handy machine learning application for detection and identification of texts from images.

Using OCR, we have created an application to process the data from various kinds of documents involved in onboarding of new customer in an international bank. 

The repository contains 5 differernt routines that process the data extracted from one of the following document types - 

1. Emirates ID
2. Indian Passport
3. Jordanian Passport
4. Pakistan Passport
5. UAE Passport

The OCR used is Tesseract 4.0, an open source OCR engine, with the terminal command as - 

```bash
tesseract <img_path> stdout --psm=7
```

Where psm indicates the page segmentation mode for OCR detection.
