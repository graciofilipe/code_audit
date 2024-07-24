import base64
import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from io import StringIO


def generate(project_id, bucket_name, path_to_code, path_to_design_document=None):

    code_base = Part.from_uri(mime_type="text/plain", uri=path_to_code)

    if path_to_design_document:
        design_document = Part.from_uri(
            mime_type="application/pdf", uri=path_to_design_document
        )
        design_string = [
            "Here is the design document and diagrams for Apache Guacamole on GCP: ",
            design_document,
            "End of design document. \n",
        ]
    else:
        design_string = "   "

    overview = Part.from_uri(
        mime_type="application/pdf",
        uri=f"gs://{bucket_name}/Google_Cloud_Architecture_Framework_Overview.pdf",
    )
    opex = Part.from_uri(
        mime_type="application/pdf",
        uri=f"gs://{bucket_name}/Google_Cloud_Architecture_Framework_OpEx.pdf",
    )
    security = Part.from_uri(
        mime_type="application/pdf",
        uri=f"gs://{bucket_name}/Google_Cloud_Architecture_Framework_Security.pdf",
    )
    reliability = Part.from_uri(
        mime_type="application/pdf",
        uri=f"gs://{bucket_name}/Google_Cloud_Architecture_Framework_Reliability.pdf",
    )
    cost = Part.from_uri(
        mime_type="application/pdf",
        uri=f"gs://{bucket_name}/Google_Cloud_Architecture_Framework_Cost.pdf",
    )
    performance = Part.from_uri(
        mime_type="application/pdf",
        uri=f"gs://{bucket_name}/Google_Cloud_Architecture_Framework_Performance.pdf",
    )

    system_instruction = "You are an expert in Google Cloud Architectures. \
         Your goal is to compare the deployment code to the  Google Cloud Architecture Framework and recommend improvements to the code and desing documents. \
         Structure your answer in the five sections of the framework: Operational Excellence, Security, Reliability, Cost Optimisation, and Performance Optimisation."

    vertexai.init(project=project_id, location="europe-west1")
    model = GenerativeModel(
        "gemini-1.5-flash-001", system_instruction=[system_instruction]
    )

    generation_config = {"max_output_tokens": 8192, "top_p": 0.5, "temperature": 0.11}

    responses = model.generate_content(
        [
            "Here is the code for the deployment: ", code_base, " End of code base. \n ",
            "Here are the recommendations of the Google Cloud Architecture framework: ",
            "Overview: ", overview,
            "Operational Excellence: ", opex,
            "Security and compliance: ", security,
            "Reliability: ", reliability,
            "Cost Optimisation: ", cost,
            "Performance Optimisation: ", performance,
            "\n Evaluate the design document and diagrams as well as the code, and recommend improvements based on the recommendations of the Google Cloud Architecture Framework.",
        ],
        generation_config=generation_config,
        stream=True,
    )

    for response in responses:
        print(response.text, end="")
