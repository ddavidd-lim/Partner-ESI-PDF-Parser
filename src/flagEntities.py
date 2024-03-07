from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline



def flagText(nlp, text: str) -> str:
    """This function uses a BERT model to identify entities in the text and flags the beginning and end of entites

    Args:
        text (str): The text to flag

    Returns:
        str: The flagged text
    """

    ner_results = nlp(text)
    flagged_text = text
    offset = 0
    startflag = "[FLAG]"
    endflag = "[/FLAG]"
    # print(type(ner_results))  # Check the type of ner_results
    # print(len(ner_results))   # Check the length of ner_results
    print("-------------------------------")     # Print the first element of ner_results
    for n in ner_results:
        print(n)
    
    
    for index, json in enumerate(ner_results):
        if json["entity"].startswith("B"):
            if index != 0:
                end = ner_results[index-1]["end"] + offset
                # print(f"Start: {start}, end: {end}")
                
                flagged_text = flagged_text[:start] + startflag + flagged_text[start:end] + endflag + flagged_text[end:]
                offset += len(startflag) + len(endflag)
                start = json["start"] + offset
                
            elif index == 0:
                start = json["start"]
        else:
            start = json["start"]
    return flagged_text
