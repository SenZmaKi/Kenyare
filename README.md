AI4I Hackathon Project Documentation

Phidel Onyango – Computer Science University of Nairobi

# Problem Description

The current process of handling Professional Indemnity Insurance (PII) quotation requests is largely manual, involving the analysis of proposal forms and associated documents. This approach is time-consuming and labor-intensive, resulting in significant delays in the submission of quotes to our business partners. Presently, we rely on an Excel template for data entry and quote generation, which not only increases the likelihood of errors but also hampers efficiency and responsiveness.

As the insurance industry evolves and the demand for timely and accurate quotes grows, our manual processes are becoming a bottleneck. The inability to quickly analyze and process requests undermines our operational effectiveness and customer satisfaction. To maintain our competitive edge and ensure optimal service delivery, there is an urgent need to automate the reinsurance underwriting quotation process. This transition aims to enhance efficiency, accuracy, and overall value for our business partners, ultimately driving better outcomes for all stakeholders involved.

# Proposed solution

he proposed solution is an AI-powered bot designed to automate the processing of Professional Indemnity Insurance (PII) quotation requests. This bot will autonomously handle the majority of the process, minimizing the need for manual input and significantly reducing time delays.

**Key Features:**

1. **Automated Data Parsing:**
   - The bot takes in a proposal form (typically a PDF) as input and parses it to extract key information such as annual fees, the number of partners, and the limit of indemnity.
   - In cases where the bot encounters data that it cannot accurately parse, user input is requested to ensure accuracy.
2. **PDF to Text Conversion:**
   - Pdf2image and Poppler are used to convert the PDF files into images, which are then fed into Tesseract (an OCR engine) to extract text.
   - The extracted text is then parsed to identify the necessary data for generating the insurance quote.
3. **Custom Yes/No Detection Algorithm:**
   - For Yes/No checkboxes in the proposal form, the bot employs a custom algorithm using the Python Imaging Library (PIL) to crop out the checkbox areas.
   - The cropped images are converted to grayscale, and the pixel values are summed up. If the sum for "Yes" is higher than "No," the bot assumes "Yes" was checked, and vice versa. The notion behind this is that the tick mark on the “Yes” will result with it having a higher number of dark pixels.
4. **Quotation Calculation:**
   - Once the relevant data is extracted from the proposal form, the bot calculates the necessary values for the insurance quote using predefined formulas and underwriting rules.
5. **Excel Output:**
   - The final calculated quote is exported into an Excel spreadsheet for easy review and record-keeping using Openpyxl. The output can be manually reviewed by an underwriter to ensure everything is in order.
6. **Web Application Interface:**
   - The bot is hosted as a web application with Sveltekit for a user-friendly experience. Users can upload proposal forms, review extracted data, and download the final quotation in Excel format.

This solution aims to drastically reduce the time and effort required to process PII quotation requests, ensuring faster turnaround, improved accuracy, and enhanced customer satisfaction.

# System diagram

![System schema](https://github.com/SenZmaKi/Kenyare/blob/master/docs/schema.png)

# Expected output

![Output](https://github.com/SenZmaKi/Kenyare/blob/master/docs/output.png)

# Checkbox algorithm schema

![Checkbox algoirthm schema](https://github.com/SenZmaKi/Kenyare/blob/master/docs/checkbox-algo.png)