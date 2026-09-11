from fastapi import APIRouter, Body
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from typing import List, Optional, Any, Dict
from dotenv import load_dotenv
from ..database import products_collection

load_dotenv()

router = APIRouter(prefix = "/chat", tags = ["ChatBot"])


class StoreDeps(BaseModel):
    found_products : List[dict[str, Any]] = []

    class Config:
        arbitrary_types_allowed = True


agent = Agent(
    "groq:openai/gpt-oss-120b",
    deps_type = StoreDeps,
    system_prompt = (
        "You are a friendly shopping assistant for clothing store - an online clothing store"
        "The store has 3 categories : men, women, kids "
        "\n\n"
        "Rules:\n"
        "1. If the user greets you or asks you who you are - reply naturally and warmly.\n"
        "2. If the user wants to buy, browse or find products -> always call the 'search_products' tool with the right filter.Never describe products yourself.\n"
        "3. After calling `search_products`, confirm to the user what you searched for (e.g. 'Here are men's shirts under ₹2000!').\n"
        "'Sorry, I can't help with that. For assistance, contact our customer care at 99664.'\n"
        "5. DO NOT make up product names, prices, or details ever."
    ),
)


@agent.tool
def search_products(
    ctx : RunContext[StoreDeps],
    category : Optional[str] = None,
    keyword : Optional[str] = None,
    max_price : Optional[int] = None,
    min_price : Optional[int] = None
    ) -> str:

    query : Dict[str, Any] = {}

    if category:
        query["category"] = {"$regex" : f"^{category.strip()}$", "$options" : "i"}

    if keyword:
        query["name"] = {"$regex" : keyword.strip(), "$options" : "i"}   


    price_filter : Dict[str, int] = {}

    if max_price is not None:
        price_filter["$lte"] = max_price

    if min_price is not None:
        price_filter["$gte"] = min_price

    if price_filter:
        query["price"] = price_filter

    raw_results = list(products_collection.find(query).limit(8))   

    processed = []

    for r in raw_results:
        r["id"] = str(r["_id"])
        r.pop("_id", None)
        r.pop("image_data", None)
        r.pop("image_content_type", None)
        processed.append(r)

    ctx.deps.found_products = processed

    if not processed:
        return "No products found matching those filters."
    return f"Found {len(processed)} products matching request."


@router.post("")
async def chat_bot(data : dict = Body(...)):
    user_message = data.get("message", "").strip()

    if not user_message:
        return {"type" : "text", "message" : "Please type a message!", "data" : None}

    deps = StoreDeps()

    try:
        result = await agent.run(user_message, deps = deps)
        text_reply = result.output

        if deps.found_products:
            return {
                "type" : "products",
                "message" : text_reply,
                "data" : deps.found_products
            }

        return {
            "type" : "text",
            "message" : text_reply,
            "data" : None
        }
    except Exception as e:
        print(f"[ChatBot Error] {e}")
        return {
            "type" : "text",
            "message" : "Sorry! I ran into an issue, please try again or contact our customer care at 99664",
            "data" : None
        }

                



