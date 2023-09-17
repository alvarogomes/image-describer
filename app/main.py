from PIL import Image
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from transformers import AutoProcessor, AutoModelForVision2Seq
import json
import uvicorn

app = FastAPI()

model = AutoModelForVision2Seq.from_pretrained(
    "ydshieh/kosmos-2-patch14-224", trust_remote_code=True)
processor = AutoProcessor.from_pretrained(
    "ydshieh/kosmos-2-patch14-224", trust_remote_code=True)


def entities_to_json(entities):
    result = []
    for e in entities:
        label = e[0]
        box_coords = e[1]
        box_size = e[2][0]
        entity_result = {
            "label": label,
            "boundingBoxPosition": {"x": box_coords[0], "y": box_coords[1]},
            "boundingBox": {"x_min": box_size[0], "y_min": box_size[1], "x_max": box_size[2], "y_max": box_size[3]}
        }
        print(entity_result)
        result.append(entity_result)

    return result


@app.post("/process")
async def process_prompt(image: UploadFile = File(...), prompt: str = Form(...)):
    try:
        image_content = await image.read()
        image = Image.open(io.BytesIO(image_content))

        print(image.size)

        prompt_tmp = "<grounding>{}".format(prompt)
        inputs = processor(text=prompt_tmp, images=image, return_tensors="pt")

        generated_ids = model.generate(
            pixel_values=inputs["pixel_values"],
            input_ids=inputs["input_ids"][:, :-1],
            attention_mask=inputs["attention_mask"][:, :-1],
            img_features=None,
            img_attn_mask=inputs["img_attn_mask"][:, :-1],
            use_cache=True,
            max_new_tokens=64,
        )
        generated_text = processor.batch_decode(
            generated_ids, skip_special_tokens=True)[0]

        processed_text, entities = processor.post_process_generation(
            generated_text)
        parsed_entities = entities_to_json(entities)
        return JSONResponse(content={"message": processed_text, "entities": parsed_entities})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=18000)
