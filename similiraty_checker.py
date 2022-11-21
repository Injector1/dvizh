def pytorch_method(s1, s2):
    from sentence_transformers import SentenceTransformer, util
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    sentence_embeddings = model.encode([s1, s2])
    return util.pytorch_cos_sim(
        sentence_embeddings[0],
        sentence_embeddings[1]).item()


if __name__ == '__main__':
    s1 = '«Бавария» и Станишич продлили контракт до 2026 года'
    s2 = 'Станишич продлил контракт с «Баварией»'
    print(f'{round(pytorch_method(s1, s2) * 100, 1)}%')
