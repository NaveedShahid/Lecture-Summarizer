import datetime
import bart_sum
import logging
import presumm.presumm as presumm

def do_summarize(contents, model):
    summaries=[]
    paragraphs=group_lines(contents)
    for paragraph in paragraphs:

        document = str(paragraph)

        if model == "bart":
            summarizer = bart_sum.BartSumSummarizer(state_dict_key='model')
        elif model == "presumm":
            summarizer = presumm.PreSummSummarizer()


        doc_length = len(document.split())

        min_length = int(doc_length/4)
        max_length = min_length+200

        transcript_summarized = summarizer.summarize_string(document, min_length=min_length, max_length=max_length)
        summaries.append(transcript_summarized)
        print(transcript_summarized)
    return summaries


def group_lines(lines):
    line_per_paragraph=6
    line_counter=0
    total_para = len(lines.split('.'))//line_per_paragraph
    para_so_far = 0
    paragraphs=[]
    paragraph=[]
    for line in lines.split('.'):
        if para_so_far<=total_para:
            if line_counter<line_per_paragraph:
                paragraph.append(line)
                line_counter=line_counter+1

            else:
                para='.'.join(map(str, paragraph))
                paragraphs.append(para)
                paragraph=[]
                line_counter=0
                para_so_far=para_so_far+1
        else:
            paragraph.append(line)
            
    para='.'.join(map(str, paragraph))
    paragraphs.append(para)

    return paragraphs
        