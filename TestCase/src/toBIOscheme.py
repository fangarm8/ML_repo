import json

def convert_to_bio_bilou(data):
    bio_data = []

    for item in data:
        text = item['data']['text']
        tokens = text.split()
        token_labels = ['O'] * len(tokens)

        for annotation in item['annotations'][0]['result']:
            start, end = annotation['value']['start'], annotation['value']['end']
            label = annotation['value']['labels'][0]

            start_token_idx = None
            end_token_idx = None
            char_pos = 0

            for i, token in enumerate(tokens):
                token_start_pos = text.find(token, char_pos)
                token_end_pos = token_start_pos + len(token)
                char_pos = token_end_pos

                # Check if token is part of the annotation
                if start_token_idx is None and start >= token_start_pos and start < token_end_pos:
                    start_token_idx = i
                if end_token_idx is None and end > token_start_pos and end <= token_end_pos:
                    end_token_idx = i

            if start_token_idx is not None and end_token_idx is not None:
                token_labels[start_token_idx] = f'B-{label}'
                for i in range(start_token_idx + 1, end_token_idx + 1):
                    token_labels[i] = f'I-{label}'

        # Append tokens and labels
        for token, label in zip(tokens, token_labels):
            bio_data.append(f"{token} {label}")
        bio_data.append("")

    return bio_data


with open('../data/project-1.json', 'r') as f:
    labeled_data = json.load(f)

converted_data = convert_to_bio_bilou(labeled_data)

with open('../data/output_bio.txt', 'w') as f:
    for line in converted_data:
        f.write(line + '\n')

print("BIO format data saved to output_bio.txt")