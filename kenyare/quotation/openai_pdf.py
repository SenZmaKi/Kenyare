import asyncio
import os
import logging
from typing import Iterable
from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OpenAI")

PROMPT = """
    The following documents are the financial audits and accounts and the insuranc proposal form of an organization. 
    Extract the following information in json format.
    Restrict yourself to the provided json format and fields, ensure the json is flat, no nesting fields, just one layer deep.
    If you can't extract the data then set the values to default i.e., default string is empty string, default boolean is false, default number is 0.

    json format start
    is_profitable: bool # Determine whether the organization is profitable
    financial_summary: str # Financial summary of the organization
    insured_name: str # The name of the person/organization seeking insurance
    reinsured_name: str # The name of the organization seeking reinsurance
    broker_name: str
    partners_count: int # The number of principals/partners in the insured organization
    qualified_assistants_count: int # The number of qualified assistants in the insured organization
    unqualified_assistants_count: int # The number of unqualified assistants in the insured organization
    others_count: int # The number of other employees in the insured organzation
    annual_fees: float # The estimated annual earnings of the insured organization
    limit_of_indemnity: float # The proposed limit of indemnity by the insured organization
    profession: str # The main profession of the insured organization
    loss_of_documents: bool # Whether the insurance should cover loss of documents
    libel_and_slander: bool # Whether the insurance should cover libel and slander
    dishonest_employees: bool # Whether the insurance should cover employee dishonesty
    retroactive_cover: bool # Whether the cover is retroactive
    json format end

    """


class OpenAIException(Exception):
    pass


client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not client.api_key:
    raise OpenAIException("OPENAI_API_KEY environment variable is not set.")

assistant_id = ""
assitant_lock = asyncio.Lock()


async def set_assistant_id():
    global assistant_id
    if assistant_id:
        return
    async with assitant_lock:
        assistant = await client.beta.assistants.create(
            name="Kenyare AI Underwriting Assistant",
            instructions="You are an underwriting assistant for Kenya Reinsurance Corporation (KRC).",
            model="gpt-4o-mini",
            tools=[{"type": "file_search"}],
        )
        assistant_id = assistant.id
        logger.info(f"Created assistant {assistant_id}")


async def upload_file(file_path: str) -> str:
    with open(file_path, "rb") as f:
        file = await client.files.create(file=f, purpose="assistants")
        logger.info(f"File {file.id} uploaded: {file_path}")
        return file.id


async def run_prompt(file_ids: Iterable[str]) -> str:
    thread = await client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Describe this document",
                "attachments": [
                    {"file_id": file_id, "tools": [{"type": "file_search"}]}
                    for file_id in file_ids
                ],
            },
        ],
    )
    if not assistant_id:
        await set_assistant_id()
    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
    logger.info(f"Created run {run.id}")
    messages = await client.beta.threads.messages.list(
        thread_id=thread.id, run_id=run.id
    )
    data = messages.data
    if not data:
        raise OpenAIException(f"No messages found in the response {messages}")
    content = data[0].content
    if not content:
        raise OpenAIException(f"No content found in the response {content}")
    first = content[0]
    if first.type != "text":
        raise OpenAIException(f"Unexpected content type {first.type}")
    output = first.text.value
    # Delete the thread and uploaded files
    await asyncio.gather(
        client.beta.threads.delete(thread_id=thread.id),
        *[client.files.delete(file_id=file_id) for file_id in file_ids],
    )
    logger.info(f"Deleted thread {thread.id} and files {file_ids}")
    logger.info(f"Prompt response: {output}")

    return output


async def main() -> None:
    financial_audit_path = "uploads/fekan-audit.pdf"
    proposal_form_path = "uploads/fekan-proposal.pdf"
    file_ids = await asyncio.gather(
        upload_file(financial_audit_path),
        upload_file(proposal_form_path),
    )
    await run_prompt(file_ids)


if __name__ == "__main__":
    asyncio.run(main())
