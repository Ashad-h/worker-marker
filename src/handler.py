""" Example handler file. """

import runpod
from runpod.serverless.utils import download_files_from_urls

from marker.converters.pdf import PdfConverter
from marker.config.parser import ConfigParser
from marker.models import create_model_dict
from marker.output import text_from_rendered


# If your handler runs inference on a model, load the model here.
# You will want models to be loaded into memory before starting serverless.

config = ConfigParser({"output_format": "markdown", "use_llm": False})

converter = PdfConverter(
    artifact_dict=create_model_dict(),
    config=config.generate_config_dict(),
)

print(converter)


def handler(job):
    """Handler function that will be used to process jobs."""
    job_input = job["input"]
    pdf_url = job_input["pdf_url"]

    print(pdf_url)
    file_path = download_files_from_urls(job["id"], [pdf_url])[0]

    rendered = converter(file_path)
    text, _, images = text_from_rendered(rendered)

    return {
        "text": text
    }


runpod.serverless.start({"handler": handler})
