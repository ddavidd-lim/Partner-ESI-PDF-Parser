from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline



def flagText(text: str) -> str:
    """This function uses a BERT model to identify entities in the text and flags the beginning and end of entites

    Args:
        text (str): The text to flag

    Returns:
        str: The flagged text
    """
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

    nlp = pipeline("ner", model=model, tokenizer=tokenizer)

    ner_results = nlp(text)
    flagged_text = text
    offset = 0
    startflag = "[FLAG]"
    endflag = "[/FLAG]"
    
    for index, json in enumerate(ner_results):
        if json["entity"].startswith("B"):
            if index != 0:
                end = ner_results[index-1]["end"] + offset
                print(f"Start: {start}, end: {end}")
                
                flagged_text = flagged_text[:start] + startflag + flagged_text[start:end] + endflag + flagged_text[end:]
                offset += len(startflag) + len(endflag)
                start = json["start"] + offset
                
            elif index == 0:
                start = json["start"]
    return flagged_text
