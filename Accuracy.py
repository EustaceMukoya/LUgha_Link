import sacrebleu
from Routes import translate_to_swahili
from googletrans import Translator, LANGUAGES

english_texts = [
    "Good morning?",
    "What's the weather like today?",
    "Can you help me with directions?",
    "I'm looking for a restaurant.",
    "Thank you for your assistance.",
    "Why very bad.",
    "I am a boy.",
    # Add more English texts here
]

swahili_translations = [
    "Habari za asubuhi?",
    "Hali ya anga iko vipi leo?",
    "Unaweza kunisaidia kupata mwongozo?",
    "Natafuta mkahawa.",
    "Asante kwa msaada wako.",
    "Mbona mbaya sana.",
    "Mimi  ni mvulana.",
    # Add corresponding Swahili translations here
]
def evaluate_translation_accuracy():
    generated_translations = []
    for text in english_texts:
        translation = translate_to_swahili(text)
        generated_translations.append(translation)

    # Calculate BLEU score
    bleu = sacrebleu.corpus_bleu(generated_translations, [swahili_translations])
    print(f"BLEU score: {bleu.score}")

    # Calculate accuracy (exact match)
    total_texts = len(english_texts)
    exact_matches = sum(1 for generated, reference in zip(generated_translations, swahili_translations) if generated == reference)
    accuracy = (exact_matches / total_texts) * 100
    print(f"Accuracy (exact match): {accuracy}%")

# Call the evaluation function
evaluate_translation_accuracy()