from datasets import load_dataset
from deep_translator import GoogleTranslator

if __name__ == '__main__':
    raw_dataset = load_dataset("go_emotions", name="raw")
    simplified_dataset = load_dataset("go_emotions", name="simplified")

    translator = GoogleTranslator(source="en", target="ru")

    def translate_samples(samples):
        original_text = samples["text"]
        translated_batch = translator.translate_batch(original_text)

        for i in range(len(translated_batch)):
            if not translated_batch[i]:
                translated_batch[i] = original_text[i]
                print(f"Replaced {original_text[i]} vs {translated_batch[i]}")

        samples["ru_text"] = translated_batch
        return samples

    ru_simplified_dataset = simplified_dataset.map(
        translate_samples, batched=True, batch_size=500
    )

    ru_raw_dataset = raw_dataset.map(
        translate_samples, batched=True, batch_size=500
        )

    features = ru_simplified_dataset["train"].features.copy()
    columns = list(features.to_dict().keys())
    columns.remove("ru_text")
    for column in ["ru_text"] + columns:
        features[column] = features.pop(column)
    ru_simplified_dataset_final = ru_simplified_dataset.cast(features)

    features = ru_raw_dataset["train"].features.copy()
    columns = list(features.to_dict().keys())
    columns.remove("ru_text")
    for column in ["ru_text"] + columns:
        features[column] = features.pop(column)
    ru_raw_dataset_final = ru_raw_dataset.cast(features)

    for split in ["train", "validation", "test"]:
        ru_simplified_dataset_final[split].to_csv(f"dataset/ru-go-emotions-simplified-{split}.csv")
    ru_raw_dataset_final["train"].to_csv("dataset/ru-go-emotions-raw.csv")

    ru_simplified_dataset_final.push_to_hub("ru_go_emotions", config_name="simplified")
    ru_raw_dataset_final.push_to_hub("ru_go_emotions", config_name="raw")


ru_bart = 'seara/rubert-tiny2-ru-go-emotions
