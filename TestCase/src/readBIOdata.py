def read_bio_file(file_path):
    sentences = []
    labels = []
    sentence = []
    label = []

    with open(file_path, 'r') as f:
        for line in f:
            # Strip any extra whitespace from the line
            line = line.strip()

            # If we encounter an empty line, we finish the current sentence
            if not line:
                if sentence:
                    sentences.append(sentence)
                    labels.append(label)
                    sentence = []
                    label = []
            else:
                # Split the word and the label by space
                word, tag = line.split()
                sentence.append(word)
                label.append(tag)

        # Catch any final sentence that might not end with a newline
        if sentence:
            sentences.append(sentence)
            labels.append(label)

    return sentences, labels

from datasets import Dataset

# Load the sentences and labels from the BIO file
sentences, labels = read_bio_file('../data/output_bio.txt')

# Create a dataset dictionary with 'text' and 'labels'
dataset_dict = {
    'text': sentences,
    'labels': labels
}

# Convert the dictionary to Hugging Face Dataset format
dataset = Dataset.from_dict(dataset_dict)

print(dataset[0])